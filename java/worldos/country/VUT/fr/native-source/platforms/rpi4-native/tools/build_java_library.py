#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/construireBibliothèqueJava.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('construireBibliothèqueJava', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('construireBibliothèqueJava')
    valeurAssociation = {'header': 'valeurEntête', 'sources': 'ListeSources', 'i': 'indiceOrdinal', 'info': 'informationSystème', 'payload': 'donnéesChargeUtile', 'src': 'adresseOriginal', 'run': 'exécuterCommande', 'build_java_library': 'créerBibliothèqueJava', 'relative': 'cheminRelatif', 'classes': 'cheminClasse', 'dist': 'cheminDistribution', 'archive': 'archive', 'output': 'sortie', 'root': 'adresseRacine', 'name': 'nom', 'jar': 'lotJava', 'b': 'valeurDeuxième', 'entries': 'listeEntréesListe'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
