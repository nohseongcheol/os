#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/دروستکراو_تۆڕ.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('دروستکراو_تۆڕ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('دروستکراو_تۆڕ')
    대응 = {'obj': 'فایلی_شوێنی_مه_به_ستی', 'objects': 'جێمەبەست_فایله_کان', 'library': 'کتێبخانە', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'فایل_لیست', 'source': '원본자료', 'run': 'جێبەجێکردن_فەرمان', 'flags': '설정비트', 'path': 'گوزەر', 'build_network': 'دروستکردن_تۆڕ', 'cc': '시언어번역기', 'ar': 'ئەرشیف_ئامراز'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
