from typing import List
from enum import Enum
import numpy as np
import bpy
import math
import nltk
from functions_classes import *
from font_3d_text_generator import Font3DTextGenerator

nltk.download('punkt')


# ===================== MAIN =====================

# Call the function to create the collection and add the text objects
# create_alphabet_collection("ARLRDBD")
efai_font_path = "/Users/efaideleon/Documents/abeldl GitHub/PrompterWebsite/ARLRDBD.ttf"
generator = Font3DTextGenerator(efai_font_path)
generator.create_alphabet_3d_collection()
bpy.ops.object.select_all(action='DESELECT')
# to be deleted#####
################

globalYCameraBG12Clips = -0.6

positions_english_array = [[165.52, 76.80], [248.64, 76.80], [378.80, 76.80], [494.86, 76.80], [581.68, 76.80],
                           [724.63, 76.80], [248.26, 231.79], [390.22, 231.79], [532.63, 231.79], [708.90, 231.79],
                           [193.72, 386.77], [308.34, 386.77], [436.70, 386.77], [667.51, 386.77], [400.57, 541.76],
                           [478.20, 541.76], [552.62, 541.76], [185.30, 696.75], [338.26, 696.75], [512.91, 696.75],
                           [686.00, 696.75], [313.62, 851.74], [484.16, 851.74], [645.52, 851.74], [336.01, 1006.72],
                           [510.35, 1006.72], [649.32, 1006.72], [174.66, 1161.71], [301.63, 1161.71],
                           [415.61, 1161.71], [544.41, 1161.71], [730.75, 1161.71], [229.29, 1316.70],
                           [408.06, 1316.70], [534.85, 1316.70], [730.09, 1316.70], [360.56, 1471.69],
                           [583.72, 1471.69], [249.45, 1626.67], [388.80, 1626.67], [463.76, 1626.67],
                           [655.48, 1626.67], [207.22, 1781.66], [329.07, 1781.66], [495.07, 1781.66],
                           [680.29, 1781.66], [202.05, 1936.65], [299.40, 1936.65], [421.25, 1936.65],
                           [530.02, 1936.65], [681.11, 1936.65]]

start_times_array = []
for i in range(len(positions_english_array)):
    start_times_array.append(i * 0.5)

start_times_with_if_new_line = []
for i in range(len(start_times_array)):
    start_times_with_if_new_line.append((start_times_array[i], False))

time_at_which_to_move_all_rows_with_flags_in_case_of_doulbe_row = []

new_row_positions = []

scale_factor = 0.02
english_words_scaled_coordinates = [(x * scale_factor, y * (scale_factor + 0.005)) for x, y in positions_english_array]
english_words_scaled_coordinates = [(x, y + 2.6) for x, y in english_words_scaled_coordinates]

english_paragraph = ("In the heart of the ocean, where the waves dance with the sun's "
                     "reflections, lies a tale of serenity and mystery. Beneath the surface,"
                     " creatures of wonder roam the vast blue expanse. Amongst the coral gardens,"
                     " secrets whisper, waiting to be discovered by those brave enough to dive into the depths.")

english_words = english_paragraph.split()

phonetic_string = ("In the heart of the ocean, where the waves dance with the sun's reflections,"
                   " lies a tale of serenity and mystery. Beneath the surface, creatures of wonder roam"
                   " the vast blue expanse. Amongst the coral gardens, secrets whisper, waiting to be discovered"
                   " by those brave enough to dive into the depths.")
phonetic_words = phonetic_string.split()

spanish_string = ("In the heart of the ocean, where the waves dance with the sun's reflections,"
                  " lies a tale of serenity and mystery. Beneath the surface, creatures of wonder"
                  " roam the vast blue expanse. Amongst the coral gardens, secrets whisper, waiting"
                  " to be discovered by those brave enough to dive into the depths.")

spanish_words = spanish_string.split()

tokens = nltk.word_tokenize(english_paragraph)
full_tags = nltk.pos_tag(tokens)
# Using list comprehension to filter out unwanted elements
tags = [item for item in full_tags if item[0] not in {',', '.', "'", "'s"}]
last_frame = 3000

bpy.context.scene.render.fps = 60
bpy.context.scene.eevee.shadow_cube_size = '4096'
bpy.context.scene.eevee.shadow_cascade_size = '4096'

rotation_x = math.radians(-32.9472)

# bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0),
# scale=(1, 1, 1), rotation=(rotation_x, 0.12, 0.1))
# the_sun = bpy.context.active_object
# the_sun.name = "the_sun"
# the_sun.data.energy = 2.5


###################################################################

# top_hiding_cube = createCube((9.29446, 62.6753, 2.72953), (9, 63, 1), "clip_cube_english_1", True)
# bottom_hiding_cube = createCube((9.29446, -42.4323, 2.72953), (9, 32.8 , 1), "clip_cube_english_2", True)


bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube = bpy.context.active_object
parent_cube.name = "parent_cube"
parent_cube.scale = (2, 2, 2)
parent_cube.location = (0, 2.25562, 2.41886)
rotation_x_parentcube = math.radians(90)
parent_cube.rotation_euler[0] = rotation_x_parentcube
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8), scale=(1, 1, 1))
highlighter_obj = bpy.context.active_object
highlighter_obj.name = "highlighter_obj"
# rotate
rotation_x_highlighter = math.radians(90)
highlighter_obj.rotation_euler[0] = rotation_x_highlighter

highlighter_material_english = bpy.data.materials.new(name="HighlighterMaterialEnglish")
hl_material = bpy.data.materials.get("hl_material")
highlighter_obj.data.materials.append(hl_material)
# highlighter_obj.active_material.use_nodes = True
# highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.478878, 0, 0.106461, 1)
# highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (1, 0.0855381, 0.194721, 1)
# highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


# outline material
outline_material = bpy.data.materials.new(name="OutlineMaterial")
outline_material.use_nodes = True
outline_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.298182  # roughness
# outline_material.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1 #transmission
# color
outline_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.001617, 0.0041617, 0.0041617, 1)
outline_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5  # Coat
outline_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.260769

# text material
text_material = bpy.data.materials.new(name="TextMaterial")
text_material.use_nodes = True
text_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)
text_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525  # metallic
text_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638  # roughness
text_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0  # emission

# text_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1


# ############cliping materialenglish #########
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

# refraction material
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

# yellow material
yellow_material = bpy.data.materials.new(name="yellowMaterial")
yellow_material.use_nodes = True
yellow_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 0, 1)
yellow_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525  # metallic
yellow_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
yellow_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638  # roughness
yellow_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
yellow_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0  # emission

# blue material
green_material = bpy.data.materials.new(name="GreenMaterial")
green_material.use_nodes = True
green_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.00992801, 0.661224, 0, 1)
green_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525  # metallic
green_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
green_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638  # roughness
green_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
green_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0  # emission

# blue material
blue_material = bpy.data.materials.new(name="BlueMaterial")
blue_material.use_nodes = True
blue_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.125479, 1, 1)
blue_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525  # metallic
blue_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
blue_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638  # roughness
blue_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
blue_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0  # emission

verb_material = bpy.data.materials.get("verb_material")
noun_material = bpy.data.materials.get("noun_material")
adjective_material = bpy.data.materials.get("adjective_material")
article_material = bpy.data.materials.get("article_material")
adverb_material = bpy.data.materials.get("adverb_material")
pronoun_material = bpy.data.materials.get("pronoun_material")
preposition_material = bpy.data.materials.get("preposition_material")
conjunction_material = bpy.data.materials.get("conjunction_material")

# BACKGROUND PLANE#########################################################################################
# bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(5.99,-11.257,-0.066 ))
# bg_plane = bpy.context.active_object
# bg_plane.scale = (5.365, 10.430, 0)
# bg_material = bpy.data.materials.new(name="bgMaterial")
# bg_material.use_nodes = True
# bg_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.214501, 0.660533, 1)  # Color
# bg_plane.data.materials.append(bg_material)


parent_cube.hide_render = True
# sticker_letters_manager = StickerLettersManager()
three_d_letters_manager = ThreeDLettersManager()
materials_instance = Materials()
material_as = MaterialAssigner(materials_instance)
# sticker_word_assembler = WordAssembler(sticker_letters_manager.sticker_letters_collection,
# 'spanish_sticker_words', 's', material_as)
threed_word_assembler = WordAssembler(three_d_letters_manager.three_d_letters_collection, 'english_3d_words', '_3d',
                                      material_as)

tag_cleaner = PartOfSpeechTagAssigner(tags)
tags = tag_cleaner.get_words_and_tags_list()
words_and_positions_and_part_of_speech_list = package_words_position_and_part_of_speech(
    english_words, english_words_scaled_coordinates, tags, start_times_array)
rp, dt, tl = create_text_objects(words_and_positions_and_part_of_speech_list, parent_cube,
                                 start_times_array, three_d_letters_manager, threed_word_assembler)

new_row_positions = convert_list_of_row_position_to_list(rp)
time_at_which_to_move_all_rows_with_flags_in_case_of_doulbe_row = convert_timestamp_flag_list_to_list(dt)
start_times_with_if_new_line = convert_timestamp_flag_list_to_list(tl)
english_word_objects = get_all_children_objects(parent_cube)

phonetic_array_position = add_offset_to_x_axis_double_array_coordinates(english_words_scaled_coordinates, 0.20,
                                                                        english_word_objects)
create_children_text_object(phonetic_words, english_words_scaled_coordinates, parent_cube, "ARLRDBD", 0.68, 2, 0.02, 0,
                            0.7, True)
create_children_text_object(spanish_words, english_words_scaled_coordinates, parent_cube, "ARLRDBD", 0.68, 2, 0.02,
                            0.05,
                            1.4, False)
# createChildrenTextObjectsFromCollection(spanish_words, sticker_letters_manager, sticker_word_assembler,
# english_words_scaled_coordinates, parent_cube, 1.4)

apply_key_frame_to_words(parent_cube)
setup_highlighter_key_frames(highlighter_obj, english_words_scaled_coordinates, threed_word_assembler)

all_word_objects = get_all_children_objects(parent_cube)
# addingBooleanModifierToAllChildrenObjects(all_word_objects, "clip_cube_english_1", "clip_cube_english_2")
