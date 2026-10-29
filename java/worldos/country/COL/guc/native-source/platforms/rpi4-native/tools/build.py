#!/usr/bin/env python3
"""기존 wopu_a_ttaaleemüin 호환 ekeroliaa_o_uchikanain. 실제 구현: ../도구/akompiraajaa_a_yatawaajiraaya.py"""
import importlib as 가져오기
import sys as a_yatawajiraaya_a_laülaasü_ajutuu
from pathlib import Path as wopu_a_ttaaleemüin
a_yatawajiraaya_a_laülaasü_ajutuu.path.insert(0, str(wopu_a_ttaaleemüin(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('akompiraajaa_a_yatawaajiraaya', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('akompiraajaa_a_yatawaajiraaya')
    대응 = {'network': 'kusu', 'BUILD': 'akompiraajaa_wopu_a_ttaaleemüin', 'ar': 'anaajawaa_a_yataaya', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ashajiaakua_ipa_atijaaya', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ajutuu_matüriisü', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': '메소드', 'main': '시작', 'objcopy': '목적파일변환기', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': 'anaajaalaa_ekeroliaa', 'extra': '추가영역', 'exports': 'ee_irataa_eemüin_taapüla', 'jobs': '빌드작업', 'run': '실행', 'path': 'wopu_a_ttaaleemüin', 'REPO': '저장소', 'tool': '도구', 'classes': 'akotchijuushi_wopu_a_ttaaleemüin', 'output': '출력결과', 'samples': '예제들', 'symbol': '심볼', 'source': '원본자료', 'name': '이름', 'build_network': '통신망만들기', 'font_info': '글꼴정보', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
