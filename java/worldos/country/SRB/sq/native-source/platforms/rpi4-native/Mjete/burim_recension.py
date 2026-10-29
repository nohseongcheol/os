#!/usr/bin/env python3
"""depo_rrënjë 전체의 자체 원문을 목록화한다. 외부/gjeneroj 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_rrënjë = Path(__file__).resolve().parents[1]
depo_rrënjë = Project_rrënjë.parents[1]

def Ekzekuto():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for direktori_VALUE, 하위들, 파일들 in os.walk(str(depo_rrënjë)):
        하위들[:] = sorted(Emër for Emër in 하위들 if Emër not in 제외)
        for Emër in sorted(파일들):
            POZICIONI = Path(direktori_VALUE)/Emër
            if POZICIONI.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            të_dhëna = POZICIONI.read_bytes()
            futje_VALUE = {'path': str(POZICIONI.relative_to(depo_rrënjë)), 'sha256': hashlib.sha256(të_dhëna).hexdigest(),
                  'ascii_filename': all(ord(karakter_VALUE)<128 for karakter_VALUE in POZICIONI.stem)}
            if POZICIONI.suffix == '.py':
                남은선언 = []
                try:
                    for nyjë_VALUE in ast.walk(ast.parse(të_dhëna.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nyjë_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nyjë_VALUE.name
                        elif isinstance(nyjë_VALUE, ast.arg): 낱말 = nyjë_VALUE.arg
                        elif isinstance(nyjë_VALUE, ast.Name) and isinstance(nyjë_VALUE.ctx, ast.Store): 낱말 = nyjë_VALUE.id
                        if 낱말 and all(ord(karakter_VALUE)<128 for karakter_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nyjë_VALUE.lineno})
                    futje_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as GABIM:
                    futje_VALUE['parse_error'] = str(GABIM)
            LOG_RECORD.append(futje_VALUE)
    llogaritje = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(futje_VALUE['ascii_filename'] for futje_VALUE in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(futje_VALUE.get('ascii_python_declarations')) for futje_VALUE in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Lidhu 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    vendmbërritje_VALUE = Project_rrënjë/'build/verification/naming'; vendmbërritje_VALUE.mkdir(parents=True, exist_ok=True)
    (vendmbërritje_VALUE/'source-review.json').write_text(json.dumps(llogaritje, ensure_ascii=False, indent=2)+'\n')
    print('BURIMI', llogaritje['file_count'], '개; ASCII skedar_emër_SMS', llogaritje['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Kartelë', llogaritje['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Ekzekuto()
