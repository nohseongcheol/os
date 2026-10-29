#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/hanga_whatunga.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('hanga_whatunga', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('hanga_whatunga')
    대응 = {'obj': 'kōnae_ūnga_ffac9b48', 'objects': 'ūnga_Ngā_Kōnae', 'library': 'puna', 'output': '출력결과', 'port': '접속번호', 'root': 'pūtake_ADDRESS', 'files': 'kōnae_Rārangi', 'source': '원본자료', 'run': 'kawe_tono', 'flags': '설정비트', 'path': 'ara', 'build_network': 'Waihanga_whatunga', 'cc': '시언어번역기', 'ar': 'Pūranga_utauta'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
