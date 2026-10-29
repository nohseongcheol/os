#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/sDKExporter.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('sDKExporter', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('sDKExporter')
    valeurAssociation = {'out': 'donnéesRésultat', 'obj': 'fichierDestination', 'relative': 'cheminRelatif', 'compiler_archive': 'archiveCompilateur', 'sdk': 'trousseDéveloppement', 'dist': 'cheminDistribution', 'archive': 'archive', 'main': 'lancer', 'posix': 'pOSIX', 'files': 'listeFichier', 'source': 'donnéesOriginal', 'name': 'nom', 'target': 'valeurCible', 'ROOT': 'racineProjet', 'destination': 'adresseDonnéesDestination', 'manifest': 'manifesteLot', 'work': 'cheminTravailEnCours'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
