#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Тақырып_мән', 'sources': '원문목록', 'i': '순번', 'info': 'Жүйелік_ақпарат', 'payload': 'жүктеме_деректер', 'src': '원본주소', 'run': 'орындау_пәрмен', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'оқу_жол', 'dist': '배포경로', 'archive': 'Мұрағат', 'output': '출력결과', 'root': 'түбір_мекенжай', 'name': 'Аты', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
