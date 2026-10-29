#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def چلاؤ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    لاگ_صف = []
    for ڈائریکٹری_قدر, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ناں for ناں in 하위들 if ناں not in 제외)
        for ناں in sorted(파일들):
            راہ = Path(ڈائریکٹری_قدر)/ناں
            if راہ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            کوائف = راہ.read_bytes()
            داخلہ_قدر = {'path': str(راہ.relative_to(저장소)), 'sha256': hashlib.sha256(کوائف).hexdigest(),
                  'ascii_filename': all(ord(کریکٹر_قدر)<128 for کریکٹر_قدر in راہ.stem)}
            if راہ.suffix == '.py':
                남은선언 = []
                try:
                    for نوڈ_قدر in ast.walk(ast.parse(کوائف.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(نوڈ_قدر, (ast.FunctionDef, ast.ClassDef)): 낱말 = نوڈ_قدر.name
                        elif isinstance(نوڈ_قدر, ast.arg): 낱말 = نوڈ_قدر.arg
                        elif isinstance(نوڈ_قدر, ast.Name) and isinstance(نوڈ_قدر.ctx, ast.Store): 낱말 = نوڈ_قدر.id
                        if 낱말 and all(ord(کریکٹر_قدر)<128 for کریکٹر_قدر in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': نوڈ_قدر.lineno})
                    داخلہ_قدر['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as نقص:
                    داخلہ_قدر['parse_error'] = str(نقص)
            لاگ_صف.append(داخلہ_قدر)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': لاگ_صف,
          'file_count': len(لاگ_صف), 'ascii_filename_count': sum(داخلہ_قدر['ascii_filename'] for داخلہ_قدر in لاگ_صف),
          'python_files_with_ascii_declarations': sum(bool(داخلہ_قدر.get('ascii_python_declarations')) for داخلہ_قدر in لاگ_صف),
          'all_repository_identifiers_korean': False,
          'note': '표준 جڑو 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    منزل_مقصود_قدر = 기준/'build/verification/naming'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    (منزل_مقصود_قدر/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ماخذ', 결과['file_count'], '개; ASCII فائل_ناں_متن', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python فائل', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': چلاؤ()
