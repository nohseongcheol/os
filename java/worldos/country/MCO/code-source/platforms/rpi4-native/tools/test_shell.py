#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testInterpréteurCommandes.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testInterpréteurCommandes', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testInterpréteurCommandes')
    valeurAssociation = {'timeout': 'délaiExpirationExécution', 'x': 'coordonnéeCoordonnéeHorizontale', 'msg': 'messageRéseau', 'i': 'indiceOrdinal', 'reply': 'réponse', 'call': 'invoquer', 'args': 'tableauArgument', 'chunk': 'valeurFragment', 'data': 'Données', 'proc': 'processus', 'long_text': 'texteLong', 'restored': 'donnéesRestauré', 'send': 'envoyer', 'file': 'Fichier', 'main': 'lancer', 'found': 'chercherRésultat', 'ROOT': 'racineProjet', 'text': 'texte', 'marker': 'marqueur', 'command': 'commande', 'expected': 'attendu', 'pixel': 'pixel', 'shell': 'interpréteurCommandes', 'poll': 'moniteurDisponibilitéÉtat', 'transcript': 'transcription', 'end': 'décalageFin', 'image': 'image', 'key': 'valeurEnfoncé', 'y': 'coordonnéeCoordonnéeVerticale', 'output': 'sortie', 'result': 'résultat', 'client': 'client', 'line': 'ligne', 'stream': 'valeurFlux', 'name': 'nom', 'value': 'valeur', 'receive': 'recevoirMessage', 'report': 'rapportValidation', 'work': 'cheminTravailEnCours', 'qmp': 'connexionContrôleSimulacre'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
