#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/құрастыру_жүйе.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('құрастыру_жүйе', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('құрастыру_жүйе')
    대응 = {'network': 'желі', 'BUILD': 'құрастыру_жол', 'ar': 'Мұрағат_құрал', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'қаріп_деректер', 'flags': 'конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_массив', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'әдіс_енгізу', 'main': 'Орындау_2', 'objcopy': 'нысан_файл_түрлендіргіш', 'ROOT': 'жоба_түбір', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'жасау_пайдаланушы_орын', 'f': 'файл_енгізу', 'extra': '추가영역', 'exports': 'экспорттау_кесте', 'jobs': '빌드작업', 'run': 'орындау_пәрмен', 'path': 'Жол_2', 'REPO': 'репозиторий_түбір', 'tool': 'Құралдар', 'classes': 'оқу_жол', 'output': '출력결과', 'samples': '예제들', 'symbol': 'символ_мән', 'source': '원본자료', 'name': 'Аты', 'build_network': 'жасау_желі', 'font_info': 'қаріп_ақпарат', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
