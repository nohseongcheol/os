#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/tóg_Líonra.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('tóg_Líonra', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tóg_Líonra')
    대응 = {'obj': 'comhad_sprice', 'objects': 'sprioc_Comhaid', 'library': 'leabharlann', 'output': '출력결과', 'port': 'uimhir_phoirt', 'root': 'fréamh_ADDRESS', 'files': 'comhad_Liosta', 'source': '원본자료', 'run': 'Rith_ordú', 'flags': '설정비트', 'path': 'CONAIR', 'build_network': 'Create_Líonra', 'cc': '시언어번역기', 'ar': 'Cartlann_uirlis'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
