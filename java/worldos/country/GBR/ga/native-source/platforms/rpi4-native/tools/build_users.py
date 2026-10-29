#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/tóg_úsáideoir_spás.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('tóg_úsáideoir_spás', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tóg_úsáideoir_spás')
    대응 = {'mode': 'modh_mód', 'header': 'Ceanntásc_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Cartlann_uirlis', 'posix': '포직스경로', 'payload': 'pálasta_sonraí', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'sonraí', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': 'Create_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Téacs', 'headers': 'Ceanntásc_Liosta', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'tóg', 'build_users': 'Create_úsáideoir_spás', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'clár_Ceanntásc_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'ordú_ADDRESS', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'Rith_ordú', 'path': 'CONAIR', 'p': 'sonraí_suíomh', 'changed': '바뀐자료', 'n': 'mír_COUNT', 'flag': 'Socruithe_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'aicme_cosán', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'sonraí_ADDRESS', 'symbol': 'siombail_VALUE', 'root': 'fréamh_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ainm', 'value': 'VALUE', 'fmt': 'formáid_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
