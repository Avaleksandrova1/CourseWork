import json
import numpy as np
import skimage
import tifffile
import os
import shutil


def create_mask(info, annotations, output_dir):
    """
    Создает маску сегментации на основе аннотаций для конкретного изображения.
    """

    mask_np = np.zeros((info['height'], info['width']), dtype=np.uint16)
    count = 1

    for ann in annotations:
        if ann['image_id'] == info['id']:
            # count += 1
            for seg in ann['segmentation']:
                rows, columns = skimage.draw.polygon(seg[1::2], seg[0::2], mask_np.shape)
                mask_np[rows, columns] = count
                count += 1

    mask_path = os.path.join(output_dir, info['file_name'].replace('.jpg', '_mask.tif'))
    tifffile.imwrite(mask_path, mask_np)
    print(f"Маска сохранена для {info['file_name']} в {mask_path}")


def main(json_file, mask_output_dir, image_output_dir, start_image_dir):
    with open(json_file, 'r') as f:
        data = json.load(f)

    images = data['images']
    annotations = data['annotations']

    if not os.path.exists(mask_output_dir):
        os.makedirs(mask_output_dir)
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)

    for img in images:
        create_mask(img, annotations, mask_output_dir)
        original_image_path = os.path.join(start_image_dir, img['file_name'])

        new_image_path = os.path.join(image_output_dir, os.path.basename(original_image_path))
        shutil.copy2(original_image_path, new_image_path)


        print(f"Скопировано изначальное изображение в {new_image_path}")


if __name__ == '__main__':
    start_images_dir = 'train_start'  # Путь к изначальным изображениям
    json_file = 'train_start/labels_my-project-name_2024-01-22-01-34-02.json'

    mask_output_dir = 'train/masks'
    image_output_dir = 'train/images'
    main(json_file, mask_output_dir, image_output_dir, start_images_dir)