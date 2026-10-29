#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/BLD_Terminale_tipo_di_carattere.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_Terminale_tipo_di_carattere', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('BLD_Terminale_tipo_di_carattere')
    mapping_VALORE = {'data': 'dati', 'img': 'disegno_VALORE', 'bits': 'BITS_elenco', 'x': 'coordinata_x', 'draw': 'Disegno_schermata', 'licences': '이용허락목록', 'paths': 'percorso_elenco', 'y': 'Y_coordinata', 'main': 'avvia', 'src': '원본주소', 'fonts': 'tipo_di_carattere_elenco', 'ROOT': 'azione_radice', 'p': 'dati_funzione', 'cp': 'codifica_dei_caratteri', 'target': 'target'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
