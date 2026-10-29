#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/한글입력.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('한글입력')
    mapeamento_VALOR = {'old': 'Anterior_item', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Chave_Layout', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'commit_composição', 'feed': 'feed_Chave', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'enviar', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Histórico', 'pair': '한쌍', 'char': 'dados_de_caractere', 'VOWEL': '가운뎃소리목록', 'right': 'DIREITA', 'value': 'VALOR', 'text': 'texto'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
