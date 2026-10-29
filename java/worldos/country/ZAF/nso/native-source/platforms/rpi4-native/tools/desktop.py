#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/teskethopo_pogelo.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('teskethopo_pogelo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('teskethopo_pogelo')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Phošo', 'exact': '정확한값', 'network': 'Netweke', 'closed': '닫힘', 'length': 'botelele_boleng', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'seba_boleng', 'resources': 'Methopo', 'data': 'data', 'shift': 'khii_ya_SHIFT', 'send': 'Romela', 'run_desktop': 'sepetša_teskethopo', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'go_nea_ditirelo', 'text': 'Sengwalwa', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'kgokaganyo', 'kind': 'legoro_boleng', 'tail': '끝부분', 'size': 'Bogolo', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klaente', 'char': 'tlhaka_data', 'work': '작업경로', 'Keyboard': 'khiipote', 'x': 'kamano_ya_x', 'down': '누르는중', 'net': 'Netweke_kgokaganyo_go_tsenya_tshedimošo', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'akumente_arei', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'tiragalo_a7054519', 'Desktop': 'KGOKAGANYA_teskethopo', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'fetogela_mokgwa', 'command': 'Taelo', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Tsejana', 'cp': 'tlhaka_go_enkhouta', 'terminate': '종료시키기', 'security': 'Tšhireletšo', 'vnc_port': '원격화면접속번호', 'body': 'mmele_wa_sengwalwa', 'index': '색인', 'exited': '종료됨', 'keysym': 'khii_leswao', 'output': '출력결과', 'keyboard': 'khiipote_go_tsenya_tshedimošo', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'mmadi', 'NetworkBridge': 'Netweke_kgokaganyo', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
