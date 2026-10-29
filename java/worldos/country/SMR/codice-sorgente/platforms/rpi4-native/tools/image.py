#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/Crea_foto.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Crea_foto', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('Crea_foto')
    mapping_VALORE = {'total': 'totale_capacità', 'start': 'avvia', 'firmware': 'firmware_VALORE', 'files': 'elenco_file', 'archive_base': 'Archivio_BASE', 'partition': 'partizione_File', 'archive': 'Archivio', 'main': 'avvia', 'block': 'blocco_di_dati', 'ROOT': 'azione_radice', 'boot': '부팅경로', 'stage': 'area_VALORE_29ee1bb7', 'out': 'KR_dati', 'expected': '예상결과', 'f': 'File_voce', 'src': '원본주소', 'path': 'percorso', 'p': 'dati_funzione', 'extracted': '추출자료', 'member': 'membro', 'mbr': 'record_principale_di_avvio', 'image': 'foto', 'sector_count': 'settore_CONTA_NUMERI', 'dist': 'distribuzione_percorso', 'sha': 'calcolare_hash', 'license_': 'licenza', 'source': '원본자료', 'name': 'Nome', 'value': 'VALORE', 'manifest': 'aggregare_manifesto', 'dest': 'meta_VALORE_funzione', 'work': '작업경로'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
