import numpy as np
import bpy
import math

namesOfObjects = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']

bpy.data.objects["morph"].select_set(True)
morphing_obj = bpy.data.objects["morph"]
node_modifier = morphing_obj.modifiers.get("morphgeo")
node_group = node_modifier.node_group

def createGroupGeoTop1GeoTop2Switch():
  geometryNodeObjectInfo1 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo1.location = (-900, 600)
  geometryNodeObjectInfo1.name = "Object Info.004"
  geometryNodeObjectInfo1.label = "Object Info.004"
  geometryNodeObjectInfo1.inputs[0].default_value = bpy.data.objects["Cube"]
  geometryNodeObjectInfo1.transform_space = 'RELATIVE'


  geometryNodeObjectInfo2 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo2.location = (-900, 600)
  geometryNodeObjectInfo2.name = "Object Info.005"
  geometryNodeObjectInfo2.label = "Object Info.005"
  geometryNodeObjectInfo2.inputs[0].default_value = bpy.data.objects["Cone"]
  geometryNodeObjectInfo2.transform_space = 'RELATIVE'


  switchNext = node_group.nodes.new("GeometryNodeSwitch")
  switchNext.location = (-135 * 7.8, 200 * 5.5)


  node_group.links.new(geometryNodeObjectInfo1.outputs[3], switchNext.inputs[1])
  node_group.links.new(geometryNodeObjectInfo2.outputs[3], switchNext.inputs[2])

  node_group.links.new(switchNext.outputs[0], switchNext.inputs[1])


#second  ###############
def createGroupGeoBottom1GeoBottom2Switch():
  geometryNodeObjectInfo3 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo3.location = (-135 * 9, 200 * -7)
  geometryNodeObjectInfo3.name = "Object Info.006"
  geometryNodeObjectInfo3.label = "Object Info.006"
  geometryNodeObjectInfo3.inputs[0].default_value = bpy.data.objects["Cube"]
  geometryNodeObjectInfo3.transform_space = 'RELATIVE'


  geometryNodeObjectInfo4 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo4.location = (-135 * 9, 200 * -8)
  geometryNodeObjectInfo4.name = "Object Info.007"
  geometryNodeObjectInfo4.label = "Object Info.007"
  geometryNodeObjectInfo4.inputs[0].default_value = bpy.data.objects["Cone"]
  geometryNodeObjectInfo4.transform_space = 'RELATIVE'


  switchNodeBottomFinal = node_group.nodes.new("GeometryNodeSwitch")
  switchNodeBottomFinal.location = (-135 * 7.8, 200 * -7.5)


  node_group.links.new(geometryNodeObjectInfo3.outputs[3], switchNodeBottomFinal.inputs[1])
  node_group.links.new(geometryNodeObjectInfo4.outputs[3], switchNodeBottomFinal.inputs[2])


  correctsdf2 = node_group.nodes.get('correctsdf2')
  growth2 = node_group.nodes.get('growth2')
  joinGeometry = node_group.nodes.get('Join Geometry')

  node_group.links.new(switchNodeBottomFinal.outputs[0], correctsdf2.inputs[0])
  node_group.links.new(switchNodeBottomFinal.outputs[0], growth2.inputs[0])
  node_group.links.new(switchNodeBottomFinal.outputs[0], joinGeometry.inputs[0])

def createGroupGeoTop1GeoTop2SwitchFinal():
  geometryNodeObjectInfo1 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo1.location = (-135 * 9, 200 * 6)
  geometryNodeObjectInfo1.name = "Object Info.004"
  geometryNodeObjectInfo1.label = "Object Info.004"
  geometryNodeObjectInfo1.inputs[0].default_value = bpy.data.objects["Cube"]
  geometryNodeObjectInfo1.transform_space = 'RELATIVE'


  geometryNodeObjectInfo2 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo2.location = (-135 * 9, 200 * 5)
  geometryNodeObjectInfo2.name = "Object Info.005"
  geometryNodeObjectInfo2.label = "Object Info.005"
  geometryNodeObjectInfo2.inputs[0].default_value = bpy.data.objects["Cone"]
  geometryNodeObjectInfo2.transform_space = 'RELATIVE'


  switchNodeTopFinal = node_group.nodes.new("GeometryNodeSwitch")
  switchNodeTopFinal.location = (-135 * 7.8, 200 * 5.5)


  node_group.links.new(geometryNodeObjectInfo1.outputs[3], switchNodeTopFinal.inputs[1])
  node_group.links.new(geometryNodeObjectInfo2.outputs[3], switchNodeTopFinal.inputs[2])


  correctsdf1 = node_group.nodes.get('correctsdf1')
  growth1 = node_group.nodes.get('growth1')
  joinGeometry = node_group.nodes.get('Join Geometry')

  node_group.links.new(switchNodeTopFinal.outputs[0], correctsdf1.inputs[0])
  node_group.links.new(switchNodeTopFinal.outputs[0], growth1.inputs[0])
  node_group.links.new(switchNodeTopFinal.outputs[0], joinGeometry.inputs[0])

def createGroupGeoBottom1GeoBottom2Switch():
  geometryNodeObjectInfo3 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo3.location = (-135 * 9, 200 * -7)
  geometryNodeObjectInfo3.name = "Object Info.006"
  geometryNodeObjectInfo3.label = "Object Info.006"
  geometryNodeObjectInfo3.inputs[0].default_value = bpy.data.objects["Cube"]
  geometryNodeObjectInfo3.transform_space = 'RELATIVE'


  geometryNodeObjectInfo4 = node_group.nodes.new("GeometryNodeObjectInfo")
  geometryNodeObjectInfo4.location = (-135 * 9, 200 * -8)
  geometryNodeObjectInfo4.name = "Object Info.007"
  geometryNodeObjectInfo4.label = "Object Info.007"
  geometryNodeObjectInfo4.inputs[0].default_value = bpy.data.objects["Cone"]
  geometryNodeObjectInfo4.transform_space = 'RELATIVE'


  switchNodeBottomFinal = node_group.nodes.new("GeometryNodeSwitch")
  switchNodeBottomFinal.location = (-135 * 7.8, 200 * -7.5)


  node_group.links.new(geometryNodeObjectInfo3.outputs[3], switchNodeBottomFinal.inputs[1])
  node_group.links.new(geometryNodeObjectInfo4.outputs[3], switchNodeBottomFinal.inputs[2])


  correctsdf2 = node_group.nodes.get('correctsdf2')
  growth2 = node_group.nodes.get('growth2')
  joinGeometry = node_group.nodes.get('Join Geometry')

  node_group.links.new(switchNodeBottomFinal.outputs[0], correctsdf2.inputs[0])
  node_group.links.new(switchNodeBottomFinal.outputs[0], growth2.inputs[0])
  node_group.links.new(switchNodeBottomFinal.outputs[0], joinGeometry.inputs[0])
