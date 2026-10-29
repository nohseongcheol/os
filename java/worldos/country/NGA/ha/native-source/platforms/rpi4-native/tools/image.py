#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/ƙirƙíra_Hoto.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('ƙirƙíra_Hoto', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ƙirƙíra_Hoto')
    대응 = {'total': '총량', 'start': 'Tafiyar_da', 'firmware': '기초제어프로그램', 'files': 'Fayil_Jeri', 'archive_base': '압축기준', 'partition': 'Shamakin_faifai_Fayil', 'archive': 'Rumbun_ajiya', 'main': 'Tafiyar_da', 'block': 'Tarin_bayani_bulo', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'mumbari_Daraja', 'out': '결과자료', 'expected': '예상결과', 'f': 'Fayil_Mashigar_bayanai', 'src': '원본주소', 'path': 'Hanyar_shiga', 'p': '자료위치', 'extracted': '추출자료', 'member': 'Memba', 'mbr': '주부트기록', 'image': 'Hoto', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'Lasisi', 'source': '원본자료', 'name': 'Suna', 'value': 'Daraja', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
