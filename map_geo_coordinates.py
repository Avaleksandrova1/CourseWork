### Пока наброски

import cv2
import numpy as np




map_image = cv2.imread("first_test.jpg")
gray_image = cv2.cvtColor(map_image, cv2.COLOR_BGR2GRAY)
dst = cv2.cornerHarris(gray_image, blockSize=2, ksize=3, k=0.04)


dst_norm = cv2.normalize(dst, None, 0, 255, cv2.NORM_MINMAX)
thresh = 0.01 * dst_norm.max()
corner_image = np.copy(map_image)
corner_image[dst_norm > thresh] = [0, 0, 255]  # Красный цвет для углов
cv2.imshow("Corner Points", corner_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


corner_coords = np.column_stack(np.where(dst > thresh))
print("Найденные пиксельные координаты угловых точек:")
for coord in corner_coords:
    print(coord)


# known_geo_coords = {
#     "point1": (lat1, lon1),
#     "point2": (lat2, lon2)
# }


known_pixel_coords = {
    "point1": (corner_coords[0, 1], corner_coords[0, 0]),
    "point2": (corner_coords[1, 1], corner_coords[1, 0])
}


def compute_transform(pixel_coords, geo_coords):
    pixel_points = np.float32(list(pixel_coords.values())).reshape(-1, 1, 2)
    geo_points = np.float32(list(geo_coords.values())).reshape(-1, 1, 2)
    M = cv2.getAffineTransform(pixel_points, geo_points)
    return M


def compute_geo_coords(object_x, object_y, transform_matrix):
    object_pixel_coords = np.array([[[object_x, object_y]]], dtype=np.float32)
    geo_coords = cv2.transform(object_pixel_coords, transform_matrix)
    return geo_coords[0][0]


# transform_matrix = compute_transform(known_pixel_coords, known_geo_coords)
# object_x, object_y = 2200, 20000
# object_geo_coords = compute_geo_coords(object_x, object_y, transform_matrix)

# Примерно
object_x, object_y = corner_coords[2, 1], corner_coords[2, 0]
object_geo_coords = compute_geo_coords(object_x, object_y, compute_transform(known_pixel_coords, known_geo_coords))
print("Географические координаты объекта:", object_geo_coords)

