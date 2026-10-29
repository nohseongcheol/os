#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਬਿਲਡ_ਉਪਭੋਗਤਾ_ਥਾਂ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਬਿਲਡ_ਉਪਭੋਗਤਾ_ਥਾਂ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਬਿਲਡ_ਉਪਭੋਗਤਾ_ਥਾਂ')
    대응 = {'mode': 'ਮੈਥਡ_ਮੋਡ', 'header': 'ਸਿਰਲੇਖ_ਕੀਮਤ', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ਸੰਗ੍ਰਹਿ_ਸਾਧਨ', 'posix': '포직스경로', 'payload': 'ਪੇਲੋਡ_ਸਮੱਗਰੀ', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ਸਮੱਗਰੀ', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'ਟੈਕਸਟ', 'headers': 'ਸਿਰਲੇਖ_ਸੂਚੀ', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ਬਿਲਡ', 'build_users': 'ਬਣਾਓ_ਉਪਭੋਗਤਾ_ਥਾਂ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ਐਪਲੀਕੇਸ਼_ਸਿਰਲੇਖ_ਔਫਸੈਟ', 'offset': 'ਔਫਸੈਟ_ਕੀਮਤ', 'text_address': 'ਆਦੇਸ਼_ਪਤਾ', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'path': 'ਮਾਰਗ', 'p': 'ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ਸੈਟਿੰਗਾਂ_ਕੀਮਤ', 'index': 'ਲੱਭਣਾ_ਅਨੁਕ੍ਰਮਣਿਕਾ', 'classes': 'ਸ੍ਰੇਣੀ_ਰਸਤਾ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ਸਮੱਗਰੀ_ਪਤਾ', 'symbol': 'ਪ੍ਰਤੀਕ_ਕੀਮਤ', 'root': 'ਰੂਟ_ਪਤਾ', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'ਨਾਂ', 'value': 'ਕੀਮਤ', 'fmt': 'ਸਰੂਪ_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
