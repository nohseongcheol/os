#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/desktop_vizualiza.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('desktop_vizualiza', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('desktop_vizualiza')
    mapare_VALUE = {'count': 'intrare_COUNT', 'special': '특수글쇠', 'error': 'eroare', 'exact': 'EXACT_VALUE', 'network': 'rețea', 'closed': '닫힘', 'length': 'lungime_VALUE', 'opened': '열림', 'ftp_port': 'transfer_de_fișiere_număr_port', 'server': 'server_VALUE', 'resources': 'Resurse', 'data': 'date', 'shift': '윗글쇠', 'send': 'trimite', 'run_desktop': 'rula_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'gazdă', 'text': 'SMS', 'korean': '한글여부', 'port': 'număr_port', 'signum': '신호번호', 'version': 'număr_de_versiune', 'parser': 'parser', 'bridge': 'punte', 'kind': 'zonă_VALUE', 'tail': '끝부분', 'size': 'Mărime', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'client', 'char': 'date_de_tip_caracter', 'work': '작업경로', 'Keyboard': 'tastatură', 'x': 'coordonata_X', 'down': '누르는중', 'net': 'punte_intrare', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proces', 'Desktop': 'conecta_desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': 'Anteriorul', 'toggle': 'SWITCH_mod', 'command': 'Comandă', 'sock': '소켓', 'frame': 'executare_cadru', 'ctrl': 'control_Cheie', 'path': 'Cale', 'cp': 'codificare_caractere', 'terminate': '종료시키기', 'security': 'Securitate', 'vnc_port': '원격화면접속번호', 'body': 'text_corp', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Cheie_simbol', 'output': '출력결과', 'keyboard': 'tastatură_intrare', 'interrupted': '가로채기됨', 'listener': 'primi_muta', 'reader': 'Reader', 'NetworkBridge': 'punte_3de4fe3a', 'gui': '그림화면', 'worker': 'procesare_sarcină'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
