#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/teste_JVM.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('teste_JVM', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('teste_JVM')
    mapeamento_VALOR = {'message': 'aviso_SMS', 's': 'cadeia_dados', 'actual': 'real_RC', 'match': '일치', 'payload': 'carga_dados', 'cases': 'caso_de_teste', 'fixture': 'teste_dados', 'main': 'iniciar', 'ROOT': 'ação_raiz', 'text': 'texto', 'valid': 'válido', 'includes': '포함인수', 'include': 'incluir', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'concluído_valor', 'classes': 'aula_caminho', 'output': 'saída', 'result': 'resultado', 'cmd': '명령인수', 'name': 'Nome', 'jar': '자바꾸러미', 'report': 'validação_relatar', 'tests': 'lista_de_testes'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
