#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/예제빌드.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'файл_Жагсаалт', 'java': '자바실행', 'run': 'Гүйцэтгэх_команд', 'path': 'ЗАМ', 'p': '자료위치', 'readme': 'заавал_унших', 'build_java_library': '자바라이브러리만들기', 'code': 'заавар_ДАРААЛАЛ', 'index': '색인', 'classes': 'класс_зам', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Агуулга_утга', 'source': '원본자료', 'name': 'Нэр', 'target': 'зорилго', 'manifest': '꾸러미명세', 'language': 'Хэл'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
