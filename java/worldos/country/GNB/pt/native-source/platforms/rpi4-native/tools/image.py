#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/Criar_foto.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('Criar_foto', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('Criar_foto')
    mapeamento_VALOR = {'total': 'total_capacidade', 'start': 'iniciar', 'firmware': 'firmware_VALOR', 'files': 'lista_de_arquivos', 'archive_base': 'arquivo_BASE', 'partition': 'partição_Arquivo', 'archive': 'arquivo', 'main': 'iniciar', 'block': 'bloco_de_dados', 'ROOT': 'ação_raiz', 'boot': '부팅경로', 'stage': 'fase_VALOR', 'out': 'RC_dados', 'expected': '예상결과', 'f': 'Arquivo_entrada', 'src': '원본주소', 'path': 'caminho', 'p': 'dados_cargo', 'extracted': '추출자료', 'member': 'membro', 'mbr': 'registo_principal_de_arranque', 'image': 'foto', 'sector_count': '섹터개수', 'dist': 'distribuição_caminho', 'sha': 'calcular_hash', 'license_': 'licença', 'source': '원본자료', 'name': 'Nome', 'value': 'VALOR', 'manifest': 'grupo_manifesto', 'dest': 'destino_VALOR_cargo', 'work': '작업경로'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
