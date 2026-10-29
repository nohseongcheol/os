#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/자바라이브러리빌드.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('자바라이브러리빌드')
    mapeamento_VALOR = {'header': 'Cabeçalho_VALOR', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'carga_dados', 'src': '원본주소', 'run': 'Executar_comando', 'build_java_library': '자바라이브러리만들기', 'relative': 'caminho_relativo', 'classes': 'aula_caminho', 'dist': 'distribuição_caminho', 'archive': 'arquivo', 'output': 'saída', 'root': 'raiz_email', 'name': 'Nome', 'jar': '자바꾸러미', 'b': 'SEGUNDO_VALOR', 'entries': '항목들'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
