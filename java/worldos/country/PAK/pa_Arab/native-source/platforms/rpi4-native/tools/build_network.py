#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/بلڈ_نیٹ_ورک.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('بلڈ_نیٹ_ورک', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_نیٹ_ورک')
    대응 = {'obj': 'منزل_فائل', 'objects': 'منزل_مقصود_فائلاں', 'library': 'لائبریری', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'فائل_فرست', 'source': '원본자료', 'run': 'نفاذ_کرو_حکم', 'flags': '설정비트', 'path': 'راہ', 'build_network': 'بنڑاؤ_نیٹ_ورک_48d29d6d', 'cc': '시언어번역기', 'ar': 'محفوظہ_ٹول'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
