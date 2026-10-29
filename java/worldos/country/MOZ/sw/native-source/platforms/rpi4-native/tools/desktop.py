#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/Eneo_kazi_Onesha.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('Eneo_kazi_Onesha', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Eneo_kazi_Onesha')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'kosa', 'exact': '정확한값', 'network': 'Mtandao', 'closed': '닫힘', 'length': 'urefu_thamani', 'opened': '열림', 'ftp_port': 'faili_hamisha_namba_ya_kituo', 'server': 'seva_thamani', 'resources': 'Rasilimali', 'data': 'data', 'shift': 'kibonye_SHIFT', 'send': 'tuma', 'run_desktop': 'endesha_Eneo_kazi', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'mwenyeji', 'text': 'SMS', 'korean': '한글여부', 'port': 'namba_ya_kituo', 'signum': '신호번호', 'version': '판번호', 'parser': 'kichanganuzi', 'bridge': 'daraja', 'kind': 'kategoria_thamani', 'tail': '끝부분', 'size': 'panga_ukubwa', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Kitufe_cha_Y_kiratibu', 'prefix': '앞부분', 'client': 'teja', 'char': 'kibambo_data', 'work': '작업경로', 'Keyboard': 'kibodi', 'x': 'jira_x', 'down': '누르는중', 'net': 'Mtandao_daraja_ingizo', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'hoja_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Mchakato', 'Desktop': 'UNGANISHA_Eneo_kazi', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'badili_hali_tumizi', 'command': 'amri', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'Ctrl', 'path': 'njia', 'cp': 'kibambo_usimbaji', 'terminate': '종료시키기', 'security': 'Usalama', 'vnc_port': '원격화면접속번호', 'body': 'Matini_kiini', 'index': '색인', 'exited': '종료됨', 'keysym': 'Kitufe_ishara', 'output': '출력결과', 'keyboard': 'kibodi_ingizo', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'msomaji', 'NetworkBridge': 'Mtandao_daraja', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
