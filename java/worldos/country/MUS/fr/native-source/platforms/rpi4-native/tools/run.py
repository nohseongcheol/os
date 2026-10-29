#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/exécuterCommande.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('exécuterCommande', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('exécuterCommande')
    valeurAssociation = {'supported': 'fonctionnalitésPrisEnCharge', 'parser': 'analyseur', 'qemu': 'MachineSimulacre', 'run_desktop': 'lancerBureau', 'main': 'lancer', 'host': 'Hôte', 'status': 'valeurÉtatValeur', 'NetworkBridge': 'pontRéseau', 'ROOT': 'racineProjet', 'bridge': 'pont', 'loader': 'chargeur', 'base': 'valeurArrièrePlan', 'options': 'options', 'binary': 'binaire', 'args': 'tableauArgument', 'command': 'commande'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
