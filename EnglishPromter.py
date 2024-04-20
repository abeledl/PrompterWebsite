import numpy as np
import bpy
import math


globalYCameraBG12Clips = -0.6


positions_english_array = [[361.76, 77.33], [552.91, 77.33], [385.56, 232.33], [625.80, 232.33], [399.28, 387.33], [612.08, 387.33], [475.00, 542.33], [475.00, 697.33], [474.99, 852.33], [385.54, 1007.33], [558.36, 1007.33], [308.90, 1162.33], [552.08, 1162.33], [326.08, 1317.33], [531.95, 1317.33], [319.96, 1472.33], [479.57, 1472.33], [634.61, 1472.33], [475.00, 1627.33], [309.04, 1782.33], [536.68, 1782.33], [437.51, 1937.33], [606.01, 1937.33], [475.00, 2092.33], [474.99, 2247.33], [475.00, 2402.33], [393.31, 2557.33], [579.19, 2557.33], [475.00, 2712.33], [475.00, 2867.33], [390.13, 3022.33], [536.67, 3022.33], [312.86, 3177.33], [562.92, 3177.33], [414.15, 3332.33], [552.48, 3332.33], [475.00, 3487.33], [360.31, 3642.33], [552.48, 3642.33], [475.00, 3797.33], [412.90, 3952.33], [576.15, 3952.33], [474.99, 4107.33], [474.99, 4262.33], [474.99, 4417.33], [475.00, 4572.33], [475.00, 4727.33], [276.15, 4882.33], [552.09, 4882.33], [474.99, 5037.33], [474.99, 5192.33], [428.85, 5347.33], [679.79, 5347.33], [474.99, 5579.83]]

start_times_array = [0.82, 1.08, 1.86, 2.16, 3.28, 3.88, 4.26, 5.76, 5.94, 7.54, 7.96, 8.44, 8.72, 9.46, 9.68, 11.56, 11.78, 12.04, 12.78, 13.38, 13.68, 15.20, 15.82, 16.14, 18.16, 18.36, 19.94, 20.54, 20.82, 22.10, 23.42, 23.72, 24.14, 24.40, 25.80, 26.10, 26.68, 26.96, 27.32, 28.44, 30.06, 30.30, 30.86, 32.14, 32.44, 33.58, 34.82, 35.50, 35.76, 37.42, 37.66, 38.36, 39.28, 39.56]
#end times of the end of line

start_new_rows_seconds_with_new_row_flags = []

scale_factor = 0.01
english_words_scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in positions_english_array]
english_words_scaled_coordinates = [(x, y + 2.6) for x, y in english_words_scaled_coordinates]


english_paragraph = "His attire, though new, hinted at_a different_reality. The cheap_gray_cap still bore the stiffness of novelty, and his suit, despite its creases, spoke of recent_acquisition. A chambray_shirt, rigid with filler, clung_to_him, its coat and trousers too big and too short, respectively. New tan shoes, the army_last kind, completed the ensemble, their edges protected by horseshoe-like#half-circles."
english_words = english_paragraph.split()


phonetic_string = 'hɪz əˈtaɪər ðoʊ nuː ˈhɪntɪd æt_ə ˈdɪfərənt_riˈæləti ðə ʧiːp_ɡreɪ_kæp stɪl bɔːr ðə stɪfnəs əv ˈnɒvəlti ænd hɪz suːt dɪˈspaɪt ɪts ˈkriːsɪz spoʊk əv ˈriːsənt_ˌækwɪˈzɪʃən ə ˈʃæmbreɪ_ʃɜːrt ˈrɪdʒɪd wɪð ˈfɪlər klʌŋ_tuː_hɪm ɪts koʊt ænd ˈtraʊzərz tuː bɪɡ ænd tuː ʃɔːrt rɪˈspɛktɪvli nuː tæn ʃuːz ðə ˈɑːrmi_læst kaɪnd kəmˈpliːtɪd ðə ɑːnˈsɑːmbəl ðer ˈɛdʒɪz prəˈtɛktɪd baɪ ˈhɔːrsʃuːlaɪk#hæfˈsɜːrkəlz'
phonetic_words= phonetic_string.split()



bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(4.811, -3.5746, 6.64781), rotation=(0, -0, 0), scale=(1, 1, 1))
camera_1 = bpy.context.active_object
camera_1.name = "camera_1"
camera_1.data.lens = 30
camera_1.data.dof.use_dof = False
camera_1.data.dof.aperture_fstop = 1
camera_1.data.dof.aperture_ratio = 2
camera_1.data.type = 'ORTHO'
camera_1.data.ortho_scale = 8
camera_1.data.clip_end = 30



last_frame = 3000

bpy.context.scene.render.resolution_x = 900
bpy.context.scene.render.resolution_y = 500
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.frame_end = last_frame
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.use_ssr_refraction = True
bpy.context.scene.view_settings.view_transform = 'AgX'
bpy.context.scene.view_settings.look = 'AgX - Very High Contrast'

bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
bpy.context.scene.render.ffmpeg.codec = 'QTRLE'


bpy.context.scene.render.image_settings.color_mode = 'RGBA'
bpy.context.scene.render.ffmpeg.video_bitrate = 10000
bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'BEST'
bpy.context.scene.view_settings.look = 'AgX - Very High Contrast'
bpy.context.scene.eevee.use_ssr_halfres = False
bpy.context.scene.eevee.use_bokeh_jittered = True
bpy.context.scene.eevee.ssr_thickness = 0
bpy.context.scene.eevee.ssr_quality = 1
bpy.context.scene.eevee.use_motion_blur = True
bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
bpy.context.scene.eevee.bokeh_max_size = 200
bpy.context.scene.eevee.taa_render_samples = 128



bpy.context.scene.gravity[2] = 0
bpy.context.scene.gravity[1] = -5.8

bpy.context.scene.render.fps = 60
bpy.context.scene.eevee.shadow_cube_size = '4096'
bpy.context.scene.eevee.shadow_cascade_size = '4096'


#bpy.context.space_data.params.filename = "tesww"

#bpy.data.worlds["World"].node_tree.nodes["RGB"].outputs[0].default_value = (0, 0, 0, 1)
#AREA LIGHT
#bpy.ops.object.light_add(type='AREA', align='WORLD', location=(0, 0, 0),rotation=(0,0,0) , scale=(1, 1, 1))
#bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-0.39326, 0.096337, -0.27409),rotation=(0,4.3083,0) , scale=(0.134/2, 0.327/2, 0.071/2))
#bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-0.39326, 0.096337, -0.27409),rotation=(0,4.3083,0) , scale=(0.067, 0.1635, 0.0355))
#window_light = bpy.context.active_object
#window_light.name = "window_light"
#window_light.data.energy = 205.7
#bpy.ops.object.light_add(type='AREA', align='WORLD', location=(0.046697, -0.36449, 0.098409),rotation=(1.78793,-0.138345,-0.0163476) , scale=(0.1635, 0.067, 0.0355))
#bounce_light = bpy.context.active_object
#bounce_light.name = "bounce_light"
#bounce_light.data.energy = 105.7

rotation_x = math.radians(-32.9472)

bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), rotation=(rotation_x, 0.12, 0.1))
the_sun = bpy.context.active_object
the_sun.name = "the_sun"
the_sun.data.energy = 2.5




# Create a new material
material = bpy.data.materials.new(name="ShadowCatcher")

# Enable 'Use Nodes':
material.use_nodes = True
nodes = material.node_tree.nodes

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
color_ramp_node.color_ramp.elements[1].position = 0.239

principal_node.inputs[0].default_value = (0, 0, 0, 1)
principal_node.inputs[4].default_value = 0.5


# Link nodes
links = material.node_tree.links
links.new(diffuse_node.outputs['BSDF'], shader_to_rgb_node.inputs['Shader'])
links.new(shader_to_rgb_node.outputs['Color'], color_ramp_node.inputs['Fac'])
links.new(color_ramp_node.outputs['Color'], mix_shader_node.inputs['Fac'])
links.new(principal_node.outputs['BSDF'], mix_shader_node.inputs[1])
links.new(transparent_node.outputs['BSDF'], mix_shader_node.inputs[2])
links.new(mix_shader_node.outputs['Shader'], output_node.inputs['Surface'])



# Enable 'Transparent' in the Film section of the render settings
bpy.context.scene.render.film_transparent = True



bpy.ops.mesh.primitive_plane_add(enter_editmode=False,align='WORLD', location=(4.863, -3.5593, -0.122102), scale=(1, 1, 1))
bg_plane = bpy.context.active_object
bg_plane.scale = (3.7, -3.5593, 1)

bg_plane.data.materials.append(material)


# Set the blend mode to 'Alpha Blend' and shadow mode to 'Opaque'
bg_plane.active_material.blend_method = 'BLEND'
bg_plane.active_material.shadow_method = 'OPAQUE'


def createCube(location, scale, name, render):
  bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=location, scale=scale)
  cube = bpy.context.active_object
  cube.name = name
  cube.hide_render = render
  #cube.hide_viewport = render
  return cube

###################################################################



parent_cube = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube = bpy.context.active_object
parent_cube.name = "parent_cube"

highlighter_obj = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
highlighter_obj = bpy.context.active_object
highlighter_obj.name = "highlighter_obj"
highlighter_material_english = bpy.data.materials.new(name="HighlighterMaterialEnglish")
highlighter_obj.data.materials.append(highlighter_material_english)
highlighter_obj.active_material.use_nodes = True
highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0.213148, 1)
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
text_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.05
text_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.7

#text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


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
yellow_material.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (0, 1, 0.00649238, 1)
yellow_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


#blue material
blue_material = bpy.data.materials.new(name="BlueMaterial")
blue_material.use_nodes = True
blue_material.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (1, 0.713997, 0, 1)
blue_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


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
    #text_object.data.extrude = 0.05
    #text_object.data.bevel_depth = 0.03
    #text_object.data.bevel_resolution = 4
    #text_object.data.bevel_mode = 'ROUND'
    text_object.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object.data.align_y = 'CENTER'  # Set vertical alignment to middle
    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')
    


    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], -0.01))
    ##if (encounteredLongWord):
      #yOs = 0.1
    text_object2 = bpy.context.active_object
    text_object2.name = "zoutline"
    text_object2.data.body = word
    if doubleRow:
      text_object2.data.space_line = 1.7

    font_path2 = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data2 = bpy.data.fonts.load(font_path2)
    text_object2.data.font = font_data2
    text_object2.data.size = font_size
    text_object2.data.resolution_u = font_resolution
    text_object2.data.fill_mode = 'NONE'
    ##text_object2.data.offset = 0.02
    text_object2.data.bevel_depth = bevel_depth
    text_object2.data.bevel_resolution = 0
    text_object2.data.materials.append(outline_material)
    text_object2.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object2.data.align_y = 'CENTER'  # Set vertical alignment to middle
    #text_object2.active_material.use_nodes = True
    text_object2.active_material.use_screen_refraction = True
    text_object2.active_material.refraction_depth = 1.5
    bpy.ops.object.convert(target='MESH')
    ##bpy.ops.object.shade_smooth()
    text_object2.parent = parent_obj 
    
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
    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.48, 0))
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
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')
    


    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.48, -0.01))
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
  transition_frame_rate = 5
  direction = [0, 1, 0]
  distance = 1.55
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
  frame = 0
  transition_frame_rate = 6
  word_obj_idx = 0
  pivot_to_text_length = 0.030
  height_percentage_offset = 1
  width_percentage_offset = 1
  width_height_data_first_word = getWidthAndHeight(words[word_obj_idx])
  new_pos_y = -word_coordinates[word_obj_idx][1] - 0.2
  double_row_y_position  = -word_coordinates[word_obj_idx][1] + 0.6
  new_height = width_height_data_first_word["height"] + 0.5


  #for second in end_times_words_array:
  for second in start_times_array:
    frame = calculateFrame(second, fps)
    addKeyFrame(obj, frame, "location")
    addKeyFrame(obj, frame, "scale")
    print("index ", word_obj_idx)
    width_height_data = getWidthAndHeight(words[word_obj_idx])
    new_width = width_height_data["width"] * width_percentage_offset + 0.2
    if width_height_data["height"] > 0.8:
      new_height = width_height_data["height"] + 0.5

    changeWidthAndHeight(obj, new_width, new_height, 0.001)

    coordinate = word_coordinates[word_obj_idx]

    new_pos_x = coordinate[0]
    if width_height_data["height"] > 0.8:
      setObjPosition(new_pos_x, double_row_y_position,-0.067822, obj)
    else:
      setObjPosition(new_pos_x, new_pos_y,-0.067822, obj)
    transition_frames = frame + transition_frame_rate
    addKeyFrame(obj, transition_frames, "location")
    addKeyFrame(obj, transition_frames, "scale")
    word_obj_idx += 1
    
    
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
#ARIALNB
createTextObject(english_words, english_words_scaled_coordinates, parent_cube, "ARLRDBD", 1, 3, 0.015)
camera_1.data.dof.focus_object = bpy.data.objects["Text"]
english_word_objects = getAllChildrenObjects(parent_cube)

phonetic_array_position = addOffsetToXAxisDoubleArrayCoordinates(english_words_scaled_coordinates, 0.20, english_word_objects)
createPhoTextObject(phonetic_words, english_words_scaled_coordinates, parent_cube, "arialbd", 0.58, 2, 0.01)

applyKeyFrameToWords(parent_cube)
setupHighlighterKeyFrames(highlighter_obj, english_words_scaled_coordinates, english_word_objects) 

all_word_objects = getAllChildrenObjects(parent_cube)





