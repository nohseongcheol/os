#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/TestAmorçage.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('TestAmorçage', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('TestAmorçage')
    valeurAssociation = {'timeout': 'délaiExpirationExécution', 'response': 'réponseRetour', 'msg': 'messageRéseau', 'exact': 'valeurExact', 'markers': 'marqueurs', 'i': 'indiceOrdinal', 'match': 'estÉgal', 'execute': 'exécuterTâche', 'cancel': 'opérationAnnuler', 'cmd_byte': 'octetCommande', 'reply': 'réponse', 'points': 'points', 'server': 'valeurServeur', 'data': 'Données', 'prompt': 'invite', 'enter': 'entrer', 'imported': 'importé', 'send': 'envoyer', 'main': 'lancer', 'ROOT': 'racineProjet', 'text': 'texte', 'first_gui': 'gUIPremier', 'pixel': 'pixel', 'java_class': 'classeJava', 'upload': 'fichiersTéléverser', 'pixels_file': 'fichierPixel', 'pixels_data': 'donnéesPixel', 'edit': 'valeurÉditer', 'receive_until': 'recevoirJusquÀ', 'selector': 'sélecteur', 'size': 'taille', 'qmp_path': 'cheminQMP', 'key': 'valeurEnfoncé', 'second_gui': 'gUIDeuxième', 'y': 'coordonnéeCoordonnéeVerticale', 'result': 'résultat', 'samples': 'entréesListeExemple', 'client': 'client', 'line': 'ligne', 'report': 'rapportValidation', 'work': 'cheminTravailEnCours', 'x': 'coordonnéeCoordonnéeHorizontale', 'python_checks': 'contrôlesPython', 'download': 'télécharger', 'greeting': 'Salutation', 'dims': 'valeurDimensions', 'chunk': 'valeurFragment', 'deadline': 'tempsÉchéance', 'proc': 'processus', 'content': 'valeurContenuValeur', 'block': 'blocDonnées', 'marker': 'marqueur', 'command': 'commande', 'expected': 'attendu', 'shell': 'interpréteurCommandes', 'drawing': 'cheminDessin', 'f': 'entréeÉlémentFichier', 'transcript': 'transcription', 'offset': 'valeurDécalage', 'path': 'chemin', 'screenshot': 'captureÉcran', 'arguments': 'argumentTransféré', 'pixels': 'listePixels', 'viewer': 'clientÉcran', 'output': 'sortie', 'stream': 'valeurFlux', 'cmd': 'argumentsCommande', 'name': 'nom', 'qmp': 'connexionContrôleSimulacre'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
