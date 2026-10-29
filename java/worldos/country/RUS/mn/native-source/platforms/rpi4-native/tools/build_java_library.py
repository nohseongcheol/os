#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Толгой_утга', 'sources': '원문목록', 'i': '순번', 'info': 'системийн_мэдээлэл', 'payload': 'ашигтай_ачаалал_өгөгдөл', 'src': '원본주소', 'run': 'Гүйцэтгэх_команд', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'класс_зам', 'dist': '배포경로', 'archive': 'Архив', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Нэр', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
