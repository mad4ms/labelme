import numpy as np
from skimage import measure
import json
from PIL import Image
import io
import base64
import glob


def img_arr_to_b64(img_arr):
    img_pil = Image.fromarray(img_arr)
    f = io.BytesIO()
    img_pil.save(f, format="PNG")
    img_bin = f.getvalue()
    if hasattr(base64, "encodebytes"):
        img_b64 = base64.encodebytes(img_bin).decode('utf-8')
    else:
        img_b64 = base64.encodestring(img_bin)
    return img_b64


path_images = "/home/madams/Pictures/colab_data/train/images/"
path_masks = "/home/madams/Pictures/colab_data/train/pixels/"

list_images = glob.glob(path_images + "*.png")
list_masks = glob.glob(path_masks + "*.png")

list_images.sort()
list_masks.sort()

# print(set(zip(list_images, list_masks)))

for name_image, name_mask in zip(list_images, list_masks):

    im = Image.open(name_image)
    mask = Image.open(name_mask)
    # file_name = "/home/madams/Pictures/colab_data/train/images/img_2.png"

    annotation = {
        "version": "4.5.7",
        "flags": {},
        "shapes": [],
        "imagePath": name_image,
        "imageData": img_arr_to_b64(np.asarray(im)),
        "imageHeight": im.height,
        "imageWidth": im.width
    }

    contours = measure.find_contours(np.asarray(mask), 0.5)
    # print("First: " + str(len(contours)))
    # contours = sorted(contours, key=len, reverse=True)[:1]
    # print("Second: " + str(len(contours)))
    for n, contour in enumerate(contours):
        coords = measure.approximate_polygon(contour, tolerance=3)[:-1]
        segmentation = np.flip(coords, axis=1).tolist()
        annotation["shapes"].append(
            {"label": "bottle", "points": segmentation, "group_id": 1, "shape_type": "polygon"})
        # annotation["shapes"][0]["points"] = segmentation

    file = name_image.replace(".png", ".json")
    with open(file, 'w') as outfile:
        json.dump(annotation, outfile, indent=2)
