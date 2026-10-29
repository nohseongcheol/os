#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'سەرپەڕ_نرخ', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'بارگەى_كرێ_دەیتا', 'src': '원본주소', 'run': 'جێبەجێکردن_فەرمان', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'کلاس_گوزەر', 'dist': '배포경로', 'archive': 'ئەرشیف', 'output': '출력결과', 'root': '뿌리주소', 'name': 'ناو', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
