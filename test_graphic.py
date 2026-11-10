
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Load Brad's photograph
photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

photo = Image.open(photo_path).convert("RGB")

# Portrait graphic dimensions (4:5)
width, height = 1080, 1350

# Create full-size blurred background
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

# Preserve entire original photograph
foreground = photo.copy()

foreground.thumbnail(
    (width, height),
    Image.Resampling.LANCZOS
)

# Center original photograph
x = (width - foreground.width) // 2
y = (height - foreground.height) // 2

canvas.paste(foreground, (x, y))

# Draw loss counter
draw = ImageDraw.Draw(canvas)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 175)

number = "207"

# Calculate text dimensions
bounds = draw.textbbox(
    (0, 0),
    number,
    font=font,
    stroke_width=7
)

text_width = bounds[2] - bounds[0]
text_height = bounds[3] - bounds[1]

# Center horizontally, position near bottom
text_x = (width - text_width) // 2 - bounds[0]
text_y = height - text_height - 65 - bounds[1]

# White text with thick black outline
draw.text(
    (text_x, text_y),
    number,
    font=font,
    fill="white",
    stroke_width=7,
    stroke_fill="black"
)

# Save graphic
output_path = "test_graphic.png"

canvas.save(output_path)

print("Portrait graphic generated successfully!")
print(f"Dimensions: {width} x {height}")
print(f"Loss counter: {number}")


