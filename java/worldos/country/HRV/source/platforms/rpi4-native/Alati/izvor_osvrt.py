#!/usr/bin/env python3
"""spremište_korijen 전체의 vlastiti 원문을 목록화한다. vanjski_VALUE/generirati 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

akcija_korijen = Path(__file__).resolve().parents[1]
spremište_korijen = akcija_korijen.parents[1]

def Pokreni():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_zapis = []
    for imenik_VALUE, 하위들, 파일들 in os.walk(str(spremište_korijen)):
        하위들[:] = sorted(Ime for Ime in 하위들 if Ime not in 제외)
        for Ime in sorted(파일들):
            PUTANJA = Path(imenik_VALUE)/Ime
            if PUTANJA.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            podaci = PUTANJA.read_bytes()
            unos_VALUE = {'path': str(PUTANJA.relative_to(spremište_korijen)), 'sha256': hashlib.sha256(podaci).hexdigest(),
                  'ascii_filename': all(ord(znak_VALUE)<128 for znak_VALUE in PUTANJA.stem)}
            if PUTANJA.suffix == '.py':
                남은선언 = []
                try:
                    for čvor_VALUE in ast.walk(ast.parse(podaci.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(čvor_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = čvor_VALUE.name
                        elif isinstance(čvor_VALUE, ast.arg): 낱말 = čvor_VALUE.arg
                        elif isinstance(čvor_VALUE, ast.Name) and isinstance(čvor_VALUE.ctx, ast.Store): 낱말 = čvor_VALUE.id
                        if 낱말 and all(ord(znak_VALUE)<128 for znak_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': čvor_VALUE.lineno})
                    unos_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as GREŠKA:
                    unos_VALUE['parse_error'] = str(GREŠKA)
            LOG_zapis.append(unos_VALUE)
    REZULTAT = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_zapis,
          'file_count': len(LOG_zapis), 'ascii_filename_count': sum(unos_VALUE['ascii_filename'] for unos_VALUE in LOG_zapis),
          'python_files_with_ascii_declarations': sum(bool(unos_VALUE.get('ascii_python_declarations')) for unos_VALUE in LOG_zapis),
          'all_repository_identifiers_korean': False,
          'note': '표준 Spoji_se 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    odredište_VALUE = akcija_korijen/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'source-review.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2)+'\n')
    print('IZVOR', REZULTAT['file_count'], '개; ASCII naziv_datoteke_SMS', REZULTAT['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Datoteka', REZULTAT['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Pokreni()
