#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/compilar_Terminal_tipo_de_letra.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('compilar_Terminal_tipo_de_letra', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('compilar_Terminal_tipo_de_letra')
    대응 = {'data': 'datos', 'img': '그림', 'bits': 'Servizo_de_transferencia_intelixente_en_segundo_plano_Lista', 'x': 'X_coordenada', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'camiño_Lista', 'y': 'Y_coordenada', 'main': 'Executar_2', 'src': '원본주소', 'fonts': 'tipo_de_letra_Lista', 'ROOT': 'Project_raíz', 'p': 'datos_cargo', 'cp': 'carácter_codificación', 'target': 'obxectivo_VALOR'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
