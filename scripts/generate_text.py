from transformers import pipeline, set_seed
import torch
import os
from scripts.utils import split_text_into_sentences, save_sentences

def generate_text(prompt, max_length=200):
    """
    Génère un texte en anglais à partir d'un prompt et le sauvegarde dans un fichier.
    Limite la taille du texte pour limiter le nombre de phrases (et donc d’images).
    """
    generator = pipeline(
        'text-generation',
        model='distilgpt2',
        device=0 if torch.cuda.is_available() else -1,
        pad_token_id=50256
    )
    set_seed(42)

    output = generator(
        prompt,
        max_length=max_length,
        num_return_sequences=1,
        truncation=True
    )

    generated_text = output[0]['generated_text']

    os.makedirs("data", exist_ok=True)
    save_path = "data/generated_text.txt"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(generated_text)

    print(f"✅ Texte généré et sauvegardé dans : {save_path}")
    print(generated_text)
    return generated_text

def main():
    prompt = input("Veuillez entrer votre prompt pour générer le texte : ").strip()
    if not prompt:
        print("❌ Prompt vide. Veuillez relancer avec un texte valide.")
        return

    generated_text = generate_text(prompt)

    sentences = split_text_into_sentences(generated_text)

    # Limiter le nombre de phrases pour réduire les ressources
    max_sentences = 10
    sentences = sentences[:max_sentences]

    save_sentences(sentences)

if __name__ == "__main__":
    print(f"Device set to use {'cuda' if torch.cuda.is_available() else 'cpu'}")
    main()
