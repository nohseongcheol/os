#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/exécuterFichier.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('exécuterFichier', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('exécuterFichier')
    valeurAssociation = {'timeout': 'délaiExpirationExécution', 's': 'donnéesChaîne', 'i': 'indiceOrdinal', 'match': 'estÉgal', 'files': 'listeFichier', 'program': 'programme', 'executable': 'imageCodeExécutable', 'args': 'tableauArgument', 'chunk': 'valeurFragment', 'data': 'Données', 'proc': 'processus', 'send': 'envoyer', 'main': 'lancer', 'marker': 'marqueur', 'command': 'commande', 'include': 'inclure', 'dumped': 'extraitBrut', 'run': 'exécuterCommande', 'p': 'positionDonnées', 'parser': 'analyseur', 'options': 'options', 'kind': 'valeurCatégorie', 'selector': 'sélecteur', 'upload_data': 'donnéesTéléverser', 'end': 'décalageFin', 'n': 'nombreÉlémentsÉlémentListe', 'd': 'donnéesDestination', 'key': 'valeurEnfoncé', 'output': 'sortie', 'line': 'ligne', 'name': 'nom', 'upload_name': 'nomTéléverser', 'receive': 'recevoirMessage'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
