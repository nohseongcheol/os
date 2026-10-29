#!/usr/bin/env python3
"""хранилище_корен 전체의 자체 원문을 목록화한다. външен_стойност/генерирам 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

проект_корен = Path(__file__).resolve().parents[1]
хранилище_корен = проект_корен.parents[1]

def Стартиране():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    регистрирам_запис = []
    for указател_стойност, 하위들, 파일들 in os.walk(str(хранилище_корен)):
        하위들[:] = sorted(Име for Име in 하위들 if Име not in 제외)
        for Име in sorted(파일들):
            ПЪТ = Path(указател_стойност)/Име
            if ПЪТ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            данни = ПЪТ.read_bytes()
            запис_стойност = {'path': str(ПЪТ.relative_to(хранилище_корен)), 'sha256': hashlib.sha256(данни).hexdigest(),
                  'ascii_filename': all(ord(знак_стойност)<128 for знак_стойност in ПЪТ.stem)}
            if ПЪТ.suffix == '.py':
                남은선언 = []
                try:
                    for възел_стойност in ast.walk(ast.parse(данни.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(възел_стойност, (ast.FunctionDef, ast.ClassDef)): 낱말 = възел_стойност.name
                        elif isinstance(възел_стойност, ast.arg): 낱말 = възел_стойност.arg
                        elif isinstance(възел_стойност, ast.Name) and isinstance(възел_стойност.ctx, ast.Store): 낱말 = възел_стойност.id
                        if 낱말 and all(ord(знак_стойност)<128 for знак_стойност in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': възел_стойност.lineno})
                    запис_стойност['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ГРЕШКА:
                    запис_стойност['parse_error'] = str(ГРЕШКА)
            регистрирам_запис.append(запис_стойност)
    РЕЗУЛТАТ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': регистрирам_запис,
          'file_count': len(регистрирам_запис), 'ascii_filename_count': sum(запис_стойност['ascii_filename'] for запис_стойност in регистрирам_запис),
          'python_files_with_ascii_declarations': sum(bool(запис_стойност.get('ascii_python_declarations')) for запис_стойност in регистрирам_запис),
          'all_repository_identifiers_korean': False,
          'note': '표준 Свързване 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    местоназначение_стойност = проект_корен/'build/verification/naming'; местоназначение_стойност.mkdir(parents=True, exist_ok=True)
    (местоназначение_стойност/'source-review.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2)+'\n')
    print('ИЗТОЧНИК', РЕЗУЛТАТ['file_count'], '개; ASCII име_на_файл_Текст', РЕЗУЛТАТ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Файл', РЕЗУЛТАТ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Стартиране()
