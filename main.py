import colorsys
from PIL import Image, ImageChops
import requests
import io

img_old = None
old_max_pixel_v = 0


def rgb_to_hsv(rgb_triplet):
    (r, g, b) = (rgb_triplet[0], rgb_triplet[1], rgb_triplet[2])
    (r, g, b) = (r / 255, g / 255, b / 255)
    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    (h, s, v) = (int(h * 359), int(s * 100), int(v * 100))
    hsv_triplet = (h, s, v)
    return hsv_triplet


def hsv_to_v(hsv_triplet):
    v = hsv_triplet[2]
    return v


def get_color_name(hsv_triplet):
    hue_val = hsv_triplet[0]
    color_list_num = [0, 60, 120, 240]
    color_list_name = ["red", "yellow", "green", "blue"]
    difference = min(color_list_num, key=lambda x: abs(x - hue_val))
    difference_id = color_list_num.index(difference)
    color = color_list_name[difference_id]
    return color


while True:

    response = requests.get('http://192.168.21.188:8081/0/current')
    response.raise_for_status()
    img_new = Image.open(io.BytesIO(response.content))
    img_new = img_new.resize((32, 32), resample=Image.Resampling.BILINEAR)
    img_new_pixel_list = list(img_new.getdata())

    if img_old is not None:

        diff = ImageChops.difference(img_new, img_old)
        diff_pixel_list = list(diff.getdata())
        # print(diff_pixel_list)
        # diff.show()
        diff_pixel_list_hsv = list(map(rgb_to_hsv, diff_pixel_list))
        # print(diff_pixel_list_hsv)
        v_list = list(map(hsv_to_v, diff_pixel_list_hsv))
        new_max_pixel_v = max(v_list)
        # print(new_max_pixel_v)

        # print(new_max_pixel_v)

        if new_max_pixel_v >= 10:

            position = v_list.index(new_max_pixel_v)
            pixel_new = rgb_to_hsv(img_new_pixel_list[position])

            if pixel_new[1] > 50:
                # print(diff_pixel_list_hsv[position])
                print(pixel_new)

                print(get_color_name(pixel_new))
                # if get_color_name(rgb_to_hsv(pixel_new)) == "yellow":
                    # diff.show()
    img_old = img_new
