#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/예제시험.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    mapovanie_VALUE = {'count': 'položka_COUNT_8f7753a1', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'prenos_súborov_číslo_portu', 'data': 'údaje', 'graphics_command': 'grafické_prvky_príkaz', 'main': 'Spustiť_2', 'row': 'ROW_pozícia', 'init': '초기값', 'target': 'cieľová_hodnota', 'ROOT': 'akcia_koreň', 'text': 'Spracovanie_textu', 'binary': 'Binary', 'out': 'KR_údaje', 'entry': 'položka_bod', 'got': 'RECEIVED_COUNT', 'port': 'číslo_portu', 'graphics_start': 'START_kresba', 'col': 'COLUMN_pozícia', 'begin': 'START_Posun', 'kind': 'oblasť_VALUE', 'selector': 'selektor', 'n': 'položka_COUNT', 'key': '누름값', 'y': 'Y_súradnica', 'client': 'klient', 'line': 'riadok', 'report': 'overenie_správa', 'language': 'Jazyky', 'x': 'X_súradnica', 'start': 'Spustiť_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'odoslať_Zoznam', 'payload': 'údajová_časť_údaje', 'proc': 'Proces', 'w': '너비값', 'temporary': '임시자원', 'echo': 'ozvena_server_položka', 'label': 'názov_tabuľka', 'content': 'obsah_VALUE', 'argument': '전달값', 'EchoServers': 'ozvena_Servery', 'marker': 'fixka', 'expected': '예상결과', 'test_language': 'test_Jazyky', 'filename': 'Súbor_položka_názov', 'shell': '셸', 'color': '색상', 'transcript': 'prepis', 'offset': 'Posun_VALUE', 'h': '높이값', 'run': 'Vykonať_príkaz', 'c': 'bod_kódu', 'path': 'Cesta', 'encoding': 'tabuľka_znakov', 'end': 'ukončiť_hovor_Posun', 'ftp': 'prenos_súborov_kontakt', 'pixels': '화소들', 'symbol': 'symbol_VALUE', 'source': '원본자료', 'name': 'Názov', 'receive': 'dostať_e_mail', 'manifest': 'zväzok_manifest_zostáv'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
