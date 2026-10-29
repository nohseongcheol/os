#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/بلڈ_صارف_اسپیس.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('بلڈ_صارف_اسپیس', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_صارف_اسپیس')
    대응 = {'mode': 'طریقہ_موڈ', 'header': 'سرصفحہ_قدر', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'محفوظ_ٹول', 'posix': '포직스경로', 'payload': 'پے_لوڈ_کوائف', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'کوائف', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'متن', 'headers': 'سرصفحہ_فہرست', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'بلڈ', 'build_users': 'بنائیں_صارف_اسپیس', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ایپ_سرصفحہ_آفسٹ', 'offset': 'آفسٹ_قدر', 'text_address': 'حکم_پتہ', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'نفاذ_کریں_حکم', 'path': 'راستہ_2', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'changed': '바뀐자료', 'n': '개수', 'flag': 'سیٹنگز_قدر', 'index': 'لُک_اپ_اشاریہ', 'classes': 'صنف_راہ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'کوائف_پتہ', 'symbol': 'علامت_قدر', 'root': 'روٹ_پتہ', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'نام', 'value': 'قدر', 'fmt': 'وضع_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
