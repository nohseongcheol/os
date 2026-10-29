#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'Kai_Daraja', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'gudanar_Umarni', 'flags': 'saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango', 'path': 'Hanyar_shiga', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'Fayil_na_zangon_ƙarshe', 'flag': 'Saituna_Daraja', 'ld': '연결편집기', 'objects': 'Zangon_ƙarshe_Fayiloli', 'repo': 'matattara_Hanyar_shiga', 'v': '임시값', 'upstream': 'tushe_99f91985', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Suna', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
