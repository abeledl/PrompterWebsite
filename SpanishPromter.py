import numpy as np
import bpy

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete the selected objects
bpy.ops.object.delete()

globalYCameraBG12Clips = -0.6


positions_english_array = [[530,314],[521,444],[351,574],[395,704],[528,834],[411,964],[381,1094],[586,1094],[337,1224],[603,1224],[521,1354],[409,1484],[666,1484],[320,1614],[722,1614],[381,1743],[796,1743],[288,1873],[708,1873],[810,1873],[290,2003],[579,2003],[855,2003],[549,2133],[297,2263],[537,2393],[278,2523],[346,2653],[635,2653],[318,2783],[423,2913],[722,2913],[332,3043],[481,3043],[346,3173],[519,3173],[276,3303],[598,3303],[353,3433],[316,3563],[507,3563],[656,3563],[302,3693],[647,3693],[519,3823],[572,3953],[381,4083],[388,4213],[388,4343],[710,4343],[360,4473],[817,4473],[306,4603],[374,4733],[549,4863],[290,4993],[379,5123],[433,5253],[551,5383],[322,5513],[533,5513],[589,5643],[446,5773],[698,5773],[392,5903],[463,6033],[551,6163],[490,6293],[400,6423],[554,6423],[318,6553],[757,6553],[407,6683],[491,6813],[465,6942],[568,6942],[638,6942],[500,7072],[325,7202],[731,7202],[344,7332],[493,7332],[294,7462],[449,7462],[659,7462],[486,7592],[612,7592],[238,7722],[358,7852],[740,7852],[383,7982],[290,8112],[428,8242],[530,8242],[357,8372],[438,8372],[788,8372],[404,8502],[449,8632],[484,8762],[388,8892],[446,9022],[652,9022],[211,9164],[330,9287],[558,9287],[768,9287],[260,9429]]
positions_spanish_array = [[310,1158],[563,1288],[341,1418],[264,1548],[455,1678],[362,1808],[399,1938],[521,1938],[290,2068],[551,2068],[465,2198],[425,2328],[752,2328],[357,2458],[768,2458],[341,2587],[780,2587],[318,2717],[766,2717],[836,2717],[245,2847],[535,2847],[880,2847],[577,2977],[200,3131],[563,3247],[255,3377],[341,3507],[654,3507],[220,3637],[285,3767],[892,3767],[369,3897],[463,3897],[353,4027],[474,4027],[395,4157],[540,4157],[265,4299],[264,4422],[437,4422],[530,4422],[320,4552],[652,4552],[453,4681],[523,4811],[397,4941],[285,5071],[414,5201],[689,5201],[285,5331],[789,5331],[295,5461],[390,5591],[577,5721],[269,5851],[458,5981],[400,6111],[540,6241],[318,6371],[514,6371],[537,6501],[306,6631],[820,6631],[381,6761],[418,6891],[474,7021],[502,7151],[376,7281],[554,7281],[322,7411],[855,7411],[434,7541],[428,7671],[381,7801],[502,7801],[675,7801],[453,7931],[285,8061],[682,8061],[320,8191],[465,8191],[287,8321],[418,8321],[717,8321],[516,8451],[638,8451],[166,8600],[348,8718],[806,8718],[388,8848],[388,8978],[430,9108],[500,9108],[295,9238],[430,9238],[831,9238],[404,9368],[372,9498],[327,9628],[292,9758],[516,9888],[638,9888],[181,10030],[409,10152],[624,10152],[745,10152],[195,10294]]
end_times_array = [2.58, 4.56, 5.06, 6.3999996, 7.7, 9.775001, 10.975, 12.635, 13.135, 14.175, 15.435, 15.935, 16.71, 18.01, 19.109999, 20.949999, 21.449999, 22.63, 23.13, 24.025, 24.765, 26.045, 27.385, 29.145, 30.265, 31.645, 33.149998, 34.089996, 34.589996, 35.53, 36.75, 39.309998, 40.455, 41.395, 41.715, 42.215, 43.875, 45.857002, 47.537003, 48.037003, 49.317, 50.097, 50.337]

end_times_words_array = [0, 1.46,2.08,2.58,3.3799999,4.56,5.06,5.94,6.388,7.7,9.275001,9.775001,10.975,11.915001,12.315001,12.635,13.135,13.675,14.175,15.435,15.935,16.71,18.01,18.71,18.949999,19.109999,19.609999,20.949999,21.449999,22.169998,22.39,22.63,23.13,24.025,24.765,25.305,25.545,26.045,26.765,27.145,27.385,27.885,28.904999,29.145,29.645,30.265,30.765,31.645,32.649998,33.149998,33.85,34.089996,34.589996,35.19,35.53,36.75,38.429996,39.309998,39.795002,39.955,40.455,41.395,41.715,42.215,43.555,43.875,44.375,45.617,45.857002,46.357002,46.917,47.297,47.537003,48.037003,49.317,50.097, 50.337]

start_times_array = [0.56,0.79999995,1.12,1.92,3.1999998,3.9199998,4.56,4.7999997,5.3599997,6.3199997,6.64,6.8799996,7.44,7.7599998,9.445,9.605,10.805,11.045,11.684999,11.844999,12.005,12.485,13.125,13.285,13.525,15.924999,16.244999,17.205,17.93,18.49,20.09,20.650002,20.73,20.970001,23.61,23.77,24.57,25.05,25.61,26.33,26.57,26.810001,28.285,28.685001,29.085001,29.485,29.645,30.925001,31.885,32.445,32.685,34.125,34.365,36.045,36.88,37.12,38.72,39.6,41.12,41.44,41.84,42.399998,42.559998,42.96,43.28,44.32,44.8,45.12,46.225,46.385,47.905,48.625,48.945,50.785,51.344997,51.504997,51.745,52.864998,53.504997,54.385,54.704998,55.024998,56.28,56.68,57.239998,58.2,58.44,58.68,60.92,61.64,61.879997,63.774998,64.895,65.215,66.255,66.494995,67.055,67.375,68.255,69.534996,69.935,70.655,71.134995,71.295,73.499,73.739006,74.139,74.459]

move_up_seconds = [0.79999995,1.12,1.92,3.1999998,3.9199998,4.56,5.3599997,6.64,6.8799996,7.7599998,9.605,11.045,12.005,13.285,13.525,15.924999,16.244999,17.205,18.49,20.09,20.73,23.61,24.57,25.61,26.33,28.285,29.085001,29.485,29.645,30.925001,31.885,32.685,34.365,36.045,36.88,37.12,38.72,39.6,41.12,41.44,42.399998,42.559998,43.28,44.32,44.8,45.12,46.225,47.905,48.945,50.785,51.344997,52.864998,53.504997,54.704998,56.28,58.2,58.68,60.92,61.879997,63.774998,64.895,66.255,67.375,68.255,69.534996,69.935,70.655,71.295,73.499,74.459]
scale_factor = 0.01
english_words_scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in positions_english_array]
spanish_words_scaled_coordinates = [(x * scale_factor, y * scale_factor) for x, y in positions_spanish_array]
english_words_scaled_coordinates = [(x, y + 2.6) for x, y in english_words_scaled_coordinates]
spanish_words_scaled_coordinates = [(x, y + 5) for x, y in spanish_words_scaled_coordinates]


english_paragraph = "(As) their conversation (unfolded,) flies continued their erratic dance around (the) doors and windows, their presence, a testament to the simple charm of the (roadside_stop.) The (coffee_machine) hissed steam (intermittently) adding to the ambiance. The waitress, without breaking (eye_contact) with the driver, reached behind (her) to (shut_it_off.) Meanwhile, outside the restaurant, a (solitary_figure) approached the (colossal_truck.) (He_walked) leisurely, his eyes revealing a depth of experience beyond his years. His hands, weathered and calloused, spoke of a life spent grappling with the elements. His gaze fixated on the (No_Riders_sticker) adorning the windshield, (prompting_him) to pause. A moment of indecision lingered before (he_settled) onto the (truck's_running_board,) away from the (restaurant's_hustle.)"
english_words = english_paragraph.split()
no_under_scores_english_words = [word.replace("_", " ") for word in english_words]

spanish_paragraph = '(A_medida_que) su conversación (se_desarrollaba,) moscas continuaban su errática danza alrededor (de_las) puertas y ventanas, su presencia, un testimonio a el simple encanto de el (parón_a_lado_de_la_carretera.) La (máquina_de_café) silbaba vapor (intermitentemente) contribuyendo a el ambiente. La camarera, sin romper (el_contacto_de_ojos) con el conductor, alcanzó detrás (de_ella) para (apagarlo.) (Mientras_tanto,) afuera del restaurante, una (figura_solitaria) (se_acercó) al (camión_colosal.) Caminó (sin_prisa,) sus ojos revelaban una profundidad de experiencia (más_allá) (de_su) edad. Sus manos, desgastadas y callosas, hablaban de una vida gastada luchando contra los elementos. Su mirada fijada en la (calcomanía_de_No_Pasajeros) adornando el parabrisas, incitándolo a pausar. Un momento de indecisión (se_demoró) (antes_de_que) (el_se_acomodó) en el (estribo_de_la_camioneta,) lejos de el (ajetreo_del_restaurante.)'

spanish_words = spanish_paragraph.split()
spanish_array = [word.replace("_", " ") for word in spanish_words]



phonetic_string = '"As, ðeər ˌkɒnvəˈseɪʒən ˈʌnfoʊldɪd, flaɪz kənˈtɪnjud ðer ɪˈrætɪk dæns əˈraʊnd ðə ˈdɔrz ænd ˈwɪndoʊz, ðer ˈprɛzəns, ə ˈtɛstəmənt tu ðə ˈsɪmpəl ʧɑrm əv ðə (ˈroʊdˌsaɪd_stɑp.) ðə (ˈkɒfi_məˈʃin) hɪst stim ˌɪntəˈmɪtəntli, ˈædɪŋ tu ðə ˈæmbiəns. ðə ˈweɪtrɪs, wɪˈðaʊt ˈbreɪkɪŋ (aɪ_ˈkɒntækt) wɪð ðə ˈdraɪvər, riʧt bɪˈhaɪnd hɜr tu (ʃʌt_ɪt_ɒf.) ˈMinˌhwaɪl, aʊtˈsaɪd ðə ˈrɛstərɑnt, ə (ˈsɑləˌteri_ˈfɪɡjər) əˈproʊʧt ðə (kəˈlɑsəl_trʌk) (Hi_wɔkt) ˈliʒərli, hɪz aɪz rɪˈviːlɪŋ ə dɛpθ əv ɪksˈpɪəriəns bɪˈjɒnd hɪz jɪrz. Hɪz hændz, ˈwɛðərd ænd kəˈlɔst, spoʊk əv ə laɪf spɛnt ˈɡræplɪŋ wɪð ðə ˈɛləmənts. Hɪz ɡeɪz fɪksˈeɪtɪd ɑn ðə (Noʊ_ˈraɪdərz_ˈstɪkər) əˈdɔrnɪŋ ðə ˈwɪndˌʃild, (ˈprɑmptɪŋ_ɪm) tu pɔz. ə ˈmoʊmənt əv ˌɪndɪˈsɪʒən ˈlɪŋɡərd bɪˈfɔr (hi_ˈsɛtl̩d) ˈɑntu ðə (trʌks_ˈrʌnɪŋ_ˌbɔrd) əˈweɪ frəm ðə (ˈrɛstərɑntzˈhʌsəl)'
phonetic_array_underscore = phonetic_string.split()
phonetic_array = [word.replace("_", " ") for word in phonetic_array_underscore]



bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(6.0876, -10.638 + globalYCameraBG12Clips, 14.742), rotation=(0, -0, 0), scale=(1, 1, 1))
camera_1 = bpy.context.active_object
camera_1.name = "camera_1"
camera_1.data.lens = 30
camera_1.data.dof.use_dof = True
camera_1.data.dof.aperture_fstop = 1
camera_1.data.dof.aperture_ratio = 2



last_frame = 3800

bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 2048
bpy.context.scene.render.resolution_percentage = 50
bpy.context.scene.frame_end = last_frame
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.use_ssr_refraction = True
bpy.context.scene.view_settings.view_transform = 'AgX'
bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
bpy.context.scene.eevee.use_ssr_halfres = False
bpy.context.scene.eevee.use_bokeh_jittered = True
bpy.context.scene.eevee.ssr_thickness = 0
bpy.context.scene.eevee.ssr_quality = 1
bpy.context.scene.eevee.use_motion_blur = True
bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
bpy.context.scene.eevee.bokeh_max_size = 200


bpy.context.scene.gravity[2] = 0
bpy.context.scene.gravity[1] = -5.8

bpy.context.scene.render.fps = 50

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
#bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), rotation=(-0.6, 0.12, 0.1))
#the_sun = bpy.context.active_object
#the_sun.name = "the_sun"
#the_sun.data.energy = 1


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



# Add a plane
def createBackground(location_vector, scale, bw_image_name, color_image_name, background_material_name, background_name, other_clip):
  bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=location_vector)
  background_one = bpy.context.active_object
  background_one.name = background_name
  

  return background_one

###################################################################

#clip_bg_1 = createCube((6, -20.217 + globalYCameraBG12Clips, 0), (20, 9, 6), "clip_bg_1", True)
#clip_bg_2 = createCube((6, -2.1856 + globalYCameraBG12Clips, 0), (20, 9, 6), "clip_bg_2", True)

bg_1 = createBackground((6, -5.2911 + globalYCameraBG12Clips, -0.830748), (11.294, 12.076, 4.231), "depth1.png", "bg1.jpeg", "BackgroundOneMaterial", "bg_1", "clip_bg_1")
bg_2 = createBackground((6, -15.6356 + globalYCameraBG12Clips, -1.430748), (11.294, 12.076, 4.231), "depth2.png", "bg2.jpeg", "BackgroundTwoMaterial", "bg_2", "clip_bg_2")

top_hiding_cube = createCube((6, 26.179, 0), (8, 29.9, 1), "clip_cube_english_1", True)
bottom_hiding_cube = createCube((6, -40.343, 0), (8, 32.8 , 1), "clip_cube_english_2", True)
top_hiding_cube_spanish = createCube((6, 13.614, 0), (8, 28, 1), "clip_cube_spanish_1", True)
bottom_hiding_cube_spanish = createCube((6, -45.077, 0), (8, 26.6, 1), "clip_cube_spanish_2", True)



parent_cube = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube = bpy.context.active_object
parent_cube.name = "parent_cube"

parent_cube_spanish = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube_spanish = bpy.context.active_object
parent_cube_spanish.name = "parent_cube_spanish"




highlighter_obj = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
highlighter_obj = bpy.context.active_object
highlighter_obj.name = "highlighter_obj"
highlighter_material_english = bpy.data.materials.new(name="HighlighterMaterialEnglish")
highlighter_obj.data.materials.append(highlighter_material_english)
highlighter_obj.active_material.use_nodes = True
highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (1, 0.0855381, 0.194721, 1)
highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


highlighter_obj_spanish = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
highlighter_obj_spanish = bpy.context.active_object
highlighter_obj_spanish.name = "highlighter_obj_spanish"
highlighter_material_spanish = bpy.data.materials.new(name="HighlighterMaterialSpanish")
highlighter_obj_spanish.data.materials.append(highlighter_material_spanish)
highlighter_obj_spanish.active_material.use_nodes = True
highlighter_material_spanish.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (0, 0.223059, 1, 1)
highlighter_material_spanish.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1

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
outline_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1 #Coat



#text material
text_material = bpy.data.materials.new(name="TextMaterial")
text_material.use_nodes = True
text_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
text_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.05
text_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
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
  for word, position in zip(words, positions):
    # Create a new text object-
    if (len(word) > 18):
      font_size = 1.18
      yOffSet = 0.1
    if (len(word) > 20):
      font_size =1.05
      yOffSet = 0.2
    if (len(word) >21):
      font_size = 1.02
      yOffSet = 0.2
    if (len(word)> 23):
      font_size = 1
      encounteredLongWord = True
      yOffSet = 0.3
    if (len(word) > 26):
      font_size = 0.85
      yOffSet = 0.4
    if(len(word) <= 18):
      font_size = ft
      yOffSet = 0
    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], 0))
    text_object = bpy.context.active_object
    text_object.data.body = word
    font_path = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data = bpy.data.fonts.load(font_path)
    text_object.data.font = font_data
    text_object.data.size = font_size
    text_object.data.extrude = 0.05
    text_object.data.bevel_depth = 0.03
    text_object.data.bevel_resolution = 4
    text_object.data.bevel_mode = 'ROUND'
    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')
    


    #bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], -0.01))
    ##if (encounteredLongWord):
    #  #yOs = 0.1
    #text_object2 = bpy.context.active_object
    #text_object2.name = "zoutline"
    #text_object2.data.body = word
    #font_path2 = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    #font_data2 = bpy.data.fonts.load(font_path2)
    #text_object2.data.font = font_data2
    #text_object2.data.size = font_size
    #text_object2.data.resolution_u = font_resolution
    #text_object2.data.fill_mode = 'NONE'
    ##text_object2.data.offset = 0.02
    #text_object2.data.bevel_depth = bevel_depth
    #text_object2.data.bevel_resolution = 0
    #text_object2.data.materials.append(outline_material)
    ##text_object2.active_material.use_nodes = True
    #text_object2.active_material.use_screen_refraction = True
    #text_object2.active_material.refraction_depth = 1.5
    #bpy.ops.object.convert(target='MESH')
    ##bpy.ops.object.shade_smooth()
    #text_object2.parent = parent_obj 
    
    # Set the text object as a child of the parent cube
    text_object.parent = parent_obj



  # Select all created text objects
  bpy.ops.object.select_all(action='SELECT')

def createPhoTextObject(words, positions, parent_obj, font_name, font_size, font_resolution, bevel_depth):
  # Create a new text object for each word
  ft = font_size
  for word, position in zip(words, positions):
    # Create a new text object-
    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], 0))
    text_object = bpy.context.active_object
    text_object.data.body = word
    font_path = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data = bpy.data.fonts.load(font_path)
    text_object.data.font = font_data
    text_object.data.size = font_size
    #text_object.data.extrude = 0.01
    #text_object.data.bevel_depth = 0.01
    #text_object.data.bevel_resolution = 1
    #text_object.data.bevel_mode = 'ROUND'
    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')
    


    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], -1 * position[1], -0.01))
    text_object2 = bpy.context.active_object
    text_object2.name = "zoutline"
    text_object2.data.body = word
    font_path2 = "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    font_data2 = bpy.data.fonts.load(font_path2)
    text_object2.data.font = font_data2
    text_object2.data.size = font_size
    text_object2.data.resolution_u = font_resolution
    text_object2.data.fill_mode = 'NONE'
    #text_object2.data.offset = 0.02

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
  fps = 50
  frame = 0
  transition_frame_rate = 5
  direction = [0, 1, 0]
  distance = 1.3
  #for second in end_times_array:
  for second in move_up_seconds:
    frame = calculateFrame(second, fps)
    addKeyFrame(obj, frame, "location")


    moveObject(obj, direction, distance)
    transition_frames = frame + transition_frame_rate
    addKeyFrame(obj, transition_frames, "location")

def calculateFrame(seconds, fps):
  frames = seconds * fps -5
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
  fps = 50
  frame = 0
  transition_frame_rate = 5
  word_obj_idx = 0
  pivot_to_text_length = 0.030
  height_percentage_offset = 1.20
  width_percentage_offset = 1.10
  width_height_data_first_word = getWidthAndHeight(words[word_obj_idx])
  new_pos_y = -word_coordinates[word_obj_idx][1] + width_height_data_first_word["height"]/2
  new_height = width_height_data_first_word["height"] * height_percentage_offset


  print("end_times length ",  len(end_times_words_array))
  print("words length ", len(words))
  print("coordinates length ", len(word_coordinates))

  #for second in end_times_words_array:
  for second in start_times_array:
    frame = calculateFrame(second, fps)
    addKeyFrame(obj, frame, "location")
    addKeyFrame(obj, frame, "scale")
    print("index ", word_obj_idx)
    width_height_data = getWidthAndHeight(words[word_obj_idx])
    new_width = width_height_data["width"] * width_percentage_offset
    changeWidthAndHeight(obj, new_width, new_height, 0.02)

    coordinate = word_coordinates[word_obj_idx]

    new_pos_x = coordinate[0] + width_height_data["width"]/2 + pivot_to_text_length 
    setObjPosition(new_pos_x, new_pos_y, -0.1, obj)
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






#make window light child of background
#window_light.parent = bg_1
#bounce_light.parent = bg_1  

#backgroundbpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(5.99,-5.71,-0.156 ))
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(5.99,-11.257,-0.066 ))
bg_plane = bpy.context.active_object
bg_plane.scale = (5.365, 10.430, 0)
# Create a new material
bg_material = bpy.data.materials.new(name="bgMaterial")
bg_material.use_nodes = True
bg_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.214501, 0.660533, 1)  # Color


bg_plane.data.materials.append(bg_material)
# ------- MAIN -------



parent_cube.hide_render = True
createTextObject(no_under_scores_english_words, english_words_scaled_coordinates, parent_cube, "arial", 1.16, 3, 0.015)
camera_1.data.dof.focus_object = bpy.data.objects["Text"]
english_word_objects = getAllChildrenObjects(parent_cube)

phonetic_array_position = addOffsetToXAxisDoubleArrayCoordinates(english_words_scaled_coordinates, 0.20, english_word_objects)
createPhoTextObject(phonetic_array, phonetic_array_position, parent_cube, "arialbd", 0.58, 2, 0.01)

applyKeyFrameToWords(parent_cube)
setupHighlighterKeyFrames(highlighter_obj, english_words_scaled_coordinates, english_word_objects) 

all_word_objects = getAllChildrenObjects(parent_cube)

addingBooleanModifierToAllChildrenObjects(all_word_objects, "clip_cube_english_1", "clip_cube_english_2")

#--------Spanish Word Objects---------
createTextObject(spanish_array, spanish_words_scaled_coordinates, parent_cube_spanish, "arial", 1.16, 3, 0.015)
spanish_word_objects = getAllChildrenObjects(parent_cube_spanish)
applyKeyFrameToWords(parent_cube_spanish)
setupHighlighterKeyFrames(highlighter_obj_spanish, spanish_words_scaled_coordinates, spanish_word_objects) 

addingBooleanModifierToAllChildrenObjects(spanish_word_objects, "clip_cube_spanish_1", "clip_cube_spanish_2")

