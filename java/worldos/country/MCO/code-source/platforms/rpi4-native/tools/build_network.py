#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construireRéseau.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construireRéseau', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construireRéseau')
    valeurAssociation = {'obj': 'fichierDestination', 'objects': 'fichiersDestination', 'library': 'bibliothèque', 'output': 'sortie', 'port': 'numéroPort', 'root': 'adresseRacine', 'files': 'listeFichier', 'source': 'donnéesOriginal', 'run': 'exécuterCommande', 'flags': 'bitsConfiguration', 'path': 'chemin', 'build_network': 'créerRéseau', 'cc': 'CompilateurC', 'ar': 'outilArchive'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
