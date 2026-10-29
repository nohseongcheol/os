#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/bajarmoq_fayl.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('bajarmoq_fayl', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bajarmoq_fayl')
    대응 = {'timeout': '시간제한', 's': 'satr_ma_lumotlar', 'i': '순번', 'match': '일치', 'files': 'fayl_Ro_yxat', 'program': 'ilova', 'executable': '실행가능파일', 'args': 'dalil_ARRAY', 'chunk': '조각', 'data': 'ma_lumotlar', 'proc': 'Jarayon', 'send': 'yuborish', 'main': 'Bajarish', 'marker': '확인표시', 'command': 'Buyruq', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'bajarmoq_buyruq', 'p': 'ma_lumotlar_holat', 'parser': 'parser', 'options': 'Opsiyalar', 'kind': 'toifa_VALUE', 'selector': 'tanlagich', 'upload_data': 'uzatmoq_ma_lumotlar', 'end': 'to_xtatmoq_OFFSET', 'n': 'element_COUNT', 'd': 'ko_chirish_joyi_ma_lumotlar', 'key': '누름값', 'output': '출력결과', 'line': 'satr', 'name': 'Nomi', 'upload_name': 'uzatmoq_nom', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
