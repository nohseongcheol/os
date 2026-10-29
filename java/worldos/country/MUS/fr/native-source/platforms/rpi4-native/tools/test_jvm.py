#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testJVM.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testJVM', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testJVM')
    valeurAssociation = {'message': 'texteNotification', 's': 'donnéesChaîne', 'actual': 'résultatEffectif', 'match': 'estÉgal', 'payload': 'donnéesChargeUtile', 'cases': 'testCas', 'fixture': 'testDonnées', 'main': 'lancer', 'ROOT': 'racineProjet', 'text': 'texte', 'valid': 'valide', 'includes': 'inclusions', 'include': 'inclure', 'expected': 'attendu', 'sources': 'ListeSources', 'tmp': 'cheminTemporaire', 'done': 'montantAchevé', 'classes': 'cheminClasse', 'output': 'sortie', 'result': 'résultat', 'cmd': 'argumentsCommande', 'name': 'nom', 'jar': 'lotJava', 'report': 'rapportValidation', 'tests': 'testListe'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
