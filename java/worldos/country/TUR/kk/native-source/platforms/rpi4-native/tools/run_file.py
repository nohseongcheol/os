#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/орындау_файл.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('орындау_файл', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('орындау_файл')
    대응 = {'timeout': '시간제한', 's': 'жол_деректер', 'i': '순번', 'match': '일치', 'files': 'файл_Тізім', 'program': 'бағдарлама', 'executable': '실행가능파일', 'args': 'аргумент_массив', 'chunk': '조각', 'data': 'деректер', 'proc': 'Үрдіс', 'send': 'жіберу', 'main': 'Орындау_2', 'marker': '확인표시', 'command': 'Команда', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'орындау_пәрмен', 'p': 'деректер_лауазым', 'parser': 'талдау_құралы', 'options': 'Параметрлер', 'kind': 'Санат_мән', 'selector': 'селектор', 'upload_data': 'Жүктеп_салу_деректер', 'end': 'тоқтату_жылжыту', 'n': '개수', 'd': 'тағайындау_деректер', 'key': '누름값', 'output': '출력결과', 'line': 'Жол', 'name': 'Аты', 'upload_name': 'Жүктеп_салу_аты', 'receive': '수신하기'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
