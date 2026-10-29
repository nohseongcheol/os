#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/deasc_Amharc.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('deasc_Amharc', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('deasc_Amharc')
    대응 = {'count': 'iontráil_COUNT', 'special': '특수글쇠', 'error': 'ERREÁID', 'exact': 'EXACT_VALUE', 'network': 'Líonra', 'closed': '닫힘', 'length': 'fad_VALUE', 'opened': '열림', 'ftp_port': 'comhad_traschur_uimhir_phoirt', 'server': 'freastalaí_VALUE', 'resources': 'Acmhainní', 'data': 'sonraí', 'shift': 'eochair_SHIFT', 'send': 'seol', 'run_desktop': 'rith_deasc', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'óstach', 'text': 'Téacs', 'korean': '한글여부', 'port': 'uimhir_phoirt', 'signum': '신호번호', 'version': 'uimhir_an_leagain', 'parser': '인수해석기', 'bridge': 'traschóiritheoir', 'kind': 'catagóir_VALUE', 'tail': '끝부분', 'size': 'Méid', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'cliant', 'char': 'carachtar_sonraí', 'work': '작업경로', 'Keyboard': 'méarchlár', 'x': 'x_chomhordanáid', 'down': '누르는중', 'net': 'Líonra_traschóiritheoir_iontráil', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argóint_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Próiseas', 'Desktop': 'nasc_deasc', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_mód', 'command': 'Ordú', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'CONAIR', 'cp': 'carachtar_ionchódú', 'terminate': '종료시키기', 'security': 'Slándáil', 'vnc_port': '원격화면접속번호', 'body': 'corpthéacs', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'eochair_siombail', 'output': '출력결과', 'keyboard': 'méarchlár_iontráil', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Léitheoir', 'NetworkBridge': 'Líonra_traschóiritheoir', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
