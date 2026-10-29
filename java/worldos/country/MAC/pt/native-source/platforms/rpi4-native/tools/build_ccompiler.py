#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/BLD_C_compilador.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_C_compilador', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('BLD_C_compilador')
    mapeamento_VALOR = {'out': 'RC_dados', 'builtins': '내장연산', 'header': 'Cabeçalho_VALOR', 'sdk': 'kit_de_desenvolvimento', 'build_ccompiler': 'Criar_C_compilador', 'i': '순번', 'elf': 'executável', 'run': 'Executar_comando', 'flags': 'Configuração_BITS', 'path': 'caminho', 'p': 'dados_cargo', 'cc': 'C_compilador', 'obj': 'arquivo_de_destino', 'flag': 'Configurações_VALOR', 'ld': 'vinculador_ferramenta', 'objects': 'destino_Arquivos', 'repo': 'repositório_caminho', 'v': '임시값', 'upstream': 'upstream', 'root': 'raiz_email', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nome', 'includes': '포함인수'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
