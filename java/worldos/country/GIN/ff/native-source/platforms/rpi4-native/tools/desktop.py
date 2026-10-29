#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/biro_kollal.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('biro_kollal', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('biro_kollal')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'juumre', 'exact': '정확한값', 'network': 'laylaytol', 'closed': '닫힘', 'length': 'njuuteendi_njaru', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'sarworde_njaru', 'resources': 'Ɓulnorɗe', 'data': 'keɓe', 'shift': 'feɗoode_SHIFT', 'send': 'neldude', 'run_desktop': 'huutoraade_biro', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'njaatigi', 'text': 'binndi', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'kategorii_njaru', 'tail': '끝부분', 'size': 'waylude_etannde', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'kiliyaan', 'char': 'alkulal_keɓe', 'work': '작업경로', 'Keyboard': 'tappirde', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': '인수배열', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Yuɓɓo_golle', 'Desktop': 'seŋaade_biro', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'waylude_modd', 'command': 'ginol', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'laawol', 'cp': 'alkulal_dokkagol', 'terminate': '종료시키기', 'security': 'kisal', 'vnc_port': '원격화면접속번호', 'body': '본문', 'index': '색인', 'exited': '종료됨', 'keysym': '글쇠기호', 'output': '출력결과', 'keyboard': 'tappirde_naatnugol', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Tarirgal', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
