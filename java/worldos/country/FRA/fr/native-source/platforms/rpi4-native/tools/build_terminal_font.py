#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construirePoliceTerminal.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construirePoliceTerminal', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construirePoliceTerminal')
    valeurAssociation = {'data': 'Données', 'img': 'Dessin', 'bits': 'listeBits', 'x': 'coordonnéeCoordonnéeHorizontale', 'draw': 'dessinerÉcran', 'licences': 'licences', 'paths': 'listeChemin', 'y': 'coordonnéeCoordonnéeVerticale', 'main': 'lancer', 'src': 'adresseOriginal', 'fonts': 'listePolice', 'ROOT': 'racineProjet', 'p': 'positionDonnées', 'cp': 'encodageCaractère', 'target': 'valeurCible'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
