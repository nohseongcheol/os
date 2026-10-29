#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/화면요소시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'х_координат', 's': 'мөр_өгөгдөл', 'i': '순번', 'sel': 'сонгогч_a916db4e', 'seconds': '초단위', 'log': 'бичих_мөр_6e8b375a', 'data': 'өгөгдөл', 'at': '현재위치', 'send': 'илгээх', 'main': 'Ажиллуулах', 'req': '요청값', 'hot': 'файлын_холбоос_утга', 'pump': 'барих_үйлдэл', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Тушаал', 'shell': 'бүрхүүл', 'f': 'файл_оролт', 'click': 'товших_товч', 'k': '셋째순번', 'c': 'тэмдэгтийн_код', 'r': '반환값', 'p': '자료위치', 'command_mode': 'команд_горим', 'end': 'дуусгах_Оффсет', 'classes': 'класс_зам', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'баталгаажуулалт_тайлан', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
