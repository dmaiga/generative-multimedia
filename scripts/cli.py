
import click
import subprocess
import sys
import os

SCRIPTS = {
    "text": "generate_text.py",
    "images": "generate_images.py",
    "audio": "generate_audio.py",
    "video": "generate_video.py"
}

@click.group()
def cli():
    """🎛️ Interface CLI pour orchestrer le pipeline de génération multimédia"""
    pass

@cli.command()
@click.option("--prompt", prompt=True, help="Texte de départ pour générer le contenu.")
def text(prompt):
    """📝 Génère le texte et extrait les phrases."""
    subprocess.run([sys.executable, SCRIPTS["text"]], input=prompt.encode(), check=True)

@cli.command()
def images():
    """🖼️ Génère les images à partir des phrases."""
    subprocess.run([sys.executable, SCRIPTS["images"]], check=True)

@cli.command()
def audio():
    """🔊 Génère les audios à partir des phrases."""
    subprocess.run([sys.executable, SCRIPTS["audio"]], check=True)

@cli.command()
def video():
    """🎬 Génère la vidéo finale à partir des images et audios."""
    subprocess.run([sys.executable, SCRIPTS["video"]], check=True)

@cli.command()
@click.option("--prompt", prompt=True, help="Texte de départ pour générer l'ensemble.")
def all(prompt):
    """🔁 Orchestration complète : texte → images → audio → vidéo"""
    click.echo("📝 Étape 1 : Génération du texte...")
    subprocess.run([sys.executable, SCRIPTS["text"]], input=prompt.encode(), check=True)

    click.echo("\n🖼️ Étape 2 : Génération des images...")
    subprocess.run([sys.executable, SCRIPTS["images"]], check=True)

    click.echo("\n🔊 Étape 3 : Génération des audios...")
    subprocess.run([sys.executable, SCRIPTS["audio"]], check=True)

    click.echo("\n🎬 Étape 4 : Génération de la vidéo...")
    subprocess.run([sys.executable, SCRIPTS["video"]], check=True)

if __name__ == "__main__":
    cli()
