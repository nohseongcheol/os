#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/executa_Fișier.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('executa_Fișier', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('executa_Fișier')
    mapare_VALUE = {'timeout': 'executare_TIMEOUT', 's': 'șir_date', 'i': '순번', 'match': '일치', 'files': 'Fișier_Listă', 'program': 'program', 'executable': '실행가능파일', 'args': 'argument_ARRAY', 'chunk': '조각', 'data': 'date', 'proc': 'Proces', 'send': 'trimite', 'main': 'Pornește', 'marker': 'marcaj', 'command': 'Comandă', 'include': 'include', 'dumped': '갈무리자료', 'run': 'executa_comandă', 'p': 'date_poziție', 'parser': 'parser', 'options': 'Opțiuni', 'kind': 'zonă_VALUE', 'selector': 'selector', 'upload_data': 'Upload_date', 'end': 'termina_un_apel_OFFSET', 'n': 'element_COUNT', 'd': 'destinație_date', 'key': '누름값', 'output': '출력결과', 'line': 'Linie', 'name': 'Nume', 'upload_name': 'Upload_nume', 'receive': 'primi_mesaj'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
