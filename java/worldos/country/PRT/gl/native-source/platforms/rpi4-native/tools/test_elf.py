#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/실행파일시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('실행파일시험')
    대응 = {'out': 'medida_datos', 'expected': '예상결과', 'phoff': 'apl_Cabeceira_DESPRAZAMENTO', 'offset': 'DESPRAZAMENTO_VALOR', 'invalid': 'non_válido_datos', 'path': 'CAMIÑO', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'RESULTANTE', 'format_': 'formato_b87fd068', 'main': 'Executar_2', 'content': 'Contido_VALOR', 'source': '원본자료', 'name': 'Nome', 'reference': 'Comparación_liña_base', 'ROOT': 'Project_raíz', 'value': 'VALOR', 'report': 'validación_informe'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
