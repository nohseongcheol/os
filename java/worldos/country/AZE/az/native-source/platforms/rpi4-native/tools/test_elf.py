#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'ölçü_verilənlər', 'expected': '예상결과', 'phoff': 'proqram_Başlıq_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'yanlış_verilənlər', 'path': 'Cığır', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ölçü', 'format_': 'format_b87fd068', 'main': 'İcra_Et', 'content': 'Məzmun_VALUE', 'source': '원본자료', 'name': 'Ad', 'reference': 'Müqayisə_baza_xətti', 'ROOT': 'Project_kök', 'value': 'VALUE', 'report': 'yoxlama_hesabat'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
