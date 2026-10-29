#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'Tarin_bayani', 'img': 'zane_Daraja', 'bits': 'Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri', 'x': 'gamayyar_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'Hanyar_shiga_Jeri', 'y': 'Maɓallin_Y_Mai_tsarawa', 'main': 'Tafiyar_da', 'src': '원본주소', 'fonts': 'salon_rubutu_Jeri', 'ROOT': '기준', 'p': '자료위치', 'cp': 'Harafi_Juyar_da_bayanai_zuwa_lamba', 'target': 'tageti'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
