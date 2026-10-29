#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/Gina_na_ura.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('Gina_na_ura', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Gina_na_ura')
    대응 = {'network': 'Hanyar_sadarwa', 'BUILD': 'Gina_Hanyar_shiga', 'ar': 'Rumbun_ajiya_kayan_aiki', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'salon_rubutu_Tarin_bayani', 'flags': 'saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'Tubalin_aiki_TSARI', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'tsari_Mashigar_bayanai', 'main': 'Tafiyar_da', 'objcopy': 'abu_Fayil_Mai_canzawa', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ƙirƙíra_Mai_anfani_da_kwamfuta_wuri', 'f': 'Fayil_Mashigar_bayanai', 'extra': '추가영역', 'exports': 'Fitar_da_tebur', 'jobs': '빌드작업', 'run': 'gudanar_Umarni', 'path': 'Hanyar_shiga', 'REPO': '저장소', 'tool': 'Kaya', 'classes': 'Aji_Hanyar_shiga', 'output': '출력결과', 'samples': '예제들', 'symbol': 'alama_Daraja', 'source': '원본자료', 'name': 'Suna', 'build_network': 'ƙirƙíra_Hanyar_sadarwa', 'font_info': 'salon_rubutu_bayani', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
