#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/testEntréeHangul.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('testEntréeHangul', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('testEntréeHangul')
    valeurAssociation = {'expected': 'attendu', 'Keyboard': 'Clavier', 'press': 'toucheEnfoncer', 'self': 'valeurSoi', 'test_modes_repeat_and_commit': 'testConfirmerEtRépéterModes', 'keys': 'touchesEnfoncé', 'test_paste_and_unicode': 'testUnicodeEtColler', 'data': 'Données', 'key': 'valeurEnfoncé', 'send': 'envoyer', 'test_words': 'testMots', 'InputTests': 'testEntréeHangul', 'test_backspace': 'testRetourArrière', 'symbol': 'valeurSymbole', 'char': 'donnéesCaractère', 'type': 'catégorieType'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
