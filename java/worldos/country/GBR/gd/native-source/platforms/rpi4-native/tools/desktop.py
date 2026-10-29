#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/deasg_seall.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('deasg_seall', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('deasg_seall')
    대응 = {'count': 'cur_a_steach_COUNT', 'special': '특수글쇠', 'error': 'Mearachd', 'exact': 'EXACT_VALUE', 'network': 'lìonra', 'closed': '닫힘', 'length': 'faid_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'frithealaiche_VALUE', 'resources': 'Goireasan', 'data': 'dàta', 'shift': 'iuchair_SHIFT', 'send': 'cuir', 'run_desktop': 'ruith_deasg', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'òstair', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'drochaid', 'kind': 'roinn_seòrsa_VALUE', 'tail': '끝부분', 'size': 'atharraich_am_meud', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'cliant', 'char': 'caractar_dàta', 'work': '작업경로', 'Keyboard': 'meur_chlàr', 'x': 'co_chomharra_x', 'down': '누르는중', 'net': 'lìonra_drochaid_cur_a_steach', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argamaid_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Pròiseas', 'Desktop': 'CONNECT_deasg', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'àithne', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Slighe', 'cp': 'caractar_còdachadh', 'terminate': '종료시키기', 'security': 'tèarainteachd', 'vnc_port': '원격화면접속번호', 'body': 'bodhaig_an_teacsa', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Iuchair_samhla', 'output': '출력결과', 'keyboard': 'meur_chlàr_cur_a_steach', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Leughadair', 'NetworkBridge': 'lìonra_drochaid', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
