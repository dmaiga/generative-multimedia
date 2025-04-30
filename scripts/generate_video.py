import os
import sys
from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip
)
import moviepy.config as mpy_config
from PIL import Image
import numpy as np

mpy_config.change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"})

# 📁 Dossiers
IMG_DIR = "data/images"
AUDIO_DIR = "data/audio"
TEXT_PATH = "data/generated_text.txt"
OUTPUT_DIR = "data/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_video.mp4")

# 🎨 Paramètres visuels
VIDEO_SIZE = (1280, 720)
FONT = "Arial-Bold"  # Police plus épaisse
FONT_SIZE = 40
FONT_COLOR = "yellow"  # Couleur plus visible
BG_COLOR = (0, 0, 0, 0.7)  # Fond semi-transparent
FPS = 24
SUBTITLE_POSITION = ("center", 0.85)  # Position en % de la hauteur

def extract_prompt(text_path):
    """🔎 Extrait le prompt de la première ligne du fichier texte."""
    try:
        with open(text_path, "r", encoding="utf-8") as f:
            return f.readline().strip()
    except Exception as e:
        print(f"❌ Impossible de lire le fichier texte : {e}")
        return "Unknown prompt"

def create_text_clip(text, duration, fontsize=FONT_SIZE, bg_color=None):
    """🎞 Crée un clip texte avec fond optionnel."""
    txt_clip = TextClip(
        text,
        fontsize=fontsize,
        font=FONT,
        color=FONT_COLOR,
        method="caption",
        size=(VIDEO_SIZE[0] - 100, None),
        stroke_color="black",
        stroke_width=1
    ).set_duration(duration)
    
    if bg_color:
        # Crée un fond semi-transparent
        bg = ColorClip(
            size=(int(txt_clip.size[0]*1.1), int(txt_clip.size[1]*1.2)),
            color=bg_color[:3],
            ismask=False
        )
        bg = bg.set_opacity(bg_color[3]).set_duration(duration)
        return CompositeVideoClip([bg, txt_clip.set_position("center")])
    return txt_clip

def resize_image(image_path, target_size):
    """🖼 Redimensionne l'image en conservant le ratio."""
    img = Image.open(image_path)
    img.thumbnail((target_size[0], target_size[1]*2))  # Permet un recadrage vertical
    background = Image.new("RGB", target_size, (0, 0, 0))
    offset = ((target_size[0] - img.size[0]) // 2, (target_size[1] - img.size[1]) // 2)
    background.paste(img, offset)
    return np.array(background)

def create_video_segment(image_path, audio_path, text=None):
    """🎬 Crée un segment vidéo avec image, audio et sous-titre."""
    audio = AudioFileClip(audio_path)
    
    # Charge et redimensionne l'image
    img_array = resize_image(image_path, VIDEO_SIZE)
    image = ImageClip(img_array).set_duration(audio.duration)
    
    clips = [image.set_audio(audio)]
    
    # Ajoute le sous-titre si fourni
    if text:
        subtitle = create_text_clip(
            text,
            audio.duration,
            fontsize=FONT_SIZE,
            bg_color=BG_COLOR
        ).set_position(SUBTITLE_POSITION, relative=True)
        clips.append(subtitle)
    
    return CompositeVideoClip(clips)

def create_video():
    """🎬 Assemble les éléments en une vidéo finale."""
    try:
        # Vérification des fichiers
        if not os.path.exists(TEXT_PATH):
            raise FileNotFoundError(f"Fichier texte introuvable : {TEXT_PATH}")
        
        image_files = sorted(f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg')))
        audio_files = sorted(f for f in os.listdir(AUDIO_DIR) if f.lower().endswith('.mp3'))
        
        if not image_files or not audio_files:
            raise ValueError("Aucune image ou audio trouvée")
        
        # Lecture du texte
        with open(TEXT_PATH, "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f if line.strip()]
        
        prompt = sentences[0] if sentences else "Prompt inconnu"
        sentence_lines = sentences[1:] if len(sentences) > 1 else [""]*len(image_files)
        
        # Création des segments
        clips = []
        for i, (img, aud) in enumerate(zip(image_files, audio_files)):
            text = sentence_lines[i] if i < len(sentence_lines) else ""
            segment = create_video_segment(
                os.path.join(IMG_DIR, img),
                os.path.join(AUDIO_DIR, aud),
                text
            )
            clips.append(segment)
        
        # Intro/Outro
        intro = create_text_clip(
            f"Vidéo générée à partir du prompt :\n\n{prompt[:100]}{'...' if len(prompt)>100 else ''}",
            5, FONT_SIZE+10, (0, 0, 0, 0.9)
        )
        
        outro = create_text_clip(
            "Réalisé par MAIGA Mahamane D & BERTHE Sidi Mohamed\n© 2024",
            4, FONT_SIZE, (0, 0, 0, 0.9)
        )
        
        # Assemblage final
        final = concatenate_videoclips([intro] + clips + [outro], method="compose")
        final.write_videofile(
            OUTPUT_PATH,
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
            bitrate="8000k",
            threads=4,
            preset='slow',
            logger="bar"
        )
        print(f"\n✅ Vidéo générée avec succès : {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    create_video()