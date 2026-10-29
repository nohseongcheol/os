#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/بلڈ_نظام.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('بلڈ_نظام', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_نظام')
    대응 = {'network': 'نیٹ_ورک', 'BUILD': 'بلڈ_راہ', 'ar': 'محفوظ_ٹول', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'فانٹ_کوائف', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'دلائل_لڑی', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'طریقہ_اندراج', 'main': 'چلائیں', 'objcopy': 'آبجیکٹ_فائل_تبدیل_کار', 'ROOT': 'عکس_ڈالنا_روٹ', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'بنائیں_صارف_اسپیس', 'f': 'فائل_اندراج', 'extra': '추가영역', 'exports': 'برآمد_کریں_جدول', 'jobs': '빌드작업', 'run': 'نفاذ_کریں_حکم', 'path': 'راستہ_2', 'REPO': '저장소', 'tool': 'ٹولز', 'classes': 'صنف_راہ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'علامت_قدر', 'source': '원본자료', 'name': 'نام', 'build_network': 'بنائیں_نیٹ_ورک_48d29d6d', 'font_info': 'فانٹ_معلومات', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
