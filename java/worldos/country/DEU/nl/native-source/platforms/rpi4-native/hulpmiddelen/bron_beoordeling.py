#!/usr/bin/env python3
"""opslagplaats_wortel 전체의 Eigen 원문을 목록화한다. extern_WAARDE/genereren 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Taken_wortel = Path(__file__).resolve().parents[1]
opslagplaats_wortel = Taken_wortel.parents[1]

def starten():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for map_WAARDE, 하위들, 파일들 in os.walk(str(opslagplaats_wortel)):
        하위들[:] = sorted(Naam for Naam in 하위들 if Naam not in 제외)
        for Naam in sorted(파일들):
            pad = Path(map_WAARDE)/Naam
            if pad.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            gegevens = pad.read_bytes()
            invoer_WAARDE_962f286b = {'path': str(pad.relative_to(opslagplaats_wortel)), 'sha256': hashlib.sha256(gegevens).hexdigest(),
                  'ascii_filename': all(ord(teken_WAARDE)<128 for teken_WAARDE in pad.stem)}
            if pad.suffix == '.py':
                남은선언 = []
                try:
                    for knooppunt_WAARDE in ast.walk(ast.parse(gegevens.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(knooppunt_WAARDE, (ast.FunctionDef, ast.ClassDef)): 낱말 = knooppunt_WAARDE.name
                        elif isinstance(knooppunt_WAARDE, ast.arg): 낱말 = knooppunt_WAARDE.arg
                        elif isinstance(knooppunt_WAARDE, ast.Name) and isinstance(knooppunt_WAARDE.ctx, ast.Store): 낱말 = knooppunt_WAARDE.id
                        if 낱말 and all(ord(teken_WAARDE)<128 for teken_WAARDE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': knooppunt_WAARDE.lineno})
                    invoer_WAARDE_962f286b['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as fout:
                    invoer_WAARDE_962f286b['parse_error'] = str(fout)
            LOG_RECORD.append(invoer_WAARDE_962f286b)
    resultaat = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(invoer_WAARDE_962f286b['ascii_filename'] for invoer_WAARDE_962f286b in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(invoer_WAARDE_962f286b.get('ascii_python_declarations')) for invoer_WAARDE_962f286b in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Verbinden 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    doel_WAARDE = Taken_wortel/'build/verification/naming'; doel_WAARDE.mkdir(parents=True, exist_ok=True)
    (doel_WAARDE/'source-review.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2)+'\n')
    print('broncode', resultaat['file_count'], '개; ASCII bestandsnaam_sms', resultaat['ascii_filename_count'],
          '개; 영어 선언이 남은 Python bestand', resultaat['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': starten()
