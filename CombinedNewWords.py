import numpy as np
import bpy
import math

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
  print(namesOfObjectsNumbered)
else:
  print("Collection named 'alphabet' does not exist.")



bpy.data.objects["morph"].select_set(True)
morphing_obj = bpy.data.objects["morph"]
node_modifier = morphing_obj.modifiers.get("morphgeo")
node_group = node_modifier.node_group

class Repeats:
  top_repeats = False
  bot_repeats = False

def createGroupGeoTop1GeoTop2Switch(currentIndex, currentPosition, repeats):
  geometryNodeObjectInfo = node_group.nodes.new("GeometryNodeObjectInfo")
  nameOfObjInfo = 'ObjectInfo'
  geometryNodeObjectInfo.name = f'{nameOfObjInfo}{currentIndex}'  
  geometryNodeObjectInfo.label = f'{nameOfObjInfo}{currentIndex}'
  geometryNodeObjectInfo.inputs[0].default_value = bpy.data.objects[namesOfObjectsNumbered[currentIndex][1]]
  geometryNodeObjectInfo.transform_space = 'RELATIVE'
  if currentIndex > 4:
      repeats.top_repeats = True
      repeats.bot_repeats = True
  if currentIndex % 2 == 0:
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


  if (currentIndex > 1 and currentIndex < 5 ): # two obj info haave been created
    if currentIndex % 2 == 0:
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8) -10, 200 * (5.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousObjInfo = node_group.nodes.get(f"ObjectInfo{currentIndex - 2}")
        node_group.links.new(previousObjInfo.outputs[3], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
    else:
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8) -10, -200 * (4.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousObjInfo = node_group.nodes.get(f"ObjectInfo{currentIndex - 2}")
        node_group.links.new(previousObjInfo.outputs[3], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
  if (currentIndex > 4):
    if currentIndex % 2 == 0:
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8)-10, 200 * (5.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousSwitchInfo = node_group.nodes.get(f"Switch{currentIndex - 2}")
        node_group.links.new(previousSwitchInfo.outputs[0], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])
    else:
        switchNext = node_group.nodes.new("GeometryNodeSwitch")
        switchNext.location = (-150 * (currentPosition + 7.8) -10, -200 * (4.5))
        nameOfSwitch = 'Switch'
        switchNext.name = f'{nameOfSwitch}{currentIndex}'
        previousSwitchInfo = node_group.nodes.get(f"Switch{currentIndex - 2}")
        node_group.links.new(previousSwitchInfo.outputs[0], switchNext.inputs[1])
        node_group.links.new(geometryNodeObjectInfo.outputs[3], switchNext.inputs[2])




lengthOfObjects = len(namesOfObjectsNumbered)
def isEven(number):
  return number % 2 == 0

def isOdd(number):
  return number % 2 != 0

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
print (objInfoPositionArray) 
repeats = Repeats()
for i in range(0, len(namesOfObjectsNumbered)):
  createGroupGeoTop1GeoTop2Switch(i, objInfoPositionArray[i], repeats)
