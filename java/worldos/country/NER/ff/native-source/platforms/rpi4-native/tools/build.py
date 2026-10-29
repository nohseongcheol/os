#!/usr/bin/env python3
"""기존 laawol 호환 naatnugol_toɓɓere. laatii_keɓe 구현: ../도구/tafde_yuɓɓo.py"""
import importlib as 가져오기
import sys as yuɓɓo_kurdinɗo_njaru
from pathlib import Path as laawol
yuɓɓo_kurdinɗo_njaru.path.insert(0, str(laawol(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('tafde_yuɓɓo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tafde_yuɓɓo')
    대응 = {'network': 'laylaytol', 'BUILD': 'tafde_laawol', 'ar': 'ƴeewtirde_kuutorgal', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fontere_keɓe', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': '인수배열', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': 'huutoraade', 'objcopy': '목적파일변환기', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': 'fiilde_naatnugol', 'extra': '추가영역', 'exports': 'eksportude_taabal', 'jobs': '빌드작업', 'run': '실행', 'path': 'laawol', 'REPO': '저장소', 'tool': '도구', 'classes': 'fedde_laawol', 'output': '출력결과', 'samples': '예제들', 'symbol': '심볼', 'source': '원본자료', 'name': 'innde', 'build_network': '통신망만들기', 'font_info': 'fontere_kumpital', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
