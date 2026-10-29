#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'ڪوائف', 'img': 'ڊرائنگ_قدر', 'bits': '비트들', 'x': 'x_رطبو', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'راههه_فهرست', 'y': '세로좌표', 'main': 'هلائڻ', 'src': '원본주소', 'fonts': 'فانٽ_فهرست', 'ROOT': '기준', 'p': '자료위치', 'cp': 'ڪريڪٽر_ضابطه_ربائي', 'target': 'هدف'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
