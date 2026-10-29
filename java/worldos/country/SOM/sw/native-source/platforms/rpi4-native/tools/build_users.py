#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/jenga_mtumiaji_eneo.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('jenga_mtumiaji_eneo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('jenga_mtumiaji_eneo')
    대응 = {'mode': 'mbinu_hali_tumizi', 'header': 'kichwa_thamani', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Hifadhi_zana', 'posix': '포직스경로', 'payload': 'data_muhimu_data', 'flags': 'usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'uwekaji_njia', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'kichwa_Orodha', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'jenga', 'build_users': 'unda_mtumiaji_eneo', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programu_kichwa_Chipua', 'offset': 'Chipua_thamani', 'text_address': 'amri_anwani', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'tekeleza_amri', 'path': 'njia', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Mipangilio_thamani', 'index': '색인', 'classes': 'tabaka_njia', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_anwani', 'symbol': 'ishara_thamani', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Jina', 'value': 'thamani', 'fmt': 'umbizo', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
