#!/usr/bin/env python3
"""기존 percorso 호환 punto_di_ingresso. effettivo_dati implementazione: ../strumenti/costruire.py"""
import importlib as INCLUDI_VALORE
import sys as sistema_operativo_VALORE
from pathlib import Path as percorso
sistema_operativo_VALORE.path.insert(0, str(percorso(__file__).resolve().parents[1] / 'strumenti'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('costruire', run_name='__main__', alter_sys=True)
else:
    implementazione = INCLUDI_VALORE.import_module('costruire')
    mapping_VALORE = {'network': 'rete', 'BUILD': 'BLD_percorso', 'ar': 'Archivio_strumento', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'tipo_di_carattere_dati', 'flags': 'configurazione_BITS', 'a': '첫째값', 'cc': 'C_compilatore', 'args': 'argomento_array', 'source_flags': '원본설정', 'ld': 'linker_strumento', 'method': 'metodo_voce', 'main': 'avvia', 'objcopy': 'file_oggetto_convertitore', 'ROOT': 'azione_radice', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'compilatore_strumento', 'build_users': 'Crea_USER_Space', 'f': 'File_voce', 'extra': '추가영역', 'exports': 'esportare_tabella', 'jobs': '빌드작업', 'run': 'Esegui_comando', 'path': 'percorso', 'REPO': 'radice_del_repository', 'tool': 'strumenti', 'classes': 'Corso_percorso', 'output': 'output', 'samples': '예제들', 'symbol': 'simbolo_VALORE', 'source': '원본자료', 'name': 'Nome', 'build_network': 'Crea_rete', 'font_info': 'tipo_di_carattere_info', 'manifest': 'aggregare_manifesto', 'work': '작업경로'}
    for Indietro_articolo, Regolari_articolo in mapping_VALORE.items():
        if hasattr(implementazione, Regolari_articolo): globals()[Indietro_articolo] = getattr(implementazione, Regolari_articolo)
