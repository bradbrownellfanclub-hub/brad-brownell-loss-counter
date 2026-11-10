
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

width, height = 1200, 675

canvas = Image.new("RGB", (width, height), (245, 102, 0))

photo = Image.open(photo_path).convert("RGB")
portrait = ImageOps.fit(photo, (590, height))
canvas.paste(portrait, (0, 0))

draw = ImageDraw.Draw(canvas)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

title = ImageFont.truetype(font_path, 42)
number_font = ImageFont.truetype(font_path, 180)
subtitle = ImageFont.truetype(font_path, 34)

draw.text((620, 65), "CLEMSON BASKETBALL",
          font=title, fill="white")

number = "207"
bounds = draw.textbbox((0, 0), number, font=number_font)
number_width = bounds[2] - bounds[0]

draw.text((620 + (540 - number_width) / 2, 210),
          number, font=number_font, fill="white")

draw.text((645, 455), "CAREER LOSSES",
          font=subtitle, fill="white")

draw.text((645, 505), "AT CLEMSON",
          font=subtitle, fill="white")

canvas.save("test_graphic.png")

print("Graphic successfully created!")
