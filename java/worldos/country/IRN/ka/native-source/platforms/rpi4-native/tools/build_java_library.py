#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ზედა_კოლონტიტული_მნიშვნელობა', 'sources': '원문목록', 'i': '순번', 'info': 'სისტემის_ინფორმაცია', 'payload': 'დატვირთვა_მონაცემები', 'src': '원본주소', 'run': 'შესრულება_ბრძანება', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'კლასი_მდებარეობა', 'dist': '배포경로', 'archive': 'არქივი', 'output': '출력결과', 'root': 'ფესვი_მისამართი', 'name': 'სახელი', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
