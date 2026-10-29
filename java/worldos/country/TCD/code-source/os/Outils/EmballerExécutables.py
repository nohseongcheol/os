#!/usr/bin/env python3
"""명시한 Utilisateur ELF만 lire 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def EmballerExécutables():
    analyserValeur = argparse.ArgumentParser()
    analyserValeur.add_argument('-o', required=True)
    analyserValeur.add_argument('files', nargs='+', help='nom=ELF경로')
    argumentParamètre = analyserValeur.parse_args()
    if len(argumentParamètre.files) > 32:
        analyserValeur.error('Programme valeurMaximal 32개')
    listeEntréesListe = []
    listeNoms = set()
    for valeurEntréeÉlément in argumentParamètre.files:
        nom, chemin = valeurEntréeÉlément.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', nom) or nom in listeNoms:
            analyserValeur.error('exécuterCommande 이름이 잘못되었거나 중복됨: ' + nom)
        listeNoms.add(nom)
        Données = Path(chemin).read_bytes()
        if len(Données) > 2 * 1024 * 1024:
            analyserValeur.error('exécuterCommande 파일이 너무 큼')
        listeEntréesListe.append((nom.encode(), Données))
    résultat = bytearray(8 + 24 * len(listeEntréesListe))
    struct.pack_into('<II', résultat, 0, 0x50414b4a, len(listeEntréesListe))
    for numéro, (nom, Données) in enumerate(listeEntréesListe):
        résultat.extend(bytes((-len(résultat)) % 16))
        struct.pack_into('<16sII', résultat, 8 + numéro * 24, nom, len(résultat), len(Données))
        résultat.extend(Données)
    Path(argumentParamètre.o).write_bytes(résultat)

if __name__ == '__main__':
    EmballerExécutables()
