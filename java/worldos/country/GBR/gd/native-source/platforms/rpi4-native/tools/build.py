#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/tog_siostam.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('tog_siostam', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tog_siostam')
    대응 = {'network': 'lìonra', 'BUILD': 'tog_slighe', 'ar': 'taisg_inneal', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'cruth_clò_dàta', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argamaid_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'dòigh_cur_a_steach', 'main': 'ruith', 'objcopy': 'nì_faidhle_iompaichear', 'ROOT': 'tilg_freumh', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Create_cleachdaiche_spàs', 'f': 'faidhle_cur_a_steach', 'extra': '추가영역', 'exports': 'às_phortaich_clàr', 'jobs': '빌드작업', 'run': 'gnìomhaich_àithne', 'path': 'Slighe', 'REPO': '저장소', 'tool': 'innealan', 'classes': 'clas_slighe', 'output': '출력결과', 'samples': '예제들', 'symbol': 'samhla_VALUE', 'source': '원본자료', 'name': 'Ainm', 'build_network': 'Create_lìonra', 'font_info': 'cruth_clò_fios', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
