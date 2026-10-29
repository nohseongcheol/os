#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testBureau.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testBureau', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testBureau')
    valeurAssociation = {'x': 'coordonnéeCoordonnéeHorizontale', 'typing': 'caractèreSaisi', 'message': 'texteNotification', 'start': 'lancer', 'down': 'estEnfoncementEnCours', 'exact': 'valeurExact', 'i': 'indiceOrdinal', 'press': 'toucheEnfoncer', 'rectangles': 'listeRectangles', 'sym': 'symbole', 'j': 'ordinalInterne', 'deadline': 'tempsÉchéance', 'proc': 'processus', 'data': 'Données', 'main': 'lancer', 'w': 'valeurLargeurDemandé', 'init': 'valeurInitialValeur', 'block': 'blocDonnées', 'ROOT': 'racineProjet', 'text': 'texte', 'marker': 'marqueur', 'report': 'rapportValidation', 'until': 'jusquÀ', 'clipboard': 'valeurPressePapiers', 'dst': 'adresseDestination', 'seen': 'entréesListeVu', 'poll': 'moniteurDisponibilitéÉtat', 'transcript': 'transcription', 'port': 'numéroPort', 'offset': 'valeurDécalage', 'h': 'valeurHauteurDemandé', 'src': 'adresseOriginal', 'event': 'évènement', 'encoding': 'jeuCaractères', 'size': 'taille', 'key': 'valeurEnfoncé', 'pixels': 'listePixels', 'y': 'coordonnéeCoordonnéeVerticale', 'output': 'sortie', 'symbol': 'valeurSymbole', 'client': 'client', 'char': 'donnéesCaractère', 'rgb': 'couleurRGB'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
