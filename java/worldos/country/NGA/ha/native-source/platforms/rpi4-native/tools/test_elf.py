#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/실행파일시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'Shiri_Kai_Sassautawa', 'offset': 'Sassautawa_Daraja', 'invalid': 'mara_ƙarfi_Tarin_bayani', 'path': 'Hanyar_shiga', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'zubi_b87fd068', 'main': 'Tafiyar_da', 'content': 'kunshiya_Daraja', 'source': '원본자료', 'name': 'Suna', 'reference': 'Kwatantawa_Ginshiken_aiki', 'ROOT': '기준', 'value': 'Daraja', 'report': 'amincewa_Rahoto'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
