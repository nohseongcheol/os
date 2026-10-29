#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/Гүйцэтгэх_файл.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('Гүйцэтгэх_файл', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Гүйцэтгэх_файл')
    대응 = {'timeout': '시간제한', 's': 'мөр_өгөгдөл', 'i': '순번', 'match': '일치', 'files': 'файл_Жагсаалт', 'program': 'програм', 'executable': '실행가능파일', 'args': 'аргумент_олонлог', 'chunk': '조각', 'data': 'өгөгдөл', 'proc': 'үйл_явц', 'send': 'илгээх', 'main': 'Ажиллуулах', 'marker': '확인표시', 'command': 'Тушаал', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Гүйцэтгэх_команд', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Сонголтууд', 'kind': 'ангилал_утга', 'selector': 'сонгогч', 'upload_data': 'байршуулах_өгөгдөл', 'end': 'дуусгах_Оффсет', 'n': '개수', 'd': 'товлосон_газар_өгөгдөл', 'key': '누름값', 'output': '출력결과', 'line': 'Шугам', 'name': 'Нэр', 'upload_name': 'байршуулах_нэр', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
