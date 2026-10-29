#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/BLD_Terminál_písmo.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('BLD_Terminál_písmo', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('BLD_Terminál_písmo')
    대응 = {'data': 'data', 'img': 'kreslení_HODNOTA', 'bits': 'BITS_Seznam', 'x': 'souřadnice_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'cesta_Seznam', 'y': 'Y_souřadnice', 'main': 'Spustit_2', 'src': '원본주소', 'fonts': 'písmo_Seznam', 'ROOT': 'akce_kořen', 'p': 'data_pozice', 'cp': 'kódování_znaků', 'target': 'cílová_úroveň'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
