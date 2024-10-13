#packages

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin

import firebase_admin
from firebase_admin import credentials, storage, firestore

#built-ins
import os, math, requests, base64
from heapq import heapify, heappush, heappop 
from pprint import pprint


#file imports
from storage import uploadFile, getFile

#flask app

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("gofundtree-firebase-adminsdk-w1ib7-e1110dff25.json") #TODO get rid before deploy
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gofundtree.appspot.com' # might need to change to "gofundtree.appspot.com"
})

bucket = storage.bucket()
db = firestore.client()

#functions

def create_file_from_base64(base64_string, PID):
    decoded_bytes = base64.b64decode(base64_string)
    fname = f"{PID}.png"
    with open(fname, "wb") as output_file:
        output_file.write(decoded_bytes)

    return fname

#routes

@app.route("/")
def homepage():
    return "home"

@app.route("/nearbyProjects")
def nearbyProjectsPage(): #add frontend calls to retrieve 5 nearest projects to API
    #EXPECT A LOCATION TO BE PASSED AS A FRONTEND CALL THROUGH /api/getSurroundingProjects
    return render_template("index.html")

@app.route("/select3D")
def select3DPage():
    #PID GETS GENERATED, SENDS ITSELF TO DIFFERENT ROUTES
    return render_template("models.html")

@app.route("/visualize/<PID>")
def visualizePage(PID):
    #PASS PID
    return render_template("camera.html", PID=PID)

@app.route("/projectPage/<PID>")
def projectPage(PID):
    projectData = db.collection("Project").document(PID).get().to_dict()
    #PASS PID
    return f"projectPage for project {PID}"

@app.route("/paymentPage/<PID>")
def paymentPage(PID):
    projectData = db.collection("Project").document(PID).get().to_dict()
    #PASS PID
    return f"payment page for project {PID}"

# **** API endpoints ****
# CORS => FRONTEND

@app.route("/api/uploadFile/<PID>", methods=["POST"])
def uploadFileToFirebase(PID):
    """
    Uploads a file (SPECIFICALLY PNG) from a URL to Firebase Storage
    """

    # Check if a file URL is provided
    b64 = request.json.get('url')
    if not b64:
        return jsonify({"message" : "No data provided"}), 400

    if not PID:
        return jsonify({"message" : f"Bad PID {PID}"}), 400


    # Download the file from the given URL
    try:
        fn = create_file_from_base64(b64, PID)
        #fn is deleted in uploadFile
        uploadFile(bucket=bucket, filePath=fn, PID=PID)  

    except Exception as e:
        return jsonify({"message" : f"Failed to upload the file to Firebase: {e}"}), 500

    # Optionally, delete the local copy of the file after uploading to Firebase
    try:
        os.remove(fn)
    except Exception as e:
        pass #was likely removed in #uploadFIle

    return jsonify({'message': f"File from {b64} for {PID} uploaded successfully!"})


@app.route("/api/retrieveFile/<PID>/<_type>", methods=["GET"])
def retrieveFile(PID, _type):
    return jsonify(getFile(bucket=bucket, db=db, PID=PID, _type=_type))

@app.route("/api/initProject", methods=["POST"])
def initProject(PID):
    json = request.json

    #init to Firebase Firestore
    objectList = json["objectList"]
    finJSON = {
        "name" : json["name"],
        "description" : json["description"],
        "os_string": json["os_string"],
        "greens": objectList,
        "location" : "0.00000 0.00000", #instatiate for future editing @PG3
    }
    PID = db.collection("Project").add(finJSON)

    #Ricardo push 3D Model to Firebase Storage
    #TODO add implementation

    return jsonify({
        "PID" : PID,
    }), 200

#should be a post, but it realistically easier to parse this way
@app.route("/api/finalizeProject/<PID>/<lat>/<long>") 
def finalizeProject(PID, lat, long):
    """
    Image is uploaded separately thru /api/uploadFile/<PID>
    """

    db.collection("Project").document(PID).update({
        "location" : f"{lat},{long}"
    })

@app.route("/api/get3D/<PID>/", methods=["GET"])
def get3D(PID):
    #has proper extension for reference
    blenderFileURL = getFile(bucket=bucket, db=db, PID=PID, _type="model")

    deliverable = {
        "PID" : PID,
    }
    deliverable.update(blenderFileURL)

    return jsonify(deliverable)

@app.route("/api/getSurroundingProjects/<lat>/<long>/<int:num>", methods=["POST"])
def getSurroundingProjects(lat, long, num: int):
    #projects defined at {distance(int) : [projectDoc]}
    projects = {}
    
    heap = []
    heapify(heap)

    def getCircumferentialDistance(lat1, lon1, lat2, lon2):
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(float(lat1))
        lon1_rad = math.radians(float(lon1))
        lat2_rad = math.radians(float(lat2))
        lon2_rad = math.radians(float(lon2))

        # Radius of the Earth in kilometers
        R = 6371.0  # Use 3958.8 for miles

        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance
        distance = R * c  # Distance in kilometers

        return float(distance)

    for project in db.collection("Project").stream():
        lat2, long2 = project.get("location").split(",")
        distance = getCircumferentialDistance(lat, long, lat2, long2)
        
        if distance not in projects: #doesn't exist
            projects[distance] = [project]
        else:
            projects[distance].append(project)
        
        heappush(heap, distance)

    smallestLst = []
    #iterates over the requested number, or however many entries exist, whichever is smaller
    for _ in range(min(num, len(projects))):  
        curSmallest = heappop(heap)

        #clean entry from projects to not double dip
        smallestLst.append(projects[curSmallest].pop().to_dict())
        
        #del projects[curSmallest] == []; rasies key-errors for testing algo accuracy
        if len(projects[curSmallest]) == 0: 
            del projects[curSmallest]

    return jsonify(smallestLst)


    


    return jsonify(projects)

if __name__ == "__main__":
    app.run()