#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Загаловак_значэнне', 'sources': '원문목록', 'i': '순번', 'info': 'Сістэмная_інфармацыя', 'payload': 'карыснае_змесціва_дадзеныя', 'src': '원본주소', 'run': 'выканаць_каманда', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'клас_шлях', 'dist': '배포경로', 'archive': 'Архіў', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Назва', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
