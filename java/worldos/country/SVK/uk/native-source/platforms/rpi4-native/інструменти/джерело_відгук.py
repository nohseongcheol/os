#!/usr/bin/env python3
"""репозиторій_корінь 전체의 своє 원문을 목록화한다. зовнішній_значення/генерувати 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Дії_корінь = Path(__file__).resolve().parents[1]
репозиторій_корінь = Дії_корінь.parents[1]

def запустити():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    журнал_запис = []
    for Каталог_значення, 하위들, 파일들 in os.walk(str(репозиторій_корінь)):
        하위들[:] = sorted(Назва for Назва in 하위들 if Назва not in 제외)
        for Назва in sorted(파일들):
            шлях = Path(Каталог_значення)/Назва
            if шлях.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            дані = шлях.read_bytes()
            запис_значення_962f286b = {'path': str(шлях.relative_to(репозиторій_корінь)), 'sha256': hashlib.sha256(дані).hexdigest(),
                  'ascii_filename': all(ord(символ_значення_068c2631)<128 for символ_значення_068c2631 in шлях.stem)}
            if шлях.suffix == '.py':
                남은선언 = []
                try:
                    for вузол_значення in ast.walk(ast.parse(дані.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(вузол_значення, (ast.FunctionDef, ast.ClassDef)): 낱말 = вузол_значення.name
                        elif isinstance(вузол_значення, ast.arg): 낱말 = вузол_значення.arg
                        elif isinstance(вузол_значення, ast.Name) and isinstance(вузол_значення.ctx, ast.Store): 낱말 = вузол_значення.id
                        if 낱말 and all(ord(символ_значення_068c2631)<128 for символ_значення_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': вузол_значення.lineno})
                    запис_значення_962f286b['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ПОМИЛКА:
                    запис_значення_962f286b['parse_error'] = str(ПОМИЛКА)
            журнал_запис.append(запис_значення_962f286b)
    результат = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': журнал_запис,
          'file_count': len(журнал_запис), 'ascii_filename_count': sum(запис_значення_962f286b['ascii_filename'] for запис_значення_962f286b in журнал_запис),
          'python_files_with_ascii_declarations': sum(bool(запис_значення_962f286b.get('ascii_python_declarations')) for запис_значення_962f286b in журнал_запис),
          'all_repository_identifiers_korean': False,
          'note': '표준 З_єднання 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    місце_значення = Дії_корінь/'build/verification/naming'; місце_значення.mkdir(parents=True, exist_ok=True)
    (місце_значення/'source-review.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2)+'\n')
    print('вихіднийКод', результат['file_count'], '개; ASCII ім_я_файлу_Текст', результат['ascii_filename_count'],
          '개; 영어 선언이 남은 Python файл', результат['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': запустити()
