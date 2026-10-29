#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/DispositifTestRépercuter.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('DispositifTestRépercuter', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('DispositifTestRépercuter')
    valeurAssociation = {'data': 'Données', 'e': 'entréeÉlémentAuxiliaire', 'connection': 'connexion', 'f': 'entréeÉlémentFichier', 'peer': 'valeurPairRéseau', 'self': 'valeurSoi', 'udp': 'contrôleDatagramme', 't': 'entréeÉlémentTerminal', 'tcp': 'contrôleConnexion', 'EchoFixture': 'DispositifTestRépercuter', 'args': 'tableauArgument', 'chunk': 'valeurFragment'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
