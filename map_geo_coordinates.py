import cv2
import numpy as np

# map_image = cv2.imread("img_1.jpg")
# height, width = map_image.shape[:2]
#
# top_left_pixel = (0, 0)
# top_right_pixel = (width, 0)
# bottom_left_pixel = (0, height)
# bottom_right_pixel = (width, height)
#
# known_pixel_coords = {
#     "point1": top_left_pixel,
#     "point2": top_right_pixel,
#     "point3": bottom_left_pixel,
#     "point4": bottom_right_pixel
# }
#
# lat1, lon1 = 55.741881, 37.518982
# lat2, lon2 = 55.741981, 37.543380
# lat3, lon3 = 55.736706, 37.519407
# lat4, lon4 = 55.736807, 37.543134
#
# known_geo_coords = {
#     "point1": (lat1, lon1),
#     "point2": (lat2, lon2),
#     "point3": (lat3, lon3),
#     "point4": (lat4, lon4)
# }
#
#
# known_geo_coords = {
#     "point1": (lat1, lon1),
#     "point2": (lat2, lon2),
#     "point3": (lat3, lon3),
#     "point4": (lat4, lon4)
# }
#
# object_x, object_y = 626, 193

### Второе фото (больший шасштаб)

map_image = cv2.imread("img_2.jpg")
height, width = map_image.shape[:2]

top_left_pixel = (0, 0)
top_right_pixel = (width, 0)
bottom_left_pixel = (0, height)
bottom_right_pixel = (width, height)

known_pixel_coords = {
    "point1": top_left_pixel,
    "point2": top_right_pixel,
    "point3": bottom_left_pixel,
    "point4": bottom_right_pixel
}

lat1_2, lon1_2 = 55.746306, 37.503560
lat2_2, lon2_2 = 55.746251, 37.558414
lat3_2, lon3_2 = 55.728336, 37.504043
lat4_2, lon4_2 = 55.728418, 37.559138

known_geo_coords = {
    "point1": (lat1_2, lon1_2),
    "point2": (lat2_2, lon2_2),
    "point3": (lat3_2, lon3_2),
    "point4": (lat4_2, lon4_2)
}

object_x, object_y = 215, 631


# Функция для вычисления матрицы преобразования
def compute_transform(pixel_coords, geo_coords):
    pixel_points = np.float32(list(pixel_coords.values())).reshape(-1, 1, 2)
    geo_points = np.float32(list(geo_coords.values())).reshape(-1, 1, 2)
    M, _ = cv2.findHomography(pixel_points, geo_points, cv2.RANSAC)
    return M

# Функция для вычисления географических координат объекта
def compute_geo_coords(object_x, object_y, transform_matrix):
    object_pixel_coords = np.array([[[object_x, object_y]]], dtype=np.float32)
    geo_coords = cv2.perspectiveTransform(object_pixel_coords, transform_matrix)
    return geo_coords[0][0]


transform_matrix = compute_transform(known_pixel_coords, known_geo_coords)
object_geo_coords = compute_geo_coords(object_x, object_y, transform_matrix)
print("Географические координаты объекта:", object_geo_coords)
