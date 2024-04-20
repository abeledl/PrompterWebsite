import numpy as np
import bpy
import math


globalYCameraBG12Clips = -0.6


positions_english_array = [[393.49, 77.50], [536.27, 77.50], [475.00, 310.00], [443.79, 542.50], [543.19, 542.50], [475.00, 775.00], [474.99, 1007.50], [474.99, 1162.50], [250.27, 1317.50], [474.66, 1317.50], [699.38, 1317.50], [475.00, 1472.50], [475.00, 1705.00], [300.57, 1937.50], [615.94, 1937.50], [474.99, 2092.50], [412.09, 2247.50], [595.34, 2247.50], [474.99, 2480.00], [475.00, 2712.50], [474.99, 2867.50], [233.06, 3022.50], [512.83, 3022.50], [754.76, 3022.50], [406.58, 3177.50], [583.16, 3177.50], [350.17, 3332.50], [530.80, 3332.50], [443.79, 3487.50], [595.33, 3487.50], [475.00, 3720.00], [443.28, 3952.50], [547.77, 3952.50], [475.00, 4107.50], [474.99, 4340.00], [474.99, 4572.50], [261.58, 4727.50], [569.62, 4727.50], [443.79, 4882.50], [543.19, 4882.50], [475.00, 5115.00], [474.99, 5347.50], [474.99, 5502.50], [475.00, 5657.50], [475.00, 5812.50], [305.70, 5967.50], [569.63, 5967.50], [342.78, 6122.50], [466.27, 6122.50], [598.48, 6122.50], [344.90, 6277.50], [598.54, 6277.50], [284.21, 6432.50], [598.58, 6432.50], [474.99, 6587.50], [475.00, 6742.50], [382.01, 6897.50], [536.27, 6897.50], [474.99, 7130.00], [474.99, 7362.50], [177.39, 7517.50], [609.99, 7517.50], [380.37, 7672.50], [583.84, 7672.50], [365.04, 7827.50], [613.42, 7827.50], [475.00, 7982.50], [316.20, 8137.50], [552.13, 8137.50], [393.50, 8292.50], [584.36, 8292.50], [475.00, 8525.00], [393.49, 8757.50], [543.19, 8757.50], [474.99, 8912.50], [474.99, 9067.50], [475.00, 9222.50], [356.28, 9377.50], [534.06, 9377.50], [474.99, 9532.50], [474.99, 9687.50]]

start_times_array = [0.40, 0.64, 0.96, 2.24, 2.40, 2.64, 5.28, 6.56, 7.04, 7.28, 7.52, 8.96, 9.20, 12.16, 12.55, 13.28, 13.91, 14.16, 14.55, 17.82, 18.46, 20.14, 20.62, 20.94, 21.82, 22.06, 22.38, 22.70, 23.10, 23.34, 23.50, 26.95, 27.11, 27.36, 27.60, 29.76, 30.48, 30.71, 31.52, 31.68, 31.91, 35.04, 36.48, 36.96, 37.52, 37.84, 38.08, 39.76, 40.00, 40.24, 40.40, 40.88, 41.52, 41.92, 42.80, 43.12, 45.08, 45.23, 45.63, 48.27, 48.67, 49.31, 50.91, 51.16, 51.55, 51.95, 52.43, 52.67, 52.91, 54.07, 54.39, 54.55, 56.71, 56.95, 57.19, 59.43, 59.91, 60.79, 61.11, 61.51, 62.79]
#end times of the end of line

start_new_rows_seconds_with_new_row_flags = []

scale_factor = 0.01
english_words_scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in positions_english_array]
english_words_scaled_coordinates = [(x, y + 2.6) for x, y in english_words_scaled_coordinates]


english_paragraph = "In the ethereal#glow of a yellow-tiled#chamber, lime_crystals sprout from the walls like nature's#delicate_artwork. Each crystal gleams with an otherworldly#luminescence, casting dancing_shadows across the room. The air is filled with a faint,_sweet#fragrance, as if the crystals#themselves exhale the essence of a distant#verdant_forest. Soft_whispers seem_to echo through the space, as if the very walls hold secrets of forgotten_ages. In this surreal#sanctuary, time feels suspended, and one can't help but be drawn into the mesmerizing#beauty of the lime_crystals, losing oneself in their captivating allure."
english_words = english_paragraph.split()


phonetic_string = 'ɪn ðə ɪˈθɪərɪəl#ɡloʊ ʌv ə ˈjɛloʊ_taɪld#ˈtʃæmbər, laɪm_ˈkrɪstəlz spraʊt frʌm ðə wɔlz laɪk ˈneɪʧərz#ˈdɛlɪkət_ˈɑrtwɜrk. iʧ ˈkrɪstəl ɡliːmz wɪð ən ˌʌðərˈwɜrldli#luːməˈnɛsəns, ˈkæstɪŋ ˈdænsɪŋ_ˈʃædoʊz əˈkrɒs ðə ruːm. ði ɛr ɪz fɪld wɪð ə feɪnt,_swit#ˈfreɪɡrəns, æz ɪf ðə ˈkrɪstəlz#ðəmˈsɛlvz ɛksˈheɪl ði ˈɛsəns ʌv ə ˈdɪstənt,#ˈvɜrdnt_ˈfɔrɪst. sɔft_ˈwɪspərz sim_tuː ˈɛkoʊ θruː ðə speɪs, æz ɪf ði ˈvɛri wɔlz hoʊld ˈsikrɪts ʌv fɚˈɡɑtn̩_ˈeɪʤɪz. ɪn ðɪs səˈriəl#ˈsæŋkʧuˌɛri, taɪm fiːlz səˈspɛndɪd, ænd wʌn kænt ˈhɛlp bət biː drɔn ˈɪntuː ðə mɛzˈmɛrɑɪzɪŋ#ˈbjuti ʌv ðə laɪm_ˈkrɪstəlz, ˈluzɪŋ wʌnsɛlf ɪn ðer ˈkæptɪˌveɪtɪŋ əˈlʊr.'
phonetic_words= phonetic_string.split()







last_frame = 3000


bpy.context.scene.render.fps = 60
bpy.context.scene.eevee.shadow_cube_size = '4096'
bpy.context.scene.eevee.shadow_cascade_size = '4096'


rotation_x = math.radians(-32.9472)

#bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), rotation=(rotation_x, 0.12, 0.1))
#the_sun = bpy.context.active_object
#the_sun.name = "the_sun"
#the_sun.data.energy = 2.5

def createCube(location, scale, name, render):
  bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=location, scale=scale)
  cube = bpy.context.active_object
  cube.name = name
  cube.hide_render = render
  #cube.hide_viewport = render
  return cube

def addBooleanModifier(obj, clip_obj_name, modifier_name):
  obj.modifiers.new(name=modifier_name, type='BOOLEAN')
  obj.modifiers[modifier_name].object = bpy.data.objects[clip_obj_name]
  obj.modifiers[modifier_name].solver = 'FAST'
  #obj.modifiers[modifier_name].double_threshold = 0.001
###################################################################

top_hiding_cube = createCube((9.29446, 62.6753, 2.72953), (9, 63, 1), "clip_cube_english_1", True)
bottom_hiding_cube = createCube((9.29446, -42.4323, 2.72953), (9, 32.8 , 1), "clip_cube_english_2", True)


parent_cube = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube = bpy.context.active_object
parent_cube.name = "parent_cube"
parent_cube.scale = (2, 2, 2)
parent_cube.location = (0, 2.25562, 2.41886)

highlighter_obj = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8), scale=(1, 1, 1))
highlighter_obj = bpy.context.active_object
highlighter_obj.name = "highlighter_obj"
highlighter_obj.scale = (1, 1, 1)
highlighter_material_english = bpy.data.materials.new(name="HighlighterMaterialEnglish")
highlighter_obj.data.materials.append(highlighter_material_english)
highlighter_obj.active_material.use_nodes = True
highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.478878, 0, 0.106461, 1)


#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (1, 0.0855381, 0.194721, 1)
#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


def min_max_norm(data):
  """
  Normalizes data to the range [0, 1]
  """
  min_val = np.min(data)
  max_val = np.max(data)
  return (data - min_val) / (max_val - min_val)


#outline material
outline_material = bpy.data.materials.new(name="OutlineMaterial")
outline_material.use_nodes = True
outline_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value =  0.298182 #roughness
#outline_material.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1 #transmission
outline_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.001617, 0.0041617, 0.0041617, 1) #color
outline_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5 #Coat
outline_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.260769



#text material
text_material = bpy.data.materials.new(name="TextMaterial")
text_material.use_nodes = True
text_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1,1, 1)
text_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic

text_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
text_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission

#text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1





#############cliping materialenglish #########
clip_material_english = bpy.data.materials.new(name="clipMaterialEnglishWhite")
clip_material_english.use_nodes = True
nodesenglishWhite = clip_material_english.node_tree.nodes
clip_material_english.blend_method = 'CLIP'

# Clear default nodes
for node in nodesenglishWhite:
    nodesenglishWhite.remove(node)

# Create necessary nodes
output_node = nodesenglishWhite.new(type='ShaderNodeOutputMaterial')
principal_node = nodesenglishWhite.new(type='ShaderNodeBsdfPrincipled')
principal_node2 = nodesenglishWhite.new(type='ShaderNodeBsdfPrincipled')
mapping_node = nodesenglishWhite.new(type='ShaderNodeMapping')
camera_data_node = nodesenglishWhite.new(type='ShaderNodeCameraData')
dot_product_node = nodesenglishWhite.new(type='ShaderNodeVectorMath')
mapping_node2 = nodesenglishWhite.new(type='ShaderNodeMapping')
camera_data_node2 = nodesenglishWhite.new(type='ShaderNodeCameraData')
dot_product_node2 = nodesenglishWhite.new(type='ShaderNodeVectorMath')
mix_shader_node = nodesenglishWhite.new(type='ShaderNodeMixShader')
math_greater_node = nodesenglishWhite.new(type='ShaderNodeMath')
math_greater_node2 = nodesenglishWhite.new(type='ShaderNodeMath')
math_add_node = nodesenglishWhite.new(type='ShaderNodeMath')
clamp_node = nodesenglishWhite.new(type='ShaderNodeClamp')

math_add_node.operation = 'ADD'
math_greater_node.operation = 'GREATER_THAN'
math_greater_node2.operation = 'GREATER_THAN'
principal_node2.inputs[4].default_value = 0
dot_product_node.operation = 'DOT_PRODUCT'
dot_product_node2.operation = 'DOT_PRODUCT'
mapping_node.inputs[0].default_value[1] = 1.7
mapping_node2.inputs[0].default_value[1] = -84.100
mapping_node2.inputs[2].default_value[0] = -0.0366519

# Link nodes
links = clip_material_english.node_tree.links
links.new(camera_data_node.outputs['View Vector'], dot_product_node.inputs[1])
links.new(mapping_node.outputs['Vector'], dot_product_node.inputs[0])
links.new(camera_data_node2.outputs['View Vector'], dot_product_node2.inputs[1])
links.new(mapping_node2.outputs['Vector'], dot_product_node2.inputs[0])
links.new(principal_node.outputs['BSDF'], mix_shader_node.inputs[1])
links.new(principal_node2.outputs['BSDF'], mix_shader_node.inputs[2])
links.new(dot_product_node.outputs['Value'], math_greater_node.inputs[0])
links.new(dot_product_node2.outputs['Value'], math_greater_node2.inputs[0])
links.new(math_greater_node.outputs['Value'], math_add_node.inputs[0])
links.new(math_greater_node2.outputs['Value'], math_add_node.inputs[1])
links.new(math_add_node.outputs['Value'], clamp_node.inputs[0])
links.new(clamp_node.outputs['Result'], mix_shader_node.inputs['Fac'])
links.new(mix_shader_node.outputs['Shader'], output_node.inputs['Surface'])


#refraction material
# Create a new material
material_name = "RefractionMaterial"
refra_material = bpy.data.materials.new(name=material_name)
refra_material.use_nodes = True
nodes = refra_material.node_tree.nodes

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Add refraction shader nodes
shader_node = nodes.new(type='ShaderNodeBsdfRefraction')
output_node = nodes.new(type='ShaderNodeOutputMaterial')

# Link nodes
refra_material.node_tree.links.new(shader_node.outputs['BSDF'], output_node.inputs['Surface'])
refra_material.node_tree.nodes["Refraction BSDF"].inputs[1].default_value = 0.4
refra_material.node_tree.nodes["Refraction BSDF"].inputs[2].default_value = 0.3

#yellow material
yellow_material = bpy.data.materials.new(name="yellowMaterial")
yellow_material.use_nodes = True
yellow_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 0, 1)
yellow_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic
yellow_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
yellow_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
yellow_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
yellow_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission


#blue material
green_material = bpy.data.materials.new(name="GreenMaterial")
green_material.use_nodes = True
green_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.00992801, 0.661224, 0, 1)
green_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic
green_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
green_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
green_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
green_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission


def createTextObject(words, positions, parent_obj, font_name, font_size, font_resolution, bevel_depth):
  # Create a new text object for each word
  ft = font_size
  yOffSet = 0
  yOs = 0
  encounteredLongWord = False
  IndexWord = 0
  prevPositionY = -1 * positions[0][1]
  for word, position in zip(words, positions):
    currentPosition = -1 * position[1]
    


    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], 0))
    text_object = bpy.context.active_object
    word = word.replace("_", "  ")
    doubleRow = False

    if '#' in word:

      word = word.replace('#', '\n')
      doubleRow = True

    text_object.data.body = word
    if currentPosition < prevPositionY:
      if doubleRow:
        start_new_rows_seconds_with_new_row_flags.append((start_times_array[IndexWord],True))
      else:
        start_new_rows_seconds_with_new_row_flags.append((start_times_array[IndexWord],False))

    if doubleRow:
      text_object.data.space_line = 1.6

    font_path = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data = bpy.data.fonts.load(font_path)
    text_object.data.font = font_data
    text_object.data.size = font_size
    text_object.data.extrude = 0.05
    text_object.data.bevel_depth = 0.02
    text_object.data.bevel_resolution = 3
    text_object.data.fill_mode = 'FRONT'
    #text_object.data.bevel_mode = 'ROUND'
    text_object.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object.data.align_y = 'CENTER'  # Set vertical alignment to middle
    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(green_material)
    text_object.data.resolution_u = 2

    bpy.ops.object.convert(target='MESH')
    

    ########################outline text############################################
    #bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], -0.01))
    #text_object2 = bpy.context.active_object
    #text_object2.name = "zoutline"
    #text_object2.data.body = word
    #if doubleRow:
    #  text_object2.data.space_line = 1.7
    #font_path2 = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    #font_data2 = bpy.data.fonts.load(font_path2)
    #text_object2.data.font = font_data2
    #text_object2.data.size = font_size
    #text_object2.data.resolution_u = font_resolution
    #text_object2.data.fill_mode = 'NONE'
    #text_object2.data.extrude = 0.05
    #text_object2.data.bevel_depth = bevel_depth
    #text_object2.data.bevel_resolution = 0
    #text_object2.data.materials.append(outline_material)
    #text_object2.data.align_x = 'CENTER'  # Set horizontal alignment to center
    #text_object2.data.align_y = 'CENTER'  # Set vertical alignment to middle
    #text_object2.active_material.use_screen_refraction = True
    #text_object2.active_material.refraction_depth = 1.5
    #bpy.ops.object.convert(target='MESH')
    #text_object2.parent = parent_obj 
    
    # Set the text object as a child of the parent cube
    text_object.parent = parent_obj

    IndexWord = IndexWord + 1
    prevPositionY = -1 * position[1]



  # Select all created text objects
  bpy.ops.object.select_all(action='SELECT')

def createPhoTextObject(words, positions, parent_obj, font_name, font_size, font_resolution, bevel_depth):
  # Create a new text object for each word
  ft = font_size
  for word, position in zip(words, positions):
    # Create a new text object-
    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.7, 0))
    text_object = bpy.context.active_object
    word = word.replace("_", "  ")
    doubleRow = False
    if '#' in word:
      word = word.replace('#', '\n')
      doubleRow = True


    text_object.data.body = word
    if doubleRow:
      text_object.data.space_line = 2.3
    font_path = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data = bpy.data.fonts.load(font_path)
    text_object.data.font = font_data
    text_object.data.size = font_size
    text_object.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object.data.align_y = 'CENTER'  # Set vertical alignment to middle
    #text_object.data.extrude = 0.01
    #text_object.data.bevel_depth = 0.01
    #text_object.data.bevel_resolution = 1
    #text_object.data.bevel_mode = 'ROUND'
    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(green_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')
    


    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.7, -0.01))
    text_object2 = bpy.context.active_object
    text_object2.name = "zoutline"
    text_object2.data.body = word
    if doubleRow:
      text_object2.data.space_line = 2.3
    font_path2 = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data2 = bpy.data.fonts.load(font_path2)
    text_object2.data.font = font_data2
    text_object2.data.size = font_size
    text_object2.data.resolution_u = font_resolution
    text_object2.data.fill_mode = 'NONE'
    #text_object2.data.offset = 0.02
    text_object2.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object2.data.align_y = 'CENTER'  # Set vertical alignment to middle
    text_object2.data.bevel_depth = bevel_depth
    text_object2.data.bevel_resolution = 0

    text_object2.data.materials.append(outline_material)
    #text_object2.active_material.use_nodes = True
    text_object2.active_material.use_screen_refraction = True
    text_object2.active_material.refraction_depth = 1.5



    bpy.ops.object.convert(target='MESH')
    #bpy.ops.object.shade_smooth()
    
    # Set the text object as a child of the parent cube
    text_object.parent = parent_obj
    text_object2.parent = parent_obj 



  # Select all created text objects
  bpy.ops.object.select_all(action='SELECT')


############################ADDINGBOOLEaN
def addingBooleanModifierToAllChildrenObjects(word_objects, clip_cube_name_1, clip_cube_name_2):
  for word in word_objects:
    addBooleanModifier(word, clip_cube_name_1, "BOOLEAN1")
    addBooleanModifier(word, clip_cube_name_2, "BOOLEAN2")


def moveObject(obj, direction, distance):
  # Get the object by its name
  obj_name = obj.name 

  obj = bpy.context.scene.objects[obj_name]
  obj.location.x += direction[0] * distance 
  obj.location.y += direction[1] * distance 
  obj.location.z += direction[2] * distance

def addKeyFrame(obj, frame_number, property_name):
  # Insert a keyframe
  obj.keyframe_insert(data_path=property_name, frame=frame_number)

def applyKeyFrameToWords(obj):
  fps = 60
  frame = 0
  transition_frame_rate = 10
  direction = [0, 1, 0]
  distance = 1.55 * 2
  #for second in end_times_array:
  for second, bool_val in start_new_rows_seconds_with_new_row_flags:
    frame = calculateFrame(second, fps)
    addKeyFrame(obj, frame, "location")

    if bool_val == True:
      moveObject(obj, direction, distance * 2)
    else:
      moveObject(obj, direction, distance)
      
    transition_frames = frame + transition_frame_rate
    addKeyFrame(obj, transition_frames, "location")

def calculateFrame(seconds, fps):
  frames = seconds * fps -6
  return int(frames)

def setObjPosition(x, y, z, obj):
  obj.location.x = x
  obj.location.y = y
  obj.location.z = z

def getWidthAndHeight(obj):
  width = obj.dimensions.x
  height = obj.dimensions.y
  return {'width': width, 'height': height}

def getAllChildrenObjects(obj):
  # Get all its child objects (recursive)
  children = obj.children_recursive
  return children

def changeWidthAndHeight(obj, width, height, depth):
  obj.dimensions = (width, height, depth) 

def setupHighlighterKeyFrames(obj, word_coordinates, words):
  fps = 60
  frameT = 0
  transition_frame_rate = 10
  word_obj_idx = 0
  pivot_to_text_length = 0.030
  height_percentage_offset = 1
  width_percentage_offset = 1
  width_height_data_first_word = getWidthAndHeight(words[word_obj_idx])
  new_pos_y = -word_coordinates[word_obj_idx][1] - 0.2
  double_row_y_position  = -word_coordinates[word_obj_idx][1] + 0.5
  new_height = width_height_data_first_word["height"] + 1.1

  ############GEO NODES SET UP ############################
  bpy.data.objects["highlighter_obj"].select_set(True)
  # Select the object (optional, if not already selected)
  #obj.select_set(True)
  # Make the object the active one
  bpy.context.view_layer.objects.active = obj
  # Add a Geometry Nodes modifier to the cube
  bpy.ops.node.new_geometry_nodes_modifier()
  #obj.node.new_geometry_node_group_assign()
  # Get the node group of the Geometry Nodes modifier
  node_group = bpy.data.node_groups['Geometry Nodes']
  # Clear existing nodes
  for node in node_group.nodes:
    node_group.nodes.remove(node)

  # Create Group Input and Group Output nodes
  group_input = node_group.nodes.new('NodeGroupInput')
  group_input.location = (-200, 0)
  group_output = node_group.nodes.new('NodeGroupOutput')
  group_output.location = (200, 0)

  # Create a Geometry Transform node
  transform_node = node_group.nodes.new('GeometryNodeTransform')
  transform_node.location = (0, 0)


  # Link the Geometry Transform node to the Group Input and Group Output
  node_group.links.new(group_input.outputs[0], transform_node.inputs[0])
  node_group.links.new(transform_node.outputs[0], group_output.inputs[0])

  ################# Nodes Setup End####################################

  #for second in end_times_words_array:
  for second in start_times_array:
    frameT = calculateFrame(second, fps)
    addKeyFrame(obj, frameT, "location")
    #addKeyFrame(obj, frame, "scale")
    # Add a keyframe for the scale at frame 10
    transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=frameT)
    print("index ", word_obj_idx)
    width_height_data = getWidthAndHeight(words[word_obj_idx])
    new_width = width_height_data["width"] + 0.34
    if width_height_data["height"] > 4:
      new_height = width_height_data["height"] + 1.2
    else:
      new_height = width_height_data_first_word["height"] + 1.3
    # Set the scale on the X-axis of the Transform node to 4
    transform_node.inputs['Scale'].default_value[0] = new_width/2
    transform_node.inputs['Scale'].default_value[1] = new_height/2
    transform_node.inputs['Scale'].default_value[2] = 1.04/2
    #changeWidthAndHeight(obj, new_width, new_height, 1.04)

    coordinate = word_coordinates[word_obj_idx]

    new_pos_x = coordinate[0]
    print (width_height_data["height"])
    if width_height_data["height"] > 4:
      #the 2 comes from the parent_cube scale being 2
      #z position is 2.35017
      setObjPosition(new_pos_x * 2, (double_row_y_position* 2)+ 2.15562,1.84, obj) 
    else:
      setObjPosition(new_pos_x * 2, (new_pos_y * 2) + 2.12562, 1.84, obj)
    transition_frames = frameT + transition_frame_rate
    addKeyFrame(obj, transition_frames, "location")
    transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=transition_frames)
    #addKeyFrame(obj, transition_frames, "scale")
    word_obj_idx += 1
  #add bevel modifier
  bpy.ops.object.modifier_add(type='BEVEL')
  bpy.context.object.modifiers["Bevel"].width = 0.1
  bpy.context.object.modifiers["Bevel"].segments = 4
  bpy.ops.object.shade_smooth()
  bpy.data.objects["highlighter_obj"].select_set(False)
    
    
def addOffsetToXAxisDoubleArrayCoordinates(arr, offset_x_percentage, words):
  new_pair_list = []
  new_list = []
  word_obj_idx = 0
  height_offset = 0.4
  for x, y in arr:
    width_heigh_data = getWidthAndHeight(words[word_obj_idx])
    new_pair_list.append(x + width_heigh_data["width"] * offset_x_percentage)
    new_pair_list.append(y + height_offset)
    new_list.append(new_pair_list)
    new_pair_list = []
    word_obj_idx += 1
  
  return new_list





#BACKGROUND PLANE#########################################################################################
#bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(5.99,-11.257,-0.066 ))
#bg_plane = bpy.context.active_object
#bg_plane.scale = (5.365, 10.430, 0)
#bg_material = bpy.data.materials.new(name="bgMaterial")
#bg_material.use_nodes = True
#bg_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.214501, 0.660533, 1)  # Color
#bg_plane.data.materials.append(bg_material)










# Create a new material
ShadowCatcher = bpy.data.materials.new(name="ShadowCatcher")
ShadowCatcher.shadow_method = 'NONE'

# Enable 'Use Nodes':
ShadowCatcher.use_nodes = True
nodes = ShadowCatcher.node_tree.nodes

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create necessary nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
principal_node = nodes.new(type='ShaderNodeBsdfPrincipled')
shader_to_rgb_node = nodes.new(type='ShaderNodeShaderToRGB')
color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
mix_shader_node = nodes.new(type='ShaderNodeMixShader')
transparent_node = nodes.new(type='ShaderNodeBsdfTransparent')

# Set up the color ramp
color_ramp_node.color_ramp.elements[0].position = 0.0
color_ramp_node.color_ramp.elements[1].position = 1

principal_node.inputs[0].default_value = (0, 0, 0, 1)
principal_node.inputs[4].default_value = 0.5


# Link nodes
links = ShadowCatcher.node_tree.links
links.new(diffuse_node.outputs['BSDF'], shader_to_rgb_node.inputs['Shader'])
links.new(shader_to_rgb_node.outputs['Color'], color_ramp_node.inputs['Fac'])
links.new(color_ramp_node.outputs['Color'], mix_shader_node.inputs['Fac'])
links.new(principal_node.outputs['BSDF'], mix_shader_node.inputs[1])
links.new(transparent_node.outputs['BSDF'], mix_shader_node.inputs[2])
links.new(mix_shader_node.outputs['Shader'], output_node.inputs['Surface'])



# Enable 'Transparent' in the Film section of the render settings
bpy.context.scene.render.film_transparent = True



bpy.ops.mesh.primitive_plane_add(enter_editmode=False,align='WORLD', location=(9.28609, -4.8434, 2.2842), scale=(1, 1, 1))
bg_plane = bpy.context.active_object
bg_plane.name = "ShadowCatcherEnglish"
bg_plane.scale = (7.917, 4.565, 1)
bg_plane.data.materials.append(ShadowCatcher)
ShadowCatcher.blend_method = 'BLEND'
ShadowCatcher.shadow_method = 'NONE'



bpy.ops.mesh.primitive_plane_add(enter_editmode=False,align='WORLD', location=(9.28609, -20.98, 2.2842), scale=(1, 1, 1))
bg_plane2 = bpy.context.active_object
bg_plane2.name = "ShadowCatcherSpanish"
bg_plane2.scale = (7.917, 4.565, 1)
bg_plane2.data.materials.append(ShadowCatcher)
ShadowCatcher.blend_method = 'BLEND'
ShadowCatcher.shadow_method = 'NONE'

# ------- MAIN -------




parent_cube.hide_render = True
createTextObject(english_words, english_words_scaled_coordinates, parent_cube, "ARLRDBD", 1, 3, 0.015)

english_word_objects = getAllChildrenObjects(parent_cube)

phonetic_array_position = addOffsetToXAxisDoubleArrayCoordinates(english_words_scaled_coordinates, 0.20, english_word_objects)
createPhoTextObject(phonetic_words, english_words_scaled_coordinates, parent_cube, "arialbd", 0.68, 2, 0.02)

applyKeyFrameToWords(parent_cube)
setupHighlighterKeyFrames(highlighter_obj, english_words_scaled_coordinates, english_word_objects) 

all_word_objects = getAllChildrenObjects(parent_cube)
addingBooleanModifierToAllChildrenObjects(all_word_objects, "clip_cube_english_1", "clip_cube_english_2")




