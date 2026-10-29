#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/qurmaq_Şəbəkə.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('qurmaq_Şəbəkə', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('qurmaq_Şəbəkə')
    대응 = {'obj': 'təyinat_faylı', 'objects': 'təyinat_Fayllar', 'library': 'kitabxana', 'output': '출력결과', 'port': '접속번호', 'root': 'kök_ünvan', 'files': 'fayl_Siyahı', 'source': '원본자료', 'run': 'icra_etmək_əmr', 'flags': 'konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti', 'path': 'Cığır', 'build_network': 'yarat_Şəbəkə', 'cc': '시언어번역기', 'ar': 'Arxiv_alət'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
