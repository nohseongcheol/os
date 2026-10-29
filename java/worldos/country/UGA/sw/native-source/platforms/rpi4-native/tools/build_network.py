#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/jenga_Mtandao.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('jenga_Mtandao', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('jenga_Mtandao')
    대응 = {'obj': 'faili_fikio', 'objects': 'fikio_Faili', 'library': 'maktaba', 'output': '출력결과', 'port': 'namba_ya_kituo', 'root': '뿌리주소', 'files': 'faili_Orodha', 'source': '원본자료', 'run': 'tekeleza_amri', 'flags': 'usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma', 'path': 'njia', 'build_network': 'unda_Mtandao_48d29d6d', 'cc': '시언어번역기', 'ar': 'Hifadhi_zana'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
