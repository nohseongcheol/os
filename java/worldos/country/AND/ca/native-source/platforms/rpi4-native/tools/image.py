#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/Crear_IMATGE.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('Crear_IMATGE', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('Crear_IMATGE')
    대응 = {'total': 'total_capacitat', 'start': 'Executa_2', 'firmware': '기초제어프로그램', 'files': 'arxiu_Llista', 'archive_base': 'Arxiu_BASE', 'partition': 'partició_arxiu', 'archive': 'Arxiu', 'main': 'Executa_2', 'block': 'dades_bloquejar', 'ROOT': 'Project_rel', 'boot': '부팅경로', 'stage': 'fase_VALOR', 'out': 'mesura_dades', 'expected': '예상결과', 'f': 'arxiu_introducció', 'src': '원본주소', 'path': 'Camí', 'p': 'dades_càrrec', 'extracted': '추출자료', 'member': 'membre', 'mbr': '주부트기록', 'image': 'IMATGE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'llicència', 'source': '원본자료', 'name': 'Nom', 'value': 'VALOR', 'manifest': '꾸러미명세', 'dest': 'destinació_VALOR_càrrec', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
