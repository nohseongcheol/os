#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construireSystème.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construireSystème', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construireSystème')
    valeurAssociation = {'network': 'réseau', 'BUILD': 'construireChemin', 'ar': 'outilArchive', 'build_examples': 'créerRecueilExemples', 'posix': 'pOSIX', 'font_data': 'donnéesPolice', 'flags': 'bitsConfiguration', 'a': 'valeurPremier', 'cc': 'CompilateurC', 'args': 'tableauArgument', 'source_flags': 'configurationOriginal', 'ld': 'outilÉditeurLiens', 'method': 'entréeÉlémentMéthode', 'main': 'lancer', 'objcopy': 'convertisseurFichierObjet', 'ROOT': 'racineProjet', 'cxx': 'compilateurCpp', 'includes': 'inclusions', 'compiler': 'outilCompilateur', 'build_users': 'créerEspaceUtilisateur', 'f': 'entréeÉlémentFichier', 'extra': 'régionSupplémentaire', 'exports': 'tableExporter', 'jobs': 'construireTravaux', 'run': 'exécuterCommande', 'path': 'chemin', 'REPO': 'racineDépôt', 'tool': 'Outils', 'classes': 'cheminClasse', 'output': 'sortie', 'samples': 'entréesListeExemple', 'symbol': 'valeurSymbole', 'source': 'donnéesOriginal', 'name': 'nom', 'build_network': 'créerRéseau', 'font_info': 'informationPolice', 'manifest': 'manifesteLot', 'work': 'cheminTravailEnCours'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
