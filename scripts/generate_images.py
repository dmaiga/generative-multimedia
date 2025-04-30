from diffusers import StableDiffusionPipeline
import torch
import os
from PIL.PngImagePlugin import PngInfo

def load_sentences(sentences_dir="data/sentences"):
    """
    chargement des phrases depuis le dossier data/sentences
    """
    if not os.path.exists(sentences_dir):
        raise FileNotFoundError(f"❌ Le dossier {sentences_dir} est introuvable.")
    
    files = sorted([f for f in os.listdir(sentences_dir) if f.endswith(".txt")])
    return [
        open(os.path.join(sentences_dir, f), "r", encoding="utf-8").read().strip()
        for f in files
    ]

def generate_images_from_sentences(sentences, save_dir="data/images", pipe=None, **kwargs):
    """
    génèration d'une image par phrase et sauvegarde dans data/images, avec métadonnées
    """
    os.makedirs(save_dir, exist_ok=True)

    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

    for idx, sentence in enumerate(sentences):
        print(f"🖼️ Génération de l'image pour : {sentence}")
        try:
            image = pipe(
                sentence,
                num_inference_steps=kwargs.get("num_steps", 50),
                guidance_scale=kwargs.get("guidance_scale", 7.5),
            ).images[0]

            metadata = PngInfo()
            metadata.add_text("prompt", sentence)

            image_path = os.path.join(save_dir, f"image_{idx+1}.png")
            image.save(image_path, pnginfo=metadata)
        except Exception as e:
            print(f"❌ Erreur lors de la génération pour '{sentence}' : {e}")

    print(f"✅ {len(sentences)} images générées dans {save_dir}")

def main():
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to(
        "cuda" if torch.cuda.is_available() else "cpu"
    )
    sentences = load_sentences()
    generate_images_from_sentences(sentences, pipe=pipe, num_steps=30)

if __name__ == "__main__":
    main()
