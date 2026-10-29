#!/usr/bin/env python3
"""기존 pad 호환 beginpunt. werkelijk_gegevens implementatie: ../hulpmiddelen/maken_kopie.py"""
import importlib as NEMEN_WAARDE
import sys as besturingssysteem_WAARDE
from pathlib import Path as pad
besturingssysteem_WAARDE.path.insert(0, str(pad(__file__).resolve().parents[1] / 'hulpmiddelen'))
if __name__ == '__main__':
    import runpy as app_app_lade
    app_app_lade.run_module('maken_kopie', run_name='__main__', alter_sys=True)
else:
    implementatie = NEMEN_WAARDE.import_module('maken_kopie')
    toewijzing_WAARDE = {'total': 'totaal_capaciteit', 'start': 'starten', 'firmware': 'firmware_WAARDE', 'files': 'bestandslijst', 'archive_base': 'Archief_BASIS', 'partition': 'partitie_Bestand', 'archive': 'Archief', 'main': 'starten', 'block': 'gegevensblok', 'ROOT': 'Taken_wortel', 'boot': '부팅경로', 'stage': 'fase_WAARDE', 'out': 'HR_gegevens', 'expected': '예상결과', 'f': 'Bestand_invoer', 'src': '원본주소', 'path': 'pad', 'p': 'gegevens_functie', 'extracted': '추출자료', 'member': 'lid', 'mbr': 'hoofdopstartrecord', 'image': 'kopie', 'sector_count': '섹터개수', 'dist': 'distributie_pad', 'sha': '해시계산', 'license_': 'licentie', 'source': '원본자료', 'name': 'Naam', 'value': 'WAARDE', 'manifest': 'bundel_manifest', 'dest': 'doel_WAARDE_functie', 'work': '작업경로'}
    for Vorige_item, actueel_item in toewijzing_WAARDE.items():
        if hasattr(implementatie, actueel_item): globals()[Vorige_item] = getattr(implementatie, actueel_item)
