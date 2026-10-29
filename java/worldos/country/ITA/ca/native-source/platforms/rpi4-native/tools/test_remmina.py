#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/원격한글시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Executa_2', 'profile': 'Perfil', 'focused': 'Prioritaris', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'servidor_VALOR', 'log': 'LOG_fila', 'args': 'arg_MATRIU', 'deadline': '마감시각', 'data': 'dades', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Executa_2', 'ready': '준비완료', 'found': 'Cerca_mesura', 'guest': 'convidat', 'ROOT': 'Project_rel', 'marker': '확인표시', 'text': 'SMS', 'out': 'mesura_dades', 'env': 'entorn', 'f': 'arxiu_introducció', 'port': 'número_de_port', 'offset': 'DESPLAÇAMENT_VALOR', 'version': '판번호', 'p': 'dades_càrrec', 'selector': '준비선택기', 'xvfb': 'virtual_mostrar', 'display': 'pantalla', 'n': 'element_COMPT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nom', 'window': 'Finestra', 'report': 'validació_informe', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
