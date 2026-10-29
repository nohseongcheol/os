#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/crear_IMAXE.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('crear_IMAXE', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('crear_IMAXE')
    대응 = {'total': '총량', 'start': 'Executar_2', 'firmware': '기초제어프로그램', 'files': 'Ficheiro_Lista', 'archive_base': 'Arquivo_BASE', 'partition': 'partición_Ficheiro', 'archive': 'Arquivo', 'main': 'Executar_2', 'block': 'datos_bloquear', 'ROOT': 'Project_raíz', 'boot': '부팅경로', 'stage': 'fase_VALOR', 'out': 'medida_datos', 'expected': '예상결과', 'f': 'Ficheiro_introdución', 'src': '원본주소', 'path': 'CAMIÑO', 'p': 'datos_cargo', 'extracted': '추출자료', 'member': 'membro', 'mbr': '주부트기록', 'image': 'IMAXE', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'licenciar', 'source': '원본자료', 'name': 'Nome', 'value': 'VALOR', 'manifest': '꾸러미명세', 'dest': 'destino_VALOR_cargo', 'work': '작업경로'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
