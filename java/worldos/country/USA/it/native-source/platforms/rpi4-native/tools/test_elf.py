#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/실행파일시험.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('실행파일시험')
    mapping_VALORE = {'out': 'KR_dati', 'expected': '예상결과', 'phoff': 'app_Intestazione_SCARTO', 'offset': 'SCARTO_VALORE', 'invalid': 'non_valida_dati', 'path': 'percorso', 'executable': 'eseguibile_foto', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'risultato', 'format_': 'formato_b87fd068', 'main': 'avvia', 'content': 'Contenuto_VALORE', 'source': '원본자료', 'name': 'Nome', 'reference': 'Confronto_di_base', 'ROOT': 'azione_radice', 'value': 'VALORE', 'report': 'convalida_Report'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
