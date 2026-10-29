#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/generar_usuari_espai.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('generar_usuari_espai', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('generar_usuari_espai')
    대응 = {'mode': '방식', 'header': 'Capçalera_VALOR', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arxiu_eina', 'posix': '포직스경로', 'payload': 'càrrega_dades', 'flags': 'configuració_Servei_de_transferència_intel_ligent_en_segon_terme', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'dades', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'dipòsit_camí', 'build_python': 'Crear_PYTHON', 'inc': 'incloure_camí', 'argument': '전달값', 'text': 'SMS', 'headers': 'Capçalera_Llista', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'generar_3bf98865', 'build_users': 'Crear_usuari_espai', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programa_Capçalera_DESPLAÇAMENT', 'offset': 'DESPLAÇAMENT_VALOR', 'text_address': 'ordre_ADREÇA', 'abi': '호출규약', 'assembly': 'assemblatge', 'run': 'Executa_ordre', 'path': 'Camí', 'p': 'dades_càrrec', 'changed': '바뀐자료', 'n': 'element_COMPT', 'flag': 'Configuració_VALOR', 'index': 'Cerca_INDEX', 'classes': 'Classe_camí', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'dades_ADREÇA', 'symbol': 'símbol_VALOR', 'root': 'rel_ADREÇA', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nom', 'value': 'VALOR', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
