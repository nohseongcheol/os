#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/generar_Terminal_tipus_de_lletra.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('generar_Terminal_tipus_de_lletra', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('generar_Terminal_tipus_de_lletra')
    대응 = {'data': 'dades', 'img': 'dibuix_VALOR', 'bits': 'Servei_de_transferència_intel_ligent_en_segon_terme_Llista', 'x': 'X_coordenada', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'camí_Llista', 'y': 'Y_coordenada', 'main': 'Executa_2', 'src': '원본주소', 'fonts': 'tipus_de_lletra_Llista', 'ROOT': 'Project_rel', 'p': 'dades_càrrec', 'cp': 'caràcter_codificació', 'target': 'objectiu'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
