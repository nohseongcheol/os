#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/aga_tsamaiso.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('aga_tsamaiso', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('aga_tsamaiso')
    대응 = {'network': 'Neteweke', 'BUILD': 'aga_tsela', 'ar': 'boloka_sediriswa', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'mofutatlhaka_tshedimosetso', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'Thulaganyo_setlhopha', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'mokgwa_tsenyo', 'main': 'dirisa', 'objcopy': 'selwana_faele_sefetodi', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'tlhama_modirisi_sebaka', 'f': 'faele_tsenyo', 'extra': '추가영역', 'exports': 'romelantle_lenaneothalo', 'jobs': '빌드작업', 'run': 'diragatsa_Taelo', 'path': 'tsela', 'REPO': '저장소', 'tool': 'Thuluse', 'classes': 'mofuta_tsela', 'output': '출력결과', 'samples': '예제들', 'symbol': 'letshwao_Boleng', 'source': '원본자료', 'name': 'leina', 'build_network': 'tlhama_Neteweke', 'font_info': 'mofutatlhaka_tshedimosetso_c16c0f1c', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
