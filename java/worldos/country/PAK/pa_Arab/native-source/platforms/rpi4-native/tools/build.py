#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/بلڈ_نظام.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('بلڈ_نظام', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_نظام')
    대응 = {'network': 'نیٹ_ورک', 'BUILD': 'بلڈ_راہ', 'ar': 'محفوظہ_ٹول', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'فانٹ_کوائف', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'دلیل_ایرے', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'طریقہ_داخلہ', 'main': 'چلاؤ', 'objcopy': 'آبجیکٹ_فائل_تبدیل_کرنڑ_آلا', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'بنڑاؤ_صارف_جگہ', 'f': 'فائل_داخلہ', 'extra': '추가영역', 'exports': 'برآمد_جدول', 'jobs': '빌드작업', 'run': 'نفاذ_کرو_حکم', 'path': 'راہ', 'REPO': '저장소', 'tool': 'اوزار', 'classes': 'درجہ_راہ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'علامت_قدر', 'source': '원본자료', 'name': 'ناں', 'build_network': 'بنڑاؤ_نیٹ_ورک_48d29d6d', 'font_info': 'فانٹ_معلومات', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
