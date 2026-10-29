#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/qurmaq_istifadəçi_məkan.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('qurmaq_istifadəçi_məkan', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('qurmaq_istifadəçi_məkan')
    대응 = {'mode': 'metod_MODE', 'header': 'Başlıq_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arxiv_alət', 'posix': '포직스경로', 'payload': 'faydalı_yük_verilənlər', 'flags': 'konfiqurasiya_Fon_Ağıllı_Ötürmə_Xidməti', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'verilənlər', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'anbar_yol', 'build_python': 'yarat_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Mətn', 'headers': 'Başlıq_Siyahı', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'qurmaq', 'build_users': 'yarat_istifadəçi_məkan', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'proqram_Başlıq_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'əmr_ünvan', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'icra_etmək_əmr', 'path': 'Cığır', 'p': 'verilənlər_yerinə_qoymaq', 'changed': '바뀐자료', 'n': 'element_COUNT', 'flag': 'Parametrlər_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'Sinif_yol', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'verilənlər_ünvan', 'symbol': 'simvol_VALUE', 'root': 'kök_ünvan', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ad', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
