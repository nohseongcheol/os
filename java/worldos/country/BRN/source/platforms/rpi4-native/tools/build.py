#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/bina_sistem.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('bina_sistem', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('bina_sistem')
    대응 = {'network': 'rangkaian', 'BUILD': 'bina_laluan', 'ar': 'Arkib_alat', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fon_data', 'flags': 'konfigurasi_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argumen_ARRAY', 'source_flags': '원본설정', 'ld': 'pemaut_alat', 'method': 'kaedah_pemasukan', 'main': 'Jalan', 'objcopy': 'objek_fail_penukar', 'ROOT': 'projek_akar', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'cipta_pengguna_SPACE', 'f': 'fail_pemasukan', 'extra': '추가영역', 'exports': 'Eksport_jadual', 'jobs': '빌드작업', 'run': 'laksanakan_perintah', 'path': 'LALUAN', 'REPO': 'repositori_akar', 'tool': 'alat', 'classes': 'Kelas_laluan', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Nama', 'build_network': 'cipta_rangkaian', 'font_info': 'fon_info', 'manifest': 'pakej_manifes_aplikasi', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
