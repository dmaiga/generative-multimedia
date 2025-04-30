from gtts import gTTS
import os
import time
import sys
import subprocess
from scripts.utils import load_sentences_audio

AUDIO_DIR = "data/audio"
FINAL_AUDIO = "final_audio.mp3"

def check_ffmpeg():
    """Vérifie si FFmpeg est installé"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False

def install_ffmpeg_windows():
    """Tente d'installer FFmpeg automatiquement sur Windows"""
    try:
        import requests
        import zipfile
        import io
        
        print("🔧 Installation de FFmpeg...")
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("ffmpeg")
        os.environ["PATH"] += os.pathsep + os.path.abspath("ffmpeg/ffmpeg-master-latest-win64-gpl/bin")
        return True
    except Exception as e:
        print(f"❌ Échec de l'installation automatique: {e}")
        return False

def combine_with_ffmpeg(audio_files, output_path):
    """Combine les audios en utilisant FFmpeg directement"""
    try:
        # Crée un fichier texte listant les MP3
        list_file = os.path.join(AUDIO_DIR, "concat_list.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for file in sorted(audio_files):
                f.write(f"file '{os.path.basename(file)}'\n")
        
        # Commande FFmpeg
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path,
            "-y"  # Overwrite sans demander
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        os.remove(list_file)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur FFmpeg (code {e.returncode}):")
        print(e.stderr.decode())
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def generate_individual_audios(sentences):
    """Génère les fichiers audio individuels"""
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_files = []
    
    for idx, sentence in enumerate(sentences, 1):
        try:
            print(f"🔊 [{idx}/{len(sentences)}] Génération: {sentence[:50]}...")
            output_file = os.path.join(AUDIO_DIR, f"audio_{idx}.mp3")
            
            tts = gTTS(text=sentence, lang='en', slow=False)
            tts.save(output_file)
            audio_files.append(output_file)
            
            time.sleep(1)  # Pause anti-rate limiting
            
        except Exception as e:
            print(f"❌ Erreur phrase {idx}: {str(e)[:100]}...")
    
    return audio_files

def main():
    # Vérification FFmpeg
    if not check_ffmpeg():
        print("FFmpeg non détecté, tentative d'installation...")
        if sys.platform == "win32":
            if not install_ffmpeg_windows():
                print("Veuillez installer FFmpeg manuellement depuis ffmpeg.org")
                return
        else:
            print("Veuillez installer FFmpeg: sudo apt install ffmpeg (Linux) ou brew install ffmpeg (Mac)")
            return
    
    # Chargement des phrases
    sentences = load_sentences_audio()
    if not sentences:
        print("❌ Aucune phrase trouvée")
        return
    
    # Génération des audios
    audio_files = generate_individual_audios(sentences)
    
    # Combinaison
    if audio_files:
        final_path = os.path.join(AUDIO_DIR, FINAL_AUDIO)
        print("\n🔧 Combinaison des fichiers audio...")
        
        if combine_with_ffmpeg(audio_files, final_path):
            print(f"✅ Audio final généré: {final_path}")
            print(f"Taille: {os.path.getsize(final_path)/1024:.1f} KB")
        else:
            print("⚠️ Audio final non généré")
    
    print(f"\nTerminé - {len(audio_files)}/{len(sentences)} audios générés")

if __name__ == "__main__":
    main()