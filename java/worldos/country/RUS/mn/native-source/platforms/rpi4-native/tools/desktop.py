#!/usr/bin/env python3
"""기존 ЗАМ 호환 оролт_цэг. бодит_өгөгдөл 구현: ../Хэрэгслүүд/дэлгэц_харах.py"""
import importlib as 가져오기
import sys as үйлдлийн_систем_утга
from pathlib import Path as ЗАМ
үйлдлийн_систем_утга.path.insert(0, str(ЗАМ(__file__).resolve().parents[1] / 'Хэрэгслүүд'))
if __name__ == '__main__':
    import runpy as програм_гишүүн
    програм_гишүүн.run_module('дэлгэц_харах', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('дэлгэц_харах')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Алдаа', 'exact': '정확한값', 'network': 'Сүлжээ', 'closed': '닫힘', 'length': 'урт_утга', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'сервер_утга', 'resources': 'Эх_үүсвэрүүд', 'data': 'өгөгдөл', 'shift': 'SHIFT_товчлуур', 'send': 'илгээх', 'run_desktop': 'ажиллах_дэлгэц', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'хост', 'text': 'Бичвэр', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'ангилал_утга', 'tail': '끝부분', 'size': 'Хэмжээ', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'клиент', 'char': 'тэмдэгт_өгөгдөл', 'work': '작업경로', 'Keyboard': 'товчлуурт_гар', 'x': 'х_координат', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'аргумент_олонлог', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'үйл_явц', 'Desktop': 'холбох_дэлгэц', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'шилжих_горим', 'command': 'Тушаал', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_товчлуур', 'path': 'ЗАМ', 'cp': 'тэмдэгт_кодчлол', 'terminate': '종료시키기', 'security': 'хамгаалалт', 'vnc_port': '원격화면접속번호', 'body': 'үндсэн_бичвэр', 'index': '색인', 'exited': '종료됨', 'keysym': 'түлхүүр_тэмдэг', 'output': '출력결과', 'keyboard': 'товчлуурт_гар_оролт', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Уншигч', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
