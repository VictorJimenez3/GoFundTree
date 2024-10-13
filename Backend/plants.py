import bpy
import random
import math
import os

def generatePlants(nTrees:int, nBushes:int, fileType:str):
    """
    Generates a 3D model of trees and bushes, as .glb or .usd as needed.
    The model appears in the same directory where this function was run (hopefully).
    The model is named "output.glb" or "output.usd", depending on fileType.
    Take into account that generatePlants will overwrite any past output files.

    Args:
        nTrees (int): No. of trees.
        nBushes (int): No. of bushes.
        fileType (str): Either "glb" or "usd", in lowercase.

    Returns:
        None
    """
    # Open the existing .blend file from your local directory
    blend_file_path = "plants.blend"
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Initialize variables
    num_trees = nTrees  # Number of trees to generate
    num_bushes = nBushes  # Number of bushes to generate
    area_size = 50  # Defines the square area (50x50 units)
    min_distance_between_objects = 3.0  # Minimum distance between objects

    # Lists to store object locations
    object_locations = []
    tree_objects = []  # List to store the generated tree objects
    bush_objects = []  # List to store the generated bush objects

    # Function to check if a location is too close to existing objects
    def is_too_close(location, min_distance):
        for obj_loc in object_locations:
            distance = math.sqrt((obj_loc[0] - location[0]) ** 2 + (obj_loc[1] - location[1]) ** 2)
            if distance < min_distance:
                return True
        return False
    
    # Function to randomly generate objects (trees or bushes)
    def generate_objects(object_type, num_objects, object_list, min_distance):
        for i in range(num_objects):
            while True:
                # Randomly generate x and y coordinates within the area
                x = random.uniform(-area_size / 2, area_size / 2)
                y = random.uniform(-area_size / 2, area_size / 2)
                location = (x, y)
                
                # Check if the new object is far enough from others
                if not is_too_close(location, min_distance):
                    object_locations.append(location)
                    break

            # Add the object at the location
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_by_type(type='MESH')
            
            # Assuming your models are stored as specific objects in the blend file
            new_object = bpy.data.objects[object_type].copy()
            new_object.location = (x, y, 0)  # Set the location of the object
            bpy.context.collection.objects.link(new_object)
            
            # Add the new object to the corresponding list (trees or bushes)
            object_list.append(new_object)

    # Generate trees and bushes without collision
    generate_objects('Tree', num_trees, tree_objects, min_distance_between_objects)
    generate_objects('Bush', num_bushes, bush_objects, min_distance_between_objects)

    # Select all tree and bush objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in tree_objects + bush_objects:
        obj.select_set(True)

    # Join the selected objects into one
    bpy.context.view_layer.objects.active = tree_objects[0]  # Set one tree as the active object
    bpy.ops.object.join()  # Join all selected objects into the active object

    # Get the path of the current script directory
    script_dir = os.path.dirname(bpy.data.filepath)

    # Export the combined object as a GLB file in the same folder as the script
    if fileType == "glb":
        # Export the combined object as a GLB file
        export_filepath = os.path.join(script_dir, "output_model.glb")    # parameter
        bpy.ops.export_scene.gltf(
            filepath=export_filepath,
            export_format='GLB',                                                    # parameter
            use_selection=True,        # Export only selected objects
            export_apply=True           # Apply transforms (rotation, scale, etc.)
        )
    elif fileType == "usd":
        # Export the object as a GLB file
        export_filepath = os.path.join(script_dir, "output_model.usd")    # parameter
        bpy.ops.wm.usd_export(
            filepath=export_filepath,
            selected_objects_only=True,     # Export only selected objects
            export_textures=True,           # Export with textures (similar to GLB)
        )

    '''
    # Function to gather data about the generated model
    def gather_model_data():
        total_trees = len(tree_objects)
        total_bushes = len(bush_objects)
        data_summary = {
            'Number of Trees': total_trees,
            'Number of Bushes': total_bushes,
            'Model File Path': export_filepath
        }
        return data_summary
    
    # Gather and print data
    model_data = gather_model_data()
    print(f"Model Data: {model_data}")
    print(f"Generated trees and bushes successfully and exported as one model at {export_filepath}!")
    '''

generatePlants(5, 12, "glb")
