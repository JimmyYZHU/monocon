import numpy as np 
import cv2


path = '/home/jimmy/ZY/Graduate_Courses/ROB535/proj/DevKit/KITTIDataset_new/testing/image_2/000203.png'
# Read the image
image = cv2.imread(path)

blurred_image = cv2.GaussianBlur(image, (9, 9), 0)

print(f"The size of the images: original:{image.shape}, new: {blurred_image.shape}")

# Display the original and blurred images (optional)
cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

