#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/گڏ_ڪريو_صارف_جڳهه.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('گڏ_ڪريو_صارف_جڳهه', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('گڏ_ڪريو_صارف_جڳهه')
    대응 = {'mode': 'طريقو_موڊ', 'header': 'هيڊر_قدر', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'محفوظ_ٽول', 'posix': '포직스경로', 'payload': 'بنيادي_بار_ڪوائف', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ڪوائف', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'متن', 'headers': 'هيڊر_فهرست', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'گڏ_ڪريو', 'build_users': 'ٺاھيو_صارف_جڳهه', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ائپ_هيڊر_آف_سيٽ', 'offset': 'آف_سيٽ_قدر', 'text_address': 'حڪم_پتو', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'تعميل_ڪرڻ_حڪم', 'path': 'راههه', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'سيٽنگون_قدر', 'index': '색인', 'classes': 'درجو_راههه', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ڪوائف_پتو', 'symbol': 'نشاني_قدر', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'نالو', 'value': 'قدر', 'fmt': 'وضع_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
