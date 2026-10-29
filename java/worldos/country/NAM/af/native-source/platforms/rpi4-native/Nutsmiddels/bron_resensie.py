#!/usr/bin/env python3
"""bewaarplek_wortel 전체의 자체 원문을 목록화한다. 외부/genereer 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_wortel = Path(__file__).resolve().parents[1]
bewaarplek_wortel = Project_wortel.parents[1]

def Loop():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_ry = []
    for gids_VALUE, 하위들, 파일들 in os.walk(str(bewaarplek_wortel)):
        하위들[:] = sorted(Naam for Naam in 하위들 if Naam not in 제외)
        for Naam in sorted(파일들):
            Pad = Path(gids_VALUE)/Naam
            if Pad.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = Pad.read_bytes()
            inskrywing_VALUE = {'path': str(Pad.relative_to(bewaarplek_wortel)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(karakter_VALUE)<128 for karakter_VALUE in Pad.stem)}
            if Pad.suffix == '.py':
                남은선언 = []
                try:
                    for nodus_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nodus_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nodus_VALUE.name
                        elif isinstance(nodus_VALUE, ast.arg): 낱말 = nodus_VALUE.arg
                        elif isinstance(nodus_VALUE, ast.Name) and isinstance(nodus_VALUE.ctx, ast.Store): 낱말 = nodus_VALUE.id
                        if 낱말 and all(ord(karakter_VALUE)<128 for karakter_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nodus_VALUE.lineno})
                    inskrywing_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Fout:
                    inskrywing_VALUE['parse_error'] = str(Fout)
            LOG_ry.append(inskrywing_VALUE)
    maatreël = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_ry,
          'file_count': len(LOG_ry), 'ascii_filename_count': sum(inskrywing_VALUE['ascii_filename'] for inskrywing_VALUE in LOG_ry),
          'python_files_with_ascii_declarations': sum(bool(inskrywing_VALUE.get('ascii_python_declarations')) for inskrywing_VALUE in LOG_ry),
          'all_repository_identifiers_korean': False,
          'note': '표준 Koppel 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    bestemming_VALUE = Project_wortel/'build/verification/naming'; bestemming_VALUE.mkdir(parents=True, exist_ok=True)
    (bestemming_VALUE/'source-review.json').write_text(json.dumps(maatreël, ensure_ascii=False, indent=2)+'\n')
    print('Bron', maatreël['file_count'], '개; ASCII lêer_naam_SMS', maatreël['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Lêer', maatreël['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Loop()
