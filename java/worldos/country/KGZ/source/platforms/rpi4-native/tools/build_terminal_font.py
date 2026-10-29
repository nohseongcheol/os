#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'берилмелер', 'img': 'чийүү_маани', 'bits': '비트들', 'x': 'x_координата', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'жол_Тизме', 'y': '세로좌표', 'main': 'Жүргүзүү', 'src': '원본주소', 'fonts': 'арип_Тизме', 'ROOT': '기준', 'p': '자료위치', 'cp': 'символ_коддоо', 'target': 'максат'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
