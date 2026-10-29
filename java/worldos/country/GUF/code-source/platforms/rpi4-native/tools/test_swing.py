#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testSwing.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testSwing', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testSwing')
    valeurAssociation = {'wait': 'attendreFin', 'x': 'coordonnéeCoordonnéeHorizontale', 's': 'donnéesChaîne', 'i': 'indiceOrdinal', 'sel': 'Sélecteur', 'seconds': 'unitéSecondes', 'log': 'enregistrementJournal', 'data': 'Données', 'at': 'positionActuel', 'send': 'envoyer', 'main': 'lancer', 'req': 'valeurRequête', 'hot': 'valeurRaccourci', 'pump': 'évènementPoignée', 'ROOT': 'racineProjet', 'marker': 'marqueur', 'b': 'valeurDeuxième', 'command': 'commande', 'shell': 'interpréteurCommandes', 'f': 'entréeÉlémentFichier', 'click': 'boutonCliquer', 'k': 'indiceTroisième', 'c': 'codeCaractère', 'r': 'valeurRetourné', 'p': 'positionDonnées', 'command_mode': 'modeCommande', 'end': 'décalageFin', 'classes': 'cheminClasse', 'key': 'valeurEnfoncé', 'y': 'coordonnéeCoordonnéeVerticale', 'result': 'résultat', 'report': 'rapportValidation', 'dest': 'positionValeurDestination', 'work': 'cheminTravailEnCours', 'qmp': 'connexionContrôleSimulacre'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
