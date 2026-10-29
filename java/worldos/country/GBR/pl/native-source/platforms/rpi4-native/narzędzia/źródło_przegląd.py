#!/usr/bin/env python3
"""repozytorium_korzeń 전체의 własny 원문을 목록화한다. zewnętrzny_WARTOŚĆ/generować 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_korzeń = Path(__file__).resolve().parents[1]
repozytorium_korzeń = Project_korzeń.parents[1]

def Uruchom_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_zapis = []
    for Katalog_WARTOŚĆ, 하위들, 파일들 in os.walk(str(repozytorium_korzeń)):
        하위들[:] = sorted(Nazwa for Nazwa in 하위들 if Nazwa not in 제외)
        for Nazwa in sorted(파일들):
            ścieżka_2 = Path(Katalog_WARTOŚĆ)/Nazwa
            if ścieżka_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            dane = ścieżka_2.read_bytes()
            wpis_WARTOŚĆ = {'path': str(ścieżka_2.relative_to(repozytorium_korzeń)), 'sha256': hashlib.sha256(dane).hexdigest(),
                  'ascii_filename': all(ord(znak_WARTOŚĆ)<128 for znak_WARTOŚĆ in ścieżka_2.stem)}
            if ścieżka_2.suffix == '.py':
                남은선언 = []
                try:
                    for węzeł_WARTOŚĆ in ast.walk(ast.parse(dane.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(węzeł_WARTOŚĆ, (ast.FunctionDef, ast.ClassDef)): 낱말 = węzeł_WARTOŚĆ.name
                        elif isinstance(węzeł_WARTOŚĆ, ast.arg): 낱말 = węzeł_WARTOŚĆ.arg
                        elif isinstance(węzeł_WARTOŚĆ, ast.Name) and isinstance(węzeł_WARTOŚĆ.ctx, ast.Store): 낱말 = węzeł_WARTOŚĆ.id
                        if 낱말 and all(ord(znak_WARTOŚĆ)<128 for znak_WARTOŚĆ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': węzeł_WARTOŚĆ.lineno})
                    wpis_WARTOŚĆ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as błąd:
                    wpis_WARTOŚĆ['parse_error'] = str(błąd)
            LOG_zapis.append(wpis_WARTOŚĆ)
    WYNIK = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_zapis,
          'file_count': len(LOG_zapis), 'ascii_filename_count': sum(wpis_WARTOŚĆ['ascii_filename'] for wpis_WARTOŚĆ in LOG_zapis),
          'python_files_with_ascii_declarations': sum(bool(wpis_WARTOŚĆ.get('ascii_python_declarations')) for wpis_WARTOŚĆ in LOG_zapis),
          'all_repository_identifiers_korean': False,
          'note': '표준 Połącz 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    cel_WARTOŚĆ = Project_korzeń/'build/verification/naming'; cel_WARTOŚĆ.mkdir(parents=True, exist_ok=True)
    (cel_WARTOŚĆ/'source-review.json').write_text(json.dumps(WYNIK, ensure_ascii=False, indent=2)+'\n')
    print('plik_źródłowy', WYNIK['file_count'], '개; ASCII nazwa_pliku_SMS', WYNIK['ascii_filename_count'],
          '개; 영어 선언이 남은 Python nazwa_pliku', WYNIK['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Uruchom_2()
