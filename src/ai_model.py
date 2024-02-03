import asyncio
import json
from PIL import Image, ImageDraw, ImageFont
from core.config.config import config
import requests
from base64 import b64encode


api_key = config.api_key.get_secret_value()


async def tob64(img):
    return str(b64encode(img))[2:-1]


async def toimg(filename):
    with open(filename, "rb") as file:
        return await tob64(file.read())


async def ai_swap_photo(user_id: str, image: str, target: str) -> bool:
    url = "https://api.segmind.com/v1/sd2.1-faceswapper"

    # Request payload
    data = {
        "input_face_image": await toimg(image),
        "target_face_image": await toimg(target),
        "file_type": "png",
        "face_restore": True
    }

    response = requests.post(url, json=data, headers={'x-api-key': api_key})
    print(f"Свап фото:{response.status_code}")
    with open(f'images/{user_id}_res.jpeg', 'wb') as file:
        file.write(response.content)

    return response.status_code == 200


async def ai_gen_photo(user_id: str, sex: str, prof: str) -> bool:
    url = "https://api.segmind.com/v1/sdxl1.0-txt2img"

    # Request payload
    with open("core/database/db_ai.json", "r") as json_file:
        data = json.load(json_file)

    response = requests.post(url, json=data[prof][sex], headers={'x-api-key': api_key})
    print(f"Генерация фото:{response.status_code}")
    with open(f'images/{user_id}_prof.jpeg', 'wb') as file:
        file.write(response.content)

    return response.status_code == 200


async def watermark_text(input_image_path: str,
                         output_image_path: str,
                         text: str):
    photo = Image.open(input_image_path)
    draw = ImageDraw.Draw(photo)

    icon = Image.open("images/icon.png")
    icon = icon.convert("RGBA")
    icon_with_alpha = Image.new("RGBA", icon.size)
    for x in range(icon.width):
        for y in range(icon.height):
            r, g, b, a = icon.getpixel((x, y))
            icon_with_alpha.putpixel((x, y), (r, g, b, a))

    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", 60)

    icon_width, icon_height = icon_with_alpha.size

    watermark_size = draw.textbbox((0, 0), text, font=font)
    watermark = Image.new("RGBA", watermark_size[2:], (0, 0, 0, 0))

    watermark_color = (255, 255, 255, 128)

    watermark_draw = ImageDraw.Draw(watermark)
    watermark_draw.text((0, 0), text, font=font, fill=watermark_color)

    icon_x = int((photo.width - (icon_width + watermark_size[2])) // 2)
    icon_y = int((photo.height - icon_height) // 2)
    c_x = int(icon_x + icon_width)
    c_y = int((photo.height - watermark_size[3]) // 2)

    photo.paste(icon_with_alpha, (icon_x, icon_y), mask=icon_with_alpha)
    photo.paste(watermark, (c_x, c_y), mask=watermark)

    # photo.show()
    photo.save(output_image_path)

# if __name__ == '__main__':
#     ai_gen_photo("701275421", "man", "Firefighter")
#     asyncio.run(ai_swap_photo("338928024", "images/338928024.jpeg", "images/338928024_prof.jpeg"))
# watermark_text("image_1.jpeg", "image_res.jpeg", text='HappyMom')

