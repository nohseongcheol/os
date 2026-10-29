#!/usr/bin/env python3
"""기존 ПЪТ 호환 запис_пункт. действителен_данни 구현: ../Инструменти/실행파일시험.py"""
import importlib as 가져오기
import sys as операционна_система_стойност
from pathlib import Path as ПЪТ
операционна_система_стойност.path.insert(0, str(ПЪТ(__file__).resolve().parents[1] / 'Инструменти'))
if __name__ == '__main__':
    import runpy as програма_програма_за_стартиране
    програма_програма_за_стартиране.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    съпоставяне_стойност = {'out': 'мярка_данни', 'expected': '예상결과', 'phoff': 'програма_Заглавка_Изместване', 'offset': 'Изместване_стойност', 'invalid': 'невалиден_данни', 'path': 'ПЪТ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'РЕЗУЛТАТ', 'format_': 'формат_b87fd068', 'main': 'Стартиране', 'content': 'Съдържание_стойност', 'source': '원본자료', 'name': 'Име', 'reference': 'Сравнение_Базова_линия', 'ROOT': 'проект_корен', 'value': 'стойност', 'report': 'проверка_отчет'}
    for 이전, в_срок_артикул in съпоставяне_стойност.items():
        if hasattr(구현, в_срок_артикул): globals()[이전] = getattr(구현, в_срок_артикул)
