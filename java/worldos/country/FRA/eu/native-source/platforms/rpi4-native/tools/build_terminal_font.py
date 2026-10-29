#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/eraiki_Terminal_letra_tipo.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('eraiki_Terminal_letra_tipo', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('eraiki_Terminal_letra_tipo')
    대응 = {'data': 'datuak', 'img': '그림', 'bits': 'Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda', 'x': 'X_koordenatu', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'bide_izen_Zerrenda', 'y': 'Y_koordenatu', 'main': 'Exekutatu_2', 'src': '원본주소', 'fonts': 'letra_tipo_Zerrenda', 'ROOT': 'Project_erro', 'p': 'datuak_kargu', 'cp': 'karaktere_kodeketa', 'target': 'helburu_balio'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
