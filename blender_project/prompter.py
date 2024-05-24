import bpy
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import nltk
import math
import mathutils

nltk.download('punkt')


# Abstract classes
class Collection(ABC):
    @abstractmethod
    def create_collection(self, name: str):
        pass

    @abstractmethod
    def get_collection(self):
        pass

    @abstractmethod
    def get_object(self, name):
        pass


class Assembler(ABC):
    @abstractmethod
    def assemble(self, obj):
        pass


class MaterialIdentifier(ABC):
    @abstractmethod
    def get_material_for(self, name):
        pass


class ObjectAligner(ABC):
    def align(self, obj):
        pass


class ObjectBuilder(ABC):
    def build(self):
        pass


class POSTaggingStrategy(ABC):
    @abstractmethod
    def assign_tag(self, word: str, tag: str, index: int, words_and_tag_list: List[Tuple[str, str]]):
        pass


class ObjectFactory(ABC):
    @abstractmethod
    def create_object(self, name: str):
        pass

    @abstractmethod
    def clone_obj(self, obj):
        pass


# Data Classes
@dataclass
class Position:
    x: float
    y: float


@dataclass
class TimestampNewline:
    timestamp: float
    is_newline: bool


@dataclass
class WordData:
    """
    Attributes:
        text: (str)
        position: (Position)
        part_of_speech: (str)
        is_double_row: (bool)
        timestamp_and_newline: (TimeStampNewLine)
    """
    text: str
    position: Position
    part_of_speech: str
    is_double_row: bool
    timestamp_and_newline: TimestampNewline


# Collections
class BaseCollection(Collection):
    """
    Manages a blender collection
    """

    def __init__(self, collection):
        self.collection = collection

    def create_collection(self, name: str):
        """
        Create a blender collection with a given name

        Args:
            name: The name for the collection
        """
        if name not in bpy.data.collections:
            self.collection = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(self.collection)
        else:
            self.collection = bpy.data.collections(name)

    def get_collection(self):
        """
        Accesses the blender collection

        Returns:
             A blender collection
        """
        return self.collection

    def get_object(self, name):
        """
        Searches for an object in a blender collection with a given name

        Args:
            name: The name of the object to get from the collection

        Returns:
            A blender object
        """
        return self.collection.objects.get(name)


class Alphabet3DCollection(BaseCollection):
    """
    Holds a collection for 3D alphabet letter objects
    """

    def __init__(self, letters_collection):
        super().__init__(letters_collection)

    def get_object(self, name: str):
        """
        Returns an object in the collection given its name

        Args:
            name: the name of the object in the collection

        Returns: an object in the collection
        """
        obj_name = name.upper() + '_3d' if name.isupper() else name + '_3d'
        return self.collection.objects.get(obj_name)


class StickerLetterCollection(BaseCollection):
    def __init__(self, letters_collection):
        super().__init__(letters_collection)

    def get_object(self, name):
        obj_name = name.upper() + 's' if name.isupper() else name + 's'
        return self.collection.objects.get(obj_name)


class WordsCollection(BaseCollection):
    """
    containers a collection to store empty word objects
    """

    def __init__(self):
        super().__init__(None)


# Blender Code Proxies
class BlenderObjectFactory(ObjectFactory):
    def create_object(self, name: str):
        return bpy.data.objects.new(name + "_Empty", None)

    def clone_obj(self, obj):
        if obj is not None:
            new_obj_copy = obj.copy()
            new_obj_copy.data = obj.data
            return new_obj_copy
        else:
            print(f"Object was not found.")
            return None


# Generating Text Object
class Font3DTextGenerator:
    def __init__(self, font_path: str, extrusion: float = 0.05, resolution: int = 3, bevel_depth: float = 0.03):
        """
        Initializes the Font3DTextGenerator with the given parameters.

        Args:
            font_path: Path to the font file.
            extrusion: The extrusion depth for each text object.
            resolution: The resolution of each text object.
            bevel_depth: The bevel depth for each text object.
        """
        self.font = self.load_font(font_path)
        if self.font is None:
            raise ValueError(f"Font file not found at path: {font_path}")

        self.extrusion = extrusion
        self.resolution = resolution
        self.bevel_depth = bevel_depth

    @staticmethod
    def load_font(font_path: str):
        """
        Loads a font from the given path.

        Args:
            font_path: Path to the font file.

        Returns:
            The loaded font object or None if loading failed.
        """
        try:
            return bpy.data.fonts.load(font_path)
        except RuntimeError:
            print(f"Error: Font file not found: {font_path}")
            return None

    @staticmethod
    def link_object_to_collection(collection, obj):
        """
        Links an object to a collection, ensuring it is not in the scene's root collection.

        Args:
            collection: The collection to link the object to.
            obj: The object to link.
        """

        if obj.name not in collection.objects:
            collection.objects.link(obj)
            bpy.context.scene.collection.objects.unlink(obj)

    def create_text_object(self, character: str):
        """
        Creates a 3D text object with the given parameters.

        Args:
            character: The character to create.

        Returns:
            The created text object.
        """

        bpy.ops.object.text_add(enter_editmode=False, location=(0, 0, 0))
        text_object = bpy.context.active_object
        text_object.data.body = character
        text_object.data.font = self.font
        text_object.data.size = 1
        text_object.data.extrude = self.extrusion
        text_object.data.resolution_u = self.resolution
        text_object.data.bevel_depth = self.bevel_depth
        text_object.data.align_x = 'CENTER'

        text_object.name = f"{character}_3d"

        bpy.ops.object.convert(target="MESH")
        return text_object

    def create_alphabet_3d_collection(self,
                                      characters: str = "'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.?",
                                      collection_name: str = 'alphabet3dletters'):
        """
        Creates a collection of 3D text objects for each character in the provided string.

        Args:
            characters: A string of characters to create 3D objects for.
            collection_name: The name of the new collection

        Returns:
            The collection containing all the 3D text objects.
        """

        alphabet_collection = bpy.data.collections.new(collection_name)
        scene_collection = bpy.context.scene.collection
        scene_collection.children.link(alphabet_collection)

        for char in characters:
            text_object = self.create_text_object(char)
            bpy.ops.object.material_slot_add()
            bpy.ops.object.material_slot_assign()
            self.link_object_to_collection(alphabet_collection, text_object)

        return alphabet_collection


# Materials
class PartOfSpeechMaterialIdentifier(MaterialIdentifier):
    def __init__(self):
        self.part_of_speech_to_material_map = {
            "verb": bpy.data.materials.get("verb_material"),
            "noun": bpy.data.materials.get("noun_material"),
            "adjective": bpy.data.materials.get("adjective_material"),
            "article": bpy.data.materials.get("article_material"),
            "adverb": bpy.data.materials.get("adverb_material"),
            "pronoun": bpy.data.materials.get("pronoun_material"),
            "preposition": bpy.data.materials.get("preposition_material"),
            "conjunction": bpy.data.materials.get("conjunction_material"),
            "infinitive": bpy.data.materials.get("verb_material")
        }

    def get_material_for(self, name):
        return self.part_of_speech_to_material_map[name]


# Assembling Words
class HorizontalAligner(ObjectAligner):
    """
    Aligns objects horizontally based on their bounding boxes.
    """

    @staticmethod
    def _get_object_width(obj):
        """
        Calculate blender object width

        Args:
            obj: A blender object

        Returns:
            width of a blender object
        """
        bbox = obj.bound_box
        min_x, max_x = min(bbox, key=lambda p: p[0])[0], max(bbox, key=lambda p: p[0])[0]
        return max_x - min_x

    def align(self, obj):
        children_obj_width_sum = 0.0
        children_objects_and_width = []

        for child_obj in obj:
            child_obj_width = self._get_object_width(child_obj)
            children_objects_and_width.append((child_obj, child_obj_width))
            children_obj_width_sum += child_obj_width

        start_position = -children_obj_width_sum / 2

        for child_obj, child_width in children_objects_and_width:
            child_obj.location.x = start_position + child_width / 2
            start_position += child_width


class WordAssembler(Assembler):
    """
    Uses a collection of objects and puts the objects together in the form of a word

    Attributes:
        letter_pool: A collection of letter object
    """

    def __init__(self, letters_collection: Collection, object_factory: ObjectFactory):
        self.letter_pool = letters_collection
        self.blender_object_factory = object_factory

    def assemble(self, word: str):
        """
        Given a word it puts together the corresponding letter objects to make up the word

        Args:
            word: The word to create from the letters

        Returns:
            A list of the letter objects that make up the word
        """
        return [self.blender_object_factory.clone_obj(self.letter_pool.get_object(letter)) for letter in word]


class WordObjectBuilder:
    def __init__(self, word_assembler: Assembler, material_identifier: MaterialIdentifier,
                 object_aligner: ObjectAligner, object_factory: ObjectFactory):

        self.word_assembler = word_assembler
        self.material_identifier = material_identifier
        self.object_aligner = object_aligner
        self.blender_object_factory = object_factory
        self._letter_object_list = []
        self.empty_word_object = None

    # Public
    def create_object(self, text: str) -> "WordObjectBuilder":
        self._assemble_text(text)
        self._create_empty_object(text)
        self._align_letter_objects()
        self._attach_letter_objects_to_word_object()
        return self

    def apply_material(self, part_of_speech: str) -> "WordObjectBuilder":
        material = self.material_identifier.get_material_for(part_of_speech)
        self._apply_material_to_letter_objects(material)
        return self

    def link_to_collection(self, collection: Collection) -> "WordObjectBuilder":
        self._link_objects_to_collection(collection)
        return self

    def set_position(self, x, y) -> "WordObjectBuilder":
        self.empty_word_object.location = (x, y, 0)
        return self

    def add_key_frame(self, property_name: str, frame_number: int):
        self.empty_word_object.keyframe_insert(data_path=property_name, frame=frame_number)

    def get_word_object(self):
        return self.empty_word_object

    # Private
    def _assemble_text(self, text: str) -> None:
        self._letter_object_list = self.word_assembler.assemble(text)

    def _create_empty_object(self, text: str) -> None:
        self.empty_word_object = self.blender_object_factory.create_object(text)

    def _align_letter_objects(self) -> None:
        self.object_aligner.align(self._letter_object_list)

    def _attach_letter_objects_to_word_object(self) -> None:
        for letter_object in self._letter_object_list:
            letter_object.parent = self.empty_word_object

    def _link_objects_to_collection(self, collection: Collection) -> None:
        collection.get_collection().objects.link(self.empty_word_object)
        for letter_object in self._letter_object_list:
            collection.get_collection().objects.link(letter_object)

    def _apply_material_to_letter_objects(self, material):
        if material:
            for letter_obj in self._letter_object_list:
                letter_obj.material_slots[0].material = material


class WordsAssemblerManager:
    def __init__(self, word_assembler: Assembler, material_identifier: MaterialIdentifier,
                 blender_object_factory: ObjectFactory, words_collection: Collection, word_data_list: List[WordData]):
        self.word_assembler = word_assembler
        self.material_identifier = material_identifier
        self.blender_object_factory = blender_object_factory
        self.words_collection = words_collection
        self.word_data_list = word_data_list
        self.object_aligner = HorizontalAligner()
        self.words_object_list = []

    def get_words_object_list(self):
        return self.words_object_list

    def assemble_word(self, word_data: WordData):
        builder = (WordObjectBuilder(self.word_assembler, self.material_identifier, self.object_aligner,
                                     self.blender_object_factory)
                   .create_object(word_data.text)
                   .link_to_collection(self.words_collection)
                   .set_position(word_data.position.x, word_data.position.y)
                   .apply_material(word_data.part_of_speech))
        self.words_object_list.append(builder.get_word_object())

    def assemble_words(self):
        """
        Assembles empty word objects form the words list linking them to a words_collection
        """
        for word in self.word_data_list:
            self.assemble_word(word)


# Tags and Part of Speech
class TagToPartOfSpeech:
    def __init__(self):
        self.part_of_speech_tags_dictionary = {
            "verb": ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
            "noun": ['NN', 'NNS', 'NNP', 'NNPS'],
            "adjective": ['JJ', 'JJR', 'JJS'],
            "article": ['DT', 'PDT', 'WDT'],
            "adverb": ['RB', 'RBR', 'RBS', 'WRB'],
            "pronoun": ['PRP', 'PRP$', 'WP', 'WP$'],
            "preposition": ['IN'],
            "conjunction": ['CC'],
            "infinitive": ['IF']  # I made the IF tag up
        }

    def get_part_of_speech(self, tag: str):
        for part_of_speech, tags in self.part_of_speech_tags_dictionary.items():
            if tag in tags:
                return part_of_speech


class InfinitiveStrategy(POSTaggingStrategy):
    def assign_tag(self, word: str, tag: str, index: int, words_and_tag_list: List[Tuple[str, str]]):
        if index < len(words_and_tag_list) - 1:
            next_word_tag = words_and_tag_list[index + 1][1]
            # if to is followed by a verb, then it is infinitive
            if word == 'to' and TagToPartOfSpeech().get_part_of_speech(next_word_tag):
                return 'IF'
        return tag


class PrepositionStrategy(POSTaggingStrategy):
    def assign_tag(self, word: str, tag: str, index: int, words_and_tag_list: List[Tuple[str, str]]):
        if index < len(words_and_tag_list) - 1:
            next_word_tag = words_and_tag_list[index + 1][1]
            # if to is not followed by a verb, then it is a preposition
            if word == 'to' and TagToPartOfSpeech().get_part_of_speech(next_word_tag) != 'verb':
                return 'IN'
        return tag


class PartOfSpeechTagAssigner:
    def __init__(self, words_and_tags_list: List[Tuple[str, str]]):
        self.words_and_tags_list = words_and_tags_list
        self.tagging_strategies = [InfinitiveStrategy(), PrepositionStrategy()]

    def assign_tags(self):
        tagged_words = []
        for index, (word, tag) in enumerate(self.words_and_tags_list):
            for strategy in self.tagging_strategies:
                tag = strategy.assign_tag(word, tag, index, self.words_and_tags_list)
            tagged_words.append((word, tag))
        return tagged_words


# WordData List Packaging
class WordDataListCreator:
    def __init__(self, tag_to_part_of_speech: TagToPartOfSpeech, words: List[str], positions: List[Tuple[float, float]],
                 parts_of_speech_tags: List[str], start_times_array: List[float]):
        self.tag_to_part_of_speech = tag_to_part_of_speech
        self.words = words
        self.positions = positions
        self.part_of_speech_tags = parts_of_speech_tags
        self.start_times_array = start_times_array
        self.word_data_list = []

    def build(self):
        return [
            WordData(
                text=word.replace("_", " ").replace("#", "\n"),
                position=Position(x=position[0], y=-1 * position[1] - 0.25),
                part_of_speech=self.tag_to_part_of_speech.get_part_of_speech(part_of_speech_tag),
                is_double_row='#' in word,
                timestamp_and_newline=TimestampNewline(timestamp=start_time, is_newline=False)
            )
            for word, position, part_of_speech_tag, start_time in zip(
                self.words, self.positions, self.part_of_speech_tags, self.start_times_array
            )
        ]


# Rows and TimeStampNewline
class RowsCalculator:
    def __init__(self):
        self.rows_positions: List[Position] = []

    def get_rows(self, word_data: List[WordData]):
        first_row_position = word_data[0].position

        if first_row_position:
            prev_word_position_y = first_row_position.y
            for word in word_data:
                if word.position:
                    current_row_position_y = word.position.y
                    if current_row_position_y < prev_word_position_y:
                        self.rows_positions.append(Position(word.position.x, -word.position.y))
                        prev_word_position_y = current_row_position_y
        return self.rows_positions


class TimeStampCreator:
    def __init__(self):
        self.timestamps: List[TimestampNewline] = []
        self.double_row_timestamps: List[TimestampNewline] = []
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


# Highlighter
class GeometryModifier:
    def __init__(self, node_modifier):
        self.node_modifier = node_modifier
        self.transform_node = None
        self._create_geometry_node_group()

    # Public
    @property
    def geometry_transform_node(self):
        return self.transform_node

    # Private
    def _create_geometry_node_group(self):
        bpy.ops.node.new_geometry_node_group_assign()

        # Get the node group of the Geometry Nodes modifier
        node_group = self.node_modifier.node_group
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
        self.transform_node = node_group.nodes.new('GeometryNodeTransform')
        self.transform_node.location = (0, 0)

        # Link the Geometry Transform node to the Group Input and Group Output
        node_group.links.new(group_input.outputs[0], self.transform_node.inputs[0])
        node_group.links.new(self.transform_node.outputs[0], group_output.inputs[0])


class Highlighter:
    def __init__(self):
        self._highlighter_obj = None
        self._geometry_modifier = None

    # Public
    @property
    def obj(self):
        if self._highlighter_obj is None:
            raise RuntimeError("highlighter_obj not created yet")
        return self._highlighter_obj

    @property
    def geometry_modifier(self) -> GeometryModifier:
        if self._geometry_modifier is not None:
            return self._geometry_modifier
        raise RuntimeError("Geometry Modifier not set")

    def create(self, name: str):
        bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8),
                                         scale=(1, 1, 1))
        self._highlighter_obj = bpy.context.active_object
        self._highlighter_obj.name = name
        self._add_geometry_modifier()
        self._add_bevel_modifier_before_solidify()
        self._add_solidify_modifier()
        self._add_bevel_modifier_after_solidify()
        self._shade_flat()

    def rotate_on_x_axis(self, degrees: float):
        self._highlighter_obj.rotation_euler[0] = math.radians(degrees)

    def add_material(self, material_name: str):
        material = bpy.data.materials.get(material_name)
        self._highlighter_obj.data.materials.append(material)

    def add_key_frame(self, property_name, frame_number):
        self._highlighter_obj.keyframe_insert(data_path=property_name, frame=frame_number)
        self.geometry_modifier.transform_node.inputs['Scale'].keyframe_insert(data_path='default_value',
                                                                              frame=frame_number)

    def set_position(self, x_pos, y_pos):
        self._set_obj_position(x_pos * 2, 2.5288, (y_pos * 2) + 2.12562, self._highlighter_obj)

    # Private
    def _add_geometry_modifier(self):
        self._highlighter_obj.modifiers.new(name="NodesModifier2", type='NODES')
        self._highlighter_obj.modifiers[-1].name = "geo1"
        node_modifier = self._highlighter_obj.modifiers.get("geo1")
        self._geometry_modifier = GeometryModifier(node_modifier)

    def _add_bevel_modifier_before_solidify(self):
        self._highlighter_obj.modifiers.new(name="Bevel", type='BEVEL')
        self._highlighter_obj.modifiers["Bevel"].width = 0.34
        self._highlighter_obj.modifiers["Bevel"].segments = 7
        self._highlighter_obj.modifiers["Bevel"].affect = 'VERTICES'

    def _add_solidify_modifier(self):
        self._highlighter_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        self._highlighter_obj.modifiers["Solidify"].thickness = 0.04
        self._highlighter_obj.modifiers["Solidify"].offset = 0

    def _add_bevel_modifier_after_solidify(self):
        self._highlighter_obj.modifiers.new(name="Bevel", type='BEVEL')
        self._highlighter_obj.modifiers["Bevel"].width = 0.2
        self._highlighter_obj.modifiers["Bevel"].segments = 4

    def _shade_flat(self):
        mesh = self._highlighter_obj.data
        mesh.polygons.foreach_set("use_smooth", [False] * len(mesh.polygons))
        mesh.update()

    @staticmethod
    def _set_obj_position(x, y, z, obj):
        obj.location.x = x
        obj.location.y = y
        obj.location.z = z


# Highlighter Animator
class HighlighterAnimator:
    """
    The purpose of this class is to create a highlighter object from a plane, giving it right properties.
    And Giving the behaviour to follow the words by moving to their position while adjusting its size
    """
    HIGHLIGHTER_ROW1_OFFSET = 0.5  # Units: Blender Units
    HIGHLIGHTER_ROW2_OFFSET = 0.3  # Units: Blender Units
    TARGET_HEIGHT = 4  # Units: Blender Units

    def __init__(
            self,
            highlighter: Highlighter,
            target_coordinates: List[Tuple[float, float]],
            row_positions: List[Position],
            timestamps_and_newline_flag: List[TimestampNewline],
            target_list: List[bpy.types.Object]
    ):
        self._highlighter = highlighter

        self._validate_non_empty_list(target_coordinates, "target_coordinates")
        self._target_coordinates = target_coordinates

        self._validate_non_empty_list(row_positions, "row_position")
        self._row_positions = row_positions

        self._validate_non_empty_list(timestamps_and_newline_flag, "timestamps_and_newline_flag")
        self._timestamps_and_newline_flag = timestamps_and_newline_flag

        self._validate_non_empty_list(target_list, "target_list")
        self._target_list = target_list

        self._target_widths_and_heights = self._generate_target_widths_and_heights()
        self._in_second_row = False

    # Public
    def setup_highlighter_animation(self, fps: int, animation_duration: int) -> None:
        """
        Animates the highlighter to each target object in the list.

        Args:
            fps: Animations frames per second.
            animation_duration: How long the animation takes in frames.
        """

        for index, timestamp_newline in enumerate(self._timestamps_and_newline_flag):
            self._animate_highlighter_to_target(
                index,
                timestamp_newline.timestamp,
                timestamp_newline.is_newline,
                fps,
                animation_duration
            )

    # Private
    def _animate_highlighter_to_target(self, target_index: int, current_timestamp: float, is_new_line: bool, fps: int,
                                       animation_duration: int) -> None:
        """
        Animates the highlighter to move to the right target while adapting its dimensions to fit around it
        Args:
            target_index (int): Index of the current target in the target_list
            current_timestamp (float): The current timestamp to start the animation at
            is_new_line (bool): A flag to know if the current obj is the last in the line
            fps (int): The number of frames the animation should take every second
            animation_duration (int): How long in seconds the animation should be
        """

        target_width_and_height: Dict[str, float] = self._target_widths_and_heights[target_index]
        coordinate: Tuple[float, float] = self._target_coordinates[target_index]

        start_frame: int = self._calculate_frame(current_timestamp, fps)
        end_frame: int = start_frame + animation_duration

        self._highlighter.add_key_frame("location", start_frame)

        self._update_highlighter_dimensions(target_width_and_height)
        if is_new_line:
            self._toggle_in_second_row()
        self._update_highlighter_position(coordinate)

        self._highlighter.add_key_frame("location", end_frame)

    def _toggle_in_second_row(self) -> None:
        """
        Toggles if the highlighter is in the second row
        """
        self._in_second_row = not self._in_second_row  # toggle

    def _update_highlighter_position(self, coordinate: Tuple[float, float]) -> None:
        """
        Moves the highlighter objects to the indicated coordinate

        Args:
            coordinate (List[float, float)): The location to move the highlighter to
        """

        if not coordinate:
            raise ValueError("coordinate is empty")

        first_row_pos_y: float = -self._target_coordinates[0][1] - self.HIGHLIGHTER_ROW1_OFFSET
        second_row_pos_y: float = -self._row_positions[0].y - self.HIGHLIGHTER_ROW2_OFFSET
        new_pos_x = coordinate[0]

        if self._in_second_row:
            new_pos_y: float = second_row_pos_y
        else:
            new_pos_y: float = first_row_pos_y
        self._highlighter.set_position(new_pos_x, new_pos_y)

    def _update_highlighter_dimensions(self, target_width_height: Dict[str, float]) -> None:
        """
        Adapts the highlighter size to fit around the target object

        Args:
            target_width_height (dict[str, float]): Dimensions of the target object to fit the highlighter around
        """

        if not all(key in target_width_height for key in ("width", "height")):
            raise TypeError("target_width_and_height must contain 'width' and 'height' keys")

        width = target_width_height["width"]
        height = target_width_height["height"]
        # Set the scale on the X-axis of the Transform node to 4
        self._highlighter.geometry_modifier.transform_node.inputs['Scale'].default_value[0] = width / 2
        self._highlighter.geometry_modifier.transform_node.inputs['Scale'].default_value[1] = height / 2

    @staticmethod
    def _calculate_frame(seconds: float, fps: int) -> int:
        """
        Calculates the frame number at a given time in seconds

        Args:
            seconds (float): Time of the frame
            fps (int): Frame rate of the animation

        Returns:
            int: A frame number
        """

        frames: float = seconds * fps - 6
        return int(frames)

    @staticmethod
    def _get_object_width(obj: bpy.types.Object) -> float:
        """
        Calculates the width of an object using the bounding box corners

        Args:
            obj (bpy.types.Object): The object whose width is going to be calculated

        Returns:
            float: The width of an object
        """
        # Ensure the object has a bounding box
        if not obj or not hasattr(obj, 'bound_box'):
            raise ValueError("Object does not have a valid bounding box.")

        bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        x_coordinates = [corner.x for corner in bbox_corners]
        _min_x = min(x_coordinates)
        _max_x = max(x_coordinates)
        width = _max_x - _min_x
        return width

    def _calculate_children_obj_total_width(self, obj: bpy.types.Object) -> float:
        """
        Calculates the width of objects using its bounding box corners
        Args:
            obj (bpy.types.Object): The blender object whose children widths needs to be calculated

        Returns:
            float: The total width of all the children objects
        """
        total_width: float = 0
        for child_obj in obj.children:
            total_width += (self._get_object_width(child_obj) * 2)
        return total_width

    def _generate_target_width_and_height(self, target_obj: bpy.types.Object) -> Dict[str, float]:
        """
        Creates a dictionary object that store the target obj width and height.
        The keys are "width" and "height"
        Args:
            target_obj (bpy.types.Object): Object that needs width and height to be calculated

        Returns:
            Dict[str, float]: The dictionary that contains the objects with and height
        """
        return {"width": self._calculate_children_obj_total_width(target_obj), "height": self.TARGET_HEIGHT}

    def _generate_target_widths_and_heights(self) -> List[Dict[str, float]]:
        """
        Calculates and packagers the with and height of each target object in to a dictionary

        Returns:
            List[dict[str, float]]: A list of dictionaries, where each dictionary represents a target object
            and contains its calculated width and height. The dictionary keys are "width" and "height"
        """
        return [self._generate_target_width_and_height(target_obj) for target_obj in self._target_list]

    @staticmethod
    def _validate_non_empty_list(value: List, name: str) -> None:
        if not value:
            raise ValueError(f"{name} cannot be empty")


# Parent Cube Animator
class ParentCubeAnimator:
    def __init__(self, parent_cub: bpy.types.Object, double_row_timestamps: List[TimestampNewline]):
        self._parent_cube = parent_cub
        self._double_row_timestamps = double_row_timestamps

    # Public
    def animate_parent_cube(
            self,
            fps: int,
            animation_duration: int,
            direction: List[int],
            distance: float
    ) -> None:
        # for second in end_times_array:
        for timestamp_flag in self._double_row_timestamps:
            second = timestamp_flag.timestamp
            bool_val = timestamp_flag.is_newline

            frame = self._calculate_frame(second, fps)
            self._add_key_frame(frame, "location")

            if bool_val:
                self._move_parent_cube(direction, distance)
            else:
                self._move_parent_cube(direction, distance)

            transition_frames = frame + animation_duration
            self._add_key_frame(transition_frames, "location")

    # Private
    @staticmethod
    def _calculate_frame(seconds: float, fps: int) -> int:
        frames = seconds * fps - 6
        return int(frames)

    def _move_parent_cube(self, direction: List[int], distance: float) -> None:
        self._parent_cube.location.x += direction[0] * distance
        self._parent_cube.location.y += direction[1] * distance
        self._parent_cube.location.z += direction[2] * distance

    def _add_key_frame(self, frame_number: int, property_name: str) -> None:
        # Insert a keyframe
        self._parent_cube.keyframe_insert(data_path=property_name, frame=frame_number)


# Children Text Object Creation
class TextObjectBuilder:
    def __init__(self):
        self._text_obj = None

    @property
    def text_obj(self):
        if not self._text_obj:
            raise ValueError("text_obj not set")
        return self._text_obj

    def create(self, location: Tuple[float, float, float]):
        bpy.ops.object.text_add(enter_editmode=False, location=location)
        self._text_obj = bpy.context.active_object
        return self

    def set_name(self, name: str):
        self._text_obj.name = name
        return self

    def set_font(self, font_path: str):
        font_path = font_path
        font_data = bpy.data.fonts.load(font_path)
        self.text_obj.data.font = font_data
        return self

    def set_size(self, size):
        self.text_obj.data.size = size
        return self

    def set_text(self, text: str):
        self.text_obj.data.body = text
        return self

    def set_space_line(self, amount: float):
        self.text_obj.data.space_line = amount
        return self

    def set_x_alignment(self, alignment: str):
        self.text_obj.data.align_x = alignment
        return self

    def set_y_alignment(self, alignment: str):
        self.text_obj.data.align_y = alignment
        return self

    def set_extrude(self, extrusion):
        self.text_obj.data.extrude = extrusion
        return self

    def add_material(self, material):
        self.text_obj.data.materials.append(material)
        return self

    def set_resolution(self, resolution):
        self.text_obj.data.resolution_u = resolution
        return self

    def set_refraction(self, flag, depth):
        self.text_obj.active_material.use_screen_refraction = flag
        if flag:
            self.text_obj.active_material.refraction_depth = depth
        return self

    def set_fill_mode(self, mode: str):
        self.text_obj.data.fill_mode = mode
        return self

    def set_parent(self, parent_obj):
        self.text_obj.parent = parent_obj
        return self

    def set_bevel_depth(self, bevel_depth, resolution):
        self.text_obj.data.bevel_depth = bevel_depth
        self.text_obj.data.bevel_resolution = resolution
        return self

    def convert_to_mesh(self):
        bpy.ops.object.convert(target='MESH')
        return self


class TextObjectFactory:
    def create_text_objects(
            self,
            word_data_list: List[WordData],
            y_offset: float,
            font_size: float,
            font_path: str,
            materials,
            extrusion,
            resolution,
            space_line,
            parent_obj
    ):
        for word_data in word_data_list:
            builder = (TextObjectBuilder()
                       .create(self.get_adjusted_position(word_data.position.x, word_data.position.y, y_offset))
                       .set_text(word_data.text)
                       .set_resolution(resolution)
                       .set_font(font_path)
                       .set_size(font_size)
                       .set_x_alignment('CENTER')
                       .set_y_alignment('CENTER')
                       .set_extrude(extrusion)
                       .add_material(materials["text_material"])
                       .add_material(materials["yellow_material"])
                       .add_material(materials["green_material"])
                       .add_material(materials["blue_material"])
                       .set_resolution(resolution)
                       )

            if word_data.is_double_row:
                builder.set_space_line(space_line)

            builder.convert_to_mesh()
            builder.set_parent(parent_obj)

    def create_outline_text_objects(
            self,
            word_data_list: List[WordData],
            y_offset: float,
            font_size: float,
            font_path: str,
            material,
            resolution,
            space_line,
            bevel_depth,
            parent_obj
    ):
        for word_data in word_data_list:
            builder = (TextObjectBuilder()
                       .create(self.get_adjusted_position(word_data.position.x, word_data.position.y, y_offset))
                       .set_name("zoutline")
                       .set_text(word_data.text)
                       .set_font(font_path)
                       .set_size(font_size)
                       .set_resolution(resolution)
                       .set_fill_mode('NONE')
                       .set_x_alignment('CENTER')
                       .set_y_alignment('CENTER')
                       .set_bevel_depth(bevel_depth, 0)
                       .add_material(material)
                       .set_refraction(True, 1.5)
                       )

            if word_data.is_double_row:
                builder.set_space_line(space_line)

            builder.convert_to_mesh()
            builder.set_parent(parent_obj)

    @staticmethod
    def get_adjusted_position(x_pos: float, y_pos: float, y_offset: float) -> Tuple[float, float, float]:
        return x_pos, (y_pos - y_offset), 0


class MainProgram:
    def __init__(self):
        self.efai_font_path = "/Users/efaideleon/Documents/abeldl GitHub/PrompterWebsite/ARLRDBD.ttf"

    def run(self):
        # Create TextObjects
        font_3d_text_generator = Font3DTextGenerator(self.efai_font_path)
        alphabet_letters_collection = Alphabet3DCollection(font_3d_text_generator.create_alphabet_3d_collection())

        # Create Parent Cube
        parent_cube = bpy.context.active_object
        parent_cube.name = "parent_cube"
        parent_cube.scale = (2, 2, 2)
        parent_cube.location = (0, 2.25562, 2.41886)
        rotation_x_parent_cube = math.radians(90)
        parent_cube.rotation_euler[0] = rotation_x_parent_cube

        # Materials
        # outline material
        outline_material = bpy.data.materials.new(name="OutlineMaterial")
        outline_material.use_nodes = True
        outline_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = 0.298182  # roughness
        # outline_material.node_tree.nodes["Principled BSDF"].inputs[17].default_value = 1 #transmission
        # color
        outline_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
            0.001617, 0.0041617, 0.0041617, 1)
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

        # ############cliping material english #########
        clip_material_english = bpy.data.materials.new(name="clipMaterialEnglishWhite")
        clip_material_english.use_nodes = True
        nodes_english_white = clip_material_english.node_tree.nodes
        clip_material_english.blend_method = 'CLIP'

        # Clear default nodes
        for node in nodes_english_white:
            nodes_english_white.remove(node)

        # Create necessary nodes
        output_node = nodes_english_white.new(type='ShaderNodeOutputMaterial')
        principal_node = nodes_english_white.new(type='ShaderNodeBsdfPrincipled')
        principal_node2 = nodes_english_white.new(type='ShaderNodeBsdfPrincipled')
        mapping_node = nodes_english_white.new(type='ShaderNodeMapping')
        camera_data_node = nodes_english_white.new(type='ShaderNodeCameraData')
        dot_product_node = nodes_english_white.new(type='ShaderNodeVectorMath')
        mapping_node2 = nodes_english_white.new(type='ShaderNodeMapping')
        camera_data_node2 = nodes_english_white.new(type='ShaderNodeCameraData')
        dot_product_node2 = nodes_english_white.new(type='ShaderNodeVectorMath')
        mix_shader_node = nodes_english_white.new(type='ShaderNodeMixShader')
        math_greater_node = nodes_english_white.new(type='ShaderNodeMath')
        math_greater_node2 = nodes_english_white.new(type='ShaderNodeMath')
        math_add_node = nodes_english_white.new(type='ShaderNodeMath')
        clamp_node = nodes_english_white.new(type='ShaderNodeClamp')

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

        # green material
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

        # Data
        english_paragraph = ("In the heart of the ocean, where the waves dance with the sun's "
                             "reflections, lies a tale of serenity and mystery. Beneath the surface,"
                             " creatures of wonder roam the vast blue expanse. Amongst the coral gardens,"
                             " secrets whisper, waiting to be discovered by those brave enough to dive into the depths."
                             )

        positions_english_array = [[165.52, 76.80], [248.64, 76.80], [378.80, 76.80], [494.86, 76.80], [581.68, 76.80],
                                   [724.63, 76.80], [248.26, 231.79], [390.22, 231.79], [532.63, 231.79],
                                   [708.90, 231.79],
                                   [193.72, 386.77], [308.34, 386.77], [436.70, 386.77], [667.51, 386.77],
                                   [400.57, 541.76],
                                   [478.20, 541.76], [552.62, 541.76], [185.30, 696.75], [338.26, 696.75],
                                   [512.91, 696.75],
                                   [686.00, 696.75], [313.62, 851.74], [484.16, 851.74], [645.52, 851.74],
                                   [336.01, 1006.72],
                                   [510.35, 1006.72], [649.32, 1006.72], [174.66, 1161.71], [301.63, 1161.71],
                                   [415.61, 1161.71], [544.41, 1161.71], [730.75, 1161.71], [229.29, 1316.70],
                                   [408.06, 1316.70], [534.85, 1316.70], [730.09, 1316.70], [360.56, 1471.69],
                                   [583.72, 1471.69], [249.45, 1626.67], [388.80, 1626.67], [463.76, 1626.67],
                                   [655.48, 1626.67], [207.22, 1781.66], [329.07, 1781.66], [495.07, 1781.66],
                                   [680.29, 1781.66], [202.05, 1936.65], [299.40, 1936.65], [421.25, 1936.65],
                                   [530.02, 1936.65], [681.11, 1936.65]]

        english_words = english_paragraph.split()

        scale_factor = 0.02
        english_words_scaled_coordinates = [(x * scale_factor, y * (scale_factor + 0.005)) for x, y in
                                            positions_english_array]
        english_words_scaled_coordinates = [(x, y + 2.6) for x, y in english_words_scaled_coordinates]

        tokens = nltk.word_tokenize(english_paragraph)
        full_tags = nltk.pos_tag(tokens)
        tags = [item for item in full_tags if item[0] not in {',', '.', "'", "'s"}]

        start_times_array = []
        for i in range(len(positions_english_array)):
            start_times_array.append(i * 0.5)

        # Loading WordData List
        tags_to_part_of_speech = TagToPartOfSpeech()
        new_words_and_tags = PartOfSpeechTagAssigner(tags).assign_tags()

        just_tags = []
        for word, tag in new_words_and_tags:
            just_tags.append(tag)

        word_data_list_creator = WordDataListCreator(tags_to_part_of_speech, english_words,
                                                     english_words_scaled_coordinates,
                                                     just_tags,
                                                     start_times_array)
        word_data_list = word_data_list_creator.build()

        # Collections
        words_3d_collection = WordsCollection()
        words_3d_collection.create_collection('english_3d_words')

        # Assembling Words
        material_identifier_g = PartOfSpeechMaterialIdentifier()
        blender_object_factory = BlenderObjectFactory()
        word_assembler_g = WordAssembler(alphabet_letters_collection, blender_object_factory)
        words_assembler_manager = WordsAssemblerManager(word_assembler_g, material_identifier_g, blender_object_factory,
                                                        words_3d_collection, word_data_list)
        # Assigning Word Objects to Parent Cube
        words_assembler_manager.assemble_words()
        for word_obj in words_assembler_manager.get_words_object_list():
            word_obj.parent = parent_cube

        # Rows Position and TimeStampNewline
        rows_position_calculator = RowsCalculator()
        rows_position = rows_position_calculator.get_rows(word_data_list)
        timestamp_creator = TimeStampCreator()
        double_row_timestamps = timestamp_creator.get_double_row_timestamps(word_data_list, 2)
        timestamps = timestamp_creator.get_timestamps(word_data_list)

        # Highlighter
        highlighter = Highlighter()
        highlighter.create("highlighter_obj")
        highlighter.rotate_on_x_axis(90)

        highlighter.add_material("hl_material")

        word_obj_list = words_assembler_manager.get_words_object_list()
        (HighlighterAnimator(highlighter, english_words_scaled_coordinates, rows_position, timestamps, word_obj_list)
         .setup_highlighter_animation(60, 10))

        # Parent Cube Animation
        parent_cube_animator = ParentCubeAnimator(parent_cube, double_row_timestamps)
        parent_cube_animator.animate_parent_cube(60, 10, [0, 0, 1], 15.5)

        materials = {
            "text_material": text_material,
            "yellow_material": yellow_material,
            "green_material": green_material,
            "blue_material": blue_material
        }
        # Children Text Objects
        text_object_factory = TextObjectFactory()
        text_object_factory.create_text_objects(
            word_data_list,
            0.7,
            0.68,
            self.efai_font_path,
            materials,
            0,
            2,
            2.3,
            parent_cube
        )

        text_object_factory.create_outline_text_objects(
            word_data_list,
            0.01,
            0.68,
            self.efai_font_path,
            outline_material,
            2,
            2.3,
            0.02,
            parent_cube
        )


main = MainProgram()
main.run()
