#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/예제빌드.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'өлшем_деректер', 'build_examples': '예제만들기', 'files': 'файл_Тізім', 'java': '자바실행', 'run': 'орындау_пәрмен', 'path': 'Жол_2', 'p': 'деректер_лауазым', 'readme': 'readme_файлы', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Іздеу_индекс', 'classes': 'оқу_жол', 'repo': 'репозиторий_жол', 'root': 'түбір_мекенжай', 'content': 'мазмұн_мән', 'source': '원본자료', 'name': 'Аты', 'target': 'мақсатты_мән', 'manifest': '꾸러미명세', 'language': 'Тіл'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
