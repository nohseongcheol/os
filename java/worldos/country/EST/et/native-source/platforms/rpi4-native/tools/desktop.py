#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/töölaud_Kuva.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('töölaud_Kuva', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('töölaud_Kuva')
    vastendamine_VALUE = {'count': 'kirje_COUNT', 'special': '특수글쇠', 'error': 'VIGA', 'exact': 'EXACT_VALUE', 'network': 'võrk', 'closed': 'infotehnoloogia_suletud', 'length': '길이', 'opened': '열림', 'ftp_port': 'failiedastus_pordinumber', 'server': 'server_VALUE', 'resources': 'Ressursid', 'data': 'andmed', 'shift': '윗글쇠', 'send': 'saatma', 'run_desktop': 'sari_töölaud', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'Tekst', 'korean': '한글여부', 'port': 'pordinumber', 'signum': 'signaal_number', 'version': 'versiooninumber', 'parser': 'parser', 'bridge': 'sild', 'kind': 'ala_VALUE', 'tail': '끝부분', 'size': 'Suurus', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klient', 'char': 'tähemärgiandmed', 'work': '작업경로', 'Keyboard': 'klaviatuur', 'x': '가로좌표', 'down': '누르는중', 'net': 'sild_kirje', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Protsess', 'Desktop': 'Ühenda_töölaud', 'buttons': '단추들', 'thread': 'töötaja', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Käsk', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'meede_Võti', 'path': 'RADA', 'cp': 'märk_kodeerimine', 'terminate': '종료시키기', 'security': 'Turve', 'vnc_port': '원격화면접속번호', 'body': 'sisu_SMS', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Võti_sümbol', 'output': 'toodang', 'keyboard': 'klaviatuur_kirje', 'interrupted': '가로채기됨', 'listener': 'saama_port', 'reader': 'Reader', 'NetworkBridge': 'sild_3de4fe3a', 'gui': '그림화면', 'worker': 'töötlemine_tööüksus'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
