import numpy as np
import bpy
import math
import random
namesOfObjectsNumbered = []

# Get the collection named 'alphabet'
alphabet_collection = bpy.data.collections.get("alphabet")

# Check if the collection exists
if alphabet_collection:
  # Get all objects in the 'alphabet' collection
  objects_in_alphabet = [obj for obj in alphabet_collection.objects]
  # Now you can iterate over the objects_in_alphabet list and perform actions
  for i, obj in enumerate(objects_in_alphabet, start= 0):
    namesOfObjectsNumbered.append((i, obj.name))
  #print(namesOfObjectsNumbered)
else:
  print("Collection named 'alphabet' does not exist.")

lengthOfObjects = len(namesOfObjectsNumbered)

class Repeats:
  top_repeats = False
  bot_repeats = False

def isEven(number):
  return number % 2 == 0

def isOdd(number):
  return number % 2 != 0


bpy.data.objects["morph"].select_set(True)
morphing_obj = bpy.data.objects["morph"]
node_modifier = morphing_obj.modifiers.get("morphgeo")
node_group = node_modifier.node_group


def createGroupGeoTop1GeoTop2Switch(currentIndex, currentPosition, repeats, isLast):
  geometryNodeObjectInfo = node_group.nodes.new("GeometryNodeObjectInfo")
  nameOfObjInfo = 'ObjectInfo'
  geometryNodeObjectInfo.name = f'{nameOfObjInfo}{currentIndex}'  
  geometryNodeObjectInfo.label = f'{nameOfObjInfo}{currentIndex}'
  geometryNodeObjectInfo.inputs[0].default_value = bpy.data.objects[namesOfObjectsNumbered[currentIndex][1]]
  geometryNodeObjectInfo.transform_space = 'RELATIVE'
  if currentIndex > 4:
      repeats.top_repeats = True
      repeats.bot_repeats = True
  if isEven(currentIndex):
    if repeats.top_repeats:
      geometryNodeObjectInfo.location = (-150 * (currentPosition + 9) , 200 *  4)
    else:
      geometryNodeObjectInfo.location = (-150 * (currentPosition + 9) , 200 *  6)
      repeats.top_repeats = True
    
  else:
    if repeats.bot_repeats:
      geometryNodeObjectInfo.location = (-150 * (currentPosition + 9) , -200 *  6)
    else:
      geometryNodeObjectInfo.location = (-150 * (currentPosition + 9) , -200 *  4)
      repeats.bot_repeats = True
  if (currentIndex < 2):
     if isLast:
        if isEven(currentIndex):
          correctsdf1 = node_group.nodes.get('correctsdf1')
          growth1 = node_group.nodes.get('growth1')
          joinGeometry = node_group.nodes.get('Join Geometry')
          node_group.links.new(geometryNodeObjectInfo.outputs[3], correctsdf1.inputs[0])
          node_group.links.new(geometryNodeObjectInfo.outputs[3], growth1.inputs[0])
          node_group.links.new(geometryNodeObjectInfo.outputs[3], joinGeometry.inputs[0])
        else:
          correctsdf2 = node_group.nodes.get('correctsdf2')
          growth2 = node_group.nodes.get('growth2')
          joinGeometry = node_group.nodes.get('Join Geometry')
          node_group.links.new(geometryNodeObjectInfo.outputs[3], correctsdf2.inputs[0])
          node_group.links.new(geometryNodeObjectInfo.outputs[3], growth2.inputs[0])
          node_group.links.new(geometryNodeObjectInfo.outputs[3], joinGeometry.inputs[0])

  if (currentIndex > 1 and currentIndex < 4 ): # two obj info haave been created
    if isEven(currentIndex):
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8) -10, 200 * (5.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousObjInfo = node_group.nodes.get(f"ObjectInfo{currentIndex - 2}")
        node_group.links.new(previousObjInfo.outputs[3], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
        if isLast:
          correctsdf1 = node_group.nodes.get('correctsdf1')
          growth1 = node_group.nodes.get('growth1')
          joinGeometry = node_group.nodes.get('Join Geometry')
          node_group.links.new(switchNext.outputs[0], correctsdf1.inputs[0])
          node_group.links.new(switchNext.outputs[0], growth1.inputs[0])
          node_group.links.new(switchNext.outputs[0], joinGeometry.inputs[0])
    else:
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8) -10, -200 * (4.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousObjInfo = node_group.nodes.get(f"ObjectInfo{currentIndex - 2}")
        node_group.links.new(previousObjInfo.outputs[3], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
        if isLast:
          correctsdf2 = node_group.nodes.get('correctsdf2')
          growth2 = node_group.nodes.get('growth2')
          joinGeometry = node_group.nodes.get('Join Geometry')
          node_group.links.new(switchNext.outputs[0], correctsdf2.inputs[0])
          node_group.links.new(switchNext.outputs[0], growth2.inputs[0])
          node_group.links.new(switchNext.outputs[0], joinGeometry.inputs[0])
  if (currentIndex > 3):
    if isEven(currentIndex):
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8)-10, 200 * (5.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousSwitchInfo = node_group.nodes.get(f"Switch{currentIndex - 2}")
        node_group.links.new(previousSwitchInfo.outputs[0], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
        if isLast:
          correctsdf1 = node_group.nodes.get('correctsdf1')
          growth1 = node_group.nodes.get('growth1')
          joinGeometry = node_group.nodes.get('Join Geometry')
          node_group.links.new(switchNext.outputs[0], correctsdf1.inputs[0])
          node_group.links.new(switchNext.outputs[0], growth1.inputs[0])
          node_group.links.new(switchNext.outputs[0], joinGeometry.inputs[0])
    else:
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8) -10, -200 * (4.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousSwitchInfo = node_group.nodes.get(f"Switch{currentIndex - 2}")
        node_group.links.new(previousSwitchInfo.outputs[0], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
        if isLast:
          correctsdf2 = node_group.nodes.get('correctsdf2')
          growth2 = node_group.nodes.get('growth2')
          joinGeometry = node_group.nodes.get('Join Geometry')
          node_group.links.new(switchNext.outputs[0], correctsdf2.inputs[0])
          node_group.links.new(switchNext.outputs[0], growth2.inputs[0])
          node_group.links.new(switchNext.outputs[0], joinGeometry.inputs[0]) 


def create_pattern(length):
    pattern = []
    twoZero = True
    firstPosition = 0
    if isEven(length):
        firstPosition = int(length / 2) - 2
    else:
        firstPosition = int((length + 1) / 2) - 2
        twoZero = False 
    if length == 1:
        pattern.append(firstPosition)   
    if length == 2:
        for _ in range(2):
            pattern.append(firstPosition)   
    if length == 3:
        for _ in range(3):
            pattern.append(firstPosition)   
    if length > 3:
        for _ in range(4):
            pattern.append(firstPosition)   
    if length > 4:
        # Pattern for even numbers
        if twoZero:
            for i in range(int(firstPosition) - 1, 0, -1):
                pattern.append(i)
                pattern.append(i)
            pattern.append(0)
            pattern.append(0)
        else: 
            for i in range(int(firstPosition) -1, 0, -1):
                pattern.append(i)
                pattern.append(i)
            pattern.append(0)
    return pattern


objInfoPositionArray = create_pattern(lengthOfObjects)
ramaining = lengthOfObjects
repeats = Repeats()
for i in range(0, len(namesOfObjectsNumbered)):
  if ramaining < 3:
    isLast = True
  else:
    isLast = False
  createGroupGeoTop1GeoTop2Switch(i, objInfoPositionArray[i], repeats, isLast)
  ramaining -= 1




random_times = []
smallest_difference = 0
def generate_random_times():
  array = []
  # Generate 50 random decimal numbers less than 200
  random_decimals = [random.uniform(0, 60) for _ in range(26)]
  # Sort the list to ensure they are in incremental order
  sorted_decimals = sorted(random_decimals)
  # Print the sorted list
  for number in sorted_decimals:
    array.append(round(number, 2))
  return array
def generate_order_integers():
  array = []
  for i in range(0, lengthOfObjects):
    array.append(i)
  return array
#random_times = generate_random_times()
random_times = generate_order_integers()
def find_smallest_difference(randomTimes):
  #assuming array is sorted
  differences = [round(randomTimes[i+1] - randomTimes[i], 2) for i in range(len(randomTimes)-1)]
  # Find the smallest difference
  smallest_difference = min(differences)
  return smallest_difference

smallest_difference = find_smallest_difference(random_times)
print (random_times) 
print ("smallest difference:", smallest_difference)

transition_duration = 30
#transition duration is frame interval - word duration
def animate_mix_factor(transitionDuration, randomTimes):
  # Create the keyframes
  morphmix = node_group.nodes.get('morphmix')
  if morphmix is not None:
    for index in range(lengthOfObjects):
      # Set the mix factor value
      value = 0 if isEven(index ) else 1
      morphmix.inputs[0].default_value = value
      # Insert the keyframe
      print ("after ", randomTimes[index], " seconds ", "turns into ", namesOfObjectsNumbered[index][1])
      morphmix.inputs[0].keyframe_insert(data_path='default_value', frame=(randomTimes[index] * 60))
      if index < lengthOfObjects - 1: #if it is the last object
        morphmix.inputs[0].keyframe_insert(data_path='default_value', frame=(randomTimes[index + 1] * 60 - transitionDuration)) #it will be 10 frames before the next word starts
         
animate_mix_factor(transition_duration, random_times)

def animate_switches(transitionDuration, randomTimes):
  for i in range(0, len(namesOfObjectsNumbered)):
    if i > 1:
      switch = node_group.nodes.get(f'Switch{i}')
      if switch is not None:
        switch.inputs[0].default_value = 0
        switch.inputs[0].keyframe_insert(data_path='default_value', frame=((60 * randomTimes[i]) - transitionDuration + 1))
        switch.inputs[0].default_value = 1
        switch.inputs[0].keyframe_insert(data_path='default_value', frame=((60 * randomTimes[i]) - transitionDuration + 2))
animate_switches(transition_duration, random_times)


objInfoPositionArray = create_pattern(lengthOfObjects)
ramaining2 = lengthOfObjects
repeats2 = Repeats()
def setupMorphingMaterial(currentIndex, currentPosition, repeats, isLast):
  #get material "MorphingMaterial"
  morphMaterial = bpy.data.materials.get("MorphingMaterial")
  node_group = morphMaterial.node_tree
  rgbNode = node_group.nodes.new("ShaderNodeRGB")
  rgbNode.location = (0, 0)
  #generate random color

  rgbNode.outputs[0].default_value = (random.random(), random.random(), random.random(), 1)
  rgbNode.name = f'RGB{currentIndex}' 
  if currentIndex > 4:
      repeats.top_repeats = True
      repeats.bot_repeats = True
  if isEven(currentIndex):
    if repeats.top_repeats:
      rgbNode.location = (-150 * (currentPosition + 9) , 200 *  4)
    else:
      rgbNode.location = (-150 * (currentPosition + 9) , 200 *  6)
      repeats.top_repeats = True
  else:
    if repeats.bot_repeats:
      rgbNode.location = (-150 * (currentPosition + 9) , -200 *  6)
    else:
      rgbNode.location = (-150 * (currentPosition + 9) , -200 *  4)
      repeats.bot_repeats = True
  if (currentIndex < 2):
      if isLast:
          if isEven(currentIndex):
            #pbsdf1 = node_group.nodes.get('pbsdf1')
            mixcolor5 = node_group.nodes.get('Mix5')
            node_group.links.new(rgbNode.outputs[0], mixcolor5.inputs[6])
          else:
            #pbsdf2 = node_group.nodes.get('pbsdf2')
            mixcolor6 = node_group.nodes.get('Mix6')
            node_group.links.new(rgbNode.outputs[0], mixcolor6.inputs[6])
  if (currentIndex > 1 and currentIndex < 4 ): # two obj info haave been created
      if isEven(currentIndex):
        mixColorNode1 = node_group.nodes.new("ShaderNodeMixRGB")
        mixColorNode1.location = (-150 * (currentPosition + 7.8) -10, 200 * (5.5))
        mixColorNode1.name = f'MixColor{currentIndex}'
        mixColorNode1.inputs[0].default_value = 0
        previousRGB = node_group.nodes.get(f"RGB{currentIndex - 2}")
        node_group.links.new(previousRGB.outputs[0], mixColorNode1.inputs[1])
        node_group.links.new(rgbNode.outputs[0], mixColorNode1.inputs[2])
        if isLast:
          #pbsdf1 = node_group.nodes.get('pbsdf1')
          mixcolor5 = node_group.nodes.get('Mix5')
          node_group.links.new(mixColorNode1.outputs[0], mixcolor5.inputs[6])
      else:
        mixColorNode1 = node_group.nodes.new("ShaderNodeMixRGB")
        mixColorNode1.location = (-150 * (currentPosition + 7.8) -10, -200 * (4.5))
        mixColorNode1.name = f'MixColor{currentIndex}'
        mixColorNode1.inputs[0].default_value = 0
        previousRGB = node_group.nodes.get(f"RGB{currentIndex - 2}")
        node_group.links.new(previousRGB.outputs[0], mixColorNode1.inputs[1])
        node_group.links.new(rgbNode.outputs[0], mixColorNode1.inputs[2])
        if isLast:
          #pbsdf2 = node_group.nodes.get('pbsdf2')
          mixcolor6 = node_group.nodes.get('Mix6')
          node_group.links.new(mixColorNode1.outputs[0], mixcolor6.inputs[6])
  if (currentIndex > 3):
    if isEven(currentIndex):
        mixColorNode1 = node_group.nodes.new("ShaderNodeMixRGB")
        mixColorNode1.location = (-150 * (currentPosition + 7.8)-10, 200 * (5.5))
        mixColorNode1.name = f'MixColor{currentIndex}'
        mixColorNode1.inputs[0].default_value = 0
        previousMixColor = node_group.nodes.get(f"MixColor{currentIndex - 2}")
        node_group.links.new(previousMixColor.outputs[0], mixColorNode1.inputs[1])
        node_group.links.new(rgbNode.outputs[0], mixColorNode1.inputs[2])
        if isLast:
          #pbsdf1 = node_group.nodes.get('pbsdf1')
          mixcolor5 = node_group.nodes.get('Mix5')
          node_group.links.new(mixColorNode1.outputs[0], mixcolor5.inputs[6])
    else:
        mixColorNode1 = node_group.nodes.new("ShaderNodeMixRGB")
        mixColorNode1.location = (-150 * (currentPosition + 7.8) -10, -200 * (4.5))
        mixColorNode1.name = f'MixColor{currentIndex}'
        mixColorNode1.inputs[0].default_value = 0
        previousMixColor = node_group.nodes.get(f"MixColor{currentIndex - 2}")
        node_group.links.new(previousMixColor.outputs[0], mixColorNode1.inputs[1])
        node_group.links.new(rgbNode.outputs[0], mixColorNode1.inputs[2])
        if isLast:
          #pbsdf2 = node_group.nodes.get('pbsdf2')
          mixcolor6 = node_group.nodes.get('Mix6')
          node_group.links.new(mixColorNode1.outputs[0], mixcolor6.inputs[6])



def animate_mixswitch_factor(random_times):
  morphMaterial = bpy.data.materials.get("MorphingMaterial")
  node_group = morphMaterial.node_tree
  for i in range(0, lengthOfObjects):
    if i > 1:
      mixColor = node_group.nodes.get(f'MixColor{i}')
      if mixColor is not None:
        mixColor.inputs[0].default_value = 0
        mixColor.inputs[0].keyframe_insert(data_path='default_value', frame=((60 * random_times[i]) + 1))
        mixColor.inputs[0].default_value = 1
        mixColor.inputs[0].keyframe_insert(data_path='default_value', frame=((60 * random_times[i]) + 2))


def painterlyMaterial():
  #get material "MorphingMaterial"
  morphMaterial = bpy.data.materials.get("MorphingMaterial")
  node_group = morphMaterial.node_tree
  
  pbsdf1 = node_group.nodes.get('pbsdf1')
  pbsdf2 = node_group.nodes.get('pbsdf2')


  #NORMALS
  textureCoordinate = node_group.nodes.new("ShaderNodeTexCoord")
  textureCoordinate.location = (-1800, 0)
  mapping = node_group.nodes.new("ShaderNodeMapping")
  mapping.location = (-1700, -200)
  mapping.inputs[3].default_value = (1, 1, 1)
  valuescale = node_group.nodes.new("ShaderNodeValue")
  valuescale.location = (-1800, -400)
  valuescale.outputs[0].default_value = 1
  mixcolor = node_group.nodes.new("ShaderNodeMix")
  mixcolor.location = (-1550, 0)
  mixcolor.data_type = 'RGBA'
  mixcolor.inputs[0].default_value = 0.15
  mixcolor.blend_type = 'LINEAR_LIGHT'
  mixcolor2 = node_group.nodes.new("ShaderNodeMix")
  mixcolor2.location = (-1300, 0) 
  mixcolor2.data_type = 'RGBA'
  mixcolor2.inputs[0].default_value = 0.15
  mixcolor2.blend_type = 'LINEAR_LIGHT'
  noiseTexture = node_group.nodes.new("ShaderNodeTexNoise")
  noiseTexture.location = (-1550, -200)
  veronoiTexture = node_group.nodes.new("ShaderNodeTexVoronoi")
  veronoiTexture.location = (-850, 0)
  veronoiTexture.inputs[1].default_value = 4
  veronoiTexture.inputs[2].default_value = 1
  imagetexturenormal = node_group.nodes.new("ShaderNodeTexImage")
  imagetexturenormal.location = (-1000, -400)
  imagetexturenormal.image = bpy.data.images.load("C:/Users/abeld/Pictures/zTextures/paitingbrush/Paint-Brush_normal.png")
  imagetexturenormal.projection = 'BOX'
  imagetexturenormal.projection_blend = 1
  imagetexturenormal.image.colorspace_settings.name = 'Non-Color'
  normalmap = node_group.nodes.new("ShaderNodeNormalMap")
  normalmap.location = (-450, -250)
  normalmap.inputs[0].default_value = 5
  mixcolor3 = node_group.nodes.new("ShaderNodeMix")
  mixcolor3.location = (-250, 0)
  mixcolor3.data_type = 'RGBA'
  mixcolor3.inputs[0].default_value = 0.3

  #DIFFUSE
  imagetexturediffuse = node_group.nodes.new("ShaderNodeTexImage")
  imagetexturediffuse.location = (-1000, 400)
  imagetexturediffuse.image = bpy.data.images.load("C:/Users/abeld/Pictures/zTextures/paitingbrush/Paint-Brush_diffuse.png")
  imagetexturediffuse.projection = 'BOX'
  imagetexturediffuse.projection_blend = 1
  mixcolor4 = node_group.nodes.new("ShaderNodeMix")
  mixcolor4.location = (-250, 400)
  mixcolor4.data_type = 'RGBA'
  mixcolor4.inputs[0].default_value = 0.7
  mixcolor4.blend_type = 'MULTIPLY'
  colorramp = node_group.nodes.new("ShaderNodeValToRGB")
  mixcolor5 = node_group.nodes.new("ShaderNodeMix")
  mixcolor5.location = (-250, 800)
  mixcolor5.data_type = 'RGBA'
  mixcolor5.name = 'MixColor5'
  mixcolor6 = node_group.nodes.new("ShaderNodeMix")
  mixcolor6.location = (-250, -800)
  mixcolor6.data_type = 'RGBA'
  mixcolor6.name = 'MixColor6'
  colorramp2 = node_group.nodes.new("ShaderNodeValToRGB")
  colorramp2.location = (-250, 1200)


  #linking 
  node_group.links.new(textureCoordinate.outputs[1], mixcolor.inputs[6])
  node_group.links.new(noiseTexture.outputs[1], mixcolor.inputs[7])
  node_group.links.new(mixcolor.outputs[2], mixcolor2.inputs[6])
  node_group.links.new(mixcolor2.outputs[2], veronoiTexture.inputs[0])
  node_group.links.new(textureCoordinate.outputs[1], mixcolor.inputs[6])
  node_group.links.new(textureCoordinate.outputs[3], noiseTexture.inputs[0])
  node_group.links.new(imagetexturenormal.outputs[0], normalmap.inputs[1])
  node_group.links.new(normalmap.outputs[0], mixcolor3.inputs[7])
  node_group.links.new(imagetexturenormal.outputs[0], mixcolor2.inputs[7])
  node_group.links.new(veronoiTexture.outputs[2], mixcolor3.inputs[6])
  #mix rgba output is 2 nto 0
  node_group.links.new(mixcolor3.outputs[2], pbsdf1.inputs[5])
  node_group.links.new(mixcolor3.outputs[2], pbsdf2.inputs[5])
  node_group.links.new(textureCoordinate.outputs[3], mapping.inputs[0])
  node_group.links.new(mapping.outputs[0], imagetexturenormal.inputs[0])
  node_group.links.new(valuescale.outputs[0], mapping.inputs[3])
  #Dfuse link
  node_group.links.new(mapping.outputs[0], imagetexturediffuse.inputs[0])
  node_group.links.new(imagetexturediffuse.outputs[0], mixcolor4.inputs[7])
  node_group.links.new(veronoiTexture.outputs[1], colorramp.inputs[0])
  node_group.links.new(colorramp.outputs[0], mixcolor4.inputs[6])
  node_group.links.new(mixcolor4.outputs[2], mixcolor5.inputs[0])
  node_group.links.new(mixcolor4.outputs[2], colorramp2.inputs[0])
  node_group.links.new(colorramp2.outputs[0], pbsdf1.inputs[2])
  node_group.links.new(colorramp2.outputs[0], pbsdf2.inputs[2])
  node_group.links.new(mixcolor5.outputs[2], pbsdf1.inputs[0])
  #node_group.links.new(mixcolor5.outputs[2], pbsdf2.inputs[0]) maybe cool effect mixing?
  node_group.links.new(mixcolor6.outputs[2], pbsdf2.inputs[1])
  node_group.links.new(mixcolor4.outputs[2], mixcolor6.inputs[0])


#if no painterlyMaterial is used
def mixnodesonrgb():
  morphMaterial = bpy.data.materials.get("MorphingMaterial")
  node_group = morphMaterial.node_tree
  
  pbsdf1 = node_group.nodes.get('pbsdf1')
  pbsdf2 = node_group.nodes.get('pbsdf2')
  mixcolor5 = node_group.nodes.new("ShaderNodeMix")
  mixcolor5.location = (-250, 800)
  mixcolor5.data_type = 'RGBA'
  mixcolor5.name = 'Mix5'
  mixcolor6 = node_group.nodes.new("ShaderNodeMix")
  mixcolor6.location = (-250, -800)
  mixcolor6.data_type = 'RGBA'
  mixcolor6.name = 'Mix6'
  node_group.links.new(mixcolor5.outputs[2], pbsdf1.inputs[0])
  #node_group.links.new(mixcolor5.outputs[2], pbsdf2.inputs[0]) maybe cool effect mixing with eachother?
  node_group.links.new(mixcolor6.outputs[2], pbsdf2.inputs[0])


#painterlyMaterial()
mixnodesonrgb()
#sets up the postion of the rgbs
for i in range(0,lengthOfObjects):
  if ramaining2 < 3:
    isLast = True
  else:
    isLast = False
  setupMorphingMaterial(i, objInfoPositionArray[i], repeats2, isLast)
  ramaining2 -= 1
animate_mixswitch_factor(random_times)
