import bpy


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
                                      characters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.?',
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
            self.link_object_to_collection(alphabet_collection, text_object)

        return alphabet_collection
