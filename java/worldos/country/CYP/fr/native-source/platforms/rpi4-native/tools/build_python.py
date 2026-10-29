#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construirePython.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construirePython', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construirePython')
    valeurAssociation = {'ld': 'outilÉditeurLiens', 'archive': 'archive', 'SHA256': 'hachageValidation', 'build_python': 'créerPython', 'root': 'adresseRacine', 'source': 'donnéesOriginal', 'name': 'nom', 'path': 'chemin', 'VERSION': 'valeurÉdition', 'cc': 'CompilateurC', 'tar': 'lotTAR', 'newlib': 'newlib', 'member': 'membre'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
