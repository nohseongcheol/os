#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'سرۍ_ارزښت', 'sources': '원문목록', 'i': '순번', 'info': '정보', 'payload': '내용자료', 'src': '원본주소', 'run': '실행', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'پاړکى_يونلور', 'dist': '배포경로', 'archive': 'ارشیف', 'output': '출력결과', 'root': '뿌리주소', 'name': 'نوم', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
