#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/부팅시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'პასუხი_1262b476', 'msg': 'ქსელი_წერილი', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'შესრულება', 'cancel': 'გაუქმება_ოპერაცია', 'cmd_byte': 'ბრძანება_ბაიტი', 'reply': 'პასუხი', 'points': '지점들', 'server': 'სერვერი_მნიშვნელობა', 'data': 'მონაცემები', 'prompt': 'მოთხოვნა', 'enter': 'შეყვანა', 'imported': '들여온파일', 'send': 'გაგზავნა', 'main': 'გაშვება', 'ROOT': 'პროეცირება_ფესვი', 'text': 'ტექსტი', 'first_gui': '첫화면', 'pixel': 'პიქსელი', 'java_class': '자바클래스', 'upload': 'ატვირთვა_ფაილები', 'pixels_file': 'პიქსელი_ფაილი', 'pixels_data': 'პიქსელი_მონაცემები', 'edit': 'რედაქტირება_მნიშვნელობა', 'receive_until': '표시까지받기', 'selector': 'სელექტორი', 'size': 'ზომა', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_ღილაკი_კოორდინატი', 'result': 'გაზომვა', 'samples': '예제들', 'client': 'კლიენტი', 'line': 'ხაზი', 'report': 'გადამოწმება_ანგარიში', 'work': '작업경로', 'x': 'x_კოორდინატა', 'python_checks': '파이썬검사', 'download': 'ჩამოტვირთვა', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'პროცესი', 'content': 'შიგთავსი_მნიშვნელობა', 'block': 'მონაცემები_დაბლოკვა', 'marker': '확인표시', 'command': 'ბრძანება', 'expected': '예상결과', 'shell': 'გარემო', 'drawing': 'ნახატი_მდებარეობა', 'f': 'ფაილი_შენატანი', 'transcript': '대화기록', 'offset': 'ოფსეტი_მნიშვნელობა', 'path': 'გეზი', 'screenshot': 'ეკრანის_ამოჭრა', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ნაკადი_მნიშვნელობა', 'cmd': '명령인수', 'name': 'სახელი', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
