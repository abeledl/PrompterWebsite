import bpy

# The collection containing the letter objects
letter_collection = bpy.data.collections['GoogleLetters']

# Ensure the 'words' collection exists or create it
if 'google_tag_words' not in bpy.data.collections:
    words_collection = bpy.data.collections.new('google_tag_words2')
    bpy.context.scene.collection.children.link(words_collection)
else:
    words_collection = bpy.data.collections['google_tag_words']

# Function to create a linked duplicate
def create_linked_duplicate(name):
    original = letter_collection.objects.get(name)
    if original is not None:
        new_obj = original.copy()
        new_obj.data = original.data
        words_collection.objects.link(new_obj)
        return new_obj
    else:
        print(f"Object named {name} not found.")
        return None

# Function to get the width of an object
def get_object_width(obj):
    bbox = obj.bound_box
    min_x, max_x = min(bbox, key=lambda p: p[0])[0], max(bbox, key=lambda p: p[0])[0]
    return max_x - min_x

# Function to create a word using linked instances
def create_word(word):
    empty = bpy.data.objects.new(word + "_Empty", None)
    words_collection.objects.link(empty)
    empty.location = (0, 0, 0)

    position = 0.0  # Starting position of the first letter
    for letter in word:
        obj_name = letter.upper() + 'g' if letter.isupper() else letter + 'g'
        obj = create_linked_duplicate(obj_name)
        if obj:
            obj_width = get_object_width(obj)
            obj.location.x = position + obj_width / 2  # Center the letter
            position += obj_width
            obj.parent = empty

# Example usage: Creating the word 'Hello'
create_word("Adjective")
create_word("Adverb")
create_word("Conjunction")
create_word("Determiner")
create_word("Preposition")
create_word("Pronoun")
create_word("Verb")
create_word("Noun")
#create_word("Infinitive")
