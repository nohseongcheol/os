#!/usr/bin/env python3
"""기존 LLWYBR 호환 cofnod_p. go_iawn_data 구현: ../Offer/bwrdd_gwaith_Gwedd.py"""
import importlib as TAKE_VALUE
import sys as system_weithredu_VALUE
from pathlib import Path as LLWYBR
system_weithredu_VALUE.path.insert(0, str(LLWYBR(__file__).resolve().parents[1] / 'Offer'))
if __name__ == '__main__':
    import runpy as Rhaglen_lansiwr
    Rhaglen_lansiwr.run_module('bwrdd_gwaith_Gwedd', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bwrdd_gwaith_Gwedd')
    대응 = {'count': 'cofnod_COUNT', 'special': '특수글쇠', 'error': 'Gwall', 'exact': 'EXACT_VALUE', 'network': 'Rhwydwaith', 'closed': '닫힘', 'length': 'hyd_VALUE', 'opened': '열림', 'ftp_port': 'ffeil_trosglwyddo_rhif_porth', 'server': 'gweinydd_VALUE', 'resources': 'Adnoddau', 'data': 'data', 'shift': 'bysell_SHIFT', 'send': 'anfon', 'run_desktop': 'rhedeg_bwrdd_gwaith', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'lletya', 'text': 'Testun', 'korean': '한글여부', 'port': 'rhif_porth', 'signum': '신호번호', 'version': 'rhif_fersiwn', 'parser': '인수해석기', 'bridge': 'pont', 'kind': 'ardal_VALUE', 'tail': '끝부분', 'size': 'Maint', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_cyfesuryn', 'prefix': '앞부분', 'client': 'cleient', 'char': 'nod_data', 'work': '작업경로', 'Keyboard': 'allweddell', 'x': 'cyfesuryn_x', 'down': '누르는중', 'net': 'Rhwydwaith_pont_cofnod', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'arg_ARAE', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proses', 'Desktop': 'Cysylltu_bwrdd_gwaith', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'newid_MODE', 'command': 'Gorchymyn', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'LLWYBR', 'cp': 'nod_amgodio', 'terminate': '종료시키기', 'security': 'Diogelwch', 'vnc_port': '원격화면접속번호', 'body': 'corff_y_testun', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'bysell_symbol', 'output': '출력결과', 'keyboard': 'allweddell_cofnod', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'darllenwr', 'NetworkBridge': 'Rhwydwaith_pont', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
