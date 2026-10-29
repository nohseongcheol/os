#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ڕادان():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    تۆمار_ڕزن = []
    for ڕێبەرنامە_نرخ, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ناو for ناو in 하위들 if ناو not in 제외)
        for ناو in sorted(파일들):
            گوزەر = Path(ڕێبەرنامە_نرخ)/ناو
            if گوزەر.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            دەیتا = گوزەر.read_bytes()
            تێنووسین_نرخ = {'path': str(گوزەر.relative_to(저장소)), 'sha256': hashlib.sha256(دەیتا).hexdigest(),
                  'ascii_filename': all(ord(نووسە_نرخ)<128 for نووسە_نرخ in گوزەر.stem)}
            if گوزەر.suffix == '.py':
                남은선언 = []
                try:
                    for گرێ_نرخ in ast.walk(ast.parse(دەیتا.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(گرێ_نرخ, (ast.FunctionDef, ast.ClassDef)): 낱말 = گرێ_نرخ.name
                        elif isinstance(گرێ_نرخ, ast.arg): 낱말 = گرێ_نرخ.arg
                        elif isinstance(گرێ_نرخ, ast.Name) and isinstance(گرێ_نرخ.ctx, ast.Store): 낱말 = گرێ_نرخ.id
                        if 낱말 and all(ord(نووسە_نرخ)<128 for نووسە_نرخ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': گرێ_نرخ.lineno})
                    تێنووسین_نرخ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as هەڵە:
                    تێنووسین_نرخ['parse_error'] = str(هەڵە)
            تۆمار_ڕزن.append(تێنووسین_نرخ)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': تۆمار_ڕزن,
          'file_count': len(تۆمار_ڕزن), 'ascii_filename_count': sum(تێنووسین_نرخ['ascii_filename'] for تێنووسین_نرخ in تۆمار_ڕزن),
          'python_files_with_ascii_declarations': sum(bool(تێنووسین_نرخ.get('ascii_python_declarations')) for تێنووسین_نرخ in تۆمار_ڕزن),
          'all_repository_identifiers_korean': False,
          'note': '표준 لكاندن 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    جێمەبەست_نرخ = 기준/'build/verification/naming'; جێمەبەست_نرخ.mkdir(parents=True, exist_ok=True)
    (جێمەبەست_نرخ/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ژێدەر', 결과['file_count'], '개; ASCII فایل_ناو_دەق', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python فایل', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ڕادان()
