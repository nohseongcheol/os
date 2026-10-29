#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/créerImage.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('créerImage', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('créerImage')
    valeurAssociation = {'total': 'capacitéTotal', 'start': 'lancer', 'firmware': 'valeurMicrologiciel', 'files': 'listeFichier', 'archive_base': 'baseArchive', 'partition': 'fichierPartition', 'archive': 'archive', 'main': 'lancer', 'block': 'blocDonnées', 'ROOT': 'racineProjet', 'boot': 'cheminAmorçage', 'stage': 'valeurÉtapePhase', 'out': 'donnéesRésultat', 'expected': 'attendu', 'f': 'entréeÉlémentFichier', 'src': 'adresseOriginal', 'path': 'chemin', 'p': 'positionDonnées', 'extracted': 'extrait', 'member': 'membre', 'mbr': 'EnregistrementAmorçageMaître', 'image': 'image', 'sector_count': 'nombreÉlémentsSecteur', 'dist': 'cheminDistribution', 'sha': 'calculerHachage', 'license_': 'licence', 'source': 'donnéesOriginal', 'name': 'nom', 'value': 'valeur', 'manifest': 'manifesteLot', 'dest': 'positionValeurDestination', 'work': 'cheminTravailEnCours'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
