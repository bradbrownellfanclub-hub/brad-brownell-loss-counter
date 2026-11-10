
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

# Full-bleed photograph
width, height = 1200, 675

photo = Image.open(photo_path).convert("RGB")
canvas = ImageOps.fit(photo, (width, height))

draw = ImageDraw.Draw(canvas)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
number_font = ImageFont.truetype(font_path, 190)

number = "207"

# Center number horizontally near the bottom
bounds = draw.textbbox(
    (0, 0),
    number,
    font=number_font,
    stroke_width=9
)

text_width = bounds[2] - bounds[0]
text_height = bounds[3] - bounds[1]

x = (width - text_width) // 2 - bounds[0]
y = height - text_height - 45 - bounds[1]

draw.text(
    (x, y),
    number,
    font=number_font,
    fill="white",
    stroke_width=9,
    stroke_fill="black"
)

canvas.save("test_graphic.png", quality=95)

print("Minimal Brownell graphic generated!")
