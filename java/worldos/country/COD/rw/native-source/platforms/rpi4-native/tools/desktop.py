#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/biro_igaragaza.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('biro_igaragaza', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('biro_igaragaza')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'IKOSA', 'exact': '정확한값', 'network': 'Urusobemiyoboro', 'closed': '닫힘', 'length': 'uburebure_agaciro', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'seriveri_agaciro', 'resources': 'Ibikoresho_50487cae', 'data': 'amakurushingiro', 'shift': 'buto_SHIFT', 'send': 'kohereza', 'run_desktop': 'ihuriro_biro', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'gucumbikira', 'text': 'Umwandiko', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'icyiciro_agaciro', 'tail': '끝부분', 'size': 'Ingano', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'umukiriya', 'char': 'inyuguti_amakurushingiro', 'work': '작업경로', 'Keyboard': 'mwandikisho', 'x': 'Ihuza_rya_x', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ingingo_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Inzira_a7054519', 'Desktop': 'Guhuza_biro', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'guhinduranya_uburyo', 'command': 'Icyo_wifuza', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Inzira', 'cp': 'inyuguti_gusobeka', 'terminate': '종료시키기', 'security': 'Umutekano', 'vnc_port': '원격화면접속번호', 'body': 'igihimba_cy_umwandiko', 'index': '색인', 'exited': '종료됨', 'keysym': 'buto_ikimenyetso', 'output': '출력결과', 'keyboard': 'mwandikisho_icyinjizwa', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Musomyi', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
