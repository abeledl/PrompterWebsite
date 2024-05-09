from typing import List, Tuple
from enum import Enum
import numpy as np
import bpy
import math
import nltk
from abc import ABC, abstractmethod

nltk.download('punkt')

def addBooleanModifier(obj, clip_obj_name, modifier_name):
  obj.modifiers.new(name=modifier_name, type='BOOLEAN')
  obj.modifiers[modifier_name].object = bpy.data.objects[clip_obj_name]
  obj.modifiers[modifier_name].solver = 'FAST'
  #obj.modifiers[modifier_name].double_threshold = 0.001


def min_max_norm(data):
  """
  Normalizes data to the range [0, 1]
  """
  min_val = np.min(data)
  max_val = np.max(data)
  return (data - min_val) / (max_val - min_val)

class PartsOfSpeechEnum(Enum):
    VERB = "verb"
    NOUN = "noun"
    ADJECTIVE = "adjective"
    ARTICLE = "article"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUCTION = "conjuction"
    INFINITIVE = "infinitive"

class PartOfSpeechTagsDictionary():
    def __init__(self):
        self.part_of_speech = PartsOfSpeechEnum
        self.dictionary = {
            self.part_of_speech.VERB: ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
            self.part_of_speech.NOUN: ['NN', 'NNS', 'NNP', 'NNPS'],
            self.part_of_speech.ADJECTIVE: ['JJ', 'JJR', 'JJS'],
            self.part_of_speech.ARTICLE: ['DT', 'PDT', 'WDT'],
            self.part_of_speech.ADVERB: ['RB', 'RBR', 'RBS', 'WRB'],
            self.part_of_speech.PRONOUN: ['PRP', 'PRP$', 'WP', 'WP$'],
            self.part_of_speech.PREPOSITION: ['IN'],
            self.part_of_speech.CONJUCTION: ['CC'],
            self.part_of_speech.INFINITIVE: ['IF'] # I made the IF tag up
        }

class Position():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class TimestampNewline():
    def __init__(self, timestamp: float, is_newline: bool):
        self.timestamp = timestamp
        self.is_newline = is_newline

class WordData():
    def __init__(self, word: str, position: Position|None, part_of_speech: PartsOfSpeechEnum|None, is_double_row: bool, timestamp_and_newline: TimestampNewline):
        self.word = word
        self.position = position
        self.part_of_speech = part_of_speech
        self.is_double_row = is_double_row
        self.timestamp_and_newline = timestamp_and_newline

class RowPosition():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class WordAndPartOfSpeechTag():
    def __init__(self, word: str, part_of_speech_tag: str):
        self.word = word
        self.part_of_speech_tag = part_of_speech_tag

class Materials():
    def __init__(self):
        self.verb_material = bpy.data.materials.get("verb_material")
        self.noun_material = bpy.data.materials.get("noun_material")
        self.adjective_material = bpy.data.materials.get("adjective_material")
        self.article_material = bpy.data.materials.get("article_material")
        self.adverb_material = bpy.data.materials.get("adverb_material")
        self.pronoun_material = bpy.data.materials.get("pronoun_material")
        self.preposition_material = bpy.data.materials.get("preposition_material")
        self.conjunction_material = bpy.data.materials.get("conjunction_material")

class PartOfSpeechTagIdentifier():
    def __init__(self):
        self.part_of_speech_tags = PartOfSpeechTagsDictionary()
        self.parts_of_speech = PartsOfSpeechEnum

    def get_part_of_speech(self, tag: str):
        for part_of_speech in self.parts_of_speech:
            if tag in self.part_of_speech_tags.dictionary[part_of_speech]:
                return part_of_speech

class PartOfSpeechTagAssigner():
    def __init__(self, words_and_tags_list):
        self.new_words_and_tags_list = []
        self.part_of_speech_identifier = PartOfSpeechTagIdentifier()
        self.words_and_tags_list = words_and_tags_list
        self.parts_of_speech = PartsOfSpeechEnum

    def get_part_of_speech_tag_of_word_at(self, index: int):
        return self.words_and_tags_list[index][1]

    def get_word_at(self, index: int):
        return self.words_and_tags_list[index][0]

    def is_verb(self, index: int):
        part_of_speech_tag = self.get_part_of_speech_tag_of_word_at(index)
        return  self.parts_of_speech.VERB == self.part_of_speech_identifier.get_part_of_speech(part_of_speech_tag)

    def is_preposition(self, index: int):
        current_word = self.get_word_at(index)
        next_word_index = index + 1
        #if to is not followed by a verb, then it is a preposition
        return (current_word == 'to' and not self.is_verb(next_word_index))

    def is_infinitive(self, index: int):
        current_word = self.get_word_at(index)
        next_word_index = index + 1
        #if to is followed by a verb, then it is infinitive
        return (current_word == 'to' and (self.is_verb(next_word_index)))

    def get_words_and_tags_list(self):
        for index in range(len(self.words_and_tags_list)):
            if self.is_infinitive(index):
                self.new_words_and_tags_list.append((self.words_and_tags_list[index][0], 'IF'))
            elif self.is_preposition(index):
                self.new_words_and_tags_list.append((self.words_and_tags_list[index][0], 'IN'))
            else:
                self.new_words_and_tags_list.append((self.words_and_tags_list[index][0], self.words_and_tags_list[index][1]))
        return self.new_words_and_tags_list

class MaterialAssigner():
    def __init__(self, materials: Materials):
        self.materials = materials
        self.parts_of_speech = PartsOfSpeechEnum
        self.part_of_speech_to_material_map = {
            self.parts_of_speech.VERB : self.materials.verb_material,
            self.parts_of_speech.NOUN : self.materials.noun_material,
            self.parts_of_speech.ADJECTIVE : self.materials.adjective_material,
            self.parts_of_speech.ARTICLE : self.materials.article_material,
            self.parts_of_speech.ADVERB : self.materials.adverb_material,
            self.parts_of_speech.PRONOUN : self.materials.pronoun_material,
            self.parts_of_speech.PREPOSITION : self.materials.preposition_material,
            self.parts_of_speech.CONJUCTION : self.materials.conjunction_material,
            self.parts_of_speech.INFINITIVE : self.materials.verb_material
        }

    def get_material(self, word: WordData):
        if word.part_of_speech:
            return self.part_of_speech_to_material_map.get(word.part_of_speech)

class TextObject():
    SPACE_LINE_AMOUNT = 1.6
    EXTRUSION = 0.05
    BEVEL_DEPTH = 0.02
    BEVEL_RESOLUTION = 3
    FILL_MODE = 'BOTH'
    X_ALIGNMENT = 'CENTER'
    Y_ALIGNMENT = 'CENTER'
    RESOLUTION = 2

    def __init__(self, x_position: float, y_position: float, word: str, double_row: bool, parent_obj, font_path: str, font_size: float, material, modifier, mod_name):
        bpy.ops.object.text_add(enter_editmode=False, location=(x_position, y_position, 0))
        self.text_object = bpy.context.active_object
        self.set_body_to(word)
        self.add_space_line(self.SPACE_LINE_AMOUNT, double_row)
        self.set_font(font_path)
        self.set_size(font_size)
        self.set_extrusion(self.EXTRUSION)
        self.set_bevel_depth_and_resolution(self.BEVEL_DEPTH, self.BEVEL_RESOLUTION)
        self.set_fill_mode(self.FILL_MODE)
        self.set_x_and_y_alignment(self.X_ALIGNMENT, self.Y_ALIGNMENT)
        self.set_material(material)
        self.set_resolution(self.RESOLUTION)
        self.convert_to_mesh()
        self.shade_smooth_by_angle()
        self.set_parent_obj(parent_obj)
        self.apply_modifier(modifier, mod_name)

    def set_body_to(self, word: str):
        self.text_object.data.body = word

    def add_space_line(self, amount: float, double_row: bool):
        if double_row:
            self.text_object.data.space_line = amount

    def set_font(self, font_path: str):
        font_data = bpy.data.fonts.load(font_path)
        self.text_object.data.font = font_data

    def set_size(self, size: float):
        self.text_object.data.size = size

    def set_extrusion(self, amount: float):
        self.text_object.data.extrude = amount

    def set_bevel_depth_and_resolution(self, depth: float, resolution: float):
        self.text_object.data.bevel_depth = depth
        self.text_object.data.bevel_resolution = resolution

    def set_fill_mode(self, mode: str):
        self.text_object.data.fill_mode = mode

    def set_x_and_y_alignment(self, x_alignment: str, y_alignment: str):
        self.text_object.data.align_x = x_alignment  # Set horizontal alignment to center
        self.text_object.data.align_y = y_alignment  # Set vertical alignment to middle

    def set_material(self, material):
        self.text_object.data.materials.append(material)

    def set_resolution(self, resolution: float):
        self.text_object.data.resolution_u = resolution

    def set_parent_obj(self, parent_obj):
        self.text_object.parent = parent_obj

    def convert_to_mesh(self):
        bpy.ops.object.convert(target='MESH')

    def shade_smooth_by_angle(self):
        bpy.ops.object.shade_smooth_by_angle()

    def apply_modifier(self, modifier, mod_name):
        if  self.text_object.type == 'MESH':
            # Add a new Geometry Node modifier to the object
            new_modifier = self.text_object.modifiers.new(name=mod_name, type='NODES')
            # Copy the node group (geometry node tree) from 'outline_geo'
            if modifier:
                new_modifier.node_group = modifier.node_group

def package_words_and_part_of_speech(words_and_part_of_speech_tags):
    list_of_words_and_part_of_speech_tags = []
    for word, part_of_speech_tag in words_and_part_of_speech_tags:
        list_of_words_and_part_of_speech_tags.append(WordAndPartOfSpeechTag(word, part_of_speech_tag))
    return list_of_words_and_part_of_speech_tags

def convertToListOfRowPositions(list):
    position_list: List[RowPosition] = []
    for position in list:
        position_list.append(RowPosition(position[0], position[1]))
    return position_list

def convertToTimestampFlagList(list):
    timestamp_list: List[TimestampNewline] = []
    for item in list:
        timestamp_list.append(TimestampNewline(item[0], item[1]))
    return timestamp_list

def convertTimestampFlagListToList(list: List[TimestampNewline]):
    clear_list = []
    for timestamp_and_newline in list:
        clear_list.append((timestamp_and_newline.timestamp, timestamp_and_newline.is_newline))
    return clear_list

def convertListOfRowPositionToList(list: List[RowPosition]):
    clear_list = []
    for position in list:
        clear_list.append((position.x, position.y))
    return clear_list

class TextObjectsCreator():
    text_objects_list = []

    def __init__(self, words: List[WordData]):
        self.words = words
        self.materials = Materials()
        self.material_assigner = MaterialAssigner(self.materials)



    def get_modifier(self, container_obj, mod_name):
        # Get the active object
        gn_modifier = None
        # Check if 'outline_geo' is a modifier of the active object
        if 'outline_geo' in container_obj.modifiers:
            # Get the 'outline_geo' modifier
            gn_modifier = container_obj.modifiers[mod_name]
        return gn_modifier

    def create_geometry_node_outline(self):
        outline_material = bpy.data.materials.new(name="OutlineMaterial_2")
        outline_material.use_nodes = True
        outline_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 0, 1) #color

        outline_obj = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8), scale=(1, 1, 1))
        outline_obj = bpy.context.active_object
        outline_obj.name = "outline_obj"

        # Make the object the active one
        bpy.context.view_layer.objects.active = outline_obj
        # Add a Geometry Nodes modifier to the cube
        outline_obj.modifiers.new(name="NodesModifier", type='NODES')
        outline_obj.modifiers[-1].name = "outline_geo"
        node_modifier = outline_obj.modifiers.get("outline_geo")
        bpy.ops.node.new_geometry_node_group_assign()

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

        join_geomtry_node = node_group.nodes.new('GeometryNodeJoinGeometry')
        join_geomtry_node.location = (0, 0)
        flip_faces_node = node_group.nodes.new('GeometryNodeFlipFaces')
        flip_faces_node.location = (-100, -100)
        set_position_node = node_group.nodes.new('GeometryNodeSetPosition')
        set_position_node.location = (-200, -100)
        vector_math = node_group.nodes.new('ShaderNodeVectorMath')
        vector_math.location = (-300, -100)
        normal_vector = node_group.nodes.new('GeometryNodeInputNormal')
        normal_vector.location = (-400, -100)
        set_material = node_group.nodes.new('GeometryNodeSetMaterial')
        set_material.location = (100, -100)


        vector_math.operation = 'SCALE'
        vector_math.inputs[3].default_value = 0.04
        set_material.inputs[2].default_value = bpy.data.materials["OutlineMaterial_2"]


        node_group.links.new(group_input.outputs[0], join_geomtry_node.inputs[0])
        node_group.links.new(group_input.outputs[0], set_position_node.inputs[0])
        node_group.links.new(vector_math.outputs[0], set_position_node.inputs[3])
        node_group.links.new(normal_vector.outputs[0], vector_math.inputs[0])
        node_group.links.new(set_position_node.outputs[0], flip_faces_node.inputs[0])
        node_group.links.new(join_geomtry_node.outputs[0], group_output.inputs[0])
        node_group.links.new(flip_faces_node.outputs[0], set_material.inputs[0])
        node_group.links.new(set_material.outputs[0], join_geomtry_node.inputs[0])
        return outline_obj

    def create_text_objects(self, parent_obj, font_path, font_size):
        outline_obj = self.create_geometry_node_outline()
        modifier = self.get_modifier(outline_obj, 'outline_geo')
        for data in self.words:
            material = self.material_assigner.get_material(data)

            if data.position:
                self.text_objects_list.append(TextObject(data.position.x, data.position.y, data.word , data.is_double_row, parent_obj, font_path, font_size, material, modifier, 'outline_geo'))

class RowsCalculator():
    def __init__(self):
        self.rows_positions: List[RowPosition] = []

    def get_rows(self, word_data: List[WordData]):
        first_row_position = word_data[0].position

        if first_row_position:
            prev_word_position_y = first_row_position.y
            for word in word_data:
                if word.position:
                    current_row_position_y = word.position.y
                    if current_row_position_y < prev_word_position_y:
                        self.rows_positions.append(RowPosition(word.position.x, -word.position.y))
                        prev_word_position_y = current_row_position_y
        return self.rows_positions

class TimeStampCreator():
    def __init__(self, start_times_array):
        self.timestamps: List[TimestampNewline] = []
        self.double_row_timestamps: List[TimestampNewline] = []
        self.start_times_array = start_times_array
        self.counter = 0

    def get_timestamps(self, word_data: List[WordData]):
        first_word_position = word_data[0].position
        if first_word_position:
            prev_word_position_y = first_word_position.y
            for word in word_data:
                if word.position:
                    if word.position.y < prev_word_position_y:
                        word.timestamp_and_newline.is_newline = True
                        prev_word_position_y = word.position.y
                self.timestamps.append(word.timestamp_and_newline)
        return self.timestamps

    def get_double_row_timestamps(self,word_data: List[WordData], max_number_of_rows):
        first_word_position = word_data[0].position
        self.counter = 0
        if first_word_position:
            prev_word_position_y = first_word_position.y
            for word in word_data:
                if word.position:
                    if word.position.y < prev_word_position_y:
                        self.counter += 1
                        if self.counter == max_number_of_rows:
                            self.counter = 0
                            if word.is_double_row:
                                self.double_row_timestamps.append(TimestampNewline(word.timestamp_and_newline.timestamp, True))
                            else:
                                self.double_row_timestamps.append(TimestampNewline(word.timestamp_and_newline.timestamp, False))
                        prev_word_position_y = word.position.y
        return self.double_row_timestamps

def createTextObjects(
    words_and_positions_and_part_of_speech_list, parent_obj,
    font_name, font_size, font_resolution,
    bevel_depth, start_times_array,
):

    font_path = "/Users/efaideleon/Documents/abeldl Github/PrompterWebsite/" + font_name + ".ttf"
    text_objects_creator = TextObjectsCreator(words_and_positions_and_part_of_speech_list)
    text_objects_creator.create_text_objects(parent_obj, font_path, font_size)
    rows_position_calculator = RowsCalculator()
    rows_position = rows_position_calculator.get_rows(words_and_positions_and_part_of_speech_list)
    timestamp_creator = TimeStampCreator(start_times_array)
    timestamps = timestamp_creator.get_timestamps(words_and_positions_and_part_of_speech_list)

    for timestamps_and_newline in timestamps:
        print("time: ", timestamps_and_newline.timestamp, " flag: ", timestamps_and_newline.is_newline)
    double_row_timestamps = timestamp_creator.get_double_row_timestamps(words_and_positions_and_part_of_speech_list, 2)
    bpy.ops.object.select_all(action='SELECT')


    return rows_position, double_row_timestamps, timestamps

#######################################################################################################################################
############################################################# REFACTORING #############################################################
#######################################################################################################################################

def createChildrenTextObject(words, positions, parent_obj, font_name, font_size, font_resolution, bevel_depth, extrution, verticalOffset,  outline):
  # Create a new text object for each word
  ft = font_size
  for word, position in zip(words, positions):
    # Create a new text object-
    bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - verticalOffset, 0))
    text_object = bpy.context.active_object
    word = word.replace("_", "  ")
    doubleRow = False
    if '#' in word:
      word = word.replace('#', '\n')
      doubleRow = True


    text_object.data.body = word
    if doubleRow:
      text_object.data.space_line = 2.3
    font_path = "/Users/efaideleon/Documents/abeldl Github/PrompterWebsite/" + font_name + ".ttf"
    font_data = bpy.data.fonts.load(font_path)
    text_object.data.font = font_data
    text_object.data.size = font_size
    text_object.data.align_x = 'CENTER'  # Set horizontal alignment to center
    text_object.data.align_y = 'CENTER'  # Set vertical alignment to middle
    text_object.data.extrude = extrution
    #text_object.data.bevel_depth = 0.01
    #text_object.data.bevel_resolution = 1
    #text_object.data.bevel_mode = 'ROUND'
    text_object.data.materials.append(text_material)
    text_object.data.materials.append(yellow_material)
    text_object.data.materials.append(green_material)
    text_object.data.materials.append(blue_material)
    text_object.data.resolution_u = font_resolution
    bpy.ops.object.convert(target='MESH')

    if outline:
      bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - 0.7, -0.01))
      text_object2 = bpy.context.active_object
      text_object2.name = "zoutline"
      text_object2.data.body = word
      if doubleRow:
        text_object2.data.space_line = 2.3
      font_path2 = "/Users/efaideleon/Documents/abeldl Github/PrompterWebsite/" + font_name + ".ttf"
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
      text_object2.parent = parent_obj
    #bpy.ops.object.shade_smooth()

    # Set the text object as a child of the parent cube
    text_object.parent = parent_obj




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
  direction = [0, 0, 1]
  distance = 15.5 # amount to move everything by
  #for second in end_times_array:
  for second, bool_val in time_at_which_to_move_all_rows_with_flags_in_case_of_doulbe_row:
    frame = calculateFrame(second, fps)
    addKeyFrame(obj, frame, "location")

    if bool_val == True:
      moveObject(obj, direction, distance)
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

def findVerticalPositionOfRow(coordiantes, row_number):
  return coordiantes[row_number][1]

def setupHighlighterKeyFrames(obj, word_coordinates, words):
  fps = 60
  frameT = 0
  transition_frame_rate = 10
  word_obj_idx = 0
  pivot_to_text_length = 0.030
  height_percentage_offset = 1
  width_percentage_offset = 1
  width_height_data_first_word = getWidthAndHeight(words[word_obj_idx])
  new_pos_y = 0
  first_row_pos_y = -word_coordinates[word_obj_idx][1] - 0.52
  second_row_pos_y = -new_row_positions[0][1] -0.5
  double_row_y_position  = -word_coordinates[word_obj_idx][1] + 0.52
  new_height = width_height_data_first_word["height"] + 1.1
  inSecondRow = False

  ############GEO NODES SET UP ############################
  bpy.data.objects["highlighter_obj"].select_set(True)
  # Select the object (optional, if not already selected)
  #obj.select_set(True)
  # Make the object the active one
  bpy.context.view_layer.objects.active = obj
  # Add a Geometry Nodes modifier to the cube
  obj.modifiers.new(name="NodesModifier", type='NODES')
  obj.modifiers[0].name = "geo1"
  node_modifier = obj.modifiers.get("geo1")
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
  for second, isNewLine in start_times_with_if_new_line:
    frameT = calculateFrame(second, fps)
    addKeyFrame(obj, frameT, "location")
    #addKeyFrame(obj, frame, "scale")
    # Add a keyframe for the scale at frame 10
    transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=frameT)
    width_height_data = getWidthAndHeight(words[word_obj_idx])
    new_width = width_height_data["width"] + 0.7
    if width_height_data["height"] > 4:
      new_height = width_height_data["height"] + 1.27
    else:
      new_height = width_height_data_first_word["height"] + 3.5
    # Set the scale on the X-axis of the Transform node to 4
    transform_node.inputs['Scale'].default_value[0] = new_width/2
    transform_node.inputs['Scale'].default_value[1] = 1.04/2
    transform_node.inputs['Scale'].default_value[2] = new_height/2
    #changeWidthAndHeight(obj, new_width, new_height, 1.04)

    coordinate = word_coordinates[word_obj_idx]

    new_pos_x = coordinate[0]

    if isNewLine:
      inSecondRow = not inSecondRow #toggle
    if inSecondRow:
      new_pos_y = second_row_pos_y
    else:
      new_pos_y = first_row_pos_y
    setObjPosition(new_pos_x * 2, 2.8,  (new_pos_y * 2) + 2.12562, obj)
    transition_frames = frameT + transition_frame_rate
    addKeyFrame(obj, transition_frames, "location")
    transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=transition_frames)
    #addKeyFrame(obj, transition_frames, "scale")
    word_obj_idx += 1
  #add bevel modifier
  bpy.ops.object.modifier_add(type='BEVEL')
  bpy.context.object.modifiers["Bevel"].width = 0.2
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

def shadowcather(x, y, z, scale_x, scale_y, scale_z, name):
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False,align='WORLD', location=(9.28609, -4.8434, 2.2842), scale=(1, 1, 1))
    bg_plane = bpy.context.active_object
    bg_plane.name = "ShadowCatcherEnglish"
    bg_plane.scale = (7.917, 4.565, 1)
    bg_plane.data.materials.append(ShadowCatcher)
    ShadowCatcher.blend_method = 'BLEND'
    ShadowCatcher.shadow_method = 'NONE'


def packageWordsPositionAndPartOfSpeech(words, position, words_and_part_of_speech_tags, start_times_array):
    list = []
    part_of_speech_identifier = PartOfSpeechTagIdentifier()
    for word, position, word_and_part_of_speech_tag, start_time in zip(words, position, words_and_part_of_speech_tags, start_times_array):
        x_pos = position[0]
        y_pos = -1 * position[1]
        word = word.replace("_", " ")
        is_double_row = False
        if '#' in word:
            word = word.replace('#', '\n')
            is_double_row = True

        list.append(WordData(word, Position(x_pos, y_pos), part_of_speech_identifier.get_part_of_speech(word_and_part_of_speech_tag[1]), is_double_row, TimestampNewline(start_time, False)))
    return list


#===================== MAIN =====================

globalYCameraBG12Clips = -0.6


positions_english_array = [[198.64, 76.80], [272.88, 76.80], [389.10, 76.80], [492.74, 76.80], [570.28, 76.80], [697.93, 76.80], [272.54, 231.80], [399.31, 231.80], [526.47, 231.80], [683.86, 231.80], [223.85, 386.80], [326.21, 386.80], [440.82, 386.80], [646.90, 386.80], [408.56, 541.80], [477.88, 541.80], [544.32, 541.80], [216.34, 696.80], [352.93, 696.80], [508.87, 696.80], [663.42, 696.80], [330.90, 851.80], [483.18, 851.80], [627.27, 851.80], [350.90, 1006.80], [506.58, 1006.80], [630.67, 1006.80], [206.83, 1161.80], [320.21, 1161.80], [421.99, 1161.80], [536.99, 1161.80], [703.38, 1161.80], [255.62, 1316.80], [415.24, 1316.80], [528.46, 1316.80], [702.78, 1316.80], [372.83, 1471.80], [572.09, 1471.80], [273.62, 1626.80], [398.03, 1626.80], [464.97, 1626.80], [636.15, 1626.80], [235.91, 1781.80], [344.70, 1781.80], [492.91, 1781.80], [658.29, 1781.80], [231.28, 1936.80], [318.21, 1936.80], [427.01, 1936.80], [524.14, 1936.80], [659.05, 1936.80]]

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


english_paragraph = "In the heart of the ocean, where the waves dance with the sun's reflections, lies a tale of serenity and mystery. Beneath the surface, creatures of wonder roam the vast blue expanse. Amongst the coral gardens, secrets whisper, waiting to be discovered by those brave enough to dive into the depths."
english_words = english_paragraph.split()


phonetic_string = "In the heart of the ocean, where the waves dance with the sun's reflections, lies a tale of serenity and mystery. Beneath the surface, creatures of wonder roam the vast blue expanse. Amongst the coral gardens, secrets whisper, waiting to be discovered by those brave enough to dive into the depths."
phonetic_words= phonetic_string.split()

spanish_string = "In the heart of the ocean, where the waves dance with the sun's reflections, lies a tale of serenity and mystery. Beneath the surface, creatures of wonder roam the vast blue expanse. Amongst the coral gardens, secrets whisper, waiting to be discovered by those brave enough to dive into the depths."

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

#bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1), rotation=(rotation_x, 0.12, 0.1))
#the_sun = bpy.context.active_object
#the_sun.name = "the_sun"
#the_sun.data.energy = 2.5


###################################################################

#top_hiding_cube = createCube((9.29446, 62.6753, 2.72953), (9, 63, 1), "clip_cube_english_1", True)
#bottom_hiding_cube = createCube((9.29446, -42.4323, 2.72953), (9, 32.8 , 1), "clip_cube_english_2", True)


parent_cube = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
parent_cube = bpy.context.active_object
parent_cube.name = "parent_cube"
parent_cube.scale = (2, 2, 2)
parent_cube.location = (0, 2.25562, 2.41886)
rotation_x_parentcube = math.radians(90)
parent_cube.rotation_euler[0] = rotation_x_parentcube
highlighter_obj = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8), scale=(1, 1, 1))
highlighter_obj = bpy.context.active_object
highlighter_obj.name = "highlighter_obj"
highlighter_obj.scale = (1, 1, 1)
highlighter_material_english = bpy.data.materials.new(name="HighlighterMaterialEnglish")

hl_material = bpy.data.materials.get("hl_material")
highlighter_obj.data.materials.append(hl_material)
#highlighter_obj.active_material.use_nodes = True
#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.478878, 0, 0.106461, 1)
#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[26].default_value = (1, 0.0855381, 0.194721, 1)
#highlighter_material_english.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 1



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

#blue material
blue_material = bpy.data.materials.new(name="BlueMaterial")
blue_material.use_nodes = True
blue_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.125479, 1, 1)
blue_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.886525 #metallic
blue_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1
blue_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.510638 #roughness
blue_material.node_tree.nodes["Principled BSDF"].inputs[12].default_value = 1
blue_material.node_tree.nodes["Principled BSDF"].inputs[27].default_value = 0.0 #emission

verb_material = bpy.data.materials.get("verb_material")
noun_material = bpy.data.materials.get("noun_material")
adjective_material = bpy.data.materials.get("adjective_material")
article_material = bpy.data.materials.get("article_material")
adverb_material = bpy.data.materials.get("adverb_material")
pronoun_material = bpy.data.materials.get("pronoun_material")
preposition_material = bpy.data.materials.get("preposition_material")
conjunction_material = bpy.data.materials.get("conjunction_material")


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


parent_cube.hide_render = True

tag_cleaner = PartOfSpeechTagAssigner(tags)
tags = tag_cleaner.get_words_and_tags_list()
words_and_positions_and_part_of_speech_list = packageWordsPositionAndPartOfSpeech(english_words, english_words_scaled_coordinates, tags, start_times_array)
rp, dt, tl = createTextObjects(words_and_positions_and_part_of_speech_list, parent_cube, "ARLRDBD", 1, 3, 0.015, start_times_array)

new_row_positions =  convertListOfRowPositionToList(rp)
time_at_which_to_move_all_rows_with_flags_in_case_of_doulbe_row = convertTimestampFlagListToList(dt)
start_times_with_if_new_line = convertTimestampFlagListToList(tl)
english_word_objects = getAllChildrenObjects(parent_cube)

phonetic_array_position = addOffsetToXAxisDoubleArrayCoordinates(english_words_scaled_coordinates, 0.20, english_word_objects)
createChildrenTextObject(phonetic_words, english_words_scaled_coordinates, parent_cube, "ARLRDBD", 0.68, 2, 0.02, 0, 0.7, True)
createChildrenTextObject(spanish_words, english_words_scaled_coordinates, parent_cube, "ARLRDBD", 0.68, 2, 0.02, 0.05, 1.4, False)
applyKeyFrameToWords(parent_cube)
setupHighlighterKeyFrames(highlighter_obj, english_words_scaled_coordinates, english_word_objects)

all_word_objects = getAllChildrenObjects(parent_cube)
#addingBooleanModifierToAllChildrenObjects(all_word_objects, "clip_cube_english_1", "clip_cube_english_2")
