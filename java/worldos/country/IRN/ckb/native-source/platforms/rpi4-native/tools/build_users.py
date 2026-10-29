#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/دروستکراو_بەکارهێنەر_مەودا.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('دروستکراو_بەکارهێنەر_مەودا', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('دروستکراو_بەکارهێنەر_مەودا')
    대응 = {'mode': 'ڕێگا_دۆخ', 'header': 'سەرپەڕ_نرخ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ئەرشیف_ئامراز', 'posix': '포직스경로', 'payload': 'بارگەى_كرێ_دەیتا', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'دەیتا', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'دەق', 'headers': 'سەرپەڕ_لیست', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'دروستکراو', 'build_users': 'دروستکردن_بەکارهێنەر_مەودا', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'بەرنامە_سەرپەڕ_ئۆفسێت', 'offset': 'ئۆفسێت_نرخ', 'text_address': 'فەرمان_ناونیشان', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'جێبەجێکردن_فەرمان', 'path': 'گوزەر', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ڕێكبەندەكان_نرخ', 'index': '색인', 'classes': 'کلاس_گوزەر', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'دەیتا_ناونیشان', 'symbol': 'سیمبۆل_نرخ', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ناو', 'value': 'نرخ', 'fmt': 'بیچم_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
