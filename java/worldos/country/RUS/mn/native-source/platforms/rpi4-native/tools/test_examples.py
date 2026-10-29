#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/예제시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'өгөгдөл', 'graphics_command': '그림명령', 'main': 'Ажиллуулах', 'row': '행위치', 'init': '초기값', 'target': 'зорилго', 'ROOT': '기준', 'text': 'Бичвэр', 'binary': 'хоёрт', 'out': '결과자료', 'entry': 'оролт_цэг', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Эхлэл_зураг', 'col': '열위치', 'begin': 'Эхлэл_Оффсет', 'kind': 'ангилал_утга', 'selector': 'сонгогч', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'клиент', 'line': 'Шугам', 'report': 'баталгаажуулалт_тайлан', 'language': 'Хэл', 'x': 'х_координат', 'start': 'Ажиллуулах', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'илгээх_Жагсаалт', 'payload': 'ашигтай_ачаалал_өгөгдөл', 'proc': 'үйл_явц', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'нэр_хүснэгт', 'content': 'Агуулга_утга', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'файл_оролт_нэр', 'shell': 'бүрхүүл', 'color': '색상', 'transcript': '대화기록', 'offset': 'Оффсет_утга', 'h': '높이값', 'run': 'Гүйцэтгэх_команд', 'c': 'тэмдэгтийн_код', 'path': 'ЗАМ', 'encoding': 'тэмдэгтийн_олонлог', 'end': 'дуусгах_Оффсет', 'ftp': 'файл_дамжуулах_холболт', 'pixels': '화소들', 'symbol': 'тэмдэг_утга', 'source': '원본자료', 'name': 'Нэр', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
