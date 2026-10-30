"""
Generates synthetic sample leaf images with realistic pathological patterns
for instant 1-click testing in the Streamlit UI.
"""

import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(SAMPLES_DIR, exist_ok=True)


def create_leaf_base(bg_color=(240, 245, 240), leaf_color=(45, 135, 55)):
    img = Image.new("RGB", (320, 320), bg_color)
    draw = ImageDraw.Draw(img)
    # Draw leaf shape
    leaf_poly = [
        (160, 30),
        (220, 70),
        (260, 130),
        (265, 200),
        (230, 260),
        (180, 280),
        (160, 290),
        (140, 280),
        (90, 260),
        (55, 200),
        (60, 130),
        (100, 70),
    ]
    draw.polygon(leaf_poly, fill=leaf_color, outline=(30, 90, 35))
    # Main vein
    draw.line([(160, 40), (160, 280)], fill=(75, 175, 75), width=3)
    # Lateral veins
    for y in range(80, 250, 35):
        draw.line([(160, y), (230, y - 20)], fill=(70, 160, 70), width=2)
        draw.line([(160, y), (90, y - 20)], fill=(70, 160, 70), width=2)
    return img


def generate_all_samples():
    # 1. Tomato Early Blight (Target board dark brown spots with yellow halo)
    img1 = create_leaf_base(leaf_color=(60, 140, 50))
    draw1 = ImageDraw.Draw(img1)
    # Concentric brown rings
    spots = [(140, 110, 25), (200, 180, 30), (110, 210, 20)]
    for sx, sy, r in spots:
        # Yellow chlorotic halo
        draw1.ellipse([sx - r - 8, sy - r - 8, sx + r + 8, sy + r + 8], fill=(185, 180, 45))
        # Concentric rings
        draw1.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(95, 55, 30))
        draw1.ellipse([sx - r + 5, sy - r + 5, sx + r - 5, sy + r - 5], fill=(65, 35, 20))
        draw1.ellipse([sx - r + 10, sy - r + 10, sx + r - 10, sy + r - 10], fill=(40, 20, 10))
    img1 = img1.filter(ImageFilter.GaussianBlur(1))
    img1.save(os.path.join(SAMPLES_DIR, "tomato_early_blight_sample.jpg"))

    # 2. Tomato Late Blight (Large dark brown water-soaked rotting lesions)
    img2 = create_leaf_base(leaf_color=(50, 120, 45))
    draw2 = ImageDraw.Draw(img2)
    # Large water-soaked lesions on edge
    draw2.ellipse([180, 70, 270, 170], fill=(55, 45, 35))
    draw2.ellipse([50, 150, 140, 240], fill=(45, 40, 30))
    draw2.ellipse([120, 190, 210, 280], fill=(35, 30, 25))
    img2 = img2.filter(ImageFilter.GaussianBlur(2))
    img2.save(os.path.join(SAMPLES_DIR, "tomato_late_blight_sample.jpg"))

    # 3. Tomato Healthy Leaf (Crisp green, no lesions)
    img3 = create_leaf_base(leaf_color=(40, 160, 50))
    img3.save(os.path.join(SAMPLES_DIR, "tomato_healthy_sample.jpg"))

    # 4. Cotton Bacterial Blight (Angular dark brown veins and lesions)
    img4 = create_leaf_base(leaf_color=(55, 145, 60))
    draw4 = ImageDraw.Draw(img4)
    angular_polys = [
        [(150, 120), (180, 110), (195, 140), (160, 145)],
        [(110, 160), (135, 150), (145, 180), (120, 190)],
        [(170, 190), (210, 180), (220, 215), (180, 220)],
    ]
    for poly in angular_polys:
        draw4.polygon(poly, fill=(50, 30, 15), outline=(170, 160, 40))
    img4 = img4.filter(ImageFilter.GaussianBlur(1))
    img4.save(os.path.join(SAMPLES_DIR, "cotton_bacterial_blight_sample.jpg"))

    # 5. Onion Purple Blotch (Elongated spindle lesion with purple center)
    img5 = Image.new("RGB", (320, 320), (245, 245, 245))
    draw5 = ImageDraw.Draw(img5)
    # Long onion blade
    draw5.polygon([(140, 20), (180, 20), (190, 300), (130, 300)], fill=(70, 150, 60))
    # Spindle purple blotch
    draw5.ellipse([140, 110, 180, 210], fill=(190, 180, 60))  # yellow halo
    draw5.ellipse([145, 125, 175, 195], fill=(110, 50, 80))  # purple zone
    draw5.ellipse([150, 140, 170, 180], fill=(60, 25, 45))   # necrotic center
    img5 = img5.filter(ImageFilter.GaussianBlur(1))
    img5.save(os.path.join(SAMPLES_DIR, "onion_purple_blotch_sample.jpg"))

    # 6. Uncertain / Blurry Sample (Low contrast, test <60% threshold)
    img6 = Image.new("RGB", (320, 320), (120, 130, 120))
    draw6 = ImageDraw.Draw(img6)
    draw6.ellipse([80, 80, 240, 240], fill=(130, 140, 120))
    img6 = img6.filter(ImageFilter.GaussianBlur(8))
    img6.save(os.path.join(SAMPLES_DIR, "uncertain_sample.jpg"))

    print(f"Generated 6 sample leaf images in {SAMPLES_DIR}")


if __name__ == "__main__":
    generate_all_samples()
