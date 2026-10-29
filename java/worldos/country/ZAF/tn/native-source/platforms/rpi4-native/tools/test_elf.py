#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/실행파일시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'Tiriso_setlhogo_Baya_ka_Tekatekanyo', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'invalid': 'Ga_e_a_siama_tshedimosetso', 'path': 'tsela', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'fometa_b87fd068', 'main': 'dirisa', 'content': 'Diteng_Boleng', 'source': '원본자료', 'name': 'leina', 'reference': '비교기준', 'ROOT': '기준', 'value': 'Boleng', 'report': 'netefatso_pego'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
