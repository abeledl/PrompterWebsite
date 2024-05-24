import cv2
import numpy as np

# Load the image
image = cv2.imread('C:\\Users\\abeld\\Pictures\\efai.jpg', cv2.IMREAD_GRAYSCALE)

# Create an empty matrix for the destination
depth_map = np.empty_like(image)

# Generate a simple depth map by normalizing the grayscale image
depth_map = cv2.normalize(image, depth_map, 0, 255, cv2.NORM_MINMAX)

# Save the depth map
cv2.imwrite('C:\\Users\\abeld\\Pictures\\depth_map.png', depth_map)

# Display the depth map
cv2.imshow('Depth Map', depth_map)
cv2.waitKey(0)
cv2.destroyAllWindows()