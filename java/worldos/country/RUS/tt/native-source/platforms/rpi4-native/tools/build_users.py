#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/төзү_кулланучы_өлкә.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('төзү_кулланучы_өлкә', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('төзү_кулланучы_өлкә')
    대응 = {'mode': 'ысул_MODE', 'header': 'Башлама_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Архив_чара', 'posix': '포직스경로', 'payload': 'төп_өлеш_мәгълүмат', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'мәгълүмат', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Төзү_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Mäten', 'headers': 'Башлама_Исемлек', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'төзү', 'build_users': 'Төзү_кулланучы_өлкә', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'кушымта_Башлама_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'команда_адрес', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'үтәргә_команда', 'path': 'Yul', 'p': 'мәгълүмат_урнаштыру', 'changed': '바뀐자료', 'n': 'элемент_COUNT', 'flag': 'Параметрлар_VALUE', 'index': 'Эзләү_INDEX', 'classes': 'класс_юл', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'мәгълүмат_адрес', 'symbol': 'символ_VALUE', 'root': 'тамыр_адрес', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'исем', 'value': 'VALUE', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
