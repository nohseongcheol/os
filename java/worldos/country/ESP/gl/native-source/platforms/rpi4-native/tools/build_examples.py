#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/예제빌드.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('예제빌드')
    대응 = {'out': 'medida_datos', 'build_examples': '예제만들기', 'files': 'Ficheiro_Lista', 'java': '자바실행', 'run': 'executar_comando', 'path': 'CAMIÑO', 'p': 'datos_cargo', 'readme': 'Léame', 'build_java_library': '자바라이브러리만들기', 'code': 'instrución_SECUENCIA', 'index': 'Busca_ÍNDICE', 'classes': 'Clase_camiño', 'repo': 'repositorio_camiño', 'root': 'raíz_ENDEREZO', 'content': 'Contido_VALOR', 'source': '원본자료', 'name': 'Nome', 'target': 'obxectivo_VALOR', 'manifest': '꾸러미명세', 'language': 'Idioma'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
