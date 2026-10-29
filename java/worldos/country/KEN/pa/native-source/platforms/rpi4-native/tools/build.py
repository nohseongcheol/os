#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/ਬਿਲਡ_ਪਰਬੰਧ.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('ਬਿਲਡ_ਪਰਬੰਧ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ਬਿਲਡ_ਪਰਬੰਧ')
    대응 = {'network': 'ਨੈਟਵਰਕ', 'BUILD': 'ਬਿਲਡ_ਰਸਤਾ', 'ar': 'ਸੰਗ੍ਰਹਿ_ਸਾਧਨ', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ਫੌਂਟ_ਸਮੱਗਰੀ', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'ਮੈਥਡ_ਦਾਖਲਾ', 'main': 'ਚਲਾਓ_2', 'objcopy': 'ਔਬਜੈਕਟ_ਲਿਖਤ_ਪੱਤਰ_ਬਦਲਣਾ', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ਬਣਾਓ_ਉਪਭੋਗਤਾ_ਥਾਂ', 'f': 'ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ', 'extra': '추가영역', 'exports': 'ਨਿਰਯਾਤ_ਤਾਲਿਕਾ', 'jobs': '빌드작업', 'run': 'ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', 'path': 'ਮਾਰਗ', 'REPO': '저장소', 'tool': 'ਸਾਧਨ', 'classes': 'ਸ੍ਰੇਣੀ_ਰਸਤਾ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ਪ੍ਰਤੀਕ_ਕੀਮਤ', 'source': '원본자료', 'name': 'ਨਾਂ', 'build_network': 'ਬਣਾਓ_ਨੈਟਵਰਕ', 'font_info': 'ਫੌਂਟ_ਜਾਣਕਾਰੀ', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
