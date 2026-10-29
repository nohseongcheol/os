#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/Gina_Mai_anfani_da_kwamfuta_wuri.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('Gina_Mai_anfani_da_kwamfuta_wuri', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Gina_Mai_anfani_da_kwamfuta_wuri')
    대응 = {'mode': 'tsari_yanayin_aiki', 'header': 'Kai_Daraja', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Rumbun_ajiya_kayan_aiki', 'posix': '포직스경로', 'payload': 'Kumshinbayanai_Tarin_bayani', 'flags': 'saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'Tarin_bayani', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'matattara_Hanyar_shiga', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'Kai_Jeri', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'Gina', 'build_users': 'ƙirƙíra_Mai_anfani_da_kwamfuta_wuri', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'Shiri_Kai_Sassautawa', 'offset': 'Sassautawa_Daraja', 'text_address': 'Umarni_imel', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'gudanar_Umarni', 'path': 'Hanyar_shiga', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Saituna_Daraja', 'index': '색인', 'classes': 'Aji_Hanyar_shiga', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'Tarin_bayani_imel', 'symbol': 'alama_Daraja', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Suna', 'value': 'Daraja', 'fmt': 'tsari', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
