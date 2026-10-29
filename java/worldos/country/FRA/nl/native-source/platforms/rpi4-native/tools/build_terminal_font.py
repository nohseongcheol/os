#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/build_Terminal_lettertype.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('build_Terminal_lettertype', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('build_Terminal_lettertype')
    toewijzing_WAARDE = {'data': 'gegevens', 'img': 'tekening_WAARDE', 'bits': 'BITS_Lijst', 'x': 'x_coördinaat', 'draw': 'Tekenen_scherm', 'licences': '이용허락목록', 'paths': 'pad_Lijst', 'y': 'Y_coördinaat', 'main': 'starten', 'src': '원본주소', 'fonts': 'lettertype_Lijst', 'ROOT': 'Taken_wortel', 'p': 'gegevens_functie', 'cp': 'tekencodering', 'target': 'doel'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
