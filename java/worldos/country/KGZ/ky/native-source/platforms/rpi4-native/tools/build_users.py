#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/курам_колдонуучу_АРАЛЫК.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('курам_колдонуучу_АРАЛЫК', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('курам_колдонуучу_АРАЛЫК')
    대응 = {'mode': 'ыкма_режим', 'header': 'баш_аты_маани', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Архив_курал', 'posix': '포직스경로', 'payload': 'керектүү_жүктөө_ченеми_берилмелер', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'берилмелер', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Текст', 'headers': 'баш_аты_Тизме', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'курам', 'build_users': 'түзүү_колдонуучу_АРАЛЫК', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'програм_баш_аты_Жылбышуу', 'offset': 'Жылбышуу_маани', 'text_address': 'буйрук_дарек', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'аткаруу_буйрук', 'path': 'ЖОЛ', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Орнотуулар_маани', 'index': '색인', 'classes': 'класс_жол', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'берилмелер_дарек', 'symbol': 'символ_маани', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Аты', 'value': 'маани', 'fmt': 'формат_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
