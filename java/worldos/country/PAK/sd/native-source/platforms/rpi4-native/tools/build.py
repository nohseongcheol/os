#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/گڏ_ڪريو_سسٽم.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('گڏ_ڪريو_سسٽم', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('گڏ_ڪريو_سسٽم')
    대응 = {'network': 'نيٽ_ورڪ', 'BUILD': 'گڏ_ڪريو_راههه', 'ar': 'محفوظ_ٽول', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'فانٽ_ڪوائف', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'دليل_ترتيب', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'طريقو_داخلا', 'main': 'هلائڻ', 'objcopy': 'عنصر_فائل_تبديل_ڪندڙ', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ٺاھيو_صارف_جڳهه', 'f': 'فائل_داخلا', 'extra': '추가영역', 'exports': 'برآمد_جدول', 'jobs': '빌드작업', 'run': 'تعميل_ڪرڻ_حڪم', 'path': 'راههه', 'REPO': '저장소', 'tool': 'اوزار', 'classes': 'درجو_راههه', 'output': '출력결과', 'samples': '예제들', 'symbol': 'نشاني_قدر', 'source': '원본자료', 'name': 'نالو', 'build_network': 'ٺاھيو_نيٽ_ورڪ_48d29d6d', 'font_info': 'فانٽ_معلومات', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
