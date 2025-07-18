import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import zipfile

def strip_extensions(filename, exts=['.jpg', '.jpeg', '.png']):
    fname = filename.lower()
    while True:
        for ext in exts:
            if fname.endswith(ext):
                fname = fname[:-len(ext)]
                break
        else:
            break
    return fname

def add_watermark(image: Image.Image, text: str, font_path="arial.ttf", font_size=80, angle=45, opacity=200) -> Image.Image:
    image = image.convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    extra_height = int(text_height * 0.3)
    text_img = Image.new("RGBA", (text_width, text_height + extra_height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)
    fill_color = (255, 255, 255, opacity)
    text_draw.text((0, 0), text, font=font, fill=fill_color)

    rotated_text = text_img.rotate(angle, expand=1)

    x = (image.width - rotated_text.width) // 2
    y = (image.height - rotated_text.height) // 2

    txt_layer.paste(rotated_text, (x, y), rotated_text)
    watermarked = Image.alpha_composite(image, txt_layer).convert("RGB")
    return watermarked

def main():
    st.title("Watermark Your Images and Download ZIP")

    uploaded_files = st.file_uploader(
        "Upload JPG, JPEG, or PNG files", 
        accept_multiple_files=True, 
        type=['jpg', 'jpeg', 'png']
    )

    if uploaded_files:
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        output_zip = io.BytesIO()
        with zipfile.ZipFile(output_zip, mode="w") as zf:
            for uploaded_file in uploaded_files:
                img_bytes = uploaded_file.read()
                img = Image.open(io.BytesIO(img_bytes))

                filename = os.path.basename(uploaded_file.name)
                base_name = strip_extensions(filename)

                watermarked_img = add_watermark(img, base_name, font_size=80, angle=45, opacity=200)

                # Save watermarked image to output folder on disk
                save_path = os.path.join(output_folder, f"{base_name}_watermarked.jpg")
                watermarked_img.save(save_path, format="JPEG")

                # Add watermarked image to zip file
                img_buffer = io.BytesIO()
                watermarked_img.save(img_buffer, format="JPEG")
                img_buffer.seek(0)
                zip_filename = f"{base_name}_watermarked.jpg"
                zf.writestr(zip_filename, img_buffer.read())

                st.image(watermarked_img, caption=f"Watermarked: {base_name}", use_container_width=True)

        output_zip.seek(0)
        st.download_button(
            label="Download All Watermarked Images as ZIP",
            data=output_zip,
            file_name="watermarked_images.zip",
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
