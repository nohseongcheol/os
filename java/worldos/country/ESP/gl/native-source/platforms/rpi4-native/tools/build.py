#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/compilar_sistema.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('compilar_sistema', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('compilar_sistema')
    대응 = {'network': 'Rede', 'BUILD': 'compilar_camiño', 'ar': 'Arquivo_ferramenta', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'tipo_de_letra_datos', 'flags': 'configuración_Servizo_de_transferencia_intelixente_en_segundo_plano', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argumento_MATRIZ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': 'Executar_2', 'objcopy': 'obxecto_Ficheiro_convertedor', 'ROOT': 'Project_raíz', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'crear_usuario_espazo', 'f': 'Ficheiro_introdución', 'extra': '추가영역', 'exports': 'exportar_táboa', 'jobs': '빌드작업', 'run': 'executar_comando', 'path': 'CAMIÑO', 'REPO': 'repositorio_raíz', 'tool': 'Ferramentas', 'classes': 'Clase_camiño', 'output': '출력결과', 'samples': '예제들', 'symbol': 'símbolo_VALOR', 'source': '원본자료', 'name': 'Nome', 'build_network': 'crear_Rede', 'font_info': 'tipo_de_letra_información', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
