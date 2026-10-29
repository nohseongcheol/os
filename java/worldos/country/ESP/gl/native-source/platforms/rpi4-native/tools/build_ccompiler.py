#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/시언어번역기빌드.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('시언어번역기빌드')
    대응 = {'out': 'medida_datos', 'builtins': '내장연산', 'header': 'Cabeceira_VALOR', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'executar_comando', 'flags': 'configuración_Servizo_de_transferencia_intelixente_en_segundo_plano', 'path': 'CAMIÑO', 'p': 'datos_cargo', 'cc': '시언어번역기', 'obj': 'ficheiro_de_destino', 'flag': 'Configuración_VALOR', 'ld': '연결편집기', 'objects': 'destino_Ficheiros', 'repo': 'repositorio_camiño', 'v': '임시값', 'upstream': 'ascendente', 'root': 'raíz_ENDEREZO', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nome', 'includes': '포함인수'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
