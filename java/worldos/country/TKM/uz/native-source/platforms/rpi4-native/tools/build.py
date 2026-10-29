#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/nashr_tizim.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('nashr_tizim', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('nashr_tizim')
    대응 = {'network': 'Tarmoq', 'BUILD': 'nashr_yo_l', 'ar': 'Arxiv_vosita', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'shrift_ma_lumotlar', 'flags': 'tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'dalil_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'uslub_kiritish', 'main': 'Bajarish', 'objcopy': 'obyekt_fayl_konverter', 'ROOT': 'Project_ildiz', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Yaratish_foydalanuvchi_joy', 'f': 'fayl_kiritish', 'extra': '추가영역', 'exports': 'eksport_qilmoq_jadval', 'jobs': '빌드작업', 'run': 'bajarmoq_buyruq', 'path': 'yo_l', 'REPO': 'repozitoriy_ildiz', 'tool': 'Vositalar', 'classes': 'Sinf_yo_l', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ramz_VALUE', 'source': '원본자료', 'name': 'Nomi', 'build_network': 'Yaratish_Tarmoq', 'font_info': 'shrift_ma_lumot', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
