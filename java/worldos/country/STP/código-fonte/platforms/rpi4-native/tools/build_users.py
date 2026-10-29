#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/BLD_usuário_ESPAÇO.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('BLD_usuário_ESPAÇO', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('BLD_usuário_ESPAÇO')
    mapeamento_VALOR = {'mode': 'método_MODO', 'header': 'Cabeçalho_VALOR', 'i': '순번', 'build_ccompiler': 'Criar_C_compilador', 'ar': 'arquivo_ferramenta', 'posix': '포직스경로', 'payload': 'carga_dados', 'flags': 'Configuração_BITS', 'cases': 'caso_de_teste', 'cc': 'C_compilador', 'data': 'dados', 'build_java_library': '자바라이브러리만들기', 'ld': 'vinculador_ferramenta', 'repo': 'repositório_caminho', 'build_python': 'Criar_PYTHON', 'inc': 'incluir_caminho', 'argument': '전달값', 'text': 'texto', 'headers': 'Cabeçalho_Lista', 'cxx': '시플플번역기', 'valid': 'válido', 'build': 'BLD', 'build_users': 'Criar_usuário_ESPAÇO', 'compiler': 'compilador_ferramenta', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'app_Cabeçalho_DESLOC', 'offset': 'DESLOC_VALOR', 'text_address': 'comando_email', 'abi': 'Ligar_ABI', 'assembly': 'assembly', 'run': 'Executar_comando', 'path': 'caminho', 'p': 'dados_cargo', 'changed': '바뀐자료', 'n': 'item_CONT_NÚM', 'flag': 'Configurações_VALOR', 'index': 'PROC_ÍNDICE', 'classes': 'aula_caminho', 'output': 'saída', 'loads': '적재구획', 'data_address': 'dados_email', 'symbol': 'símbolo_VALOR', 'root': 'raiz_email', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nome', 'value': 'VALOR', 'fmt': 'formato_932e03c8', 'work': '작업경로'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
