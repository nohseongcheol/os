#!/usr/bin/env python3
"""기존 Yolçıq 호환 진입점. 실제 구현: ../도구/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as 체계
from pathlib import Path as Yolçıq
체계.path.insert(0, str(Yolçıq(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': '자료', 'img': '그림', 'bits': '비트들', 'x': '가로좌표', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': '경로들', 'y': '세로좌표', 'main': 'Çaptır', 'src': '원본주소', 'fonts': '글꼴목록', 'ROOT': '기준', 'p': '자료위치', 'cp': '글자부호', 'target': '대상'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
