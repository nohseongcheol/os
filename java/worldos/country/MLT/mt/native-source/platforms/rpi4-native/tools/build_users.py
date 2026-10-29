#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/bena_utent_SPACE.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('bena_utent_SPACE', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bena_utent_SPACE')
    대응 = {'mode': 'metodu_MODE', 'header': 'Intestazzjoni_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arkivju_għodda', 'posix': '포직스경로', 'payload': 'payload_data', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'ħalaq_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'Intestazzjoni_Lista', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'bena', 'build_users': 'ħalaq_utent_SPACE', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programm_Intestazzjoni_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'kmand_ADDRESS', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'eżegwixxa_kmand', 'path': 'mogħdija', 'p': 'data_pożizzjoni', 'changed': '바뀐자료', 'n': 'element_COUNT', 'flag': 'Settings_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'klassi_mogħdija', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_ADDRESS', 'symbol': 'simbolu_VALUE', 'root': 'għerq_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'isem', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
