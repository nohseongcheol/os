#!/usr/bin/env python3
"""기존 path 호환 pagpasok_point. totoo_data 구현: ../Mga_Tool/build_gumagamit_SPACE.py"""
import importlib as TAKE_VALUE
import sys as operating_system_VALUE
from pathlib import Path as path
operating_system_VALUE.path.insert(0, str(path(__file__).resolve().parents[1] / 'Mga_Tool'))
if __name__ == '__main__':
    import runpy as app_launcher
    app_launcher.run_module('build_gumagamit_SPACE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('build_gumagamit_SPACE')
    대응 = {'mode': 'pamamaraan_MODE', 'header': 'Header_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Archive_tool', 'posix': '포직스경로', 'payload': 'payload_data', 'flags': 'kompigurasyon_Background_Intelligent_Transfer_Service', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'repository_path', 'build_python': 'Create_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'Header_list', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'build', 'build_users': 'Create_gumagamit_SPACE', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_Header_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'utos_email', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'Mag_execute_utos', 'path': 'path', 'p': 'data_posisyon', 'changed': '바뀐자료', 'n': 'item_COUNT', 'flag': 'Mga_Setting_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'kategorya_path', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_email', 'symbol': 'simbolo_VALUE', 'root': 'root_email', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'pangalan', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
