#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construireEspaceUtilisateur.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construireEspaceUtilisateur', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construireEspaceUtilisateur')
    valeurAssociation = {'mode': 'modeMéthode', 'header': 'valeurEntête', 'i': 'indiceOrdinal', 'build_ccompiler': 'créerCompilateurC', 'ar': 'outilArchive', 'posix': 'pOSIX', 'payload': 'donnéesChargeUtile', 'flags': 'bitsConfiguration', 'cases': 'testCas', 'cc': 'CompilateurC', 'data': 'Données', 'build_java_library': 'créerBibliothèqueJava', 'ld': 'outilÉditeurLiens', 'repo': 'cheminDépôt', 'build_python': 'créerPython', 'inc': 'cheminInclure', 'argument': 'valeurTransféré', 'text': 'texte', 'headers': 'listeEntête', 'cxx': 'compilateurCpp', 'valid': 'valide', 'build': 'construire', 'build_users': 'créerEspaceUtilisateur', 'compiler': 'outilCompilateur', 'uzlib': 'bibliothèqueDécompression', 'extra': 'régionSupplémentaire', 'phoff': 'décalageEntêteProgramme', 'offset': 'valeurDécalage', 'text_address': 'adresseCommande', 'abi': 'ABIAppel', 'assembly': 'assembleur', 'run': 'exécuterCommande', 'path': 'chemin', 'p': 'positionDonnées', 'changed': 'changé', 'n': 'nombreÉlémentsÉlémentListe', 'flag': 'valeurRéglages', 'index': 'indiceRechercher', 'classes': 'cheminClasse', 'output': 'sortie', 'loads': 'chargements', 'data_address': 'adresseDonnées', 'symbol': 'valeurSymbole', 'root': 'adresseRacine', 'patches': 'modifications', 'source': 'donnéesOriginal', 'sizes': 'tailles', 'blobs': 'blocsBinaires', 'name': 'nom', 'value': 'valeur', 'fmt': 'formatDonnées', 'work': 'cheminTravailEnCours'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
