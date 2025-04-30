import os
import re

def load_generated_text(file_path="data/generated_text.txt"):
    """
    Charge le texte généré depuis un fichier.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Le fichier {file_path} est introuvable.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def split_text_into_sentences(text):
    """
    Découpe un texte en phrases clés basées sur la ponctuation.
    Filtre les phrases trop courtes ou vides.
    """
    # Découpe sur les fins de phrase avec espace après ponctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # Nettoyage : retirer les phrases trop courtes (< 10 caractères) ou vides
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    return sentences

def save_sentences(sentences, save_dir="data/sentences"):
    """
    Sauvegarde chaque phrase dans un fichier texte distinct.
    """
    os.makedirs(save_dir, exist_ok=True)

    for idx, sentence in enumerate(sentences):
        file_path = os.path.join(save_dir, f"sentence_{idx+1}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(sentence)

    print(f"✅ {len(sentences)} phrases sauvegardées dans {save_dir}")

def load_sentences_audio(sentences_dir="data/sentences"):
    """
    Charge les phrases depuis les fichiers .txt du dossier spécifié.
    """
    if not os.path.exists(sentences_dir):
        raise FileNotFoundError(f"❌ Le dossier {sentences_dir} est introuvable.")

    files = sorted([f for f in os.listdir(sentences_dir) if f.endswith(".txt")])
    sentences = []

    for filename in files:
        path = os.path.join(sentences_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            sentence = f.read().strip()
            if sentence:
                sentences.append(sentence)

    return sentences

# Pour tester individuellement le fichier utils
if __name__ == "__main__":
    text = load_generated_text()
    sentences = split_text_into_sentences(text)
    save_sentences(sentences)
