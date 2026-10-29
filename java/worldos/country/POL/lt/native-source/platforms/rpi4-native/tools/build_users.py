#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/kompiliuoti_naudotojas_erdvė.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('kompiliuoti_naudotojas_erdvė', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('kompiliuoti_naudotojas_erdvė')
    susiejimas_VALUE = {'mode': 'metodas_MODE', 'header': 'Antraštė_VALUE', 'i': '순번', 'build_ccompiler': 'kurti_C_kompiliatorius', 'ar': 'Archyvas_įrankis', 'posix': '포직스경로', 'payload': 'mokamoji_krova_duomenys', 'flags': 'konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba', 'cases': '시험사례', 'cc': 'C_kompiliatorius', 'data': 'duomenys', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'saugykla_kelias', 'build_python': 'kurti_PYTHON', 'inc': 'apimti_kelias', 'argument': '전달값', 'text': 'Tekstas', 'headers': 'Antraštė_Sąrašas', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'kompiliuoti', 'build_users': 'kurti_naudotojas_erdvė', 'compiler': 'kompiliatorius_įrankis', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programa_Antraštė_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'komanda_ADDRESS', 'abi': '호출규약', 'assembly': 'rinkinys', 'run': 'Vykdyti_komanda', 'path': 'KELIAS', 'p': 'duomenys_padėtis', 'changed': '바뀐자료', 'n': 'prekė_COUNT', 'flag': 'Parametrai_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'klasė_kelias', 'output': 'išeiga', 'loads': '적재구획', 'data_address': 'duomenys_ADDRESS', 'symbol': 'simbolis_VALUE', 'root': 'šaknis_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Pavadinimas_2', 'value': 'VALUE', 'fmt': 'formatas_932e03c8', 'work': '작업경로'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
