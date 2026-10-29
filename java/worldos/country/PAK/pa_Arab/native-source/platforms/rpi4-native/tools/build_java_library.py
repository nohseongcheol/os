#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'سرتحریر_قدر', 'sources': '원문목록', 'i': '순번', 'info': 'سسٹم_دی_معلومات', 'payload': 'پے_لوڈ_کوائف', 'src': '원본주소', 'run': 'نفاذ_کرو_حکم', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'درجہ_راہ', 'dist': '배포경로', 'archive': 'محفوظہ', 'output': '출력결과', 'root': '뿌리주소', 'name': 'ناں', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
