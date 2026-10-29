#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'баш_аты_маани', 'sources': '원문목록', 'i': '순번', 'info': 'Система_маалыматы', 'payload': 'керектүү_жүктөө_ченеми_берилмелер', 'src': '원본주소', 'run': 'аткаруу_буйрук', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'класс_жол', 'dist': '배포경로', 'archive': 'Архив', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Аты', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
