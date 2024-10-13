from flask import request
import os

"""
blobPaths and names are defined as 
(models|images)/PID.((glb|usdz)|png)

can be queried knowing PID by searching noSQL firestore for PID and finding os_string (gives hint on file type)
"""



def uploadFile(bucket, filePath, PID):
    """
    Assumes file to upload is locally stored at the position defined in filePath
    """
    # bucket: bucket ref for firebase storage
    # filePath: path to your file
    # PID: ProjectID

    # Extract the file extension (e.g., 'usdz', 'png')
    inputExtensionName = filePath.split("/")[-1].split(".")[-1]  # Corrected this line to extract extension

    # Determine the path in Firebase Storage
    firestorePath = f"{'images' if inputExtensionName in ['png', 'jpeg'] else 'models'}/{PID}.{inputExtensionName}"
    blob = bucket.blob(firestorePath)

    # Set the correct content type based on the file extension
    content_type = "model/vnd.usdz+zip" if inputExtensionName == "usdz" else \
                   "model/gltf-binary" if inputExtensionName == "glb" else \
                   "image/png"

    # Set metadata with the content type and PID
    blob.metadata = {
        "contentType": content_type,
        "PID": PID
    }

    # Upload the file to Firebase Storage
    blob.upload_from_filename(filePath)
    
    # Remove the local file after uploading
    os.remove(filePath)

    # Optionally make the file publicly accessible
    blob.make_public()

    print(f"File {firestorePath} uploaded with metadata: {blob.metadata}")

def getDownloadUrl(bucket, PID, _type):
    # bucket: bucket ref for firebase storage
    # PID: ProjectID
    # _type = extension

    # blobName: the file path in Firebase Storage
    blobName = f"{'images' if _type in ['png', 'jpeg'] else 'models'}/{PID}.{_type}"

    # Get a reference to the blob in the storage bucket
    blob = bucket.blob(blobName)

    # Double check that the blob is public
    blob.make_public()

    print(f"Public URL for the file: {blob.public_url}")

    # Return the public URL for the file to avoid local download for sending frondend
    return blob.public_url

def getFile(bucket, db, PID, _type):
    #type (model|image)
    OS = None
    if _type == "model":
        document = db.collection("Project").document(PID).get()
        OS = document.get("os_string")

    extension = "usdz" if OS == "IOS" else "glb" if OS == "Android" else "png"

    #returns a public link that gives access to file for nonlocalized storage client-side
    return {"url" : getDownloadUrl(bucket=bucket, PID=PID, _type=extension)}