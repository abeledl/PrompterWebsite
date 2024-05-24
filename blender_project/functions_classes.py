import numpy as np
from enum import Enum
from typing import List
import bpy


class Collection:
    def __init__(self, name: str):
        self._collection = bpy.data.collections(name)

    def get_collection(self):
        return self._collection


class StickerLettersManager:
    """
    It holds the sticker_letters_collection from blender collection "sticker_lowpoly_letters"

    Attributes:
        sticker_letters_collection
    """
    def __init__(self):
        self.sticker_letters_collection = bpy.data.collections['sticker_lowpoly_letters']


class ThreeDLettersManager:

    def __init__(self):
        self.three_d_letters_collection = bpy.data.collections['alphabet3dletters']


class PartsOfSpeechEnum(Enum):
    VERB = "verb"
    NOUN = "noun"
    ADJECTIVE = "adjective"
    ARTICLE = "article"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INFINITIVE = "infinitive"


class PartOfSpeechTagsDictionary:
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
            self.part_of_speech.CONJUNCTION: ['CC'],
            self.part_of_speech.INFINITIVE: ['IF']  # I made the IF tag up
        }


class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class TimestampNewline:
    def __init__(self, timestamp: float, is_newline: bool):
        self.timestamp = timestamp
        self.is_newline = is_newline


class WordData:
    def __init__(self, word: str, position: Position | None, part_of_speech: PartsOfSpeechEnum | None,
                 is_double_row: bool, timestamp_and_newline: TimestampNewline):
        self.word = word
        self.position = position
        self.part_of_speech = part_of_speech
        self.is_double_row = is_double_row
        self.timestamp_and_newline = timestamp_and_newline


class RowPosition:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class WordAndPartOfSpeechTag:
    def __init__(self, word: str, part_of_speech_tag: str):
        self.word = word
        self.part_of_speech_tag = part_of_speech_tag


class Materials:
    def __init__(self):
        self.verb_material = bpy.data.materials.get("verb_material")
        self.noun_material = bpy.data.materials.get("noun_material")
        self.adjective_material = bpy.data.materials.get("adjective_material")
        self.article_material = bpy.data.materials.get("article_material")
        self.adverb_material = bpy.data.materials.get("adverb_material")
        self.pronoun_material = bpy.data.materials.get("pronoun_material")
        self.preposition_material = bpy.data.materials.get("preposition_material")
        self.conjunction_material = bpy.data.materials.get("conjunction_material")


class PartOfSpeechTagIdentifier:
    def __init__(self):
        self.part_of_speech_tags = PartOfSpeechTagsDictionary()
        self.parts_of_speech = PartsOfSpeechEnum

    def get_part_of_speech(self, tag: str):
        for part_of_speech in self.parts_of_speech:
            if tag in self.part_of_speech_tags.dictionary[part_of_speech]:
                return part_of_speech


class PartOfSpeechTagAssigner:
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
        return self.parts_of_speech.VERB == self.part_of_speech_identifier.get_part_of_speech(part_of_speech_tag)

    def is_preposition(self, index: int):
        current_word = self.get_word_at(index)
        next_word_index = index + 1
        # if to is not followed by a verb, then it is a preposition
        return current_word == 'to' and not self.is_verb(next_word_index)

    def is_infinitive(self, index: int):
        current_word = self.get_word_at(index)
        next_word_index = index + 1
        # if to is followed by a verb, then it is infinitive
        return current_word == 'to' and (self.is_verb(next_word_index))

    def get_words_and_tags_list(self):
        for index in range(len(self.words_and_tags_list)):
            if self.is_infinitive(index):
                self.new_words_and_tags_list.append((self.words_and_tags_list[index][0], 'IF'))
            elif self.is_preposition(index):
                self.new_words_and_tags_list.append((self.words_and_tags_list[index][0], 'IN'))
            else:
                self.new_words_and_tags_list.append(
                    (self.words_and_tags_list[index][0], self.words_and_tags_list[index][1]))
        return self.new_words_and_tags_list


class MaterialAssigner:
    def __init__(self, materials: Materials):
        self.materials = materials
        self.parts_of_speech = PartsOfSpeechEnum
        self.part_of_speech_to_material_map = {
            self.parts_of_speech.VERB: self.materials.verb_material,
            self.parts_of_speech.NOUN: self.materials.noun_material,
            self.parts_of_speech.ADJECTIVE: self.materials.adjective_material,
            self.parts_of_speech.ARTICLE: self.materials.article_material,
            self.parts_of_speech.ADVERB: self.materials.adverb_material,
            self.parts_of_speech.PRONOUN: self.materials.pronoun_material,
            self.parts_of_speech.PREPOSITION: self.materials.preposition_material,
            self.parts_of_speech.CONJUNCTION: self.materials.conjunction_material,
            self.parts_of_speech.INFINITIVE: self.materials.verb_material
        }

    def get_material(self, word: WordData):
        if word.part_of_speech:
            return self.part_of_speech_to_material_map.get(word.part_of_speech)


class WordObject:
    SPACE_LINE_AMOUNT = 1.6

    def __init__(self, word_object, x_position: float, y_position: float, parent_obj):
        word_object.location = (x_position, y_position, 0)
        # rotate
        self.word_obj = word_object
        # self.set_material(material)
        self.set_parent_obj(parent_obj)
        # self.apply_modifier(modifier, mod_name)

    def set_material(self, material):
        self.word_obj.data.materials.append(material)

    def set_parent_obj(self, parent_obj):
        self.word_obj.parent = parent_obj

    def apply_modifier(self, modifier, mod_name):
        if self.word_obj.type == 'MESH':
            # Add a new Geometry Node modifier to the object
            new_modifier = self.word_obj.modifiers.new(name=mod_name, type='NODES')
            # Copy the node group (geometry node tree) from 'outline_geo'
            if modifier:
                new_modifier.node_group = modifier.node_group


def convert_to_mesh():
    bpy.ops.object.convert(target='MESH')


def shade_smooth_by_angle():
    bpy.ops.object.shade_smooth_by_angle()


class TextObject:
    SPACE_LINE_AMOUNT = 1.6
    EXTRUSION = 0.05
    BEVEL_DEPTH = 0.02
    BEVEL_RESOLUTION = 3
    FILL_MODE = 'BOTH'
    X_ALIGNMENT = 'CENTER'
    Y_ALIGNMENT = 'CENTER'
    RESOLUTION = 2

    def __init__(self, x_position: float, y_position: float, word: str, double_row: bool, parent_obj, font_path: str,
                 font_size: float, material, modifier, mod_name):
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
        convert_to_mesh()
        shade_smooth_by_angle()
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

    def apply_modifier(self, modifier, mod_name):
        if self.text_object.type == 'MESH':
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


def convert_to_list_of_row_positions(row_position_list):
    position_list: List[RowPosition] = []
    for position in row_position_list:
        position_list.append(RowPosition(position[0], position[1]))
    return position_list


def convert_to_timestamp_flag_list(timestamp_new_line_list):
    timestamp_list: List[TimestampNewline] = []
    for item in timestamp_new_line_list:
        timestamp_list.append(TimestampNewline(item[0], item[1]))
    return timestamp_list


def convert_timestamp_flag_list_to_list(timestamp_newline_list: List[TimestampNewline]):
    clear_list = []
    for timestamp_and_newline in timestamp_newline_list:
        clear_list.append((timestamp_and_newline.timestamp, timestamp_and_newline.is_newline))
    return clear_list


def convert_list_of_row_position_to_list(row_position_list: List[RowPosition]):
    clear_list = []
    for position in row_position_list:
        clear_list.append((position.x, position.y))
    return clear_list


def get_object_width(obj):
    bbox = obj.bound_box
    min_x, max_x = min(bbox, key=lambda p: p[0])[0], max(bbox, key=lambda p: p[0])[0]
    return max_x - min_x


def get_word_width(obj):
    width = 0
    for letter in obj.children:
        width += (get_object_width(letter) * 2)

    return {"width": width, "height": 3}


class WordAssembler:
    def __init__(self, letters_collection, words_collection_name, kind, material_assigner: MaterialAssigner):
        self.letter_collection = letters_collection
        self.empty_list = []
        self.empty = None
        self.kind = kind
        self.material_assigner = material_assigner
        # Ensure the 'words' collection exists or create it
        if words_collection_name not in bpy.data.collections:
            self.words_collection = bpy.data.collections.new(words_collection_name)
            bpy.context.scene.collection.children.link(self.words_collection)
        else:
            self.words_collection = bpy.data.collections[words_collection_name]

    # Function to create a linked duplicate
    def create_linked_duplicate(self, name):
        original = self.letter_collection.objects.get(name)
        if original is not None:
            new_obj = original.copy()
            new_obj.data = original.data
            self.words_collection.objects.link(new_obj)
            return new_obj
        else:
            print(f"Object named {name} not found.")
            return None

    # Function to create a word using linked instances
    def create_word(self, word: WordData):
        self.empty = bpy.data.objects.new(word.word + "_Empty", None)
        self.words_collection.objects.link(self.empty)
        self.empty.location = (0, 0, 0)
        self.empty_list.append(self.empty)
        total_width = 0.0
        letter_objects = []

        # First, create all letter objects and calculate the total width
        for letter in word.word:
            obj_name = letter.upper() + self.kind if letter.isupper() else letter + self.kind
            obj = self.create_linked_duplicate(obj_name)
            if obj:
                material = self.material_assigner.get_material(word)
                # create material slot
                # obj.material_slots[0].link = 'OBJECT'
                if material:
                    obj.material_slots[0].material = material
                obj_width = get_object_width(obj)
                letter_objects.append((obj, obj_width))
                total_width += obj_width

        # Calculate the starting position to center the word
        start_position = -total_width / 2

        # Position each letter object
        for obj, obj_width in letter_objects:
            obj.location.x = start_position + obj_width / 2
            start_position += obj_width
            obj.parent = self.empty

        if self.kind == "s":
            self.empty.scale = (0.5, 0.5, 0.5)

        return self.empty


def get_modifier(container_obj, mod_name):
    # Get the active object
    gn_modifier = None
    # Check if 'outline_geo' is a modifier of the active object
    if 'outline_geo' in container_obj.modifiers:
        # Get the 'outline_geo' modifier
        gn_modifier = container_obj.modifiers[mod_name]
    return gn_modifier


class TextObjectsCreator:
    text_objects_list = []

    def __init__(self, words: List[WordData], letter_manager: ThreeDLettersManager, word_assembler: WordAssembler):
        self.words = words
        self.materials = Materials()
        self.material_assigner = MaterialAssigner(self.materials)
        self.letters_manager = letter_manager
        self.word_assembler = word_assembler

    def create_text_objects(self, parent_obj):
        for data in self.words:
            word = self.word_assembler.create_word(data)
            if data.position:
                # self.text_objects_list.append(TextObject(data.position.x, data.position.y, data.word ,
                # data.is_double_row, parent_obj, font_path, font_size, material, modifier, 'outline_geo'))
                self.text_objects_list.append(WordObject(word, data.position.x, data.position.y, parent_obj))


class RowsCalculator:
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


class TimeStampCreator:
    def __init__(self, _start_times_array):
        self.timestamps: List[TimestampNewline] = []
        self.double_row_timestamps: List[TimestampNewline] = []
        self.start_times_array = _start_times_array
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

    def get_double_row_timestamps(self, word_data: List[WordData], max_number_of_rows):
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
                                self.double_row_timestamps.append(
                                    TimestampNewline(word.timestamp_and_newline.timestamp, True))
                            else:
                                self.double_row_timestamps.append(
                                    TimestampNewline(word.timestamp_and_newline.timestamp, False))
                        prev_word_position_y = word.position.y
        return self.double_row_timestamps


def create_text_objects(
        _words_and_positions_and_part_of_speech_list, parent_obj, _start_times_array,
        sticker_letters_manager, word_assembler):
    # "/Users/efaideleon/Documents/abeldl GitHub/PrompterWebsite/" + font_name + ".ttf"
    # "C:\\WINDOWS\\Fonts\\" + font_name + ".ttf"
    text_objects_creator = TextObjectsCreator(_words_and_positions_and_part_of_speech_list, sticker_letters_manager,
                                              word_assembler)
    text_objects_creator.create_text_objects(parent_obj)
    rows_position_calculator = RowsCalculator()
    rows_position = rows_position_calculator.get_rows(_words_and_positions_and_part_of_speech_list)
    timestamp_creator = TimeStampCreator(_start_times_array)
    timestamps = timestamp_creator.get_timestamps(_words_and_positions_and_part_of_speech_list)

    for timestamps_and_newline in timestamps:
        print("time: ", timestamps_and_newline.timestamp, " flag: ", timestamps_and_newline.is_newline)
    double_row_timestamps = timestamp_creator.get_double_row_timestamps(_words_and_positions_and_part_of_speech_list, 2)
    bpy.ops.object.select_all(action='SELECT')

    return rows_position, double_row_timestamps, timestamps


# ############ REFACTORING ############


def create_children_text_objects_from_collection(stringwordsarray, assembler: WordAssembler, positions, parent_obj,
                                                 vertical_offset):
    # assmble words
    for word, position in zip(stringwordsarray, positions):
        word_data = WordData(word, position, None, False, TimestampNewline(0, False))
        word_with_empty = assembler.create_word(word_data)
        # not putting the wordObjects in a container don't know if it is necessary, yet I think it is
        WordObject(word_with_empty, position[0], -1 * position[1] - vertical_offset, parent_obj)


def create_children_text_object(words, positions, parent_obj, font_name, font_size, font_resolution, bevel_depth,
                                extrution, vertical_offset, outline):
    # Create a new text object for each word
    for word, position in zip(words, positions):
        # Create a new text object-
        bpy.ops.object.text_add(enter_editmode=False, location=(position[0], (-1 * position[1]) - vertical_offset, 0))
        text_object = bpy.context.active_object
        word = word.replace("_", "  ")
        double_row = False
        if '#' in word:
            word = word.replace('#', '\n')
            double_row = True

        text_object.data.body = word
        if double_row:
            text_object.data.space_line = 2.3
        font_path = "/Users/efaideleon/Documents/abeldl Github/PrompterWebsite/" + font_name + ".ttf"
        font_data = bpy.data.fonts.load(font_path)
        text_object.data.font = font_data
        text_object.data.size = font_size
        text_object.data.align_x = 'CENTER'  # Set horizontal alignment to center
        text_object.data.align_y = 'CENTER'  # Set vertical alignment to middle
        text_object.data.extrude = extrution
        # text_object.data.bevel_depth = 0.01
        # text_object.data.bevel_resolution = 1
        # text_object.data.bevel_mode = 'ROUND'
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
            if double_row:
                text_object2.data.space_line = 2.3
            font_path2 = "/Users/efaideleon/Documents/abeldl Github/PrompterWebsite/" + font_name + ".ttf"
            font_data2 = bpy.data.fonts.load(font_path2)
            text_object2.data.font = font_data2
            text_object2.data.size = font_size
            text_object2.data.resolution_u = font_resolution
            text_object2.data.fill_mode = 'NONE'
            # text_object2.data.offset = 0.02
            text_object2.data.align_x = 'CENTER'  # Set horizontal alignment to center
            text_object2.data.align_y = 'CENTER'  # Set vertical alignment to middle
            text_object2.data.bevel_depth = bevel_depth
            text_object2.data.bevel_resolution = 0

            text_object2.data.materials.append(outline_material)
            # text_object2.active_material.use_nodes = True
            text_object2.active_material.use_screen_refraction = True
            text_object2.active_material.refraction_depth = 1.5

            bpy.ops.object.convert(target='MESH')
            text_object2.parent = parent_obj
        # bpy.ops.object.shade_smooth()

        # Set the text object as a child of the parent cube
        text_object.parent = parent_obj

    # Select all created text objects
    bpy.ops.object.select_all(action='SELECT')


def move_object(obj, direction, distance):
    # Get the object by its name
    obj_name = obj.name

    obj = bpy.context.scene.objects[obj_name]
    obj.location.x += direction[0] * distance
    obj.location.y += direction[1] * distance
    obj.location.z += direction[2] * distance


def add_key_frame(obj, frame_number, property_name):
    # Insert a keyframe
    obj.keyframe_insert(data_path=property_name, frame=frame_number)


def apply_key_frame_to_words(obj):
    fps = 60
    transition_frame_rate = 10
    direction = [0, 0, 1]
    distance = 15.5  # amount to move everything by
    # for second in end_times_array:
    for second, bool_val in time_at_which_to_move_all_rows_with_flags_in_case_of_doulbe_row:
        frame = calculate_frame(second, fps)
        add_key_frame(obj, frame, "location")

        if bool_val:
            move_object(obj, direction, distance)
        else:
            move_object(obj, direction, distance)

        transition_frames = frame + transition_frame_rate
        add_key_frame(obj, transition_frames, "location")


def calculate_frame(seconds, fps):
    frames = seconds * fps - 6
    return int(frames)


def set_obj_position(x, y, z, obj):
    obj.location.x = x
    obj.location.y = y
    obj.location.z = z


def get_width_and_height(obj):
    width = obj.dimensions.x
    height = obj.dimensions.y
    return {'width': width, 'height': height}


def get_all_children_objects(obj):
    # Get all its child objects (recursive)
    children = obj.children_recursive
    return children


def setup_highlighter_key_frames(obj, word_coordinates, word_assembler: WordAssembler):
    fps = 60
    transition_frame_rate = 10
    word_obj_idx = 0
    word_collection_object = word_assembler.empty_list
    width_height_data_first_word = get_word_width(word_collection_object[0])
    first_row_pos_y = -word_coordinates[word_obj_idx][1] - 0.5
    second_row_pos_y = -new_row_positions[0][1] - 0.3
    in_second_row = False

    # ###########GEO NODES SET UP ############################
    bpy.data.objects["highlighter_obj"].select_set(True)
    # Select the object (optional, if not already selected)
    # obj.select_set(True)
    # Make the object the active one
    bpy.context.view_layer.objects.active = obj
    # Add a Geometry Nodes modifier to the cube
    obj.modifiers.new(name="NodesModifier2", type='NODES')
    obj.modifiers[-1].name = "geo1"
    node_modifier = obj.modifiers.get("geo1")
    bpy.ops.node.new_geometry_node_group_assign()

    # obj.node.new_geometry_node_group_assign()
    # Get the node group of the Geometry Nodes modifier
    node_group = node_modifier.node_group
    node_group.name = "highlighter_geo"
    # Clear existing nodes
    for _node in node_group.nodes:
        node_group.nodes.remove(_node)

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

    # ################ Nodes Setup End####################################

    # add bevel modifier
    bpy.ops.object.modifier_add(type='BEVEL')
    highlighter_obj.modifiers["Bevel"].width = 0.34
    highlighter_obj.modifiers["Bevel"].segments = 7
    highlighter_obj.modifiers["Bevel"].affect = 'VERTICES'
    # add solidify modifier
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    highlighter_obj.modifiers["Solidify"].thickness = 0.04
    highlighter_obj.modifiers["Solidify"].offset = 0

    # for second in end_times_words_array:
    for second, isNewLine in start_times_with_if_new_line:
        frame_t = calculate_frame(second, fps)
        add_key_frame(obj, frame_t, "location")
        # addKeyFrame(obj, frame, "scale")
        # Add a keyframe for the scale at frame 10
        transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=frame_t)

        width_height_data = get_word_width(word_collection_object[word_obj_idx])
        new_width = width_height_data["width"] + 0.7
        if width_height_data["height"] > 4:
            new_height = width_height_data["height"] + 1.27
        else:
            new_height = width_height_data_first_word["height"] + 3
        # Set the scale on the X-axis of the Transform node to 4
        transform_node.inputs['Scale'].default_value[0] = new_width / 2
        transform_node.inputs['Scale'].default_value[1] = new_height / 2
        # transform_node.inputs['Scale'].default_value[1] = 1.04/2
        # transform_node.inputs['Scale'].default_value[2] = new_height/2
        # changeWidthAndHeight(obj, new_width, new_height, 1.04)

        coordinate = word_coordinates[word_obj_idx]

        new_pos_x = coordinate[0]

        if isNewLine:
            in_second_row = not in_second_row  # toggle
        if in_second_row:
            new_pos_y = second_row_pos_y
        else:
            new_pos_y = first_row_pos_y
        set_obj_position(new_pos_x * 2, 2.5288, (new_pos_y * 2) + 2.12562, obj)
        transition_frames = frame_t + transition_frame_rate
        add_key_frame(obj, transition_frames, "location")
        transform_node.inputs['Scale'].keyframe_insert(data_path='default_value', frame=transition_frames)
        # addKeyFrame(obj, transition_frames, "scale")
        word_obj_idx += 1
    # add bevel modifier
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].width = 0.2
    bpy.context.object.modifiers["Bevel"].segments = 4
    # shade flat
    bpy.ops.object.shade_flat()
    bpy.data.objects["highlighter_obj"].select_set(False)


def add_offset_to_x_axis_double_array_coordinates(arr, offset_x_percentage, words):
    new_pair_list = []
    new_list = []
    word_obj_idx = 0
    height_offset = 0.4
    for x, y in arr:
        width_heigh_data = get_width_and_height(words[word_obj_idx])
        new_pair_list.append(x + width_heigh_data["width"] * offset_x_percentage)
        new_pair_list.append(y + height_offset)
        new_list.append(new_pair_list)
        new_pair_list = []
        word_obj_idx += 1

    return new_list


def package_words_position_and_part_of_speech(words, position, words_and_part_of_speech_tags, _start_times_array):
    word_data_list = []
    part_of_speech_identifier = PartOfSpeechTagIdentifier()
    for word, position, word_and_part_of_speech_tag, start_time in zip(words, position, words_and_part_of_speech_tags,
                                                                       _start_times_array):
        x_pos = position[0]
        y_pos = -1 * position[1] - 0.25
        word = word.replace("_", " ")
        is_double_row = False
        if '#' in word:
            word = word.replace('#', '\n')
            is_double_row = True

        word_data_list.append(WordData(word, Position(x_pos, y_pos),
                                       part_of_speech_identifier.get_part_of_speech(word_and_part_of_speech_tag[1]),
                                       is_double_row, TimestampNewline(start_time, False)))
    return word_data_list
