#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/nashr_Tarmoq.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('nashr_Tarmoq', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('nashr_Tarmoq')
    대응 = {'obj': 'natijalar_fayli', 'objects': 'ko_chirish_joyi_Fayllar', 'library': 'kutubxona', 'output': '출력결과', 'port': '접속번호', 'root': 'ildiz_manzil', 'files': 'fayl_Ro_yxat', 'source': '원본자료', 'run': 'bajarmoq_buyruq', 'flags': 'tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati', 'path': 'yo_l', 'build_network': 'Yaratish_Tarmoq', 'cc': '시언어번역기', 'ar': 'Arxiv_vosita'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
