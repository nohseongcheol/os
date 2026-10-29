#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/파일전송시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'керектүү_жүктөө_ченеми_берилмелер', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'берилмелер', 'proc': 'Процесси', 'code': 'аткаруу_буйругу_ЫРААТТУУЛУК', 'linux': '리눅스파일', 'archive': 'Архив', 'main': 'Жүргүзүү', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'статикалык_башат', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Текст', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Команда', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'сервер_башат', 'shell': 'сырты', 'upload': 'жүктөп_жөнөтүү_Файлдар', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'селектор', 'end': 'аяктоо_Жылбышуу', 'e': '보조항목', 'ftp': 'файл_ташүү_туташуу', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'бирдей_маани', 'result': '결과', 'unchanged': '보존자료', 'line': 'сап', 'server_tcp_port': 'сервер_агым_порт', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ырастоо_отчет'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
