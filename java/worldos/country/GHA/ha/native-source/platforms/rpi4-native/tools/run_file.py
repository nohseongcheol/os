#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/gudanar_Fayil.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('gudanar_Fayil', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gudanar_Fayil')
    대응 = {'timeout': '시간제한', 's': 'Zare_Tarin_bayani', 'i': '순번', 'match': '일치', 'files': 'Fayil_Jeri', 'program': 'Shiri', 'executable': '실행가능파일', 'args': 'Tubalin_aiki_TSARI', 'chunk': '조각', 'data': 'Tarin_bayani', 'proc': 'haryar_aikin_na_ura', 'send': 'Aika', 'main': 'Tafiyar_da', 'marker': '확인표시', 'command': 'Umarni', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'gudanar_Umarni', 'p': '자료위치', 'parser': 'tatsar_manhaja', 'options': 'Zaɓuɓɓuka', 'kind': 'ɓangare_Daraja', 'selector': 'mai_zabe', 'upload_data': 'lodawa_Tarin_bayani', 'end': 'Ƙarshe_Sassautawa', 'n': '개수', 'd': 'Zangon_ƙarshe_Tarin_bayani', 'key': '누름값', 'output': '출력결과', 'line': 'Layi', 'name': 'Suna', 'upload_name': 'lodawa_Suna', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
