#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/실행파일시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'програм_Толгой_Оффсет', 'offset': 'Оффсет_утга', 'invalid': 'буруу_өгөгдөл', 'path': 'ЗАМ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'формат_b87fd068', 'main': 'Ажиллуулах', 'content': 'Агуулга_утга', 'source': '원본자료', 'name': 'Нэр', 'reference': '비교기준', 'ROOT': '기준', 'value': 'утга', 'report': 'баталгаажуулалт_тайлан'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
