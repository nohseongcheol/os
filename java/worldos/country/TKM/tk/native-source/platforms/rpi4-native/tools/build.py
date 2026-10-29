#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/düz_ulgam.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('düz_ulgam', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('düz_ulgam')
    대응 = {'network': 'Tor', 'BUILD': 'düz_ýol', 'ar': 'Arhiw_gural', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'şrift_maglumat', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'usul_girizmeklik', 'main': 'Bitir', 'objcopy': 'obýekt_faýl_özgerdiji', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'döretmek_ulanyjy_ýer', 'f': 'faýl_girizmeklik', 'extra': '추가영역', 'exports': 'eksport_et_tablisa', 'jobs': '빌드작업', 'run': 'ýerine_ýetir_buýruk', 'path': 'Ýol', 'REPO': '저장소', 'tool': 'Gurallar', 'classes': 'klas_ýol', 'output': '출력결과', 'samples': '예제들', 'symbol': 'nyşan_baha', 'source': '원본자료', 'name': 'Ad', 'build_network': 'döretmek_Tor', 'font_info': 'şrift_maglumat_c16c0f1c', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
