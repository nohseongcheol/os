#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/화면요소시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('화면요소시험')
    mapare_VALUE = {'wait': '기다리기', 'x': 'coordonata_X', 's': 'șir_date', 'i': '순번', 'sel': 'selector_a916db4e', 'seconds': '초단위', 'log': 'LOG_RECORD', 'data': 'date', 'at': 'curent_poziție', 'send': 'trimite', 'main': 'Pornește', 'req': 'cerere_VALUE', 'hot': 'comandă_rapidă_VALUE', 'pump': 'handle_eveniment', 'ROOT': 'Project_rădăcină', 'marker': 'marcaj', 'b': 'SECOND_VALUE', 'command': 'Comandă', 'shell': 'shell', 'f': 'Fișier_intrare', 'click': 'clic_buton', 'k': '셋째순번', 'c': 'cod_caracter', 'r': '반환값', 'p': 'date_poziție', 'command_mode': 'comandă_mod', 'end': 'termina_un_apel_OFFSET', 'classes': 'Clasă_cale', 'key': '누름값', 'y': '세로좌표', 'result': 'KR', 'report': 'validare_raport', 'dest': 'destinație_VALUE_poziție', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
