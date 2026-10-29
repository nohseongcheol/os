#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/pontRéseau.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('pontRéseau', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('pontRéseau')
    valeurAssociation = {'response': 'réponseRetour', 'parts': 'composantChemin', 's': 'donnéesChaîne', 'i': 'indiceOrdinal', 'close': 'fermer', 'forward': 'règleTransfertEnCours', 'slip_input': 'entréeSLIP', 'self': 'valeurSoi', 'item': 'valeurEntréeÉlément', 'flags': 'bitsConfiguration', 'ftp_port': 'numéroPortTransfertFichier', 'args': 'tableauArgument', 'server': 'valeurServeur', 'data': 'Données', 'ethernet_input': 'entréeEthernet', 'trace_packet': 'paquetTrace', 'GATEWAY': 'adresseMatérielPasserelle', 'rule': 'valeurRègle', 'protocol': 'ABIRéseau', 'forwards': 'règlesTransfertEnCours', 'occupied': 'occupé', 'host': 'Hôte', 'ack': 'numéroConfirmation', 'serial_port': 'numéroPortSériel', 'readers': 'lecteurs', 'guest': 'invité', 'destination': 'adresseDonnéesDestination', 'ethernet_port': 'portEthernet', 'b': 'valeurDeuxième', 'MAC': 'adresseMachine', 'arp': 'paquetRésolutionAdresse', 'writable': 'inscriptible', 'direction': 'direction', 'seq': 'numéroOrdre', 'frame': 'cadreExécution', 'loop': 'valeurCycle', 'port': 'numéroPort', 'offset': 'valeurDécalage', 'readable': 'peutLire', 'c': 'codeCaractère', 'p': 'positionDonnées', 'writers': 'rédacteurs', 'IP': 'valeurAdresseInternet', 'e': 'entréeÉlémentAuxiliaire', 'n': 'nombreÉlémentsÉlémentListe', 'packet': 'donnéesPaquet', 'arguments': 'argumentTransféré', 'source': 'donnéesOriginal', 'NetworkBridge': 'pontRéseau', 'window': 'fenêtre', 'capture': 'capturer'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
