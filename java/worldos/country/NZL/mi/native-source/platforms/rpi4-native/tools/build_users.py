#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/hanga_kaiwhakamahi_wāhi.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('hanga_kaiwhakamahi_wāhi', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('hanga_kaiwhakamahi_wāhi')
    대응 = {'mode': 'aratuka_MODE', 'header': 'Pane_uara', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Pūranga_utauta', 'posix': '포직스경로', 'payload': 'tino_raraunga_raraunga', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'raraunga', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Waihanga_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Ngā_kupu', 'headers': 'Pane_Rārangi', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'hanga', 'build_users': 'Waihanga_kaiwhakamahi_wāhi', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'kaupapa_Pane_OFFSET', 'offset': 'OFFSET_uara', 'text_address': 'tono_ADDRESS', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'kawe_tono', 'path': 'ara', 'p': 'raraunga_tūranga', 'changed': '바뀐자료', 'n': 'tuemi_COUNT', 'flag': 'Ngā_Tautuhinga_uara', 'index': 'Rapu_INDEX', 'classes': 'tauaha_ara', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'raraunga_ADDRESS', 'symbol': 'tohu_uara', 'root': 'pūtake_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ingoa', 'value': 'uara', 'fmt': 'hōputu_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
