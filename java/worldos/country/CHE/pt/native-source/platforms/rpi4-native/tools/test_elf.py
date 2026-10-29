#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/실행파일시험.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('실행파일시험')
    mapeamento_VALOR = {'out': 'RC_dados', 'expected': '예상결과', 'phoff': 'app_Cabeçalho_DESLOC', 'offset': 'DESLOC_VALOR', 'invalid': 'inválido_dados', 'path': 'caminho', 'executable': 'executável_foto', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'resultado', 'format_': 'formato_b87fd068', 'main': 'iniciar', 'content': 'Conteúdo_VALOR', 'source': '원본자료', 'name': 'Nome', 'reference': 'Comparação_linha_de_base', 'ROOT': 'ação_raiz', 'value': 'VALOR', 'report': 'validação_relatar'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
