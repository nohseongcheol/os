#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'o_lchov_ma_lumotlar', 'expected': '예상결과', 'phoff': 'ilova_Sarlavha_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'xato_ma_lumotlar', 'path': 'yo_l', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'o_lchov', 'format_': 'format_b87fd068', 'main': 'Bajarish', 'content': 'tarkib_VALUE', 'source': '원본자료', 'name': 'Nomi', 'reference': 'Taqqoslama_bazaviy_koʻrsatkich', 'ROOT': 'Project_ildiz', 'value': 'VALUE', 'report': 'tasdiq_hisobot'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
