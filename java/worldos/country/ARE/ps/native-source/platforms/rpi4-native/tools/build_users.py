#!/usr/bin/env python3
"""기존 يونلور 호환 ننوت_ټکى. 실제 구현: ../도구/جوړول_کارن_تشې_پټۍ.py"""
import importlib as 가져오기
import sys as چليز_غونډال_ارزښت
from pathlib import Path as يونلور
چليز_غونډال_ارزښت.path.insert(0, str(يونلور(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('جوړول_کارن_تشې_پټۍ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('جوړول_کارن_تشې_پټۍ')
    대응 = {'mode': '방식', 'header': 'سرۍ_ارزښت', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ارشیف_توکى', 'posix': '포직스경로', 'payload': '내용자료', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'اومتوک', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ليکنه', 'headers': '머리목록', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'جوړول', 'build_users': '사용자영역만들기', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': '프로그램머리변위', 'offset': '변위', 'text_address': 'بولۍ_پته', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': '실행', 'path': 'يونلور', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': '설정값', 'index': '색인', 'classes': 'پاړکى_يونلور', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'اومتوک_پته', 'symbol': '심볼', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'نوم', 'value': 'ارزښت', 'fmt': 'بڼه_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
