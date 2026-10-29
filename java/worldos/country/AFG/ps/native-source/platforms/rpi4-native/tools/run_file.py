#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/파일실행.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일실행')
    대응 = {'timeout': '시간제한', 's': 'مزى_اومتوک', 'i': '순번', 'match': '일치', 'files': '파일목록', 'program': 'کاريال', 'executable': '실행가능파일', 'args': 'ارزښتوړى_لړوند', 'chunk': '조각', 'data': 'اومتوک', 'proc': 'بهير', 'send': 'استول', 'main': 'ځغلول', 'marker': '확인표시', 'command': 'بولۍ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': '실행', 'p': '자료위치', 'parser': '인수해석기', 'options': 'غوراوي', 'kind': 'ټولۍ_ارزښت', 'selector': '준비선택기', 'upload_data': 'ورلېښل_اومتوک', 'end': '끝위치', 'n': '개수', 'd': 'موخه_اومتوک', 'key': '누름값', 'output': '출력결과', 'line': 'ليکه', 'name': 'نوم', 'upload_name': '올릴이름', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
