#!/usr/bin/env python3
"""기존 путь 호환 точка_входа. фактический_данные реализация: ../инструменты/실행파일시험.py"""
import importlib as ВЗЯТЬ_ЗНАЧЕН
import sys as операционная_система_ЗНАЧЕН
from pathlib import Path as путь
операционная_система_ЗНАЧЕН.path.insert(0, str(путь(__file__).resolve().parents[1] / 'инструменты'))
if __name__ == '__main__':
    import runpy as программа_Launcher
    программа_Launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    реализация = ВЗЯТЬ_ЗНАЧЕН.import_module('실행파일시험')
    сопоставление_ЗНАЧЕН = {'out': 'KR_данные', 'expected': '예상결과', 'phoff': 'программа_Заголовок_СМЕЩ', 'offset': 'СМЕЩ_ЗНАЧЕН', 'invalid': 'неверный_данные', 'path': 'путь', 'executable': 'исполняемый_фото', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'результат', 'format_': 'формат_b87fd068', 'main': 'запустить', 'content': 'контент_ЗНАЧЕН', 'source': '원본자료', 'name': 'Название', 'reference': 'Сравнение_базовый_план', 'ROOT': 'задача_корень', 'value': 'ЗНАЧЕН', 'report': 'проверка_Отчет'}
    for Назад_товар, текущий_товар in сопоставление_ЗНАЧЕН.items():
        if hasattr(реализация, текущий_товар): globals()[Назад_товар] = getattr(реализация, текущий_товар)
