#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/예제빌드.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'Fayil_Jeri', 'java': '자바실행', 'run': 'gudanar_Umarni', 'path': 'Hanyar_shiga', 'p': '자료위치', 'readme': 'README', 'build_java_library': '자바라이브러리만들기', 'code': 'Sharadi_JERI', 'index': '색인', 'classes': 'Aji_Hanyar_shiga', 'repo': 'matattara_Hanyar_shiga', 'root': '뿌리주소', 'content': 'kunshiya_Daraja', 'source': '원본자료', 'name': 'Suna', 'target': 'tageti', 'manifest': '꾸러미명세', 'language': 'yare'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
