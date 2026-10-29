#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/셸시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'х_координат', 'msg': 'Сүлжээ_мэдээлэл', 'i': '순번', 'reply': 'хариулах', 'call': '호출', 'args': 'аргумент_олонлог', 'chunk': '조각', 'data': 'өгөгдөл', 'proc': 'үйл_явц', 'long_text': '긴글', 'restored': '복원자료', 'send': 'илгээх', 'file': 'Файл', 'main': 'Ажиллуулах', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Бичвэр', 'marker': '확인표시', 'command': 'Тушаал', 'expected': '예상결과', 'pixel': 'нягтрал', 'shell': 'бүрхүүл', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'дуусгах_Оффсет', 'image': 'зураг', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'клиент', 'line': 'Шугам', 'stream': 'урсгал_утга', 'name': 'Нэр', 'value': 'утга', 'receive': '수신하기', 'report': 'баталгаажуулалт_тайлан', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
