#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/예제시험.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'მონაცემები', 'graphics_command': 'გრაფიკა_ბრძანება', 'main': 'გაშვება', 'row': 'ჩაწერა_პოზიცია', 'init': '초기값', 'target': 'მიზანი', 'ROOT': 'პროეცირება_ფესვი', 'text': 'ტექსტი', 'binary': 'ორობითი', 'out': 'გაზომვა_მონაცემები', 'entry': 'შენატანი_პტ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'დაწყება_ნახატი', 'col': 'სვეტი_პოზიცია', 'begin': 'დაწყება_ოფსეტი', 'kind': 'კატეგორია_მნიშვნელობა', 'selector': 'სელექტორი', 'n': '개수', 'key': '누름값', 'y': 'Y_ღილაკი_კოორდინატი', 'client': 'კლიენტი', 'line': 'ხაზი', 'report': 'გადამოწმება_ანგარიში', 'language': 'ენა', 'x': 'x_კოორდინატა', 'start': 'გაშვება', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'გაგზავნა_სია', 'payload': 'დატვირთვა_მონაცემები', 'proc': 'პროცესი', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'სახელი_ცხრილი', 'content': 'შიგთავსი_მნიშვნელობა', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ფაილი_შენატანი_სახელი', 'shell': 'გარემო', 'color': '색상', 'transcript': '대화기록', 'offset': 'ოფსეტი_მნიშვნელობა', 'h': '높이값', 'run': 'შესრულება_ბრძანება', 'c': 'სიმბოლოს_კოდი', 'path': 'გეზი', 'encoding': 'კოდირება', 'end': 'დასასრული_ოფსეტი', 'ftp': 'ფაილი_გადატანა_კავშირი', 'pixels': '화소들', 'symbol': 'სიმბოლო_მნიშვნელობა', 'source': '원본자료', 'name': 'სახელი', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
