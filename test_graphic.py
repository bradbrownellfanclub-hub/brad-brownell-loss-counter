
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

photo = Image.open(photo_path).convert("RGB")

# Preserve the entire photograph.
# Fit it inside the canvas without cropping.
width, height = 1200, 675

photo.thumbnail((width, height), Image.Resampling.LANCZOS)

canvas = Image.new("RGB", (width, height), "white")

x = (width - photo.width) // 2
y = (height - photo.height) // 2

canvas.paste(photo, (x, y))

draw = ImageDraw.Draw(canvas)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 175)

number = "207"

bounds = draw.textbbox((0, 0), number, font=font)
text_width = bounds[2] - bounds[0]
text_height = bounds[3] - bounds[1]

text_x = (width - text_width) // 2 - bounds[0]
text_y = height - text_height - 35 - bounds[1]

draw.text(
    (text_x, text_y),
    number,
    font=font,
    fill="black"
)

canvas.save("test_graphic.png", quality=95)

print("Graphic generated without cropping!")

