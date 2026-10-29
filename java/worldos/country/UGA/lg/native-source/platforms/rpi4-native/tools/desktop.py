#!/usr/bin/env python3
"""기존 경로 호환 진입점. 실제 구현: ../도구/바탕화면.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as 경로
체계.path.insert(0, str(경로(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('바탕화면', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Kiremya', 'exact': '정확한값', 'network': '통신사용', 'closed': '닫힘', 'length': '길이', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': '서버', 'resources': '자원관리', 'data': '자료', 'shift': '윗글쇠', 'send': '보내기', 'run_desktop': '바탕화면실행', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': '호스트', 'text': 'Bigambo', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': '분류', 'tail': '끝부분', 'size': 'Bunene', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': '접속자', 'char': '글자값', 'work': '작업경로', 'Keyboard': '글쇠판', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': '인수배열', 'Hangul': '한글조합', 'chunk': '조각', 'proc': '실행과정', 'Desktop': '바탕화면연결', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': '전환', 'command': 'Mulimu', 'sock': '소켓', 'frame': '실행틀', 'ctrl': '제어글쇠', 'path': '경로', 'cp': '글자부호', 'terminate': '종료시키기', 'security': '보호정책', 'vnc_port': '원격화면접속번호', 'body': '본문', 'index': '색인', 'exited': '종료됨', 'keysym': '글쇠기호', 'output': '출력결과', 'keyboard': '글쇠판항목', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': '읽기작업', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
