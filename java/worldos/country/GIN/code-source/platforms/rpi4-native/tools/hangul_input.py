#!/usr/bin/env python3
"""기존 chemin 호환 pointEntréeÉlément. donnéesEffectif réalisation: ../Outils/entréeHangul.py"""
import importlib as valeurPrendre
import sys as valeurSystèmeExploitation
from pathlib import Path as chemin
valeurSystèmeExploitation.path.insert(0, str(chemin(__file__).resolve().parents[1] / 'Outils'))
if __name__ == '__main__':
    import runpy as LanceurProgramme
    LanceurProgramme.run_module('entréeHangul', run_name='__main__', alter_sys=True)
else:
    réalisation = valeurPrendre.import_module('entréeHangul')
    valeurAssociation = {'old': 'élémentListePrécédentÉlément', 'backspace': 'retourArrière', 'committed': 'validé', 'KEYS': 'dispositionTouche', 'self': 'valeurSoi', 'FINALS': 'lettreHangulFinalComposéMot', 'VOWELS': 'lettreHangulVoyelleMédianeComposéMot', 'INITIAL': 'tableLettreHangulInitialValeur', 'initial': 'lettreHangulInitialValeur', 'commit': 'compositionConfirmer', 'feed': 'toucheAlimenter', 'vowel': 'lettreHangulVoyelleMédiane', 'Hangul': 'composerHangul', 'SPLIT': 'séparerLettreHangulFinal', 'final': 'lettreHangulFinal', 'key': 'valeurEnfoncé', 'send': 'envoyer', 'left': 'côtéGauche', 'FINAL': 'tableLettreHangulFinal', 'history': 'historique', 'pair': 'paireUn', 'char': 'donnéesCaractère', 'VOWEL': 'tableLettreHangulVoyelleMédiane', 'right': 'droit', 'value': 'valeur', 'text': 'texte'}
    for élémentListePrécédentÉlément, élémentListeActuel in valeurAssociation.items():
        if hasattr(réalisation, élémentListeActuel): globals()[élémentListePrécédentÉlément] = getattr(réalisation, élémentListeActuel)
