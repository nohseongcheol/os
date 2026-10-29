#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/파일전송시험.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ашигтай_ачаалал_өгөгдөл', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'өгөгдөл', 'proc': 'үйл_явц', 'code': 'заавар_ДАРААЛАЛ', 'linux': '리눅스파일', 'archive': 'Архив', 'main': 'Ажиллуулах', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'статик_эх', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Бичвэр', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Тушаал', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'сервер_эх', 'shell': 'бүрхүүл', 'upload': 'байршуулах_Файлууд', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'сонгогч', 'end': 'дуусгах_Оффсет', 'e': '보조항목', 'ftp': 'файл_дамжуулах_холболт', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ижил_түвшин_утга', 'result': '결과', 'unchanged': '보존자료', 'line': 'Шугам', 'server_tcp_port': 'сервер_урсгал_порт', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'баталгаажуулалт_тайлан'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
