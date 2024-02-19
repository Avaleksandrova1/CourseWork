import cv2
import numpy as np

map_image = cv2.imread("img_2.jpg")
clicked_points = []
# height, width = map_image.shape[:2]
print("\n*･゜ﾟ･*:.｡..｡.:*･'(*ﾟ▽ﾟ*)'･*:.｡. .｡.:*･゜ﾟ･*")
print("Управление:")
print("  - Щелкните мышью на изображении, чтобы выбрать точку.")
print("  - Нажмите 'r', чтобы отменить последнюю выбранную точку.")
print("  - Нажмите 'n', чтобы начать выбор точек заново.")
print("  - Нажмите 'e', чтобы завершить выбор точек и ввести географические координаты.")
print("*･゜ﾟ･*:.｡..｡.:*･'(*ﾟ▽ﾟ*)'･*:.｡. .｡.:*･゜ﾟ･*\n")


def click(event, x, y, fl, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        cv2.circle(map_image, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(map_image, str(len(clicked_points)), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 0), 2)
        cv2.imshow("Map", map_image)


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


# top_left_pixel = (0, 0)
# top_right_pixel = (width, 0)
# bottom_left_pixel = (0, height)
# bottom_right_pixel = (width, height)

# known_pixel_coords = {
#     "point1": top_left_pixel,
#     "point2": top_right_pixel,
#     "point3": bottom_left_pixel,
#     "point4": bottom_right_pixel
# }


known_geo_coords = {}

cv2.imshow("Map", map_image)
cv2.setMouseCallback("Map", click)

while True:
    key = cv2.waitKey(1)
    key &= 0xFF ## для надежности берем последние 8 бит
    if key == ord("e"):
        if len(clicked_points) < 4:
            print("Необходимо выбрать ровно 4 точки на изображении.")

            # Очистка изображения и списка точек для повторного выбора
            map_image = cv2.imread("img_2.jpg")
            cv2.imshow("Map", map_image)
            clicked_points = []
        else:
            break

    elif key == ord("r"):
        if clicked_points:
            clicked_points.pop()
            map_image = cv2.imread("img_2.jpg")  # сброс изображения
            for i, point in enumerate(clicked_points, 1):
                cv2.circle(map_image, point, 5, (0, 0, 255), -1)
                cv2.putText(map_image, str(i), (point[0] - 10, point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 0), 2)
            cv2.imshow("Map", map_image)

    elif key == ord("n"):
        map_image = cv2.imread("img_2.jpg")
        cv2.imshow("Map", map_image)
        clicked_points = []

if len(clicked_points) >= 4:
    known_geo_coords = {}
    for i, point in enumerate(clicked_points):
        while True:
            lat = input(f"Введите широту для точки {i + 1}: ")
            lon = input(f"Введите долготу для точки {i + 1}: ")

            try:
                lat = float(lat)
                lon = float(lon)
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    known_geo_coords[f"point{i + 1}"] = (lat, lon)
                    break
                else:
                    print("Широта должна быть в диапазоне [-90.0, 90.0], а долгота - в диапазоне [-180.0, 180.0].")
            except ValueError:
                print("Введите числовое значение для широты и долготы.")

    object_x, object_y = 215, 631

    known_pixel_coords = dict(enumerate(clicked_points, 1))
    transform_matrix = compute_transform(known_pixel_coords, known_geo_coords)
    object_geo_coords = compute_geo_coords(object_x, object_y, transform_matrix)
    print("Географические координаты объекта:", object_geo_coords)

cv2.destroyAllWindows()
