import numpy as np
import bpy
import math


globalYCameraBG12Clips = -0.6


positions_spanish_array = [[474.99, 76.80], [474.99, 231.79], [474.98, 464.27], [474.98, 696.75], [474.98, 929.23], [474.98, 1161.71], [429.68, 1316.70], [585.14, 1316.70], [474.98, 1471.69], [474.99, 1626.67], [474.98, 1781.66], [474.98, 1936.65], [474.98, 2091.64], [309.94, 2246.62], [589.91, 2246.62], [344.11, 2401.61], [530.09, 2401.61], [474.99, 2556.60], [474.98, 2711.59], [474.98, 2944.07], [474.98, 3176.55], [474.98, 3409.03], [474.98, 3641.51], [474.99, 3796.50], [359.50, 3951.49], [551.95, 3951.49], [474.98, 4106.47], [474.98, 4338.96], [422.22, 4571.44], [529.30, 4571.44], [474.98, 4803.92], [474.99, 5113.89], [474.98, 5346.37], [474.99, 5501.36], [474.99, 5656.35], [474.99, 5811.34], [474.99, 5966.32], [432.01, 6121.31], [529.29, 6121.31], [474.98, 6353.79], [283.81, 6586.27], [521.50, 6586.27], [303.38, 6741.26], [516.82, 6741.26], [474.98, 6896.25], [442.55, 7051.24], [530.09, 7051.24], [474.98, 7206.22], [407.41, 7361.21], [585.14, 7361.21], [474.98, 7516.20], [474.98, 7671.19], [474.99, 7826.17], [322.15, 7981.16], [506.65, 7981.16], [474.99, 8136.15], [474.99, 8368.63]]

start_times_array = [0.72, 1.20, 1.36, 3.92, 4.16, 5.52, 6.00, 6.24, 6.40, 7.70, 7.86, 9.62, 10.81, 11.05, 11.70, 13.38, 13.70, 14.41, 15.21, 15.62, 17.80, 18.28, 19.40, 19.72, 21.80, 21.96, 22.36, 22.76, 24.76, 25.00, 25.16, 27.07, 28.20, 28.68, 28.99, 31.07, 31.55, 32.59, 32.84, 33.23, 35.23, 35.48, 36.68, 36.92, 37.32, 37.88, 38.20, 38.36, 39.40, 39.64, 39.88, 41.48, 42.20, 43.08, 43.32, 44.04, 44.44]
#end times of the end of line


start_new_rows_seconds_with_new_row_flags = []

scale_factor = 0.01
spanish_words_scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in positions_spanish_array]
spanish_words_scaled_coordinates = [(x, y + 10.5 ) for x, y in spanish_words_scaled_coordinates]


spanish_paragraph = "En_medio de_la expansión#del_desierto_dorado, una carretera#solitaria extendida como un cuerda_salvavidas. Su asfalto_agrietado susurraba_cuentos de viajes pasados, de sueños perseguidos bajo puestas_de_sol#implacables. Cada huella#de_neumático dejaba una_impresión, una marca de existencia#transitoria en las arenas#atemporales. Remolinos#de_polvo danzaban su vals_silencioso, velando recuerdos en su abrazo#giratorio. Al amanecer, la carretera emergía de el horizonte como una promesa, llamando viajeros a recorrer su camino#interminable."
spanish_words = spanish_paragraph.split()


#phonetic_string = 'hɪz əˈtaɪər ðoʊ nuː ˈhɪntɪd æt_ə ˈdɪfərənt_riˈæləti ðə ʧiːp_ɡreɪ_kæp stɪl bɔːr ðə stɪfnəs əv ˈnɒvəlti ænd hɪz suːt dɪˈspaɪt ɪts ˈkriːsɪz spoʊk əv ˈriːsənt_ˌækwɪˈzɪʃən ə ˈʃæmbreɪ_ʃɜːrt ˈrɪdʒɪd wɪð ˈfɪlər klʌŋ_tuː_hɪm ɪts koʊt ænd ˈtraʊzərz tuː bɪɡ ænd tuː ʃɔːrt rɪˈspɛktɪvli nuː tæn ʃuːz ðə ˈɑːrmi_læst kaɪnd kəmˈpliːtɪd ðə ɑːnˈsɑːmbəl ðer ˈɛdʒɪz prəˈtɛktɪd baɪ ˈhɔːrsʃuːlaɪk#hæfˈsɜːrkəlz'
#phonetic_words= phonetic_string.split()





rotation_x = math.radians(-32.9472)


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

top_hiding_cube = createCube((9.29446, 14.0661, 2.72953), (9, 29.9, 1), "clip_cube_spanish_1", True)
bottom_hiding_cube = createCube((9.29446, -57.724, 2.72953), (9, 32.8 , 1), "clip_cube_spanish_2", True)


parent_cube = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube = bpy.context.active_object
parent_cube.name = "parent_cube_spanisih"
parent_cube.scale = (2, 2, 2)
parent_cube.location = (0, 2.25562, 2.41886)

highlighter_obj = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(2.8, -17.75, 1.8), scale=(1, 1, 1))
highlighter_obj = bpy.context.active_object
highlighter_obj.name = "highlighter_obj_spanish"
highlighter_obj.scale = (1, 1, 1)
highlighter_material_spanish = bpy.data.materials.new(name="HighlighterMaterialSpanish")
highlighter_obj.data.materials.append(highlighter_material_spanish)
highlighter_obj.active_material.use_nodes = True
highlighter_material_spanish.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.278552, 0, 0.526067, 1)


#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (1, 0.0855381, 0.194721, 1)
#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1
highlighter_material_spanish.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (0.0902944, 0, 1, 1)
highlighter_material_spanish.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.3



def min_max_norm(data):
  """
  Normalizes data to the range [0, 1]
  """
  min_val = np.min(data)
  max_val = np.max(data)
  return (data - min_val) / (max_val - min_val)


#outline material
outline_material = bpy.data.materials.new(name="OutlineMaterialSpanish")
outline_material.use_nodes = True
outline_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value =  0.298182 #roughness
#outline_material.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1 #transmission
outline_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.001617, 0.0041617, 0.0041617, 1) #color
outline_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5 #Coat
outline_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.260769



#text material
text_material = bpy.data.materials.new(name="TextMaterialSpanish")
text_material.use_nodes = True
text_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1,1, 1)
text_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic

text_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
text_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission

#text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


#refraction material
# Create a new material
material_name = "RefractionMaterialSpanish"
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


#green material
green_material = bpy.data.materials.new(name="GreenMaterial")
green_material.use_nodes = True
green_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.00992801, 0.661224, 0, 1)
green_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic
green_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
green_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
green_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
green_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission

#blue material
blue_material = bpy.data.materials.new(name="BlueMaterial")
blue_material.use_nodes = True
blue_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.125479, 1, 1)
blue_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic
blue_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
blue_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
blue_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
blue_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission


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
      text_object.data.space_line = 1.7

    font_path = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data = bpy.data.fonts.load(font_path)
    text_object.data.font = font_data
    text_object.data.size = font_size
    text_object.data.extrude = 0.05
    text_object.data.bevel_depth = 0.02
    text_object.data.bevel_resolution = 3
    #text_object.data.bevel_mode = 'ROUND'
    text_object.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object.data.align_y = 'CENTER'  # Set vertical alignment to middle
    text_object.data.fill_mode = 'FRONT'

    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(green_material)
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = 2
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.shade_smooth_by_angle()


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
    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.6, 0))
    text_object = bpy.context.active_object
    word = word.replace("_", "  ")
    doubleRow = False
    if '#' in word:
      word = word.replace('#', '\n')
      doubleRow = True


    text_object.data.body = word
    if doubleRow:
      text_object.data.space_line = 2.8
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
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')
    


    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.6, -0.01))
    text_object2 = bpy.context.active_object
    text_object2.name = "zoutline"
    text_object2.data.body = word
    if doubleRow:
      text_object2.data.space_line = 2.8
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
  double_row_y_position  = -word_coordinates[word_obj_idx][1] + 0.6
  new_height = width_height_data_first_word["height"] + 1.1

  ############GEO NODES SET UP ############################
  bpy.data.objects["highlighter_obj_spanish"].select_set(True)
  # Select the object (optional, if not already selected)
  #obj.select_set(True)
  # Make the object the active one
  bpy.context.view_layer.objects.active = obj
  # Add a Geometry Nodes modifier to the cube
  #bpy.ops.node.new_geometry_nodes_modifier()
  obj.modifiers.new(name="NodesModifier", type='NODES')
  obj.modifiers[-1].name = "geo2"
  node_modifier = obj.modifiers.get("geo2")
  bpy.ops.node.new_geometry_node_group_assign()

  #obj.node.new_geometry_node_group_assign()
  # Get the node group of the Geometry Nodes modifier
  node_group = node_modifier.node_group
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
    transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=frameT)
    print("index ", word_obj_idx)
    width_height_data = getWidthAndHeight(words[word_obj_idx])
    new_width = width_height_data["width"]  + 0.3
    if width_height_data["height"] > 3:
      new_height = width_height_data["height"] + 1.1
    else:
      new_height = width_height_data_first_word["height"] + 1.1
    #changeWidthAndHeight(obj, new_width, new_height, 1.04)
    transform_node.inputs['Scale'].default_value[0] = new_width/2
    transform_node.inputs['Scale'].default_value[1] = new_height/2
    transform_node.inputs['Scale'].default_value[2] = 1.04/2
    coordinate = word_coordinates[word_obj_idx]

    new_pos_x = coordinate[0]
    print (width_height_data["height"])
    if width_height_data["height"] > 3:
      #the 2 comes from the parent_cube scale being 2
      setObjPosition(new_pos_x * 2, (double_row_y_position* 2)+ 2.15562,1.84, obj) 
    else:
      setObjPosition(new_pos_x * 2, (new_pos_y * 2) + 2.55562, 1.84, obj)
    transition_frames = frameT + transition_frame_rate
    addKeyFrame(obj, transition_frames, "location")
    #addKeyFrame(obj, transition_frames, "scale")
    transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=transition_frames)
    word_obj_idx += 1
     #add bevel modifier
  bpy.ops.object.modifier_add(type='BEVEL')
  bpy.context.object.modifiers["Bevel"].width = 0.1
  bpy.context.object.modifiers["Bevel"].segments = 4
  bpy.ops.object.shade_smooth()
  bpy.data.objects["highlighter_obj_spanish"].select_set(False)
    
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
# ------- MAIN -------



parent_cube.hide_render = True
createTextObject(spanish_words, spanish_words_scaled_coordinates, parent_cube, "ARLRDBD", 0.75, 3, 0.015)

english_word_objects = getAllChildrenObjects(parent_cube)

applyKeyFrameToWords(parent_cube)
setupHighlighterKeyFrames(highlighter_obj, spanish_words_scaled_coordinates, english_word_objects) 

all_word_objects = getAllChildrenObjects(parent_cube)
addingBooleanModifierToAllChildrenObjects(all_word_objects, "clip_cube_spanish_1", "clip_cube_spanish_2")