#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testRemmina.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testRemmina', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testRemmina')
    valeurAssociation = {'wait': 'attendreFin', 'typing': 'caractèreSaisi', 'start': 'lancer', 'profile': 'profil', 'focused': 'focalisé', 'serial': 'entréeSortieSériel', 'keys': 'touchesEnfoncé', 'server': 'valeurServeur', 'log': 'enregistrementJournal', 'args': 'tableauArgument', 'deadline': 'tempsÉchéance', 'data': 'Données', 'candidate': 'candidat', 'logs': 'enregistrementsJournal', 'kw': 'argumentNommé', 'number': 'valeurNumérique', 'main': 'lancer', 'ready': 'terminéPréparation', 'found': 'chercherRésultat', 'guest': 'invité', 'ROOT': 'racineProjet', 'marker': 'marqueur', 'text': 'texte', 'out': 'donnéesRésultat', 'env': 'environnement', 'f': 'entréeÉlémentFichier', 'port': 'numéroPort', 'offset': 'valeurDécalage', 'version': 'numéroVersion', 'p': 'positionDonnées', 'selector': 'sélecteur', 'xvfb': 'présenterVirtuel', 'display': 'périphériquePrésenter', 'n': 'nombreÉlémentsÉlémentListe', 'key': 'valeurEnfoncé', 'processes': 'processusListeEnExécution', 'rootfs': 'systèmeFichiersRacine', 'xdo': 'outilEntréeVirtuel', 'name': 'nom', 'window': 'fenêtre', 'report': 'rapportValidation', 'work': 'cheminTravailEnCours'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
