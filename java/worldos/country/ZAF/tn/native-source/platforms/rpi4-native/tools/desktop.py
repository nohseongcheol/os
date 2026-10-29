#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/desekethopo_Tebego.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('desekethopo_Tebego', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('desekethopo_Tebego')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'phoso', 'exact': '정확한값', 'network': 'Neteweke', 'closed': '닫힘', 'length': 'boleele_Boleng', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'sefara_Boleng', 'resources': 'Ditsompelo', 'data': 'tshedimosetso', 'shift': 'taetsi_ya_SHIFT', 'send': 'romela', 'run_desktop': 'dirisa_desekethopo', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'pinagare', 'text': 'SMS', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'leborogo', 'kind': 'setlhopha_Boleng_4b6d6445', 'tail': '끝부분', 'size': 'lekanya', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'sedirelwa', 'char': 'Letshwao_tshedimosetso', 'work': '작업경로', 'Keyboard': 'Khiiboto', 'x': 'kgokagano_ya_x', 'down': '누르는중', 'net': 'Neteweke_leborogo_tsenyo', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'Thulaganyo_setlhopha', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Thulaganyo', 'Desktop': 'Golaganya_desekethopo', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'fetola_mokgwa', 'command': 'Taelo', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'tsela', 'cp': 'Letshwao_khoutufatso', 'terminate': '종료시키기', 'security': 'tshireletso', 'vnc_port': '원격화면접속번호', 'body': 'diteng_tsa_mokwalo', 'index': '색인', 'exited': '종료됨', 'keysym': 'taetsi_letshwao', 'output': '출력결과', 'keyboard': 'Khiiboto_tsenyo', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'mmuisi', 'NetworkBridge': 'Neteweke_leborogo', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
