#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testELF.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testELF', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testELF')
    valeurAssociation = {'out': 'donnéesRésultat', 'expected': 'attendu', 'phoff': 'décalageEntêteProgramme', 'offset': 'valeurDécalage', 'invalid': 'donnéesInvalide', 'path': 'chemin', 'executable': 'imageCodeExécutable', 'rejected': 'résultatRejet', 'linux_example': 'exempleLinux', 'original': 'original', 'result': 'résultat', 'format_': 'définirFormat', 'main': 'lancer', 'content': 'valeurContenuValeur', 'source': 'donnéesOriginal', 'name': 'nom', 'reference': 'ligneRéférenceComparaison', 'ROOT': 'racineProjet', 'value': 'valeur', 'report': 'rapportValidation'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
