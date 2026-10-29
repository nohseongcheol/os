#!/usr/bin/env python3
"""αποθετήριο_ρίζα 전체의 ίδιο 원문을 목록화한다. εξωτερικός_τιμή/δημιουργώ 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

έργο_ρίζα = Path(__file__).resolve().parents[1]
αποθετήριο_ρίζα = έργο_ρίζα.parents[1]

def Εκτέλεση_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    καταγράφω_ρεκόρ = []
    for Κατάλογος_τιμή, 하위들, 파일들 in os.walk(str(αποθετήριο_ρίζα)):
        하위들[:] = sorted(Όνομα for Όνομα in 하위들 if Όνομα not in 제외)
        for Όνομα in sorted(파일들):
            ΔΙΑΔΡΟΜΗ = Path(Κατάλογος_τιμή)/Όνομα
            if ΔΙΑΔΡΟΜΗ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            δεδομένα = ΔΙΑΔΡΟΜΗ.read_bytes()
            καταχώρηση_τιμή = {'path': str(ΔΙΑΔΡΟΜΗ.relative_to(αποθετήριο_ρίζα)), 'sha256': hashlib.sha256(δεδομένα).hexdigest(),
                  'ascii_filename': all(ord(χαρακτήρας_τιμή)<128 for χαρακτήρας_τιμή in ΔΙΑΔΡΟΜΗ.stem)}
            if ΔΙΑΔΡΟΜΗ.suffix == '.py':
                남은선언 = []
                try:
                    for κόμβος_τιμή in ast.walk(ast.parse(δεδομένα.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(κόμβος_τιμή, (ast.FunctionDef, ast.ClassDef)): 낱말 = κόμβος_τιμή.name
                        elif isinstance(κόμβος_τιμή, ast.arg): 낱말 = κόμβος_τιμή.arg
                        elif isinstance(κόμβος_τιμή, ast.Name) and isinstance(κόμβος_τιμή.ctx, ast.Store): 낱말 = κόμβος_τιμή.id
                        if 낱말 and all(ord(χαρακτήρας_τιμή)<128 for χαρακτήρας_τιμή in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': κόμβος_τιμή.lineno})
                    καταχώρηση_τιμή['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ΣΦΑΛΜΑ:
                    καταχώρηση_τιμή['parse_error'] = str(ΣΦΑΛΜΑ)
            καταγράφω_ρεκόρ.append(καταχώρηση_τιμή)
    μέτρηση = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': καταγράφω_ρεκόρ,
          'file_count': len(καταγράφω_ρεκόρ), 'ascii_filename_count': sum(καταχώρηση_τιμή['ascii_filename'] for καταχώρηση_τιμή in καταγράφω_ρεκόρ),
          'python_files_with_ascii_declarations': sum(bool(καταχώρηση_τιμή.get('ascii_python_declarations')) for καταχώρηση_τιμή in καταγράφω_ρεκόρ),
          'all_repository_identifiers_korean': False,
          'note': '표준 Σύνδεση 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    προορισμός_τιμή = έργο_ρίζα/'build/verification/naming'; προορισμός_τιμή.mkdir(parents=True, exist_ok=True)
    (προορισμός_τιμή/'source-review.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2)+'\n')
    print('ΠΗΓΗ', μέτρηση['file_count'], '개; ASCII όνομα_αρχείου_μήνυμα', μέτρηση['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Αρχείο', μέτρηση['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Εκτέλεση_2()
