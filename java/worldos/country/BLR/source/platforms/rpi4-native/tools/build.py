#!/usr/bin/env python3
"""기존 ШЛЯХ 호환 увядзенне_бал. фактычны_дадзеныя 구현: ../Інструменты/зборка_сістэма.py"""
import importlib as 가져오기
import sys as аперацыйная_сістэма_значэнне
from pathlib import Path as ШЛЯХ
аперацыйная_сістэма_значэнне.path.insert(0, str(ШЛЯХ(__file__).resolve().parents[1] / 'Інструменты'))
if __name__ == '__main__':
    import runpy as праграма_выклік_праграм
    праграма_выклік_праграм.run_module('зборка_сістэма', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('зборка_сістэма')
    대응 = {'network': 'Сетка', 'BUILD': 'зборка_шлях', 'ar': 'Архіў_інструмент', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'шрыфт_дадзеныя', 'flags': 'канфігурацыя_Служба_інтэлектуальнай_фонавай_перадачы_файлаў', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_масіў', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'спосаб_увядзенне', 'main': 'Выканаць', 'objcopy': 'аб_ект_файл_канвертар', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'стварыць_карыстальнік_ПРАБЕЛ', 'f': 'файл_увядзенне', 'extra': '추가영역', 'exports': 'экспартаваць_табліца', 'jobs': '빌드작업', 'run': 'выканаць_каманда', 'path': 'ШЛЯХ', 'REPO': '저장소', 'tool': 'Інструменты', 'classes': 'клас_шлях', 'output': '출력결과', 'samples': '예제들', 'symbol': 'сімвал_значэнне', 'source': '원본자료', 'name': 'Назва', 'build_network': 'стварыць_Сетка', 'font_info': 'шрыфт_звесткі', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
