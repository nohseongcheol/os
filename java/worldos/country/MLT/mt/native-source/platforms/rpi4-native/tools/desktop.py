#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/desktop_wera.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('desktop_wera', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('desktop_wera')
    대응 = {'count': 'entrata_COUNT', 'special': '특수글쇠', 'error': 'żball', 'exact': 'EXACT_VALUE', 'network': 'netwerk', 'closed': '닫힘', 'length': 'tul_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'server_VALUE', 'resources': 'Riżorsi', 'data': 'data', 'shift': 'tast_SHIFT', 'send': 'bagħat', 'run_desktop': 'serje_desktop', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'pont', 'kind': 'kategorija_VALUE', 'tail': '끝부분', 'size': 'daqqas', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klijent', 'char': 'karattru_data', 'work': '작업경로', 'Keyboard': 'tastiera', 'x': 'koordinat_x', 'down': '누르는중', 'net': 'netwerk_pont_entrata', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proċess', 'Desktop': 'AQBAD_desktop', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'qaleb_MODE', 'command': 'kmand', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'mogħdija', 'cp': 'karattru_kodifikar', 'terminate': '종료시키기', 'security': 'Sigurtà', 'vnc_port': '원격화면접속번호', 'body': 'il_korp_tat_test', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'tast_simbolu', 'output': '출력결과', 'keyboard': 'tastiera_entrata', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Qarrej', 'NetworkBridge': 'netwerk_pont', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
