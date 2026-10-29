#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/construir.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('construir', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('construir')
    mapeamento_VALOR = {'network': 'rede', 'BUILD': 'BLD_caminho', 'ar': 'arquivo_ferramenta', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fonte_dados', 'flags': 'Configuração_BITS', 'a': '첫째값', 'cc': 'C_compilador', 'args': 'argumento_MATRIZ', 'source_flags': '원본설정', 'ld': 'vinculador_ferramenta', 'method': 'método_entrada', 'main': 'iniciar', 'objcopy': 'arquivo_objeto_conversor', 'ROOT': 'ação_raiz', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'compilador_ferramenta', 'build_users': 'Criar_usuário_ESPAÇO', 'f': 'Arquivo_entrada', 'extra': '추가영역', 'exports': 'exportar_tabela', 'jobs': '빌드작업', 'run': 'Executar_comando', 'path': 'caminho', 'REPO': 'repositório_raiz', 'tool': 'ferramentas', 'classes': 'aula_caminho', 'output': 'saída', 'samples': '예제들', 'symbol': 'símbolo_VALOR', 'source': '원본자료', 'name': 'Nome', 'build_network': 'Criar_rede', 'font_info': 'fonte_informações', 'manifest': 'grupo_manifesto', 'work': '작업경로'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
