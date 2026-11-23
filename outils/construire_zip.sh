#!/usr/bin/env bash
# Construit jeux-revisions-logistique.zip (le fichier installé par WordPress et joint à chaque release GitHub).
# Usage : bash outils/construire_zip.sh [dossier_de_sortie]   (par défaut : dist)
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-dist}"
V=$(grep -m1 -oP '^ \* Version:\s*\K[0-9.]+' jeux-revisions-logistique.php)
rm -rf "$OUT/jeux-revisions-logistique" "$OUT/jeux-revisions-logistique.zip"
mkdir -p "$OUT/jeux-revisions-logistique"
tar --exclude='./.git' --exclude='./.github' --exclude='./outils' --exclude="./$OUT" --exclude='./README.md' --exclude='./.gitignore' -cf - . | tar -xf - -C "$OUT/jeux-revisions-logistique"
(cd "$OUT" && zip -qr -X jeux-revisions-logistique.zip jeux-revisions-logistique)
echo "$OUT/jeux-revisions-logistique.zip — version $V — $(ls "$OUT/jeux-revisions-logistique/jeux" | grep -vc index.php) jeux"
