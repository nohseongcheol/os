#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/دروستکراو_سیستم.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('دروستکراو_سیستم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('دروستکراو_سیستم')
    대응 = {'network': 'تۆڕ', 'BUILD': 'دروستکراو_گوزەر', 'ar': 'ئەرشیف_ئامراز', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'جۆرەپیت_دەیتا', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ئارگیومێنت_ڕیزی_داتا', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ڕێگا_تێنووسین', 'main': 'ڕادان', 'objcopy': 'شت_فایل_بگۆڕ', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'دروستکردن_بەکارهێنەر_مەودا', 'f': 'فایل_تێنووسین', 'extra': '추가영역', 'exports': 'دەرهێنان_خشتە', 'jobs': '빌드작업', 'run': 'جێبەجێکردن_فەرمان', 'path': 'گوزەر', 'REPO': '저장소', 'tool': 'ئامرازەکان', 'classes': 'کلاس_گوزەر', 'output': '출력결과', 'samples': '예제들', 'symbol': 'سیمبۆل_نرخ', 'source': '원본자료', 'name': 'ناو', 'build_network': 'دروستکردن_تۆڕ', 'font_info': 'جۆرەپیت_زانیاری', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
