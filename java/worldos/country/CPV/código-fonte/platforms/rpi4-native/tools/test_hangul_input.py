#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/한글입력시험.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('한글입력시험')
    mapeamento_VALOR = {'expected': '예상결과', 'Keyboard': 'teclado', 'press': '글쇠누르기', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'teste_colar_E_UNICODE', 'data': 'dados', 'key': '누름값', 'send': 'enviar', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'símbolo_VALOR', 'char': 'dados_de_caractere', 'type': 'TIPO_área'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
