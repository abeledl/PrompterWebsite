import bpy

# Original array of 2D coordinates
website_coordinates = [
    [255.04, 79.20], [403.50, 79.20], [623.44, 79.20], [219.69, 239.17], [374.74, 239.17], [630.02, 239.17],
    [474.99, 399.15], [160.24, 559.12], [414.54, 559.12], [729.30, 559.12], [258.28, 719.10], [462.97, 719.10],
    [679.69, 719.10], [474.99, 879.07], [342.11, 1039.05], [480.73, 1039.05], [613.61, 1039.05], [474.99, 1199.02],
    [383.81, 1359.00], [683.17, 1359.00], [474.97, 1518.97], [397.39, 1678.95], [689.42, 1678.95], [474.99, 1838.92],
    [428.14, 1998.90], [721.37, 1998.90], [474.97, 2158.87], [167.38, 2318.85], [394.12, 2318.85], [597.67, 2318.85],
    [815.16, 2318.85], [474.99, 2478.82], [474.99, 2638.80], [126.38, 2798.77], [352.80, 2798.77], [701.42, 2798.77],
    [270.64, 2958.75], [669.15, 2958.75], [474.99, 3118.72], [132.62, 3278.70], [266.47, 3278.70], [608.83, 3278.70],
    [191.08, 3438.67], [408.66, 3438.67], [692.57, 3438.67], [474.99, 3598.65], [349.05, 3758.62], [560.38, 3758.62],
    [205.16, 3918.60], [399.41, 3918.60], [669.22, 3918.60]
]

# Scaling factor
scale_factor = 0.02

# Scaling and shifting the coordinates
coordinates_2d = [(x * scale_factor, y * (scale_factor + 0.005)) for x, y in website_coordinates]
coordinates_2d = [(x, y + 2.6) for x, y in coordinates_2d]

# Adding the default z-coordinate of 0
coordinates_3d = [list(coord) + [0] for coord in coordinates_2d]
print(coordinates_3d)

# Create a new mesh and object
mesh = bpy.data.meshes.new(name="CoordinatesMesh")
obj = bpy.data.objects.new(name="CoordinatesPlane", object_data=mesh)

# Link the object to the scene collection
bpy.context.collection.objects.link(obj)

# Create vertices at the given coordinates
mesh.from_pydata(coordinates_3d, [], [])

# Update the mesh with new data
mesh.update()
