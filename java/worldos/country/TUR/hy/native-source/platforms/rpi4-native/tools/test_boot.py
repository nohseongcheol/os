#!/usr/bin/env python3
"""기존 Ճանապարհ 호환 մուտքագրում_կետ. իրական_տվյալ 구현: ../Գործիքներ/부팅시험.py"""
import importlib as 가져오기
import sys as գործավար_համակարգ_արժեք
from pathlib import Path as Ճանապարհ
գործավար_համակարգ_արժեք.path.insert(0, str(Ճանապարհ(__file__).resolve().parents[1] / 'Գործիքներ'))
if __name__ == '__main__':
    import runpy as ծրագիր_թողարկիչ
    ծրագիր_թողարկիչ.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Ցանց_ուղերձ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Կատարել', 'cancel': 'ապընտրել_գործողություն', 'cmd_byte': 'հրաման_բայթ', 'reply': 'պատասխանել', 'points': '지점들', 'server': 'սպասարկիչ_արժեք', 'data': 'տվյալ', 'prompt': 'հուշում', 'enter': 'մուտքագրել', 'imported': '들여온파일', 'send': 'ուղարկել', 'main': 'Գործարկել', 'ROOT': 'արձակել_արմատ', 'text': 'Տեքստ', 'first_gui': '첫화면', 'pixel': 'փիքսել', 'java_class': '자바클래스', 'upload': 'վերբեռնել_Նիշքեր', 'pixels_file': 'փիքսել_նիշք', 'pixels_data': 'փիքսել_տվյալ', 'edit': 'խմբագրել_արժեք', 'receive_until': '표시까지받기', 'selector': 'ընտրիչ', 'size': 'Չափս', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'չափ', 'samples': '예제들', 'client': 'սպասառու', 'line': 'կապ', 'report': 'վավերացում_զեկույց', 'work': '작업경로', 'x': 'x_կոորդինատ', 'python_checks': '파이썬검사', 'download': 'ներբեռնել', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Գործընթաց', 'content': 'Բովանդակություն_արժեք', 'block': 'տվյալ_արգելափակել', 'marker': '확인표시', 'command': 'Հրահանգ', 'expected': '예상결과', 'shell': 'խեցի', 'drawing': 'նկար_ուղի', 'f': 'նիշք_մուտքագրում', 'transcript': '대화기록', 'offset': 'Տեղաշարժում_արժեք', 'path': 'Ճանապարհ', 'screenshot': 'էկրանի_պատկեր', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'հոսք_արժեք', 'cmd': '명령인수', 'name': 'Անուն', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
