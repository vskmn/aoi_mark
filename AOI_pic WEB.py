import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math

def add_watermark(image, text, font_path="arial.ttf", font_size=80, angle=45, opacity=100):
    # แปลงภาพเป็น RGBA
    image = image.convert("RGBA")

    # สร้างเลเยอร์สำหรับลายน้ำ (โปร่งใส)
    txt_layer = Image.new("RGBA", image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)

    # โหลดฟอนต์
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # ขนาดของข้อความลายน้ำ
    bbox = draw.textbbox((0,0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # สร้างภาพข้อความลายน้ำแยก (เพื่อหมุน)
    text_img = Image.new("RGBA", (text_width, text_height), (255,255,255,0))
    text_draw = ImageDraw.Draw(text_img)
    # ใส่ข้อความด้วยความโปร่งใส (opacity)
    text_draw.text((0,0), text, font=font, fill=(255,255,255,opacity))

    # หมุนข้อความ
    rotated_text = text_img.rotate(angle, expand=1)

    # ตำแหน่งให้อยู่กลางภาพ
    x = (image.width - rotated_text.width) // 2
    y = (image.height - rotated_text.height) // 2

    # วางลายน้ำลงบนเลเยอร์ txt_layer
    txt_layer.paste(rotated_text, (x, y), rotated_text)

    # ผสานเลเยอร์ลายน้ำกับภาพหลัก
    watermarked = Image.alpha_composite(image, txt_layer).convert("RGB")

    return watermarked

st.title("Watermark Your JPG Files (Rotated Centered)")

uploaded_files = st.file_uploader("Upload JPG files", accept_multiple_files=True, type=['jpg', 'jpeg'])

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        filename = uploaded_file.name
        watermark_text = filename.rsplit('.', 1)[0]

        watermarked_image = add_watermark(image, watermark_text, font_size=80, angle=45, opacity=120)

        st.image(watermarked_image, caption=f"Watermarked: {filename}")

        buf = io.BytesIO()
        watermarked_image.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        st.download_button(label=f"Download {filename}", data=byte_im, file_name=filename, mime="image/jpeg")
