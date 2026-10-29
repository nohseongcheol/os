#!/usr/bin/env python3
"""명시한 Java arbreSource/valeurClasse 파일을 Amorçage 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def EmballerExécutables(listeEntréesListe):
    entréesListeFichier = []
    listeNoms = {'Hello.java'}
    nomsExplicite = set()
    for valeurEntréeÉlément in listeEntréesListe:
        if '=' not in valeurEntréeÉlément:
            raise ValueError('expected NAME=PATH: ' + valeurEntréeÉlément)
        nom, chemin = valeurEntréeÉlément.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', nom) or nom in nomsExplicite:
            raise ValueError('invalid or duplicate file name: ' + nom)
        nomsExplicite.add(nom)
        listeNoms.add(nom)
        Données = Path(chemin).read_bytes()
        if len(Données) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + nom)
        entréesListeFichier.append((nom.encode('ascii'), Données))
    if len(listeNoms) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    résultat = bytearray(struct.pack('<4sI', b'JKJF', len(entréesListeFichier)))
    résultat.extend(bytes(72 * len(entréesListeFichier)))
    for nombre, (nom, Données) in enumerate(entréesListeFichier):
        struct.pack_into('<64sII', résultat, 8 + nombre * 72, nom, len(résultat), len(Données))
        résultat.extend(Données)
    return bytes(résultat)


if __name__ == '__main__':
    analyserValeur = argparse.ArgumentParser(description=__doc__)
    analyserValeur.add_argument('-o', required=True)
    analyserValeur.add_argument('files', nargs='*', help='NAME=PATH')
    arguments = analyserValeur.parse_args()
    try:
        Données = EmballerExécutables(arguments.files)
        valeurDestination = Path(arguments.o)
        if not valeurDestination.exists() or valeurDestination.read_bytes() != Données:
            valeurTemporaire = valeurDestination.with_name(valeurDestination.name + '.tmp')
            valeurTemporaire.write_bytes(Données)
            valeurTemporaire.replace(valeurDestination)
    except (ValueError, OSError) as erreur:
        analyserValeur.error(str(erreur))
