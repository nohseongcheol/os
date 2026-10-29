#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/자바라이브러리빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('자바라이브러리빌드')
    대응 = {'header': 'Pengepala_VALUE', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'muat_beban_data', 'src': '원본주소', 'run': 'laksanakan_perintah', 'build_java_library': '자바라이브러리만들기', 'relative': 'laluan_relatif', 'classes': 'Kelas_laluan', 'dist': '배포경로', 'archive': 'Arkib', 'output': '출력결과', 'root': 'akar_e_mel', 'name': 'Nama', 'jar': '자바꾸러미', 'b': 'SECOND_VALUE', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
