#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/창시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'X_coordenada', 's': 'cadena_dades', 'xy': 'coordenada_enllaçar', 'sel': '선택기', 'seconds': '초단위', 'log': 'LOG_fila', 'at': '현재위치', 'send': 'enviar', 'main': 'Executa_2', 'req': 'sol_licitud_VALOR', 'hot': 'drecera_VALOR', 'pump': 'control_incidència', 'ROOT': 'Project_rel', 'marker': '확인표시', 'b': 'SEGON_VALOR', 'command': 'Ordre', 'shell': 'shell', 'f': 'arxiu_introducció', 'color': '색상', 'click': 'clic_botó', 'k': '셋째순번', 'c': 'codi_de_caràcter', 'r': '반환값', 'p': 'dades_càrrec', 'done': 'Completades_quantitat', 'end': 'finalitzar_DESPLAÇAMENT', 'command_mode': 'ordre_MODA', 'key': '누름값', 'y': 'Y_coordenada', 'pixels': '화소들', 'result': 'RESULTAT', 'report': 'validació_informe', 'dest': 'destinació_VALOR_càrrec', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
