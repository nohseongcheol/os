#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/executar_Ficheiro.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('executar_Ficheiro', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('executar_Ficheiro')
    대응 = {'timeout': '시간제한', 's': 'cadea_datos', 'i': '순번', 'match': '일치', 'files': 'Ficheiro_Lista', 'program': 'apl', 'executable': '실행가능파일', 'args': 'argumento_MATRIZ', 'chunk': '조각', 'data': 'datos', 'proc': 'Proceso', 'send': 'enviar', 'main': 'Executar_2', 'marker': '확인표시', 'command': 'Orde', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'executar_comando', 'p': 'datos_cargo', 'parser': 'analizador', 'options': 'Opcións', 'kind': 'Categoría_VALOR', 'selector': '준비선택기', 'upload_data': 'carga_datos', 'end': 'finalizar_DESPRAZAMENTO', 'n': 'elemento_CONTAR', 'd': 'destino_datos', 'key': '누름값', 'output': '출력결과', 'line': 'Liña', 'name': 'Nome', 'upload_name': 'carga_nome', 'receive': '수신하기'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
