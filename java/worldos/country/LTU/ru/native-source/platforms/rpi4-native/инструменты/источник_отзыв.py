#!/usr/bin/env python3
"""корень_репозитория 전체의 свой 원문을 목록화한다. внешний_ЗНАЧЕН/генерировать 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

задача_корень = Path(__file__).resolve().parents[1]
корень_репозитория = задача_корень.parents[1]

def запустить():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_ЗАПИСЬ = []
    for Каталог_ЗНАЧЕН, 하위들, 파일들 in os.walk(str(корень_репозитория)):
        하위들[:] = sorted(Название for Название in 하위들 if Название not in 제외)
        for Название in sorted(파일들):
            путь = Path(Каталог_ЗНАЧЕН)/Название
            if путь.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            данные = путь.read_bytes()
            ввод_ЗНАЧЕН = {'path': str(путь.relative_to(корень_репозитория)), 'sha256': hashlib.sha256(данные).hexdigest(),
                  'ascii_filename': all(ord(знак_ЗНАЧЕН)<128 for знак_ЗНАЧЕН in путь.stem)}
            if путь.suffix == '.py':
                남은선언 = []
                try:
                    for узел_ЗНАЧЕН in ast.walk(ast.parse(данные.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(узел_ЗНАЧЕН, (ast.FunctionDef, ast.ClassDef)): 낱말 = узел_ЗНАЧЕН.name
                        elif isinstance(узел_ЗНАЧЕН, ast.arg): 낱말 = узел_ЗНАЧЕН.arg
                        elif isinstance(узел_ЗНАЧЕН, ast.Name) and isinstance(узел_ЗНАЧЕН.ctx, ast.Store): 낱말 = узел_ЗНАЧЕН.id
                        if 낱말 and all(ord(знак_ЗНАЧЕН)<128 for знак_ЗНАЧЕН in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': узел_ЗНАЧЕН.lineno})
                    ввод_ЗНАЧЕН['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ошибка:
                    ввод_ЗНАЧЕН['parse_error'] = str(ошибка)
            LOG_ЗАПИСЬ.append(ввод_ЗНАЧЕН)
    результат = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_ЗАПИСЬ,
          'file_count': len(LOG_ЗАПИСЬ), 'ascii_filename_count': sum(ввод_ЗНАЧЕН['ascii_filename'] for ввод_ЗНАЧЕН in LOG_ЗАПИСЬ),
          'python_files_with_ascii_declarations': sum(bool(ввод_ЗНАЧЕН.get('ascii_python_declarations')) for ввод_ЗНАЧЕН in LOG_ЗАПИСЬ),
          'all_repository_identifiers_korean': False,
          'note': '표준 Подключить 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    цель_ЗНАЧЕН = задача_корень/'build/verification/naming'; цель_ЗНАЧЕН.mkdir(parents=True, exist_ok=True)
    (цель_ЗНАЧЕН/'source-review.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2)+'\n')
    print('исходныйКод', результат['file_count'], '개; ASCII имя_файла_SMS', результат['ascii_filename_count'],
          '개; 영어 선언이 남은 Python файл', результат['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': запустить()
