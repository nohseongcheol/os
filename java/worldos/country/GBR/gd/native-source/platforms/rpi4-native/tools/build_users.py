#!/usr/bin/env python3
"""기존 Slighe 호환 cur_a_steach_puing. dearbh_dàta 구현: ../innealan/tog_cleachdaiche_spàs.py"""
import importlib as TAKE_VALUE
import sys as siostam_obrachaidh_VALUE
from pathlib import Path as Slighe
siostam_obrachaidh_VALUE.path.insert(0, str(Slighe(__file__).resolve().parents[1] / 'innealan'))
if __name__ == '__main__':
    import runpy as ap_drathair_nan_aplacaid
    ap_drathair_nan_aplacaid.run_module('tog_cleachdaiche_spàs', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tog_cleachdaiche_spàs')
    대응 = {'mode': 'dòigh_MODE', 'header': 'bann_cinn_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'taisg_inneal', 'posix': '포직스경로', 'payload': 'payload_dàta', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'dàta', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Create_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'bann_cinn_Liosta', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'tog', 'build_users': 'Create_cleachdaiche_spàs', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ap_bann_cinn_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'àithne_ADDRESS', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'gnìomhaich_àithne', 'path': 'Slighe', 'p': 'dàta_suidhich', 'changed': '바뀐자료', 'n': 'nì_COUNT', 'flag': 'roghainnean_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'clas_slighe', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'dàta_ADDRESS', 'symbol': 'samhla_VALUE', 'root': 'freumh_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ainm', 'value': 'VALUE', 'fmt': 'fòrmat_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
