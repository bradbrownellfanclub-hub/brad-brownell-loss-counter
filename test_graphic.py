
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Load Brad's photograph
photo_path = Path("assets/brad.jpg")

if not photo_path.exists():
    raise FileNotFoundError("Missing assets/brad.jpg")

photo = Image.open(photo_path).convert("RGB")

# Portrait dimensions (4:5)
width, height = 1080, 1350

# Crop photograph to portrait ratio
original_width, original_height = photo.size

target_ratio = width / height
current_ratio = original_width / original_height

if current_ratio > target_ratio:
    # Image is too wide: crop from the right
    new_width = int(original_height * target_ratio)

    photo = photo.crop(
        (0, 0, new_width, original_height)
    )

else:
    # Image is too tall: crop from the bottom
    new_height = int(original_width / target_ratio)

    photo = photo.crop(
        (0, 0, original_width, new_height)
    )

# Resize cropped photograph to final dimensions
canvas = photo.resize(
    (width, height),
    Image.Resampling.LANCZOS
)

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

# Center number horizontally near bottom
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


