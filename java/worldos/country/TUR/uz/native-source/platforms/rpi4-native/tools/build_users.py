#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/nashr_foydalanuvchi_joy.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('nashr_foydalanuvchi_joy', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('nashr_foydalanuvchi_joy')
    대응 = {'mode': 'uslub_MODE', 'header': 'Sarlavha_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arxiv_vosita', 'posix': '포직스경로', 'payload': 'foydali_yuklanma_ma_lumotlar', 'flags': 'tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ma_lumotlar', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'repozitoriy_yo_l', 'build_python': 'Yaratish_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Matn', 'headers': 'Sarlavha_Ro_yxat', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'nashr', 'build_users': 'Yaratish_foydalanuvchi_joy', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ilova_Sarlavha_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'buyruq_manzil', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'bajarmoq_buyruq', 'path': 'yo_l', 'p': 'ma_lumotlar_holat', 'changed': '바뀐자료', 'n': 'element_COUNT', 'flag': 'Sozlamalar_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Sinf_yo_l', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ma_lumotlar_manzil', 'symbol': 'ramz_VALUE', 'root': 'ildiz_manzil', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nomi', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
