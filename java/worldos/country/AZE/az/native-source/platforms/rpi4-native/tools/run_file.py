#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/icra_etmək_fayl.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('icra_etmək_fayl', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('icra_etmək_fayl')
    대응 = {'timeout': '시간제한', 's': 'sətir_verilənlər', 'i': '순번', 'match': '일치', 'files': 'fayl_Siyahı', 'program': 'proqram', 'executable': '실행가능파일', 'args': 'arqument_ARRAY', 'chunk': '조각', 'data': 'verilənlər', 'proc': 'Proses', 'send': 'göndərmək', 'main': 'İcra_Et', 'marker': '확인표시', 'command': 'Əmr', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'icra_etmək_əmr', 'p': 'verilənlər_yerinə_qoymaq', 'parser': 'parser', 'options': 'Seçimlər', 'kind': 'sahə_VALUE', 'selector': 'seçici', 'upload_data': 'Upload_verilənlər', 'end': 'bitirmək_OFFSET', 'n': 'element_COUNT', 'd': 'təyinat_verilənlər', 'key': '누름값', 'output': '출력결과', 'line': 'Giriş', 'name': 'Ad', 'upload_name': 'Upload_ad', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
