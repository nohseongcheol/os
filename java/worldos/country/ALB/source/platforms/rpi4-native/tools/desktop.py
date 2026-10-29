#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/desktop_Pamja.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('desktop_Pamja', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('desktop_Pamja')
    대응 = {'count': 'futje_COUNT', 'special': '특수글쇠', 'error': 'GABIM', 'exact': 'EXACT_VALUE', 'network': 'rrjet', 'closed': '닫힘', 'length': 'gjatësi_VALUE', 'opened': '열림', 'ftp_port': 'skedar_transferim_numri_i_portës', 'server': 'server_VALUE', 'resources': 'Burimet', 'data': 'të_dhëna', 'shift': 'tasti_SHIFT', 'send': 'dërgoj', 'run_desktop': 'varg_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'pritës', 'text': 'Teksti', 'korean': '한글여부', 'port': 'numri_i_portës', 'signum': '신호번호', 'version': '판번호', 'parser': 'analizues', 'bridge': 'urë', 'kind': 'kategori_VALUE', 'tail': '끝부분', 'size': 'Madhësi', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinatë', 'prefix': '앞부분', 'client': 'klient', 'char': 'karakter_të_dhëna', 'work': '작업경로', 'Keyboard': 'tastiera', 'x': 'koordinata_x', 'down': '누르는중', 'net': 'rrjet_urë_futje', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proçes', 'Desktop': 'Lidh_desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Komanda', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'POZICIONI', 'cp': 'karakter_enkodim', 'terminate': '종료시키기', 'security': 'siguri', 'vnc_port': '원격화면접속번호', 'body': 'trupi_i_tekstit', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'tast_simbol', 'output': '출력결과', 'keyboard': 'tastiera_futje', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'lexues', 'NetworkBridge': 'rrjet_urë', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
