#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/generar_sistema.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('generar_sistema', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('generar_sistema')
    대응 = {'network': 'xarxa', 'BUILD': 'generar_camí', 'ar': 'Arxiu_eina', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'tipus_de_lletra_dades', 'flags': 'configuració_Servei_de_transferència_intel_ligent_en_segon_terme', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'arg_MATRIU', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': 'Executa_2', 'objcopy': '목적파일변환기', 'ROOT': 'Project_rel', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Crear_usuari_espai', 'f': 'arxiu_introducció', 'extra': '추가영역', 'exports': 'exportar_taula', 'jobs': '빌드작업', 'run': 'Executa_ordre', 'path': 'Camí', 'REPO': 'dipòsit_rel', 'tool': 'Eines', 'classes': 'Classe_camí', 'output': '출력결과', 'samples': '예제들', 'symbol': 'símbol_VALOR', 'source': '원본자료', 'name': 'Nom', 'build_network': 'Crear_xarxa', 'font_info': 'tipus_de_lletra_informació', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
