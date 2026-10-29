#!/usr/bin/env python3
"""기존 SLÓÐ 호환 færsla_P. raun_gögn 구현: ../Verkfæri/skjáborð_Sýn.py"""
import importlib as TAKE_VALUE
import sys as stýrikerfi_VALUE
from pathlib import Path as SLÓÐ
stýrikerfi_VALUE.path.insert(0, str(SLÓÐ(__file__).resolve().parents[1] / 'Verkfæri'))
if __name__ == '__main__':
    import runpy as forrit_ræsir
    forrit_ræsir.run_module('skjáborð_Sýn', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('skjáborð_Sýn')
    vörpun_VALUE = {'count': 'færsla_COUNT', 'special': '특수글쇠', 'error': 'Villa', 'exact': 'EXACT_VALUE', 'network': 'Net', 'closed': 'upplýsingatækni_lokað', 'length': 'lengd_VALUE', 'opened': '열림', 'ftp_port': 'skrá_flytja_tengisnúmer', 'server': 'þjónn_VALUE', 'resources': 'Tilföng', 'data': 'gögn', 'shift': 'SHIFT_lykill', 'send': 'senda', 'run_desktop': 'runa_skjáborð', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'hýsa', 'text': 'Texti', 'korean': '한글여부', 'port': 'tengisnúmer', 'signum': 'merki_númer', 'version': 'útgáfa_númer', 'parser': 'þáttari', 'bridge': 'brú', 'kind': 'tegund_VALUE', 'tail': '끝부분', 'size': 'Stærð', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_hnit', 'prefix': '앞부분', 'client': 'biðlari', 'char': 'stafur_gögn', 'work': '작업경로', 'Keyboard': 'lyklaborð', 'x': 'x_hnit', 'down': '누르는중', 'net': 'Net_brú_færsla', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'frumbreyta_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Ferli', 'Desktop': 'TENGJA_skjáborð', 'buttons': '단추들', 'thread': 'starfskraftur', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Skipun', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'SLÓÐ', 'cp': 'stafur_kóðun', 'terminate': '종료시키기', 'security': 'Öryggi', 'vnc_port': '원격화면접속번호', 'body': 'meginmál', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Lykill_tákn', 'output': 'úttak_54cd5e1d', 'keyboard': 'lyklaborð_færsla', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Lesari', 'NetworkBridge': 'Net_brú', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in vörpun_VALUE.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
