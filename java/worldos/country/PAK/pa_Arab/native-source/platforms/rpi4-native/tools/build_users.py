#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/بلڈ_صارف_جگہ.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('بلڈ_صارف_جگہ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('بلڈ_صارف_جگہ')
    대응 = {'mode': 'طریقہ_موڈ', 'header': 'سرتحریر_قدر', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'محفوظہ_ٹول', 'posix': '포직스경로', 'payload': 'پے_لوڈ_کوائف', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'کوائف', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'متن', 'headers': 'سرتحریر_فرست', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'بلڈ', 'build_users': 'بنڑاؤ_صارف_جگہ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ایپ_سرتحریر_آف_سیٹ', 'offset': 'آف_سیٹ_قدر', 'text_address': 'حکم_پتا', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'نفاذ_کرو_حکم', 'path': 'راہ', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'سیٹنگاں_قدر', 'index': '색인', 'classes': 'درجہ_راہ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'کوائف_پتا', 'symbol': 'علامت_قدر', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ناں', 'value': 'قدر', 'fmt': 'وضع_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
