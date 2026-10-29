#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/papamahi_tiro.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('papamahi_tiro', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('papamahi_tiro')
    대응 = {'count': 'tāurunga_COUNT', 'special': '특수글쇠', 'error': 'Pōhēhē', 'exact': 'EXACT_uara', 'network': 'whatunga', 'closed': '닫힘', 'length': 'roa_uara', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'tūmau_uara', 'resources': 'Ngā_Rauemi', 'data': 'raraunga', 'shift': 'pātuhi_NEKE', 'send': 'tuku', 'run_desktop': 'whakahaere_papamahi', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'taurima', 'text': 'Ngā_kupu', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'arawhata', 'kind': 'kāwai_uara', 'tail': '끝부분', 'size': 'rahi', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'kiritaki', 'char': 'pūāhua_raraunga', 'work': '작업경로', 'Keyboard': 'papapātuhi', 'x': 'taunga_x', 'down': '누르는중', 'net': 'whatunga_arawhata_tāurunga', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'tohenga_HUĀNGA', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Hātepe', 'Desktop': 'TŪHONO_papamahi', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'tono', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'MANA', 'path': 'ara', 'cp': 'pūāhua_whakawaehere', 'terminate': '종료시키기', 'security': 'Haumarutanga', 'vnc_port': '원격화면접속번호', 'body': 'kuputuhi_tinana', 'index': 'Rapu_INDEX', 'exited': '종료됨', 'keysym': 'kī_tohu', 'output': '출력결과', 'keyboard': 'papapātuhi_tāurunga', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Pūpānui', 'NetworkBridge': 'whatunga_arawhata', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
