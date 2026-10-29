#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/qurmaq_PYTHON.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('qurmaq_PYTHON', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('qurmaq_PYTHON')
    대응 = {'ld': '연결편집기', 'archive': 'Arxiv', 'SHA256': 'yoxlama_heş', 'build_python': 'yarat_PYTHON', 'root': 'kök_ünvan', 'source': '원본자료', 'name': 'Ad', 'path': 'Cığır', 'VERSION': '배포판', 'cc': '시언어번역기', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'üzv'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
