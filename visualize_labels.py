import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2


def strusture_annotations(data, indent=0):
    """
    Выводит структуру вложенных данных в виде дерева.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            print('      ' * indent + str(key))
            strusture_annotations(value, indent + 1)

    elif isinstance(data, list):
        print('      ' * indent + "[Список длиной {}, содержащий:]".format(len(data)))
        if data:
            strusture_annotations(data[0], indent + 1)


def load_coco_annotations(file_path):
    """
    Загружает аннотации из json файла.
    :param file_path: Путь к файлу с аннотациями coco.
    :return: Аннотации в формате словаря
    """
    with open(file_path, 'r') as f:
        annotations = json.load(f)
    return annotations


def get_image_files(dir, annotations):
    """
    Получаем все файлы из директории на основе аннотаций.
    """
    image_files = [os.path.join(dir, images['file_name']) for images in annotations['images']]
    return image_files


def display_bbox(ax, bbox, color):
    """
    Отображает ограничивающий прямугольник на указанной оси.
    """
    rectangle = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1, edgecolor=color, facecolor='none')
    ax.add_patch(rectangle)


def display_segmentation(ax, seg, color):
    """
    Отображает полигон сегментации.
    """
    for s in seg:
        poly = [(s[i], s[i + 1]) for i in range(0, len(s), 2)]
        ax.add_patch(patches.Polygon(poly, closed=True, edgecolor=color, fill=False))


def visualize_annotations(image_paths, coco_annotations, display_type='both', colors=plt.cm.tab10):
    """
    Визуализирует изображения с аннотациями.
    :param image_paths: Список путей к изображениям.
    :param coco_annotations: Аннотации.
    :param display_type: Тип отображения. Может быть ограничивающий прямоугольник, полигоны сегментаци и оба.
    :param colors: Цвета для отображения.
    """
    num_images = len(image_paths)
    num_cols = 1
    num_rows = (num_images + num_cols - 1) // num_cols
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(10, 5 * num_rows))

    for ax, path in zip(axs.ravel(), image_paths[:3]):
        image = cv2.imread(path)
        ax.imshow(image)
        ax.axis('off')
        img_id = next(item for item in coco_annotations['images'] if item['file_name'] == os.path.basename(path))['id']

        # Фильтрация аннотаций для текущего изображения
        img_annotations = [ann for ann in coco_annotations['annotations'] if ann['image_id'] == img_id]

        for ann in img_annotations:
            category_id = ann['category_id']
            color = colors(category_id % 10)

            if display_type in ['bbox', 'both']:
                display_bbox(ax, ann['bbox'], color)

            if display_type in ['seg', 'both']:
                display_segmentation(ax, ann['segmentation'], color)

    plt.tight_layout()
    plt.show()


#
# with open('train_start/labels_my-project-name_2024-01-22-01-34-02.json', 'r') as file:
#     data = json.load(file)
#
# for i in data['images'][:3]:
#     print(i['file_name'])
#
# strusture_annotations(data)


annotations_path = 'train_start/labels_my-project-name_2024-01-22-01-34-02.json'
directory = "train_start/"
coco_annotations = load_coco_annotations(annotations_path)
display_type = 'seg'
visualize_annotations(get_image_files(directory, coco_annotations), coco_annotations, display_type)
