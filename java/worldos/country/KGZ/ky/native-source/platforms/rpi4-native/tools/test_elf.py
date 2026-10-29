#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/실행파일시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'програм_баш_аты_Жылбышуу', 'offset': 'Жылбышуу_маани', 'invalid': 'бузук_берилмелер', 'path': 'ЖОЛ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'формат_b87fd068', 'main': 'Жүргүзүү', 'content': 'Мазмун_маани', 'source': '원본자료', 'name': 'Аты', 'reference': '비교기준', 'ROOT': '기준', 'value': 'маани', 'report': 'ырастоо_отчет'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
