#!/usr/bin/env python3
"""రిపోజిటరీ_మూలం 전체의 자체 원문을 목록화한다. 외부/రూపొందించు 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
రిపోజిటరీ_మూలం = ప్రొజెక్ట్_మూలం.parents[1]

def నడుపుము():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    లాగ్_వరుస = []
    for సంచయని_మూల్యం, 하위들, 파일들 in os.walk(str(రిపోజిటరీ_మూలం)):
        하위들[:] = sorted(పేరు for పేరు in 하위들 if పేరు not in 제외)
        for పేరు in sorted(파일들):
            పాత్ = Path(సంచయని_మూల్యం)/పేరు
            if పాత్.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            డేటా = పాత్.read_bytes()
            ప్రవేశం_మూల్యం = {'path': str(పాత్.relative_to(రిపోజిటరీ_మూలం)), 'sha256': hashlib.sha256(డేటా).hexdigest(),
                  'ascii_filename': all(ord(అక్షరం_మూల్యం)<128 for అక్షరం_మూల్యం in పాత్.stem)}
            if పాత్.suffix == '.py':
                남은선언 = []
                try:
                    for నోడ్_మూల్యం in ast.walk(ast.parse(డేటా.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(నోడ్_మూల్యం, (ast.FunctionDef, ast.ClassDef)): 낱말 = నోడ్_మూల్యం.name
                        elif isinstance(నోడ్_మూల్యం, ast.arg): 낱말 = నోడ్_మూల్యం.arg
                        elif isinstance(నోడ్_మూల్యం, ast.Name) and isinstance(నోడ్_మూల్యం.ctx, ast.Store): 낱말 = నోడ్_మూల్యం.id
                        if 낱말 and all(ord(అక్షరం_మూల్యం)<128 for అక్షరం_మూల్యం in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': నోడ్_మూల్యం.lineno})
                    ప్రవేశం_మూల్యం['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as దోషం:
                    ప్రవేశం_మూల్యం['parse_error'] = str(దోషం)
            లాగ్_వరుస.append(ప్రవేశం_మూల్యం)
    ప్రమాణం = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': లాగ్_వరుస,
          'file_count': len(లాగ్_వరుస), 'ascii_filename_count': sum(ప్రవేశం_మూల్యం['ascii_filename'] for ప్రవేశం_మూల్యం in లాగ్_వరుస),
          'python_files_with_ascii_declarations': sum(bool(ప్రవేశం_మూల్యం.get('ascii_python_declarations')) for ప్రవేశం_మూల్యం in లాగ్_వరుస),
          'all_repository_identifiers_korean': False,
          'note': '표준 కనెక్టుచేయి 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    గమ్యం_మూల్యం = ప్రొజెక్ట్_మూలం/'build/verification/naming'; గమ్యం_మూల్యం.mkdir(parents=True, exist_ok=True)
    (గమ్యం_మూల్యం/'source-review.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2)+'\n')
    print('వనరు', ప్రమాణం['file_count'], '개; ASCII ఫైలు_పేరు_పాఠం', ప్రమాణం['ascii_filename_count'],
          '개; 영어 선언이 남은 Python దస్త్రం', ప్రమాణం['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': నడుపుము()
