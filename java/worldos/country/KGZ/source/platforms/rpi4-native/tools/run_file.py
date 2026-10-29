#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/аткаруу_файл.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('аткаруу_файл', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('аткаруу_файл')
    대응 = {'timeout': '시간제한', 's': 'сап_берилмелер', 'i': '순번', 'match': '일치', 'files': 'файл_Тизме', 'program': 'програм', 'executable': '실행가능파일', 'args': 'аргумент_МАССИВ', 'chunk': '조각', 'data': 'берилмелер', 'proc': 'Процесси', 'send': 'жөнөтүү', 'main': 'Жүргүзүү', 'marker': '확인표시', 'command': 'Команда', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'аткаруу_буйрук', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Параметрлер', 'kind': 'категория_маани', 'selector': 'селектор', 'upload_data': 'жүктөп_жөнөтүү_берилмелер', 'end': 'аяктоо_Жылбышуу', 'n': '개수', 'd': 'көздөө_жайы_берилмелер', 'key': '누름값', 'output': '출력결과', 'line': 'сап', 'name': 'Аты', 'upload_name': 'жүктөп_жөнөтүү_аты', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
