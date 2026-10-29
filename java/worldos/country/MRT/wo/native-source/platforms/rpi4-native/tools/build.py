#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/tabax_kureel.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('tabax_kureel', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tabax_kureel')
    대응 = {'network': 'mbaal', 'BUILD': 'tabax_Yoonu_jëmale', 'ar': 'denc_jumtukaay', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'mbindin_mbir', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'Tegtal_TABLO', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'doxalin_dugal_xabaar', 'main': 'daw', 'objcopy': 'yëf_bara_denc_soppikaay', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'sos_kiy_jariñoo_internet_Espace', 'f': 'bara_denc_dugal_xabaar', 'extra': '추가영역', 'exports': 'toxal_àlluwa', 'jobs': '빌드작업', 'run': 'def_ndigel', 'path': 'Yoonu_jëmale', 'REPO': '저장소', 'tool': 'Jumtukaay_yi', 'classes': 'maas_Yoonu_jëmale', 'output': '출력결과', 'samples': '예제들', 'symbol': 'sembóol_xëyma', 'source': '원본자료', 'name': 'tur_253d1510', 'build_network': 'sos_mbaal_48d29d6d', 'font_info': 'mbindin_yëglë', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
