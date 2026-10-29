#!/usr/bin/env python3
"""depo_koren 전체의 자체 원문을 목록화한다. spoljni_VALUE/generisati 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

radnja_koren = Path(__file__).resolve().parents[1]
depo_koren = radnja_koren.parents[1]

def koristiti():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_snimi = []
    for Imenik_VALUE, 하위들, 파일들 in os.walk(str(depo_koren)):
        하위들[:] = sorted(ime for ime in 하위들 if ime not in 제외)
        for ime in sorted(파일들):
            putanja = Path(Imenik_VALUE)/ime
            if putanja.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            podaci = putanja.read_bytes()
            stavka_VALUE = {'path': str(putanja.relative_to(depo_koren)), 'sha256': hashlib.sha256(podaci).hexdigest(),
                  'ascii_filename': all(ord(znak_VALUE)<128 for znak_VALUE in putanja.stem)}
            if putanja.suffix == '.py':
                남은선언 = []
                try:
                    for čvor_VALUE in ast.walk(ast.parse(podaci.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(čvor_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = čvor_VALUE.name
                        elif isinstance(čvor_VALUE, ast.arg): 낱말 = čvor_VALUE.arg
                        elif isinstance(čvor_VALUE, ast.Name) and isinstance(čvor_VALUE.ctx, ast.Store): 낱말 = čvor_VALUE.id
                        if 낱말 and all(ord(znak_VALUE)<128 for znak_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': čvor_VALUE.lineno})
                    stavka_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as greška:
                    stavka_VALUE['parse_error'] = str(greška)
            LOG_snimi.append(stavka_VALUE)
    KR = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_snimi,
          'file_count': len(LOG_snimi), 'ascii_filename_count': sum(stavka_VALUE['ascii_filename'] for stavka_VALUE in LOG_snimi),
          'python_files_with_ascii_declarations': sum(bool(stavka_VALUE.get('ascii_python_declarations')) for stavka_VALUE in LOG_snimi),
          'all_repository_identifiers_korean': False,
          'note': '표준 veze 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    odredište_VALUE = radnja_koren/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'source-review.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2)+'\n')
    print('izvor', KR['file_count'], '개; ASCII ime_datoteke_SMS', KR['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Datoteka', KR['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': koristiti()
