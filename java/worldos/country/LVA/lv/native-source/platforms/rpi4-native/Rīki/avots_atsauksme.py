#!/usr/bin/env python3
"""repozitorijs_sakne 전체의 savs 원문을 목록화한다. ārējs_VALUE/ģenerēt 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_sakne = Path(__file__).resolve().parents[1]
repozitorijs_sakne = Project_sakne.parents[1]

def Palaist():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for Direktorijs_VALUE, 하위들, 파일들 in os.walk(str(repozitorijs_sakne)):
        하위들[:] = sorted(Nosaukums for Nosaukums in 하위들 if Nosaukums not in 제외)
        for Nosaukums in sorted(파일들):
            CEĻŠ = Path(Direktorijs_VALUE)/Nosaukums
            if CEĻŠ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            dati = CEĻŠ.read_bytes()
            ievade_VALUE = {'path': str(CEĻŠ.relative_to(repozitorijs_sakne)), 'sha256': hashlib.sha256(dati).hexdigest(),
                  'ascii_filename': all(ord(rakstzīme_VALUE)<128 for rakstzīme_VALUE in CEĻŠ.stem)}
            if CEĻŠ.suffix == '.py':
                남은선언 = []
                try:
                    for mezgls_VALUE in ast.walk(ast.parse(dati.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(mezgls_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = mezgls_VALUE.name
                        elif isinstance(mezgls_VALUE, ast.arg): 낱말 = mezgls_VALUE.arg
                        elif isinstance(mezgls_VALUE, ast.Name) and isinstance(mezgls_VALUE.ctx, ast.Store): 낱말 = mezgls_VALUE.id
                        if 낱말 and all(ord(rakstzīme_VALUE)<128 for rakstzīme_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': mezgls_VALUE.lineno})
                    ievade_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Kļūda:
                    ievade_VALUE['parse_error'] = str(Kļūda)
            LOG_RECORD.append(ievade_VALUE)
    mērs = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(ievade_VALUE['ascii_filename'] for ievade_VALUE in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(ievade_VALUE.get('ascii_python_declarations')) for ievade_VALUE in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Savienoties 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    mērķis_VALUE = Project_sakne/'build/verification/naming'; mērķis_VALUE.mkdir(parents=True, exist_ok=True)
    (mērķis_VALUE/'source-review.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2)+'\n')
    print('AVOTS', mērs['file_count'], '개; ASCII faila_nosaukums_SMS', mērs['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fails', mērs['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Palaist()
