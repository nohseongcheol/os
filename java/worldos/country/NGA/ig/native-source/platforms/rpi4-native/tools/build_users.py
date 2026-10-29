#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/wue_òjìàrụ_ohere.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('wue_òjìàrụ_ohere', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('wue_òjìàrụ_ohere')
    대응 = {'mode': 'usoro_moòdù', 'header': 'isi_valuu', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ọkpụ_ngwaọrụ', 'posix': '포직스경로', 'payload': 'ebe_mbulingwa_datà', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'datà', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'isi_ndepụta', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'wue', 'build_users': 'mepụta_òjìàrụ_ohere', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_isi_Nnokwata', 'offset': 'Nnokwata_valuu', 'text_address': 'nnyemiwu_àdreèsì', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'mee_nnyemiwu', 'path': 'ụzọ_ozi', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Mwube_valuu', 'index': '색인', 'classes': 'klaàsị_ụzọ_ozi', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'datà_àdreèsì', 'symbol': 'adimara_valuu', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Aha', 'value': 'valuu', 'fmt': 'nsìrìhazi', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
