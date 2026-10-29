#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/자바라이브러리빌드.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('자바라이브러리빌드')
    대응 = {'header': 'Cabeceira_VALOR', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'carga_datos_60367a51', 'src': '원본주소', 'run': 'executar_comando', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'Clase_camiño', 'dist': '배포경로', 'archive': 'Arquivo', 'output': '출력결과', 'root': 'raíz_ENDEREZO', 'name': 'Nome', 'jar': '자바꾸러미', 'b': 'SEGUNDO_VALOR', 'entries': '항목들'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
