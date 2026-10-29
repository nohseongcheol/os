#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/vueBureau.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('vueBureau', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('vueBureau')
    valeurAssociation = {'count': 'nombreÉlémentsEntréeÉlément', 'special': 'toucheSpécial', 'error': 'erreur', 'exact': 'valeurExact', 'network': 'réseau', 'closed': 'estFermé', 'length': 'longueur', 'opened': 'ouvert', 'ftp_port': 'numéroPortTransfertFichier', 'server': 'valeurServeur', 'resources': 'ressources', 'data': 'Données', 'shift': 'toucheDécaler', 'send': 'envoyer', 'run_desktop': 'lancerBureau', 'protocol': 'ABIRéseau', 'forwards': 'règlesTransfertEnCours', 'host': 'Hôte', 'text': 'texte', 'korean': 'coréen', 'port': 'numéroPort', 'signum': 'numéroSignal', 'version': 'numéroVersion', 'parser': 'analyseur', 'bridge': 'pont', 'kind': 'valeurCatégorie', 'tail': 'partieTerminaison', 'size': 'taille', 'previous_buttons': 'boutonsPrécédentÉlément', 'key': 'valeurEnfoncé', 'y': 'coordonnéeCoordonnéeVerticale', 'prefix': 'partiePréalable', 'client': 'client', 'char': 'donnéesCaractère', 'work': 'cheminTravailEnCours', 'Keyboard': 'Clavier', 'x': 'coordonnéeCoordonnéeHorizontale', 'down': 'estEnfoncementEnCours', 'net': 'entréeÉlémentPontRéseau', 'self': 'valeurSoi', 'mode_changed': 'changéMode', 'serial': 'entréeSortieSériel', 'args': 'tableauArgument', 'Hangul': 'composerHangul', 'chunk': 'valeurFragment', 'proc': 'processus', 'Desktop': 'connecterBureau', 'buttons': 'boutons', 'thread': 'tâcheFond', 'pressed': 'estEnfoncé', 'previous': 'précédentÉlément', 'toggle': 'modeCommuter', 'command': 'commande', 'sock': 'valeurPriseRéseau', 'frame': 'cadreExécution', 'ctrl': 'toucheContrôle', 'path': 'chemin', 'cp': 'encodageCaractère', 'terminate': 'terminerProcessus', 'security': 'sécurité', 'vnc_port': 'portVNC', 'body': 'texteCorps', 'index': 'indiceRechercher', 'exited': 'possèdeQuitté', 'keysym': 'symboleTouche', 'output': 'sortie', 'keyboard': 'entréeÉlémentClavier', 'interrupted': 'interrompu', 'listener': 'recevoirPort', 'reader': 'lecteur', 'NetworkBridge': 'pontRéseau', 'gui': 'écranDessin', 'worker': 'tâcheTraitement'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
