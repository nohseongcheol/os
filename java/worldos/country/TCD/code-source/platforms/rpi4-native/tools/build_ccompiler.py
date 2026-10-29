#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construireCompilateurC.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construireCompilateurC', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construireCompilateurC')
    valeurAssociation = {'out': 'donnéesRésultat', 'builtins': 'élémentsIntégrés', 'header': 'valeurEntête', 'sdk': 'trousseDéveloppement', 'build_ccompiler': 'créerCompilateurC', 'i': 'indiceOrdinal', 'elf': 'fichierCodeExécutable', 'run': 'exécuterCommande', 'flags': 'bitsConfiguration', 'path': 'chemin', 'p': 'positionDonnées', 'cc': 'CompilateurC', 'obj': 'fichierDestination', 'flag': 'valeurRéglages', 'ld': 'outilÉditeurLiens', 'objects': 'fichiersDestination', 'repo': 'cheminDépôt', 'v': 'donnéesTemporaire', 'upstream': 'amont', 'root': 'adresseRacine', 'assets': 'ressourcesVisuelles', 'source': 'donnéesOriginal', 'name': 'nom', 'includes': 'inclusions'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
