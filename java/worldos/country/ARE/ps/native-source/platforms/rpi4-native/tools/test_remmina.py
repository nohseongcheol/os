#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/원격한글시험.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ځغلول', 'profile': 'کارن_پېژنيال', 'focused': '초점요소', 'serial': '직렬입출력', 'keys': '누름열', 'server': '서버', 'log': 'خبرال_کیل', 'args': 'ارزښتوړى_لړوند', 'deadline': '마감시각', 'data': 'اومتوک', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ځغلول', 'ready': '준비완료', 'found': '찾은결과', 'guest': '커널실행', 'ROOT': '기준', 'marker': '확인표시', 'text': 'ليکنه', 'out': '결과자료', 'env': '환경', 'f': 'دوتنه_ننوت', 'port': '접속번호', 'offset': '변위', 'version': '판번호', 'p': '자료위치', 'selector': '준비선택기', 'xvfb': 'اوڅاريز_ښوون', 'display': 'ښوون', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'نوم', 'window': 'کړکۍ', 'report': 'باورکړن_راپور', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
