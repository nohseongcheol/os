#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testRecueilExemples.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testRecueilExemples', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testRecueilExemples')
    valeurAssociation = {'count': 'nombreÉlémentsEntréeÉlément', 'exact': 'valeurExact', 'expected_file': 'fichierAttendu', 'ftp_port': 'numéroPortTransfertFichier', 'data': 'Données', 'graphics_command': 'commandeGraphisme', 'main': 'lancer', 'row': 'positionRangée', 'init': 'valeurInitialValeur', 'target': 'valeurCible', 'ROOT': 'racineProjet', 'text': 'texte', 'binary': 'binaire', 'out': 'donnéesRésultat', 'entry': 'pointEntréeÉlément', 'got': 'nombreÉlémentsReçu', 'port': 'numéroPort', 'graphics_start': 'démarrerDessin', 'col': 'positionColonne', 'begin': 'démarrerDécalage', 'kind': 'valeurCatégorie', 'selector': 'sélecteur', 'n': 'nombreÉlémentsÉlémentListe', 'key': 'valeurEnfoncé', 'y': 'coordonnéeCoordonnéeVerticale', 'client': 'client', 'line': 'ligne', 'report': 'rapportValidation', 'language': 'Langue', 'x': 'coordonnéeCoordonnéeHorizontale', 'start': 'lancer', 'rgb': 'couleurRGB', 'down': 'estEnfoncementEnCours', 'listing': 'envoyerListe', 'payload': 'donnéesChargeUtile', 'proc': 'processus', 'w': 'valeurLargeurDemandé', 'temporary': 'temporaire', 'echo': 'entréeÉlémentServeurRépercuter', 'label': 'tableNom', 'content': 'valeurContenuValeur', 'argument': 'valeurTransféré', 'EchoServers': 'ServeursRépercuter', 'marker': 'marqueur', 'expected': 'attendu', 'test_language': 'testLangue', 'filename': 'nomEntréeÉlémentFichier', 'shell': 'interpréteurCommandes', 'color': 'couleurPixel', 'transcript': 'transcription', 'offset': 'valeurDécalage', 'h': 'valeurHauteurDemandé', 'run': 'exécuterCommande', 'c': 'codeCaractère', 'path': 'chemin', 'encoding': 'jeuCaractères', 'end': 'décalageFin', 'ftp': 'connexionTransfertFichier', 'pixels': 'listePixels', 'symbol': 'valeurSymbole', 'source': 'donnéesOriginal', 'name': 'nom', 'receive': 'recevoirMessage', 'manifest': 'manifesteLot'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
