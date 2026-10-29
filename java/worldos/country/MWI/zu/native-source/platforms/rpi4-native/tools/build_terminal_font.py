#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'imininingwane', 'img': 'umdwebo_inani', 'bits': '비트들', 'x': 'okuxhumanisa_u_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'umzila_Uhlu', 'y': '세로좌표', 'main': 'Sebenzisa', 'src': '원본주소', 'fonts': 'ubuso_bohlamvu_ifonti_Uhlu', 'ROOT': '기준', 'p': '자료위치', 'cp': 'uhlamvusimo_ukubhala_ngokufihla', 'target': 'impokophelo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
