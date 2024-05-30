import bpy
def createAlphabetCollection():
  # Create a new collection
  letters_collection = bpy.data.collections.new('phoneticLetters')
  # Link the collection to the scene
  bpy.context.scene.collection.children.link(letters_collection)
  #font_path = "C:\\Users\\abeld\\Documents\\fonts\\google-sans\\" + "ProductSans-Regular.ttf"
  font_path = "C:\\WINDOWS\\Fonts\\arialbd.ttf"
  # Create a new text object for each letter and link it to the collection
  english="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.?"
  ipaArray = [
    # Vowels
    'i', 'y', 'ɨ', 'ʉ', 'ɯ', 'u',
    'ɪ', 'ʏ', 'ʊ',
    'e', 'ø', 'ɘ', 'ɵ', 'ɤ', 'o',
    'ə',
    'ɛ', 'œ', 'ɜ', 'ɞ', 'ʌ', 'ɔ',
    'æ', 'ɐ',
    'a', 'ɶ', 'ɑ', 'ɒ',
    
    # Consonants
    'p', 'b', 't', 'd', 'ʈ', 'ɖ', 'c', 'ɟ', 'k', 'g', 'q', 'ɢ', 'ʔ',
    'm', 'ɱ', 'n','n', 'ɳ', 'ɲ', 'ŋ', 'ɴ',
    'ʙ', 'r', 'ʀ',
    'ⱱ', 'ɾ', 'ɽ',
    'ɸ', 'β', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'ʂ', 'ʐ', 'ç', 'ʝ', 'x', 'ɣ', 'χ', 'ʁ', 'ħ', 'ʕ', 'h', 'ɦ',
    'ɬ', 'ɮ', 'ɡ',
    'ʋ', 'ɹ', 'ɻ', 'j', 'ɰ', 'w',
    'l', 'ɭ', 'ʎ', 'ʟ', 'I',
    
    # Other Symbols
    'ˈ', 'ˌ', 'ː', 'ˑ', '|', '‖', '.', # Suprasegmentals
    '˥', '˦', '˧', '˨', '˩', ',' # Tones and Word Accents
  ]

  for letter in ipaArray:
    # Create a new text object
    bpy.ops.object.text_add(enter_editmode=False, location=(0, 0, 0))
    text_object = bpy.context.active_object
    #font resolution
    # front faces
    text_object.data.fill_mode = 'NONE'
    text_object.data.resolution_u = 5
    text_object.data.body = letter
    text_object.data.size = 1
    text_object.data.bevel_depth = 0.03
    #bevel resolution
    text_object.data.bevel_resolution = 0
    text_object.name = letter + "g"
    #alighn text to center
    text_object.data.align_y = 'CENTER'
    text_object.data.align_x = 'CENTER'

    text_object.data.font = bpy.data.fonts.load(font_path)
    # Convert the text to mesh
    bpy.ops.object.convert(target='MESH')
    text_object.data.materials.append(bpy.data.materials.get("sbackoutline"))

    #Face
    bpy.ops.object.text_add(enter_editmode=False, location=(0, 0, 0.02))
    text_object2 = bpy.context.active_object
    text_object2.data.fill_mode = 'FRONT'
    text_object2.data.resolution_u = 5
    text_object2.data.body = letter
    text_object2.data.size = 1
    text_object2.data.align_y = 'CENTER'
    text_object2.data.align_x = 'CENTER'
    text_object2.data.font = bpy.data.fonts.load(font_path)
    bpy.ops.object.convert(target='MESH')
    text_object2.data.materials.append(bpy.data.materials.get("souter"))

    
    # Select both objects
    bpy.context.view_layer.objects.active = text_object
    text_object.select_set(True)
    text_object2.select_set(True)

    # Join the objects
    bpy.ops.object.join()
    #deselct objects

    # Check if the object is already linked to a collection
    if text_object.name not in letters_collection.objects:
        # Link the text object to the new collection
        letters_collection.objects.link(text_object)
        # Remove the object from the scene collection
        bpy.context.scene.collection.objects.unlink(text_object)
    bpy.ops.object.select_all(action='DESELECT')


  # Deselect all objects
  bpy.ops.object.select_all(action='DESELECT')
  return letters_collection

# Call the function to create the collection and add the text objects
createAlphabetCollection()