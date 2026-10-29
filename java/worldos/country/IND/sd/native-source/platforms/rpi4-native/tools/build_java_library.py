#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'هيڊر_قدر', 'sources': '원문목록', 'i': '순번', 'info': 'سسٽم_معلومات', 'payload': 'بنيادي_بار_ڪوائف', 'src': '원본주소', 'run': 'تعميل_ڪرڻ_حڪم', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'درجو_راههه', 'dist': '배포경로', 'archive': 'محفوظ', 'output': '출력결과', 'root': '뿌리주소', 'name': 'نالو', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
