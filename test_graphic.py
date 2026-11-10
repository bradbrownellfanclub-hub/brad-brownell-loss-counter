
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

photo = Image.open(photo_path).convert("RGB")

width, height = 1200, 675

# Create a full-bleed background using the photograph
background = photo.resize(
    (width, height),
    Image.Resampling.LANCZOS
)

background = background.filter(
    ImageFilter.GaussianBlur(radius=30)
)

# Darken background slightly
background = ImageEnhance.Brightness(background).enhance(0.65)

canvas = background.copy()

# Preserve the entire original photograph
foreground = photo.copy()
foreground.thumbnail(
    (width, height),
    Image.Resampling.LANCZOS
)

# Center photograph over blurred background
x = (width - foreground.width) // 2
y = (height - foreground.height) // 2

canvas.paste(foreground, (x, y))

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

canvas.save("test_graphic.png")

print("Full-bleed graphic generated!")
