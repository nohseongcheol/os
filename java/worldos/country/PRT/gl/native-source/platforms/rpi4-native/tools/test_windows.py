#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/창시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'X_coordenada', 's': 'cadea_datos', 'xy': 'par_de_coordenadas', 'sel': '선택기', 'seconds': '초단위', 'log': 'LOG_fila', 'at': 'ao_corrente_cargo', 'send': 'enviar', 'main': 'Executar_2', 'req': 'solicitude_VALOR', 'hot': 'atallo_VALOR', 'pump': 'agarradoira_evento', 'ROOT': 'Project_raíz', 'marker': '확인표시', 'b': 'SEGUNDO_VALOR', 'command': 'Orde', 'shell': 'shell', 'f': 'Ficheiro_introdución', 'color': '색상', 'click': 'clic_botón', 'k': '셋째순번', 'c': 'código_de_carácter', 'r': '반환값', 'p': 'datos_cargo', 'done': 'Completadas_cantidade', 'end': 'finalizar_DESPRAZAMENTO', 'command_mode': 'comando_MODO', 'key': '누름값', 'y': 'Y_coordenada', 'pixels': '화소들', 'result': 'RESULTANTE', 'report': 'validación_informe', 'dest': 'destino_VALOR_cargo', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
