# 🎬 Création Multimédia avec l'IA Générative : Texte, Vidéo et Audio

Projet académique réalisé dans le cadre du **Master Intelligence Artificielle**, visant à concevoir un pipeline complet de génération multimédia à partir d’un **simple prompt textuel**.

## 🎯 Objectifs

- Générer **du texte**, **des images**, **de l’audio** et une **vidéo finale** via des outils IA open-source.
- Intégrer plusieurs modèles d’intelligence artificielle dans un pipeline cohérent.
- Fournir une interface CLI simple, et une version web interactive (Gradio).

## 📂 Structure du projet

```
generative_multimedia_project/
├── requirements.txt          # Bibliothèques requises
├── .gitignore
├── gmp_env/                  # Environnement virtuel
├── scripts/
│   ├── generate_text.py      # Génération et découpage du texte
│   ├── generate_images.py    # Création d’illustrations avec IA
│   ├── generate_audio.py     # Voix synthétique et concaténation audio
│   ├── generate_video.py     # Montage final : image + audio + sous-titres
│   ├── utils.py              # Fonctions utilitaires
│   └── cli.py                # Orchestrateur CLI complet
└── data/
    ├── generated_text.txt
    ├── sentences/
    ├── images/
    ├── audio/
    └── videos/
```

## 🧠 Outils IA utilisés

| Tâche                | Modèle / Librairie             | Description                                 |
|---------------------|--------------------------------|---------------------------------------------|
| Génération de texte | `distilgpt2` (HuggingFace)     | Génération de phrases narratives            |
| Génération d’image  | `StableDiffusion` via `diffusers` | Illustrations IA à partir de phrases      |
| Synthèse vocale     | `gTTS`                         | Voix synthétique naturelle (anglais)        |
| Montage vidéo       | `moviepy` + `ImageMagick`      | Vidéo avec audio, sous-titres, intro/outro  |

## ⚙️ Installation

1. Clone le dépôt :

```bash
git clone https://github.com/dmaiga/generative-multimedia.git
cd generative_multimedia_project
```

2. Crée un environnement virtuel et installe les dépendances :

```bash
python -m venv gmp_env
gmp_env\Scripts\activate   # sous Windows
pip install -r requirements.txt
```

## 🚀 Utilisation (via CLI)

```bash
python scripts/cli.py all
```

Tu peux aussi exécuter étape par étape :

```bash
python scripts/cli.py text
python scripts/cli.py images
python scripts/cli.py audio
python scripts/cli.py video
```

## 📦 Exemple de sortie

- Prompt : `"A mysterious forest lit by moonlight"`
- Vidéo générée automatiquement avec :
  - narration audio,
  - illustrations IA,
  - sous-titres synchronisés,
  - intro et outro personnalisées.

## 📌 Limites et choix

- Limitation à 10 phrases max pour un usage local sans GPU.
- Utilisation de modèles open-source simples à exécuter.
- Voix synthétique avec `gTTS` pour éviter les dépendances lourdes.

## ✅ Auteurs

**MAIGA Mahamane Daouda**  
**BERTHE Sidi Mohamed**  
Master IA — 2025

---
