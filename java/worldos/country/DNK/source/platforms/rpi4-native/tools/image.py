#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/åbne_Image.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('åbne_Image', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('åbne_Image')
    tilknytning_VÆRDI = {'total': 'i_alt_kapacitet', 'start': 'Kør_2', 'firmware': 'Firmware_VÆRDI', 'files': 'filliste', 'archive_base': 'Arkiv_BASIS', 'partition': 'partition_fil', 'archive': 'Arkiv', 'main': 'Kør_2', 'block': 'datablok', 'ROOT': 'To_do_rod', 'boot': '부팅경로', 'stage': 'fase_VÆRDI', 'out': 'KR_data', 'expected': '예상결과', 'f': 'fil_post', 'src': '원본주소', 'path': 'Sti', 'p': 'data_placere', 'extracted': '추출자료', 'member': 'medlem', 'mbr': 'MBR', 'image': 'Image', 'sector_count': '섹터개수', 'dist': 'distribution_sti', 'sha': '해시계산', 'license_': 'licens', 'source': '원본자료', 'name': 'Navn', 'value': 'VÆRDI', 'manifest': 'bundt_manifest', 'dest': 'destination_VÆRDI_placere', 'work': '작업경로'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
