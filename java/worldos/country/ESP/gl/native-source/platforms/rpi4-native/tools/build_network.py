#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/compilar_Rede.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('compilar_Rede', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('compilar_Rede')
    대응 = {'obj': 'ficheiro_de_destino', 'objects': 'destino_Ficheiros', 'library': 'biblioteca', 'output': '출력결과', 'port': 'número_do_porto', 'root': 'raíz_ENDEREZO', 'files': 'Ficheiro_Lista', 'source': '원본자료', 'run': 'executar_comando', 'flags': 'configuración_Servizo_de_transferencia_intelixente_en_segundo_plano', 'path': 'CAMIÑO', 'build_network': 'crear_Rede', 'cc': '시언어번역기', 'ar': 'Arquivo_ferramenta'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
