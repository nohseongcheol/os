#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/курам_Желе.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('курам_Желе', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('курам_Желе')
    대응 = {'obj': 'көздөлгөн_файл', 'objects': 'көздөө_жайы_Файлдар', 'library': 'жыйнак', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'файл_Тизме', 'source': '원본자료', 'run': 'аткаруу_буйрук', 'flags': '설정비트', 'path': 'ЖОЛ', 'build_network': 'түзүү_Желе', 'cc': '시언어번역기', 'ar': 'Архив_курал'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
