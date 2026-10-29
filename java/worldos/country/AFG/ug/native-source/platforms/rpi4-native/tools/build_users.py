#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/نۇسخا_ئىشلەتكۈچى_بوشلۇق.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('نۇسخا_ئىشلەتكۈچى_بوشلۇق', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('نۇسخا_ئىشلەتكۈچى_بوشلۇق')
    대응 = {'mode': 'ئۇسۇل_ھالەت', 'header': 'بېشى_قىممىتى', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ئارخىپ_قورال', 'posix': '포직스경로', 'payload': 'يۈك_مەلۇمات', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'مەلۇمات', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'تېكىست', 'headers': 'بېشى_تىزىم', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'نۇسخا', 'build_users': 'قۇرۇش_ئىشلەتكۈچى_بوشلۇق', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ئەپ_بېشى_ئاغما', 'offset': 'ئاغما_قىممىتى', 'text_address': 'بۇيرۇق_ئادرېس', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'path': 'يول', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'changed': '바뀐자료', 'n': '개수', 'flag': 'تەڭشەك_قىممىتى', 'index': 'ئىزدەش_ئىندېكس', 'classes': 'تۈركۈم_يول', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'مەلۇمات_ئادرېس', 'symbol': 'بەلگە_قىممىتى', 'root': 'يىلتىز_ئادرېس', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ئاتى', 'value': 'قىممىتى', 'fmt': 'فورمات_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
