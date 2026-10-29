#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/escriptori_visualitzar.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('escriptori_visualitzar', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('escriptori_visualitzar')
    대응 = {'count': 'introducció_COMPT', 'special': '특수글쇠', 'error': 's_ha_produït_un_error', 'exact': 'IGUAL_VALOR', 'network': 'xarxa', 'closed': '닫힘', 'length': 'durada_VALOR', 'opened': '열림', 'ftp_port': 'transferència_de_fitxers_número_de_port', 'server': 'servidor_VALOR', 'resources': 'Recursos', 'data': 'dades', 'shift': 'tecla_Maj', 'send': 'enviar', 'run_desktop': 'execució_escriptori', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'allotjar', 'text': 'SMS', 'korean': '한글여부', 'port': 'número_de_port', 'signum': '신호번호', 'version': '판번호', 'parser': 'analitzador', 'bridge': 'pont', 'kind': 'Categoria_VALOR', 'tail': '끝부분', 'size': 'Mida', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_coordenada', 'prefix': '앞부분', 'client': 'client', 'char': 'caràcter_dades', 'work': '작업경로', 'Keyboard': 'teclat', 'x': 'X_coordenada', 'down': '누르는중', 'net': 'xarxa_pont_introducció', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'arg_MATRIU', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Procés', 'Desktop': 'CONNECTA_escriptori', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'canvi_MODA', 'command': 'Ordre', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'Control', 'path': 'Camí', 'cp': 'caràcter_codificació', 'terminate': '종료시키기', 'security': 'Seguretat', 'vnc_port': '원격화면접속번호', 'body': 'text_del_cos', 'index': 'Cerca_INDEX', 'exited': '종료됨', 'keysym': 'Clau_símbol', 'output': '출력결과', 'keyboard': 'teclat_introducció', 'interrupted': '가로채기됨', 'listener': 'rebre_port', 'reader': 'Lector', 'NetworkBridge': 'xarxa_pont', 'gui': '그림화면', 'worker': 'processament_tasca'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
