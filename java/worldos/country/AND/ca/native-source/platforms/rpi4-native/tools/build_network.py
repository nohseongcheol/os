#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/generar_xarxa.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('generar_xarxa', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('generar_xarxa')
    대응 = {'obj': 'fitxer_de_destinació', 'objects': 'destinació_Fitxers', 'library': 'biblioteca', 'output': '출력결과', 'port': 'número_de_port', 'root': 'rel_ADREÇA', 'files': 'arxiu_Llista', 'source': '원본자료', 'run': 'Executa_ordre', 'flags': 'configuració_Servei_de_transferència_intel_ligent_en_segon_terme', 'path': 'Camí', 'build_network': 'Crear_xarxa', 'cc': '시언어번역기', 'ar': 'Arxiu_eina'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
