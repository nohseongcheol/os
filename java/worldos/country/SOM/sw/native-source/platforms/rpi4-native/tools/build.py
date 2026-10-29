#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/jenga_mfumo.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('jenga_mfumo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('jenga_mfumo')
    대응 = {'network': 'Mtandao', 'BUILD': 'jenga_njia', 'ar': 'Hifadhi_zana', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fonti_data', 'flags': 'usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'hoja_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'mbinu_ingizo', 'main': 'endesha', 'objcopy': 'kipengee_faili_kigeuzi', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'unda_mtumiaji_eneo', 'f': 'faili_ingizo', 'extra': '추가영역', 'exports': 'hamisha_jedwali', 'jobs': '빌드작업', 'run': 'tekeleza_amri', 'path': 'njia', 'REPO': '저장소', 'tool': 'Zana', 'classes': 'tabaka_njia', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ishara_thamani', 'source': '원본자료', 'name': 'Jina', 'build_network': 'unda_Mtandao_48d29d6d', 'font_info': 'fonti_maelezo', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
