#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/құрастыру_желі.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('құрастыру_желі', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('құрастыру_желі')
    대응 = {'obj': 'тағайындалған_файл', 'objects': 'тағайындау_Файлдар', 'library': 'кітапхана', 'output': '출력결과', 'port': 'порт_нөмірі', 'root': 'түбір_мекенжай', 'files': 'файл_Тізім', 'source': '원본자료', 'run': 'орындау_пәрмен', 'flags': 'конфигурация_фондық_интеллектуалдық_тасымалдау_қызметі', 'path': 'Жол_2', 'build_network': 'жасау_желі', 'cc': '시언어번역기', 'ar': 'Мұрағат_құрал'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
