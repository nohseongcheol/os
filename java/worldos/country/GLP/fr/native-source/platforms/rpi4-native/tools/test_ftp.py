#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testFTP.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testFTP', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testFTP')
    valeurAssociation = {'timeout': 'délaiExpirationExécution', 'payload': 'donnéesChargeUtile', 'broken': 'endommagé', 'linux_example': 'exempleLinux', 'chunk': 'valeurFragment', 'data': 'Données', 'proc': 'processus', 'code': 'séquenceInstructionMachine', 'linux': 'fichierLinux', 'archive': 'archive', 'main': 'lancer', 'net_source': 'sourceRéseauCourt', 'temporary': 'temporaire', 'static_source': 'sourceStatique', 'java_source': 'sourceJava', 'echo': 'entréeÉlémentServeurRépercuter', 'ROOT': 'racineProjet', 'text': 'texte', 'marker': 'marqueur', 'EchoFixture': 'DispositifTestRépercuter', 'command': 'commande', 'out': 'donnéesRésultat', 'expected': 'attendu', 'server_source': 'sourceServeur', 'shell': 'interpréteurCommandes', 'upload': 'fichiersTéléverser', 'transcript': 'transcription', 'port': 'numéroPort', 'native': 'natif', 'elf': 'fichierCodeExécutable', 'server_udp_port': 'portDatagrammeServeur', 'packed': 'empaqueté', 'bridge': 'pont', 'selector': 'sélecteur', 'end': 'décalageFin', 'e': 'entréeÉlémentAuxiliaire', 'ftp': 'connexionTransfertFichier', 'key': 'valeurEnfoncé', 'bytecode': 'codeOctets', 'peer': 'valeurPairRéseau', 'result': 'résultat', 'unchanged': 'donnéesPréservé', 'line': 'ligne', 'server_tcp_port': 'portFluxServeur', 'source': 'donnéesOriginal', 'NetworkBridge': 'pontRéseau', 'jar': 'lotJava', 'receive': 'recevoirMessage', 'report': 'rapportValidation'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
