#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Kai_Daraja', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'Kumshinbayanai_Tarin_bayani', 'src': '원본주소', 'run': 'gudanar_Umarni', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Aji_Hanyar_shiga', 'dist': '배포경로', 'archive': 'Rumbun_ajiya', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Suna', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
