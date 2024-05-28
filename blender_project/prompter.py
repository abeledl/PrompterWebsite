import bpy
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import nltk
import math
import mathutils
import nltk

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
    z: float


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
            self.collection = bpy.data.collections[name]

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

class Alphabet3DPremadeCollection(BaseCollection):
    """
    Holds a collection for 3D alphabet letter objects
    """
    def __init__(self):
        super().__init__(None)

    def get_object(self, name: str):
        """
        Returns an object in the collection given its name

        Args:
            name: the name of the object in the collection

        Returns: an object in the collection
        """
        obj_name = name.upper() + '_3d_premade.001' if name.isupper() else name + '_3d_premade.001'
        return self.collection.objects.get(obj_name)

class PhoneticAlphabetCollection(BaseCollection):
    """
    Holds a collection for phonetic alphabet letter objects
    """

    def __init__(self):
        super().__init__(None)

    def get_object(self, name: str):
        """
        Returns an object in the collection given its name

        Args:
            name: the name of the object in the collection

        Returns: an object in the collection
        """
        obj_name = name.upper() + 'g' if name.isupper() else name + 'g'
        return self.collection.objects.get(obj_name)

class StickerLetterCollection(BaseCollection):

    def __init__(self):
        super().__init__(None)

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
            "infinitive": bpy.data.materials.get("infinitive_material")
        }

    def get_material_for(self, name):
        return self.part_of_speech_to_material_map[name]

class StickerMaterialIdentifier(MaterialIdentifier):
    def __init__(self):
        self.part_of_speech_to_material_map = {
            "verb": bpy.data.materials.get("sticker_verb_material"),
            "noun": bpy.data.materials.get("sticker_noun_material"),
            "adjective": bpy.data.materials.get("sticker_adjective_material"),
            "article": bpy.data.materials.get("sticker_determiner_material"),
            "adverb": bpy.data.materials.get("sticker_adverb_material"),
            "pronoun": bpy.data.materials.get("sticker_pronoun_material"),
            "preposition": bpy.data.materials.get("sticker_preposition_material"),
            "conjunction": bpy.data.materials.get("sticker_conjunction_material"),
            "infinitive": bpy.data.materials.get("sticker_infinitive_material")
        }

    def get_material_for(self, name):
        return self.part_of_speech_to_material_map[name]


# Prompter Layout
class RowContent(ABC):
    @property
    @abstractmethod
    def position(self) -> Position:
        pass

    @position.setter
    @abstractmethod
    def position(self, value: Position) -> None:
        pass

    @property
    @abstractmethod
    def width(self):
        pass

    @width.setter
    @abstractmethod
    def width(self, value: float) -> None:
        pass

    @property
    @abstractmethod
    def is_newline(self) -> bool:
        pass

    @is_newline.setter
    @abstractmethod
    def is_newline(self, value) -> None:
        pass


class Row:

    def __init__(self, width: float, spacing: float):
        self._content_list: List[RowContent] = []
        self._width: float = width
        self._accumulated_width: float = 0
        self._spacing = spacing
        self._position: Position = Position(0, 0, 0)

    @property
    def content(self):
        return self._content_list

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position
        self._update_content_position()

    @property
    def width(self):
        return self._width

    def _update_content_position(self):
        for content in self._content_list:
            content.position = Position(content.position.x, self.position.y, content.position.z)

    def add_content(self, new_content) -> bool:
        """
        Adds content to the row.
        Args:
            new_content (RowContent): The content to be added to the row.

        Returns:
            (bool) : False if no more content can be added, otherwise true if the content
                     was added successfully.
        """
        self._accumulated_width += new_content.width + self._spacing
        if self._accumulated_width < self._width:
            new_content.position = self._position
            self._content_list.append(new_content)
            return True
        return False

    def align_content(self):
        total_width = 0.0
        content_and_width = []

        for content in self._content_list:
            content_and_width.append((content, content.width))
            total_width += content.width

        start_position = -total_width / 2

        for content, width in content_and_width:
            content_x_pos = start_position + width / 2
            content.position = Position(content_x_pos, content.position.y, content.position.z)
            start_position += width

    def change_content_width(self):
        pass


class PrompterLayout:
    def __init__(
            self,
            height: float,
            width: float,
            center_position: Tuple[float, float, float],
            row_content: List[RowContent]
    ):
        self._height = height    # Height of the prompter
        self._width = width      # Width of the prompter.
        self._center_position = center_position  # Center coordinate of the prompter
        self._rows: List[Row] = []
        self._row_content_list: List[RowContent] = row_content
        self._rows_position: List[Position] = []

    @property
    def height(self):
        return self._height

    @property
    def rows(self):
        return self._rows

    def assign_rows_content(self):
        row = Row(self._width, 0)
        count = 0
        for content in self._row_content_list:
            if not row.add_content(content):
                row.align_content()
                self._rows.append(row)
                count += 1
                if count % 2 == 0 and count != 0:
                    content.is_newline =True
                row = Row(self._width, 0)
                row.add_content(content)

        row.align_content()
        self._rows.append(row)

    def assign_rows_position(self):
        for row, position in zip(self._rows, self._rows_position):
            row.position = position

    def distance_between_rows(self):
        return self._height / 2

    def calculate_rows_position(self):
        first_row_position = (self._height / 2) / 2
        space_in_between_rows = self._height / 2
        current_row_position_y = first_row_position
        for row in self._rows:
            self._rows_position.append(Position(0, current_row_position_y, 0))
            current_row_position_y -= space_in_between_rows


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


class WordObjectBuilder(RowContent):

    def __init__(self, word_assembler: Assembler, material_identifier: MaterialIdentifier,
                 object_aligner: ObjectAligner, object_factory: ObjectFactory):
        super().__init__()
        self.word_assembler = word_assembler
        self.material_identifier = material_identifier
        self.object_aligner = object_aligner
        self.blender_object_factory = object_factory
        self._letter_object_list = []
        self._is_newline = False
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

    def set_position(self, position: Tuple[float, float, float]) -> "WordObjectBuilder":
        self.empty_word_object.location = position
        return self

    @property
    def position(self):
        return Position(
            self.empty_word_object.location.x,
            self.empty_word_object.location.y,
            self.empty_word_object.location.z
        )

    @position.setter
    def position(self, position: Position):
        self.empty_word_object.location.x = position.x
        self.empty_word_object.location.y = position.y
        self.empty_word_object.location.z = position.z

    @property
    def width(self):
        padding = 0.6
        return self._calculate_children_obj_total_width(self.empty_word_object) + padding

    @width.setter
    def width(self, scale):
        self.empty_word_object.scale = (scale, scale, scale)
        pass

    @property
    def is_newline(self) -> bool:
        return self._is_newline

    @is_newline.setter
    def is_newline(self, value: bool):
        self._is_newline = value

    def add_key_frame(self, property_name: str, frame_number: int):
        self.empty_word_object.keyframe_insert(data_path=property_name, frame=frame_number)

    def get_word_object(self):
        return self.empty_word_object

    def set_scale(self, scale: float) -> "WordObjectBuilder":
        self.empty_word_object.scale = (scale, scale, scale)
        self.width = scale
        return self

    # Private
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
            total_width += (self._get_object_width(child_obj))
        return total_width

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
        self.word_object_builder_list: List[WordObjectBuilder] = []

    def get_words_object_list(self):
        return self.words_object_list

    def assemble_word(self, word_data: WordData, vertical_offset: float, scale: float, with_material: bool):
        builder = (WordObjectBuilder(self.word_assembler, self.material_identifier, self.object_aligner,
                                     self.blender_object_factory)
                   .create_object(word_data.text)
                   .link_to_collection(self.words_collection)
                   .set_position((word_data.position.x, word_data.position.y + vertical_offset, 0))
                   .set_scale(scale))
        if with_material:
            builder.apply_material(word_data.part_of_speech)
        self.words_object_list.append(builder.get_word_object())
        self.word_object_builder_list.append(builder)

    def assemble_words(self, vertical_offset: float, scale: float, with_material: bool):
        """
        Assembles empty word objects form the words list linking them to a words_collection
        """
        for word in self.word_data_list:
            self.assemble_word(word, vertical_offset, scale, with_material)

    def get_word_object_builder_list(self) -> List[WordObjectBuilder]:
        return self.word_object_builder_list


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
            # if it's a verb and the previous word is to, then it is infinitive
            if tag in TagToPartOfSpeech().part_of_speech_tags_dictionary['verb'] and words_and_tag_list[index - 1][0] == 'to':
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
                position=Position(x=position[0], y=-1 * position[1] - 0.25, z=0),
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
                        self.rows_positions.append(Position(word.position.x, -word.position.y, 0))
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
        self.scale_node = None
        #self.transform_node = None
        self._create_geometry_node_group()

    # Public
    #@property
    #def geometry_transform_node(self):
    #    return self.transform_node

    @property
    def geometry_scale_node_hl(self):
        return self.scale_node

    # Private
    def _create_geometry_node_group(self):
        #bpy.ops.node.new_geometry_node_group_assign()

        # Get the node group of the Geometry Nodes modifier
        node_group = self.node_modifier.node_group
        self.scale_node = node_group.nodes.get("Vector Scale HL")
        if self.scale_node is None:
            print("scale not found", self.scale_node)
            raise RuntimeError("scale node not found")


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
        #bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8),
        #                                scale=(1, 1, 1))
        self._highlighter_obj = bpy.data.objects.get("hl_object")
        self._highlighter_obj.name = name
        self._add_geometry_modifier()
        #self._add_bevel_modifier_before_solidify()
        #self._add_solidify_modifier()
        #self._add_bevel_modifier_after_solidify()
        #self._shade_flat()

    def rotate_on_x_axis(self, degrees: float):
        self._highlighter_obj.rotation_euler[0] = math.radians(degrees)

    def add_material(self, material_name: str):
        material = bpy.data.materials.get(material_name)
        self._highlighter_obj.data.materials.append(material)

    def add_key_frame(self, property_name, frame_number):
        self._highlighter_obj.keyframe_insert(data_path=property_name, frame=frame_number)
        self.geometry_modifier.scale_node.inputs[0].keyframe_insert(data_path='default_value',
                                                                              frame=frame_number)

    def set_position(self, x_pos, y_pos):
        self._set_obj_position(x_pos, y_pos, 0, self._highlighter_obj)

    def set_parent(self, parent):
        self._highlighter_obj.parent = parent

    # Private
    def _add_geometry_modifier(self):
        #self._highlighter_obj.modifiers.new(name="NodesModifier2", type='NODES')
        #self._highlighter_obj.modifiers[-1].name = "geo1"

        # Get geometry modifier from blender for highlighter
        node_modifier = self._highlighter_obj.modifiers.get("hl_geo")
        if node_modifier is None or node_modifier.type != 'NODES':
            raise RuntimeError("Geometry Modifier not found")
        self._geometry_modifier = GeometryModifier(node_modifier)

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
    TARGET_HEIGHT = 3  # Units: Blender Units

    def __init__(
            self,
            highlighter: Highlighter,
            target_coordinates: List[Tuple[float, float]],
            row_positions: List[Position],
            timestamps_and_newline_flag: List[TimestampNewline],
            target_list: List[WordObjectBuilder],
            layout: PrompterLayout
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

        self._layout = layout

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
        coordinate: Position = self._target_list[target_index].position
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

    def _update_highlighter_position(self, coordinate: Position) -> None:
        self._highlighter.set_position(coordinate.x, coordinate.y)

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
        #self._highlighter.geometry_modifier.transform_node.inputs['Scale'].default_value[0] = width / 2
        #self._highlighter.geometry_modifier.transform_node.inputs['Scale'].default_value[1] = height / 2
        self._highlighter.geometry_modifier.scale_node.inputs[0].default_value[0] = width
        self._highlighter.geometry_modifier.scale_node.inputs[0].default_value[1] = height

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
        padding = 0.5
        for child_obj in obj.children:
            total_width += (self._get_object_width(child_obj))
        return total_width + padding

    def _generate_target_width_and_height(self, target_obj: WordObjectBuilder) -> Dict[str, float]:
        """
        Creates a dictionary object that store the target obj width and height.
        The keys are "width" and "height"
        Args:
            target_obj (bpy.types.Object): Object that needs width and height to be calculated

        Returns:
            Dict[str, float]: The dictionary that contains the objects with and height
        """
        return {"width": target_obj.width, "height": self.TARGET_HEIGHT}

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
    def __init__(self, parent_cub: bpy.types.Object, double_row_timestamps: List[TimestampNewline], word_obj_list: List[WordObjectBuilder]):
        self._parent_cube = parent_cub
        self._double_row_timestamps = double_row_timestamps
        self._word_obj_list = word_obj_list

    # Public
    def animate_parent_cube(
            self,
            fps: int,
            animation_duration: int,
            direction: List[int],
            distance: float
    ) -> None:
        # for second in end_times_array:
        for timestamp_flag, word_obj in zip(self._double_row_timestamps, self._word_obj_list):
            second = timestamp_flag.timestamp
            bool_val = word_obj.is_newline

            if bool_val:
                frame = self._calculate_frame(second, fps)
                self._add_key_frame(frame, "location")
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
        self.efai_font_path = "C:\\WINDOWS\\Fonts\\ARLRDBD.ttf"
        self.phonetic_font_path = "C:\\WINDOWS\\Fonts\\arialbd.ttf"

    def run(self):

        # Create Parent Cube
        parent_cube = bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        parent_cube = bpy.context.active_object
        parent_cube.name = "parent_cube"
        parent_cube.scale = (1, 1, 1)
        parent_cube.location = (0, 0, 0)
        rotation_x_parent_cube = math.radians(90)
        parent_cube.rotation_euler[0] = rotation_x_parent_cube

        # Data
        english_paragraph = ("In the heart of the ocean, where the waves dance with the sun's "
                             "reflections, lies a tale of serenity and mystery. Beneath the surface,"
                             " creatures of wonder roam the vast blue expanse. Amongst the coral gardens,"
                             " secrets whisper, waiting to be discovered by those brave enough to -dive- into the depths."
                             )
        spanish_paragraph = ("En el corazon de el oceano donde las olas bailan con los sol reflejos yace un cuento de serenidad y misterio Debajo de-la superficie criaturas de maravilla vagan la vasta azul extension Entre los coral jardines secretos susurran esperando a ser descubiertos por aquellos valiente suficientemente para sumergirse en las profundidades")

        phonetic_paragraph = ("In də hart əv də osin, wɛɹ də weɪvz dæns wɪð də sʌnz rɪfɛkʃənz, laɪz ə tel əv sɛrɪnəti ənd mɪstəri. bəniθ də sɜrfəs, kɹitʃəz əv wʌndəɹ ɹoʊm ðə væst blu ɪkˈspæns. əmʌŋst ðə kɔɹəl ɡɑɹdənz, sikɹɪts wɪspəɹ, weɪtɪŋ tə bi dɪˈskʌvəɹd baɪ ðoʊz breɪv ɪˈnʌf tə daɪv ɪntə ðə dɛps.")
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
        spanish_words = spanish_paragraph.split()
        phonetic_words = phonetic_paragraph.split()

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
        spanish_word_data_list_creator = WordDataListCreator(tags_to_part_of_speech, spanish_words,
                                                     english_words_scaled_coordinates,
                                                     just_tags,
                                                     start_times_array)
        spanish_word_data_list = spanish_word_data_list_creator.build()
        phonetic_word_data_list_creator = WordDataListCreator(tags_to_part_of_speech, phonetic_words,
                                                     english_words_scaled_coordinates,
                                                     just_tags,
                                                     start_times_array)
        phonetic_word_data_list = phonetic_word_data_list_creator.build()
        # Collections
        alphabet_3d_letters_premade_collection = Alphabet3DPremadeCollection()
        alphabet_3d_letters_premade_collection.create_collection('drawn_letters_premade')
        phonetic_letters_premade_collection = PhoneticAlphabetCollection()
        phonetic_letters_premade_collection.create_collection('phoneticLetters')
        spanish_letters_premade_collection = StickerLetterCollection()
        spanish_letters_premade_collection.create_collection('sticker_lowpoly_letters')
        english_words_collection = WordsCollection()
        english_words_collection.create_collection('english_words')
        phonetic_words_collection = WordsCollection()
        phonetic_words_collection.create_collection('phonetic_words')
        spanish_words_collection = WordsCollection()
        spanish_words_collection.create_collection('spanish_words')

        # Assembling Words
        material_identifier_g = PartOfSpeechMaterialIdentifier()
        sticker_material_identifier = StickerMaterialIdentifier()
        blender_object_factory = BlenderObjectFactory()
        word_assembler_g = WordAssembler(alphabet_3d_letters_premade_collection, blender_object_factory)
        words_assembler_manager = WordsAssemblerManager(word_assembler_g, material_identifier_g, blender_object_factory,
                                                        english_words_collection, word_data_list)
        phonetic_assembler = WordAssembler(phonetic_letters_premade_collection, blender_object_factory)

        phonetic_assembler_manager = WordsAssemblerManager(phonetic_assembler, material_identifier_g, blender_object_factory,
                                                          phonetic_words_collection, phonetic_word_data_list)
        spanish_assembler = WordAssembler(spanish_letters_premade_collection, blender_object_factory)
        spanish_assembler_manager = WordsAssemblerManager(spanish_assembler, sticker_material_identifier, blender_object_factory,
                                                            spanish_words_collection, spanish_word_data_list)
        # Assigning Word Objects to Parent Cube
        words_assembler_manager.assemble_words(0, 1, True)
        phonetic_assembler_manager.assemble_words(-0.5, 0.8, False)
        spanish_assembler_manager.assemble_words(-1.4, 0.5, True)



        # Prompter Layout
        prompter_layout = PrompterLayout(8, 15, (0, 0, 0),
                       words_assembler_manager.get_word_object_builder_list())

        prompter_layout.assign_rows_content()
        prompter_layout.calculate_rows_position()
        prompter_layout.assign_rows_position()


        # Making phonetic and spanish children of english and matching their positions
        for phonetic_obj, word_obj in zip(phonetic_assembler_manager.get_word_object_builder_list(), words_assembler_manager.get_word_object_builder_list()):
            phonetic_obj.position = Position(0, -0.4, 0)

        for spanish_obj, word_obj in zip(spanish_assembler_manager.get_word_object_builder_list(), spanish_assembler_manager.get_word_object_builder_list()):
            spanish_obj.position = Position(0, -1, 0)

        for word_obj in words_assembler_manager.get_words_object_list():
            word_obj.parent = parent_cube
        for phonetic_obj, word_obj in zip(phonetic_assembler_manager.get_words_object_list(), words_assembler_manager.get_words_object_list()):
            phonetic_obj.parent = word_obj
        for spanish_obj, word_obj in zip(spanish_assembler_manager.get_words_object_list(), words_assembler_manager.get_words_object_list()):
            spanish_obj.parent = word_obj


        # Rows Position and TimeStampNewline
        rows_position_calculator = RowsCalculator()
        rows_position = rows_position_calculator.get_rows(word_data_list)
        timestamp_creator = TimeStampCreator()
        double_row_timestamps = timestamp_creator.get_double_row_timestamps(word_data_list, 2)
        timestamps = timestamp_creator.get_timestamps(word_data_list)

        # Highlighter
        highlighter = Highlighter()
        highlighter.create("highlighter_obj")
        highlighter.rotate_on_x_axis(0)
        highlighter.set_parent(parent_cube)
        highlighter.add_material("hl_material")

        word_obj_list = words_assembler_manager.get_words_object_list()
        (HighlighterAnimator(highlighter, english_words_scaled_coordinates, rows_position, timestamps, words_assembler_manager.get_word_object_builder_list(), prompter_layout)
         .setup_highlighter_animation(60, 10))

        # Parent Cube Animation
        parent_cube_animator = ParentCubeAnimator(parent_cube, timestamps, words_assembler_manager.get_word_object_builder_list())
        parent_cube_animator.animate_parent_cube(60, 10, [0, 0, 1], prompter_layout.height)



main = MainProgram()
main.run()
