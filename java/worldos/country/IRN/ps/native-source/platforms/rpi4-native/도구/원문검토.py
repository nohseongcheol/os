#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ځغلول():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    خبرال_کیل = []
    for نوملړ_ارزښت, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(نوم for نوم in 하위들 if نوم not in 제외)
        for نوم in sorted(파일들):
            يونلور = Path(نوملړ_ارزښت)/نوم
            if يونلور.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            اومتوک = يونلور.read_bytes()
            ننوت_ارزښت = {'path': str(يونلور.relative_to(저장소)), 'sha256': hashlib.sha256(اومتوک).hexdigest(),
                  'ascii_filename': all(ord(لوښه_ارزښت)<128 for لوښه_ارزښت in يونلور.stem)}
            if يونلور.suffix == '.py':
                남은선언 = []
                try:
                    for غوټه_ارزښت in ast.walk(ast.parse(اومتوک.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(غوټه_ارزښت, (ast.FunctionDef, ast.ClassDef)): 낱말 = غوټه_ارزښت.name
                        elif isinstance(غوټه_ارزښت, ast.arg): 낱말 = غوټه_ارزښت.arg
                        elif isinstance(غوټه_ارزښت, ast.Name) and isinstance(غوټه_ارزښت.ctx, ast.Store): 낱말 = غوټه_ارزښت.id
                        if 낱말 and all(ord(لوښه_ارزښت)<128 for لوښه_ارزښت in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': غوټه_ارزښت.lineno})
                    ننوت_ارزښت['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as تېروتنه:
                    ننوت_ارزښت['parse_error'] = str(تېروتنه)
            خبرال_کیل.append(ننوت_ارزښت)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': خبرال_کیل,
          'file_count': len(خبرال_کیل), 'ascii_filename_count': sum(ننوت_ارزښت['ascii_filename'] for ننوت_ارزښت in خبرال_کیل),
          'python_files_with_ascii_declarations': sum(bool(ننوت_ارزښت.get('ascii_python_declarations')) for ننوت_ارزښت in خبرال_کیل),
          'all_repository_identifiers_korean': False,
          'note': '표준 نښلېدل 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    موخه_ارزښت = 기준/'build/verification/naming'; موخه_ارزښت.mkdir(parents=True, exist_ok=True)
    (موخه_ارزښت/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('سرچينه', 결과['file_count'], '개; ASCII 파일명', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python دوتنه', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ځغلول()
