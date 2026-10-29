#!/usr/bin/env python3
"""depozit_rădăcină 전체의 propriu 원문을 목록화한다. extern_VALUE/genera 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_rădăcină = Path(__file__).resolve().parents[1]
depozit_rădăcină = Project_rădăcină.parents[1]

def Pornește():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for Director_VALUE, 하위들, 파일들 in os.walk(str(depozit_rădăcină)):
        하위들[:] = sorted(Nume for Nume in 하위들 if Nume not in 제외)
        for Nume in sorted(파일들):
            Cale = Path(Director_VALUE)/Nume
            if Cale.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            date = Cale.read_bytes()
            intrare_VALUE = {'path': str(Cale.relative_to(depozit_rădăcină)), 'sha256': hashlib.sha256(date).hexdigest(),
                  'ascii_filename': all(ord(caracter_VALUE)<128 for caracter_VALUE in Cale.stem)}
            if Cale.suffix == '.py':
                남은선언 = []
                try:
                    for nod_VALUE in ast.walk(ast.parse(date.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nod_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nod_VALUE.name
                        elif isinstance(nod_VALUE, ast.arg): 낱말 = nod_VALUE.arg
                        elif isinstance(nod_VALUE, ast.Name) and isinstance(nod_VALUE.ctx, ast.Store): 낱말 = nod_VALUE.id
                        if 낱말 and all(ord(caracter_VALUE)<128 for caracter_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nod_VALUE.lineno})
                    intrare_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as eroare:
                    intrare_VALUE['parse_error'] = str(eroare)
            LOG_RECORD.append(intrare_VALUE)
    KR = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(intrare_VALUE['ascii_filename'] for intrare_VALUE in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(intrare_VALUE.get('ascii_python_declarations')) for intrare_VALUE in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Conectează 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destinație_VALUE = Project_rădăcină/'build/verification/naming'; destinație_VALUE.mkdir(parents=True, exist_ok=True)
    (destinație_VALUE/'source-review.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2)+'\n')
    print('SURSĂ', KR['file_count'], '개; ASCII nume_de_fișier_SMS', KR['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fișier', KR['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Pornește()
