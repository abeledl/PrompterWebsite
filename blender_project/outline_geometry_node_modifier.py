import bpy


def create_geometry_node_outline():
    _outline_material = bpy.data.materials.new(name="OutlineMaterial_2")
    _outline_material.use_nodes = True
    _outline_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 0, 1)  # color
    _outline_material.use_backface_culling = True
    _outline_material.shadow_method = 'NONE'
    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(2.8, -1.5, 1.8), scale=(1, 1, 1))
    outline_obj = bpy.context.active_object
    outline_obj.name = "outline_obj"

    # Make the object the active one
    bpy.context.view_layer.objects.active = outline_obj
    # Add a Geometry Nodes modifier to the cube
    outline_obj.modifiers.new(name="NodesModifier", type='NODES')
    outline_obj.modifiers[-1].name = "outline_geo"
    outline_obj.modifiers[0].name = "outline_geo"
    node_modifier = outline_obj.modifiers.get("outline_geo")
    bpy.ops.node.new_geometry_node_group_assign()

    # Get the node group of the Geometry Nodes modifier
    node_group = node_modifier.node_group
    node_group.name = "efai_sad"

    # Clear existing nodes
    for _node in node_group.nodes:
        node_group.nodes.remove(_node)

    # Create Group Input and Group Output nodes
    group_input = node_group.nodes.new('NodeGroupInput')
    group_input.location = (-200, 0)
    group_output = node_group.nodes.new('NodeGroupOutput')
    group_output.location = (200, 0)

    join_geometry_node = node_group.nodes.new('GeometryNodeJoinGeometry')
    join_geometry_node.location = (0, 0)
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

    node_group.links.new(group_input.outputs[0], join_geometry_node.inputs[0])
    node_group.links.new(group_input.outputs[0], set_position_node.inputs[0])
    node_group.links.new(vector_math.outputs[0], set_position_node.inputs[3])
    node_group.links.new(normal_vector.outputs[0], vector_math.inputs[0])
    node_group.links.new(set_position_node.outputs[0], flip_faces_node.inputs[0])
    node_group.links.new(join_geometry_node.outputs[0], group_output.inputs[0])
    node_group.links.new(flip_faces_node.outputs[0], set_material.inputs[0])
    node_group.links.new(set_material.outputs[0], join_geometry_node.inputs[0])
    return outline_obj
