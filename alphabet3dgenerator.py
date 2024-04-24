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
    text_obj.data.bevel_resolution = 1
    
    # Align to the middle
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='BOUNDS')
    text_obj.location.x = -text_obj.dimensions.x / 2
    text_obj.location.y = -text_obj.dimensions.y / 2
    
    # Convert to mesh
    bpy.ops.object.convert(target='MESH')
    
    # Rename the object
    text_obj.name = f"{index}"

# Loop through the alphabet and create each letter
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i, char in enumerate(alphabet):
    create_text_object(char, 0.05, 0.01, i + 1)