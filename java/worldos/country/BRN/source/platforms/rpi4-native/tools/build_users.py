#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/bina_pengguna_SPACE.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('bina_pengguna_SPACE', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('bina_pengguna_SPACE')
    대응 = {'mode': 'kaedah_mod', 'header': 'Pengepala_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arkib_alat', 'posix': '포직스경로', 'payload': 'muat_beban_data', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'cases': 'kes_ujian', 'cc': '시언어번역기', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': 'pemaut_alat', 'repo': 'repositori_laluan', 'build_python': 'cipta_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Teks', 'headers': 'Pengepala_Senarai', 'cxx': '시플플번역기', 'valid': 'sah', 'build': 'bina', 'build_users': 'cipta_pengguna_SPACE', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'aplikasi_Pengepala_Ofset', 'offset': 'Ofset_VALUE', 'text_address': 'perintah_e_mel', 'abi': '호출규약', 'assembly': 'himpunan', 'run': 'laksanakan_perintah', 'path': 'LALUAN', 'p': 'data_jawatan', 'changed': '바뀐자료', 'n': 'item_COUNT', 'flag': 'Seting_VALUE', 'index': 'Carian_INDEX', 'classes': 'Kelas_laluan', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'data_e_mel', 'symbol': 'simbol_VALUE', 'root': 'akar_e_mel', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nama', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
