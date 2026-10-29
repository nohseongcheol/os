#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/예제빌드.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'файл_Тизме', 'java': '자바실행', 'run': 'аткаруу_буйрук', 'path': 'ЖОЛ', 'p': '자료위치', 'readme': 'readme_файл', 'build_java_library': '자바라이브러리만들기', 'code': 'аткаруу_буйругу_ЫРААТТУУЛУК', 'index': '색인', 'classes': 'класс_жол', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Мазмун_маани', 'source': '원본자료', 'name': 'Аты', 'target': 'максат', 'manifest': '꾸러미명세', 'language': 'Тил'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
