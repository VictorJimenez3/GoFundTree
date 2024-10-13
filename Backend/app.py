#packages

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import firebase_admin
from firebase_admin import credentials, storage, firestore

#built-ins
import os, math
from heapq import heapify, heappush, heappop 
from pprint import pprint


#file imports
from storage import uploadFile, getFile

#flask app

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("gofundtree-firebase-adminsdk-w1ib7-e1110dff25.json") #TODO get rid before deploy
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://gofundtree.appspot.com' # might need to change to "gofundtree.appspot.com"
})

bucket = storage.bucket()
db = firestore.client()

#routes

@app.route("/")
def homepage():
    return "home"

@app.route("/nearbyProjects")
def nearbyProjectsPage(): #add frontend calls to retrieve 5 nearest projects to API
    return "nearby"

@app.route("/select3D")
def select3DPage():
    #PASS RANDOM PID
    return "select3D"

@app.route("/visualize/<PID>")
def visualizePage(PID):
    #PASS PID
    return f"vizualize project {PID}"

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
    Only used for uploading image to Firebase Storage
    """
    #MUST ASSUME FILE TYPE IS EITHER
    #.gbl, .usdz, .png
    #OTHERWISE WILL NOT WORK!!
    
    if 'file' not in request.files:
        return "No file part", 400

    if not PID:
        return f"Bad PID {PID}", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400

    # Get the file extension
    file_ext = file.filename.split('.')[-1].lower()

    # Check if the file extension is valid (.glb, .usdz, .png)
    if file_ext in ['glb', 'usdz', 'png']:
        # Save the file in the current working directory
        pathnm = f'./{file.filename}'  # Save in the current directory
        file.save(pathnm)  # Save the file directly

        #uploads to Firebase Storage Bucket and deletes file
        uploadFile(bucket=bucket, filePath=pathnm, PID=PID)

        return jsonify({
            'message': f"File {file.filename} for {PID} uploaded successfully!"
        })
    else:
        return "Invalid file type. Only .glb, .usdz, or .png are allowed.", 400    

@app.route("/api/retrieveFile/<PID>/<_type>", methods=["GET"])
def retrieveFile(PID, _type):
    return jsonify(getFile(bucket=bucket, db=db, PID=PID, _type=_type))

@app.route("/api/initProject", methods=["POST"])
def initProject():
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

    pprint(finJSON)

    PID = db.collection("Project").add(finJSON)

    #Ricardo push 3D Model to Firebase Storage
    #TODO add implementation

    return jsonify({
        "PID" : PID[1].id,
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

    return jsonify({
        "PID" : PID,
    }.update(blenderFileURL))

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