#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/tóg_córas.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('tóg_córas', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tóg_córas')
    대응 = {'network': 'Líonra', 'BUILD': 'tóg_cosán', 'ar': 'Cartlann_uirlis', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'clófhoireann_sonraí', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argóint_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'modh_iontráil', 'main': 'Rith_2', 'objcopy': 'oibiacht_comhad_tiontaire', 'ROOT': 'teilgean_fréamh', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Create_úsáideoir_spás', 'f': 'comhad_iontráil', 'extra': '추가영역', 'exports': 'easportáil_tábla', 'jobs': '빌드작업', 'run': 'Rith_ordú', 'path': 'CONAIR', 'REPO': '저장소', 'tool': 'Uirlisí', 'classes': 'aicme_cosán', 'output': '출력결과', 'samples': '예제들', 'symbol': 'siombail_VALUE', 'source': '원본자료', 'name': 'Ainm', 'build_network': 'Create_Líonra', 'font_info': 'clófhoireann_faisnéis', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
