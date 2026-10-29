#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/파일전송시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'օգտակար_բեռնվածք_տվյալ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'տվյալ', 'proc': 'Գործընթաց', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Պահոց', 'main': 'Գործարկել', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'հաստատուն_աղբյուր', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'արձակել_արմատ', 'text': 'Տեքստ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Հրահանգ', 'out': 'չափ_տվյալ', 'expected': '예상결과', 'server_source': 'սպասարկիչ_աղբյուր', 'shell': 'խեցի', 'upload': 'վերբեռնել_Նիշքեր', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'կամուրջ', 'selector': 'ընտրիչ', 'end': 'վերջացնել_Տեղաշարժում', 'e': '보조항목', 'ftp': 'նիշք_փոխանցել_կապ', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'հավասարազոր_սարք_արժեք', 'result': 'չափ', 'unchanged': '보존자료', 'line': 'կապ', 'server_tcp_port': 'սպասարկիչ_հոսք_միացք', 'source': '원본자료', 'NetworkBridge': 'Ցանց_կամուրջ', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'վավերացում_զեկույց'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
