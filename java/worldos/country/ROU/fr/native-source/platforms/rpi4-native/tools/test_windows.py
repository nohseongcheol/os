#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testFenêtres.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testFenêtres', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testFenêtres')
    valeurAssociation = {'wait': 'attendreFin', 'x': 'coordonnéeCoordonnéeHorizontale', 's': 'donnéesChaîne', 'xy': 'paireCoordonnée', 'sel': 'Sélecteur', 'seconds': 'unitéSecondes', 'log': 'enregistrementJournal', 'at': 'positionActuel', 'send': 'envoyer', 'main': 'lancer', 'req': 'valeurRequête', 'hot': 'valeurRaccourci', 'pump': 'évènementPoignée', 'ROOT': 'racineProjet', 'marker': 'marqueur', 'b': 'valeurDeuxième', 'command': 'commande', 'shell': 'interpréteurCommandes', 'f': 'entréeÉlémentFichier', 'color': 'couleurPixel', 'click': 'boutonCliquer', 'k': 'indiceTroisième', 'c': 'codeCaractère', 'r': 'valeurRetourné', 'p': 'positionDonnées', 'done': 'montantAchevé', 'end': 'décalageFin', 'command_mode': 'modeCommande', 'key': 'valeurEnfoncé', 'y': 'coordonnéeCoordonnéeVerticale', 'pixels': 'listePixels', 'result': 'résultat', 'report': 'rapportValidation', 'dest': 'positionValeurDestination', 'work': 'cheminTravailEnCours', 'qmp': 'connexionContrôleSimulacre'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
