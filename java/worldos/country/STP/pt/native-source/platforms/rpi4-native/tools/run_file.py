#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/Executar_Arquivo.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Executar_Arquivo', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('Executar_Arquivo')
    mapeamento_VALOR = {'timeout': 'execução_TEMPOLIMITE', 's': 'cadeia_dados', 'i': '순번', 'match': '일치', 'files': 'lista_de_arquivos', 'program': 'app', 'executable': 'executável_foto', 'args': 'argumento_MATRIZ', 'chunk': 'fragmento_VALOR', 'data': 'dados', 'proc': 'Processo', 'send': 'enviar', 'main': 'iniciar', 'marker': 'favorito', 'command': 'comando', 'include': 'incluir', 'dumped': '갈무리자료', 'run': 'Executar_comando', 'p': 'dados_cargo', 'parser': 'analisador', 'options': 'Opções', 'kind': 'área_VALOR', 'selector': 'seletor', 'upload_data': 'Upload_dados', 'end': 'encerrar_DESLOC', 'n': 'item_CONT_NÚM', 'd': 'destino_dados', 'key': '누름값', 'output': 'saída', 'line': 'linha_de_entrada', 'name': 'Nome', 'upload_name': 'Upload_nome', 'receive': 'receber_email'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
