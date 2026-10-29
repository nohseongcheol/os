#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/실행파일시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'өлшем_деректер', 'expected': '예상결과', 'phoff': 'бағдарлама_Тақырып_жылжыту', 'offset': 'жылжыту_мән_450fc799', 'invalid': 'дұрыс_емес_деректер', 'path': 'Жол_2', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'НӘТИЖЕ', 'format_': 'пішім_b87fd068', 'main': 'Орындау_2', 'content': 'мазмұн_мән', 'source': '원본자료', 'name': 'Аты', 'reference': 'Салыстыру_негізгі_жоспар', 'ROOT': 'жоба_түбір', 'value': 'мән', 'report': 'тексерім_есеп'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
