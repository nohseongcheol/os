#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/bygg_system.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_system', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bygg_system')
    대응 = {'network': 'Nettverk', 'BUILD': 'bygg_bane', 'ar': 'Arkiv_verktøy', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'skrift_data', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metode_oppføring', 'main': 'Køyr_2', 'objcopy': 'objekt_fil_konverteringsprogram', 'ROOT': 'spegle_rot', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Opprett_brukar_område', 'f': 'fil_oppføring', 'extra': '추가영역', 'exports': 'eksportere_tabell', 'jobs': '빌드작업', 'run': 'Utfør_kommando', 'path': 'STIGE', 'REPO': '저장소', 'tool': 'Verktøy', 'classes': 'time_bane', 'output': '출력결과', 'samples': '예제들', 'symbol': 'symbol_VALUE', 'source': '원본자료', 'name': 'Namn', 'build_network': 'Opprett_Nettverk', 'font_info': 'skrift_informasjon', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
