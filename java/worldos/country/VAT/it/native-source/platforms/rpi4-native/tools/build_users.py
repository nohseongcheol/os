#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/BLD_USER_Space.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_USER_Space', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('BLD_USER_Space')
    mapping_VALORE = {'mode': 'metodo_MODA', 'header': 'Intestazione_VALORE', 'i': '순번', 'build_ccompiler': 'Crea_C_compilatore', 'ar': 'Archivio_strumento', 'posix': '포직스경로', 'payload': 'payload_dati', 'flags': 'configurazione_BITS', 'cases': 'test_case', 'cc': 'C_compilatore', 'data': 'dati', 'build_java_library': '자바라이브러리만들기', 'ld': 'linker_strumento', 'repo': 'archivio_percorso', 'build_python': 'Crea_PYTHON', 'inc': 'includere_percorso', 'argument': '전달값', 'text': 'testo', 'headers': 'Intestazione_elenco', 'cxx': '시플플번역기', 'valid': 'valido', 'build': 'BLD', 'build_users': 'Crea_USER_Space', 'compiler': 'compilatore_strumento', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_Intestazione_SCARTO', 'offset': 'SCARTO_VALORE', 'text_address': 'comando_e_mail', 'abi': 'Chiama_ABI', 'assembly': 'assembly', 'run': 'Esegui_comando', 'path': 'percorso', 'p': 'dati_funzione', 'changed': '바뀐자료', 'n': 'articolo_CONTA_NUMERI', 'flag': 'Impostazioni_VALORE', 'index': 'CERCA_INDICE', 'classes': 'Corso_percorso', 'output': 'output', 'loads': '적재구획', 'data_address': 'dati_e_mail', 'symbol': 'simbolo_VALORE', 'root': 'radice_e_mail', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nome', 'value': 'VALORE', 'fmt': 'formato_932e03c8', 'work': '작업경로'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
