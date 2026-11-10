
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Load Brad's photograph
photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

photo = Image.open(photo_path).convert("RGB")

# Twitter/X graphic dimensions
width, height = 1200, 675

# Create a full-bleed background from the photograph
background = photo.resize(
    (width, height),
    Image.Resampling.LANCZOS
)

# Blur background to fill empty space
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

# Center original photograph over blurred background
x = (width - foreground.width) // 2
y = (height - foreground.height) // 2

canvas.paste(foreground, (x, y))

# Draw loss counter
draw = ImageDraw.Draw(canvas)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 175)

number = "207"

# Calculate text dimensions, including outline
bounds = draw.textbbox(
    (0, 0),
    number,
    font=font,
    stroke_width=7
)

text_width = bounds[2] - bounds[0]
text_height = bounds[3] - bounds[1]

# Center number horizontally and position near bottom
text_x = (width - text_width) // 2 - bounds[0]
text_y = height - text_height - 35 - bounds[1]

# White text with thick black outline
draw.text(
    (text_x, text_y),
    number,
    font=font,
    fill="white",
    stroke_width=7,
    stroke_fill="black"
)

# Save final graphic
output_path = "test_graphic.png"

canvas.save(output_path, quality=95)

print(f"Graphic generated successfully: {output_path}")
print(f"Dimensions: {width} x {height}")
print(f"Loss counter: {number}")
