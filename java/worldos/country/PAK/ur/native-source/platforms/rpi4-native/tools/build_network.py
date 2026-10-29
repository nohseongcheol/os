#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/بلڈ_نیٹ_ورک.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('بلڈ_نیٹ_ورک', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_نیٹ_ورک')
    대응 = {'obj': 'مقصود_فائل', 'objects': 'منزل_مقصود_فائلیں', 'library': 'لائبریری', 'output': '출력결과', 'port': 'دہانہ_نمبر', 'root': 'روٹ_پتہ', 'files': 'فائل_فہرست', 'source': '원본자료', 'run': 'نفاذ_کریں_حکم', 'flags': '설정비트', 'path': 'راستہ_2', 'build_network': 'بنائیں_نیٹ_ورک_48d29d6d', 'cc': '시언어번역기', 'ar': 'محفوظ_ٹول'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
