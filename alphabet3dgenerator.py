import bpy

# Function to create a text object, extrude, bevel, and convert to mesh
def create_text_object(letter, extrude_value, bevel_value, index):
    # Create the text object
    bpy.ops.object.text_add()
    text_obj = bpy.context.object
    text_obj.data.body = letter
    
    # Set extrude and bevel
    text_obj.data.extrude = extrude_value
    text_obj.data.bevel_depth = bevel_value
    text_obj.data.bevel_resolution = 2
    
    # Align to the middle
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    # Font size
    text_obj.data.size = 2.8
    # Convert to mesh
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.mode_set(mode='EDIT')
    # Merge vertices by distance
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    #rotate the object
    #convert to radians
    angle = 90
    angle = angle * (3.14159 / 180)
    text_obj.rotation_euler[0] = angle
    # Rename the object
    text_obj.name = f"{letter}_{index}"



# Loop through the alphabet and create each letter
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i, char in enumerate(alphabet):
    create_text_object(char, 0.1, 0.01, i + 1)
