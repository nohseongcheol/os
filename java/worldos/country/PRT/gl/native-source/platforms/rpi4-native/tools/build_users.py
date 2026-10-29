#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/compilar_usuario_espazo.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('compilar_usuario_espazo', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('compilar_usuario_espazo')
    대응 = {'mode': '방식', 'header': 'Cabeceira_VALOR', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arquivo_ferramenta', 'posix': '포직스경로', 'payload': 'carga_datos_60367a51', 'flags': 'configuración_Servizo_de_transferencia_intelixente_en_segundo_plano', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'datos', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'repositorio_camiño', 'build_python': 'crear_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Texto', 'headers': 'Cabeceira_Lista', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'compilar', 'build_users': 'crear_usuario_espazo', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'apl_Cabeceira_DESPRAZAMENTO', 'offset': 'DESPRAZAMENTO_VALOR', 'text_address': 'comando_ENDEREZO', 'abi': '호출규약', 'assembly': 'ensamblado', 'run': 'executar_comando', 'path': 'CAMIÑO', 'p': 'datos_cargo', 'changed': '바뀐자료', 'n': 'elemento_CONTAR', 'flag': 'Configuración_VALOR', 'index': 'Busca_ÍNDICE', 'classes': 'Clase_camiño', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'datos_ENDEREZO', 'symbol': 'símbolo_VALOR', 'root': 'raíz_ENDEREZO', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nome', 'value': 'VALOR', 'fmt': 'formato_932e03c8', 'work': '작업경로'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
