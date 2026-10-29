#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/파일전송시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'жүктеме_деректер', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'деректер', 'proc': 'Үрдіс', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Мұрағат', 'main': 'Орындау_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'тұрақты_көз', 'java_source': '자바원문', 'echo': 'экранға_шығару_сервер_енгізу', 'ROOT': 'жоба_түбір', 'text': 'Мәтін', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Команда', 'out': 'өлшем_деректер', 'expected': '예상결과', 'server_source': 'сервер_көз', 'shell': 'қоршам', 'upload': 'Жүктеп_салу_Файлдар', 'transcript': '대화기록', 'port': 'порт_нөмірі', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'көпір', 'selector': 'селектор', 'end': 'тоқтату_жылжыту', 'e': '보조항목', 'ftp': 'файл_тасымалдау_қосылым', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'бір_рангілі_мән', 'result': 'НӘТИЖЕ', 'unchanged': '보존자료', 'line': 'Жол', 'server_tcp_port': 'сервер_ағым_порт', 'source': '원본자료', 'NetworkBridge': 'желі_көпір', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'тексерім_есеп'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
