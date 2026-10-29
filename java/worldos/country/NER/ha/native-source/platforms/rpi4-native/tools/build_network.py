#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/Gina_Hanyar_sadarwa.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('Gina_Hanyar_sadarwa', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Gina_Hanyar_sadarwa')
    대응 = {'obj': 'Fayil_na_zangon_ƙarshe', 'objects': 'Zangon_ƙarshe_Fayiloli', 'library': 'laburare', 'output': '출력결과', 'port': 'lambar_kafa', 'root': '뿌리주소', 'files': 'Fayil_Jeri', 'source': '원본자료', 'run': 'gudanar_Umarni', 'flags': 'saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango', 'path': 'Hanyar_shiga', 'build_network': 'ƙirƙíra_Hanyar_sadarwa', 'cc': '시언어번역기', 'ar': 'Rumbun_ajiya_kayan_aiki'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
