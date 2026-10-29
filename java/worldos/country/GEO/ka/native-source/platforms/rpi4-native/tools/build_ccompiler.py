#!/usr/bin/env python3
"""기존 გეზი 호환 შენატანი_პტ. რეალური_მონაცემები 구현: ../ხელსაწყოები/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ოპერაციული_სისტემა_მნიშვნელობა
from pathlib import Path as გეზი
ოპერაციული_სისტემა_მნიშვნელობა.path.insert(0, str(გეზი(__file__).resolve().parents[1] / 'ხელსაწყოები'))
if __name__ == '__main__':
    import runpy as აპი_გამშვები
    აპი_გამშვები.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'გაზომვა_მონაცემები', 'builtins': '내장연산', 'header': 'ზედა_კოლონტიტული_მნიშვნელობა', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'შესრულება_ბრძანება', 'flags': '설정비트', 'path': 'გეზი', 'p': 'მონაცემები_პოზიცია', 'cc': '시언어번역기', 'obj': 'დანიშნულების_ფაილი', 'flag': 'პარამეტრები_მნიშვნელობა', 'ld': '연결편집기', 'objects': 'მიმართულება_ფაილები', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'ფესვი_მისამართი', 'assets': '탑재자료', 'source': '원본자료', 'name': 'სახელი', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
