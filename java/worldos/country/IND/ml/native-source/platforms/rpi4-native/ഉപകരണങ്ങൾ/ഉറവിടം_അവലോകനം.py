#!/usr/bin/env python3
"""കലവറ_വർഗ്ഗമൂലം 전체의 자체 원문을 목록화한다. 외부/സൃഷ്_ടിക്കുക 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]
കലവറ_വർഗ്ഗമൂലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]

def നടപ്പിലാക്കുക():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ലോഗ്_രേഖ = []
    for ഡയറക്ടറി_മൂല്യം, 하위들, 파일들 in os.walk(str(കലവറ_വർഗ്ഗമൂലം)):
        하위들[:] = sorted(പേരു് for പേരു് in 하위들 if പേരു് not in 제외)
        for പേരു് in sorted(파일들):
            വഴി = Path(ഡയറക്ടറി_മൂല്യം)/പേരു്
            if വഴി.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ഡാറ്റാ = വഴി.read_bytes()
            എന്_ട്രി_മൂല്യം = {'path': str(വഴി.relative_to(കലവറ_വർഗ്ഗമൂലം)), 'sha256': hashlib.sha256(ഡാറ്റാ).hexdigest(),
                  'ascii_filename': all(ord(പ്രതീകം_മൂല്യം)<128 for പ്രതീകം_മൂല്യം in വഴി.stem)}
            if വഴി.suffix == '.py':
                남은선언 = []
                try:
                    for നോഡ്_മൂല്യം in ast.walk(ast.parse(ഡാറ്റാ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(നോഡ്_മൂല്യം, (ast.FunctionDef, ast.ClassDef)): 낱말 = നോഡ്_മൂല്യം.name
                        elif isinstance(നോഡ്_മൂല്യം, ast.arg): 낱말 = നോഡ്_മൂല്യം.arg
                        elif isinstance(നോഡ്_മൂല്യം, ast.Name) and isinstance(നോഡ്_മൂല്യം.ctx, ast.Store): 낱말 = നോഡ്_മൂല്യം.id
                        if 낱말 and all(ord(പ്രതീകം_മൂല്യം)<128 for പ്രതീകം_മൂല്യം in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': നോഡ്_മൂല്യം.lineno})
                    എന്_ട്രി_മൂല്യം['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as പിശക്:
                    എന്_ട്രി_മൂല്യം['parse_error'] = str(പിശക്)
            ലോഗ്_രേഖ.append(എന്_ട്രി_മൂല്യം)
    അളവ് = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ലോഗ്_രേഖ,
          'file_count': len(ലോഗ്_രേഖ), 'ascii_filename_count': sum(എന്_ട്രി_മൂല്യം['ascii_filename'] for എന്_ട്രി_മൂല്യം in ലോഗ്_രേഖ),
          'python_files_with_ascii_declarations': sum(bool(എന്_ട്രി_മൂല്യം.get('ascii_python_declarations')) for എന്_ട്രി_മൂല്യം in ലോഗ്_രേഖ),
          'all_repository_identifiers_korean': False,
          'note': '표준 കണക്ടു്_ചെയ്യുക 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/naming'; ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.mkdir(parents=True, exist_ok=True)
    (ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'source-review.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2)+'\n')
    print('ഉറവിടം', അളവ്['file_count'], '개; ASCII ഫയല്_നാ_മം_ലിഖിതം', അളവ്['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ഫയല്', അളവ്['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': നടപ്പിലാക്കുക()
