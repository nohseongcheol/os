#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/예제빌드.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('예제빌드')
    mapeamento_VALOR = {'out': 'RC_dados', 'build_examples': '예제만들기', 'files': 'lista_de_arquivos', 'java': '자바실행', 'run': 'Executar_comando', 'path': 'caminho', 'p': 'dados_cargo', 'readme': 'LEIAME', 'build_java_library': '자바라이브러리만들기', 'code': 'instrução_SEQUÊNCIA', 'index': 'PROC_ÍNDICE', 'classes': 'aula_caminho', 'repo': 'repositório_caminho', 'root': 'raiz_email', 'content': 'Conteúdo_VALOR', 'source': '원본자료', 'name': 'Nome', 'target': 'meta', 'manifest': 'grupo_manifesto', 'language': 'Idioma'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
