#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/жасау_сурет.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('жасау_сурет', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('жасау_сурет')
    대응 = {'total': '총량', 'start': 'Орындау_2', 'firmware': '기초제어프로그램', 'files': 'файл_Тізім', 'archive_base': '압축기준', 'partition': 'бөлім_файл', 'archive': 'Мұрағат', 'main': 'Орындау_2', 'block': 'деректер_блогы', 'ROOT': 'жоба_түбір', 'boot': '부팅경로', 'stage': 'кезең_мән', 'out': 'өлшем_деректер', 'expected': '예상결과', 'f': 'файл_енгізу', 'src': '원본주소', 'path': 'Жол_2', 'p': 'деректер_лауазым', 'extracted': '추출자료', 'member': 'мүше', 'mbr': '주부트기록', 'image': 'сурет', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'лицензия', 'source': '원본자료', 'name': 'Аты', 'value': 'мән', 'manifest': '꾸러미명세', 'dest': 'тағайындау_мән_лауазым', 'work': '작업경로'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
