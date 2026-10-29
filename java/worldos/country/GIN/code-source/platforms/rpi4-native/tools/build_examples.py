#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construireRecueilExemples.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construireRecueilExemples', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construireRecueilExemples')
    valeurAssociation = {'out': 'donnéesRésultat', 'build_examples': 'créerRecueilExemples', 'files': 'listeFichier', 'java': 'exécuterJava', 'run': 'exécuterCommande', 'path': 'chemin', 'p': 'positionDonnées', 'readme': 'lisezMoi', 'build_java_library': 'créerBibliothèqueJava', 'code': 'séquenceInstructionMachine', 'index': 'indiceRechercher', 'classes': 'cheminClasse', 'repo': 'cheminDépôt', 'root': 'adresseRacine', 'content': 'valeurContenuValeur', 'source': 'donnéesOriginal', 'name': 'nom', 'target': 'valeurCible', 'manifest': 'manifesteLot', 'language': 'Langue'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
