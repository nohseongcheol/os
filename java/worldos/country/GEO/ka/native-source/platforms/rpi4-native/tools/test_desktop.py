#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/바탕화면시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_კოორდინატა', 'typing': '글자입력', 'message': '알림문', 'start': 'გაშვება', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': 'დაჭერა_კლავიში', 'rectangles': '사각형들', 'sym': 'სიმბოლო', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'პროცესი', 'data': 'მონაცემები', 'main': 'გაშვება', 'w': '너비값', 'init': '초기값', 'block': 'მონაცემები_დაბლოკვა', 'ROOT': 'პროეცირება_ფესვი', 'text': 'ტექსტი', 'marker': '확인표시', 'report': 'გადამოწმება_ანგარიში', 'until': '까지', 'clipboard': 'გაცვლის_ბუფერი_მნიშვნელობა', 'dst': 'მიმართულება_მისამართი', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ოფსეტი_მნიშვნელობა', 'h': '높이값', 'src': '원본주소', 'event': 'მოვლენა', 'encoding': 'კოდირება', 'size': 'ზომა', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_ღილაკი_კოორდინატი', 'output': '출력결과', 'symbol': 'სიმბოლო_მნიშვნელობა', 'client': 'კლიენტი', 'char': 'სიმბოლო_მონაცემები_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
