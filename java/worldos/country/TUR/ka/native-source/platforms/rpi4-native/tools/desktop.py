#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/სამუშაო_დაფა_ხედი.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('სამუშაო_დაფა_ხედი', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('სამუშაო_დაფა_ხედი')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'შეცდომა', 'exact': '정확한값', 'network': 'ქსელი', 'closed': '닫힘', 'length': 'სიგრძე_მნიშვნელობა', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'სერვერი_მნიშვნელობა', 'resources': 'რესურსები', 'data': 'მონაცემები', 'shift': 'SHIFT_კლავიში', 'send': 'გაგზავნა', 'run_desktop': 'სერია_სამუშაო_დაფა', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'მასპინძელი', 'text': 'ტექსტი', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': 'ხიდი', 'kind': 'კატეგორია_მნიშვნელობა', 'tail': '끝부분', 'size': 'ზომა', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_ღილაკი_კოორდინატი', 'prefix': '앞부분', 'client': 'კლიენტი', 'char': 'სიმბოლო_მონაცემები_4d9f8719', 'work': '작업경로', 'Keyboard': 'კლავიატურა', 'x': 'x_კოორდინატა', 'down': '누르는중', 'net': 'ქსელი_ხიდი_შენატანი', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'არგუმენტი_მასივი', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'პროცესი', 'Desktop': 'დაკავშირება_სამუშაო_დაფა', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'გადართვა_რეჟიმი', 'command': 'ბრძანება', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_კლავიში', 'path': 'გეზი', 'cp': 'სიმბოლო_კოდირება', 'terminate': '종료시키기', 'security': 'უსაფრთხოება', 'vnc_port': '원격화면접속번호', 'body': 'ძირითადი_ტექსტი', 'index': 'ძებნა_ინდექსი', 'exited': '종료됨', 'keysym': 'კლავიში_სიმბოლო', 'output': '출력결과', 'keyboard': 'კლავიატურა_შენატანი', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'წამკითხველი', 'NetworkBridge': 'ქსელი_ხიდი', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
