#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/hanga_pūnaha.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('hanga_pūnaha', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('hanga_pūnaha')
    대응 = {'network': 'whatunga', 'BUILD': 'hanga_ara', 'ar': 'Pūranga_utauta', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'momotuhi_raraunga', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'tohenga_HUĀNGA', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'aratuka_tāurunga', 'main': 'whakahaere', 'objcopy': 'ahanoa_kōnae_pūtahuri', 'ROOT': 'whakaatu_pūtake', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Waihanga_kaiwhakamahi_wāhi', 'f': 'kōnae_tāurunga', 'extra': '추가영역', 'exports': 'kaweake_ripanga', 'jobs': '빌드작업', 'run': 'kawe_tono', 'path': 'ara', 'REPO': '저장소', 'tool': 'Ngā_Utauta', 'classes': 'tauaha_ara', 'output': '출력결과', 'samples': '예제들', 'symbol': 'tohu_uara', 'source': '원본자료', 'name': 'Ingoa', 'build_network': 'Waihanga_whatunga', 'font_info': 'momotuhi_mōhiohio', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
