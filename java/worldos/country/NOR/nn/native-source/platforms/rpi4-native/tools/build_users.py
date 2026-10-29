#!/usr/bin/env python3
"""기존 STIGE 호환 oppføring_p. faktisk_data 구현: ../Verktøy/bygg_brukar_område.py"""
import importlib as TAKE_VALUE
import sys as operativsystem_VALUE
from pathlib import Path as STIGE
operativsystem_VALUE.path.insert(0, str(STIGE(__file__).resolve().parents[1] / 'Verktøy'))
if __name__ == '__main__':
    import runpy as app_appskuff
    app_appskuff.run_module('bygg_brukar_område', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bygg_brukar_område')
    대응 = {'mode': 'metode_MODE', 'header': 'hode_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arkiv_verktøy', 'posix': '포직스경로', 'payload': 'nyttelast_data', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Opprett_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Tekst', 'headers': 'hode_Liste', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'bygg', 'build_users': 'Opprett_brukar_område', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_hode_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'kommando_ADDRESS', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'Utfør_kommando', 'path': 'STIGE', 'p': 'data_plassere', 'changed': '바뀐자료', 'n': 'vare_COUNT', 'flag': 'Innstillingar_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'time_bane', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_ADDRESS', 'symbol': 'symbol_VALUE', 'root': 'rot_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Namn', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, betalt_vare in 대응.items():
        if hasattr(구현, betalt_vare): globals()[이전] = getattr(구현, betalt_vare)
