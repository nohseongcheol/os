#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'datà', 'img': 'osise_valuu', 'bits': '비트들', 'x': 'ngakọrịta_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'ụzọ_ozi_ndepụta', 'y': '세로좌표', 'main': 'Bido', 'src': '원본주소', 'fonts': 'ọnụndèe_ndepụta', 'ROOT': '기준', 'p': '자료위치', 'cp': 'mkpụrụedemede_ntinye_koòdù', 'target': 'ebenlereanya'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
