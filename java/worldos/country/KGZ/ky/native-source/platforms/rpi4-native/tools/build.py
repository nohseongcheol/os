#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/курам_тутум.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('курам_тутум', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('курам_тутум')
    대응 = {'network': 'Желе', 'BUILD': 'курам_жол', 'ar': 'Архив_курал', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'арип_берилмелер', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_МАССИВ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ыкма_киргизме_жазуу', 'main': 'Жүргүзүү', 'objcopy': 'объект_файл_маанилеш_өзгөрткүч', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'түзүү_колдонуучу_АРАЛЫК', 'f': 'файл_киргизме_жазуу', 'extra': '추가영역', 'exports': 'экспорттоо_жадыбал', 'jobs': '빌드작업', 'run': 'аткаруу_буйрук', 'path': 'ЖОЛ', 'REPO': '저장소', 'tool': 'Куралдар', 'classes': 'класс_жол', 'output': '출력결과', 'samples': '예제들', 'symbol': 'символ_маани', 'source': '원본자료', 'name': 'Аты', 'build_network': 'түзүү_Желе', 'font_info': 'арип_маалымат', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
