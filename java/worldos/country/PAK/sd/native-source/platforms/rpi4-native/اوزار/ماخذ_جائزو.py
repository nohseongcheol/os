#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def هلائڻ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    لاگ_صف = []
    for ڊائريڪٽري_قدر, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(نالو for نالو in 하위들 if نالو not in 제외)
        for نالو in sorted(파일들):
            راههه = Path(ڊائريڪٽري_قدر)/نالو
            if راههه.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ڪوائف = راههه.read_bytes()
            داخلا_قدر = {'path': str(راههه.relative_to(저장소)), 'sha256': hashlib.sha256(ڪوائف).hexdigest(),
                  'ascii_filename': all(ord(ڪريڪٽر_قدر)<128 for ڪريڪٽر_قدر in راههه.stem)}
            if راههه.suffix == '.py':
                남은선언 = []
                try:
                    for نوڊ_قدر in ast.walk(ast.parse(ڪوائف.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(نوڊ_قدر, (ast.FunctionDef, ast.ClassDef)): 낱말 = نوڊ_قدر.name
                        elif isinstance(نوڊ_قدر, ast.arg): 낱말 = نوڊ_قدر.arg
                        elif isinstance(نوڊ_قدر, ast.Name) and isinstance(نوڊ_قدر.ctx, ast.Store): 낱말 = نوڊ_قدر.id
                        if 낱말 and all(ord(ڪريڪٽر_قدر)<128 for ڪريڪٽر_قدر in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': نوڊ_قدر.lineno})
                    داخلا_قدر['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as نقص:
                    داخلا_قدر['parse_error'] = str(نقص)
            لاگ_صف.append(داخلا_قدر)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': لاگ_صف,
          'file_count': len(لاگ_صف), 'ascii_filename_count': sum(داخلا_قدر['ascii_filename'] for داخلا_قدر in لاگ_صف),
          'python_files_with_ascii_declarations': sum(bool(داخلا_قدر.get('ascii_python_declarations')) for داخلا_قدر in لاگ_صف),
          'all_repository_identifiers_korean': False,
          'note': '표준 ڪنيڪٽ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    منزل_مقصود_قدر = 기준/'build/verification/naming'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    (منزل_مقصود_قدر/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ماخذ', 결과['file_count'], '개; ASCII فائل_نالو_متن', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python فائل', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': هلائڻ()
