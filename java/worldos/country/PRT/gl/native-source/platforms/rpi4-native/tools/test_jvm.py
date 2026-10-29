#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/자바가상기계시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'cadea_datos', 'actual': 'real_medida', 'match': '일치', 'payload': 'carga_datos_60367a51', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Executar_2', 'ROOT': 'Project_raíz', 'text': 'Texto', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Completadas_cantidade', 'classes': 'Clase_camiño', 'output': '출력결과', 'result': 'RESULTANTE', 'cmd': '명령인수', 'name': 'Nome', 'jar': '자바꾸러미', 'report': 'validación_informe', 'tests': '시험목록'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
