#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/akha_iNethiwekhi.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('akha_iNethiwekhi', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('akha_iNethiwekhi')
    대응 = {'obj': 'ifayela_elamukelayo', 'objects': 'isikhumulo_Amafayela', 'library': 'umtapo', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ifayela_Uhlu', 'source': '원본자료', 'run': 'yenza_umyalo', 'flags': '설정비트', 'path': 'Indlela_2', 'build_network': 'yakha_iNethiwekhi', 'cc': '시언어번역기', 'ar': 'londoloza_ithuluzi'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
