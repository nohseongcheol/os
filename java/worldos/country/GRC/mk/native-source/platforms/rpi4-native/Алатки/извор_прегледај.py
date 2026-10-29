#!/usr/bin/env python3
"""склад_корен 전체의 자체 원문을 목록화한다. 외부/генерира 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_корен = Path(__file__).resolve().parents[1]
склад_корен = Project_корен.parents[1]

def Изврши_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_ред = []
    for Именик_VALUE, 하위들, 파일들 in os.walk(str(склад_корен)):
        하위들[:] = sorted(Име for Име in 하위들 if Име not in 제외)
        for Име in sorted(파일들):
            ПАТЕКА = Path(Именик_VALUE)/Име
            if ПАТЕКА.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            податоци = ПАТЕКА.read_bytes()
            внес_VALUE = {'path': str(ПАТЕКА.relative_to(склад_корен)), 'sha256': hashlib.sha256(податоци).hexdigest(),
                  'ascii_filename': all(ord(знак_VALUE)<128 for знак_VALUE in ПАТЕКА.stem)}
            if ПАТЕКА.suffix == '.py':
                남은선언 = []
                try:
                    for јазол_VALUE in ast.walk(ast.parse(податоци.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(јазол_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = јазол_VALUE.name
                        elif isinstance(јазол_VALUE, ast.arg): 낱말 = јазол_VALUE.arg
                        elif isinstance(јазол_VALUE, ast.Name) and isinstance(јазол_VALUE.ctx, ast.Store): 낱말 = јазол_VALUE.id
                        if 낱말 and all(ord(знак_VALUE)<128 for знак_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': јазол_VALUE.lineno})
                    внес_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ГРЕШКА:
                    внес_VALUE['parse_error'] = str(ГРЕШКА)
            LOG_ред.append(внес_VALUE)
    мерка = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_ред,
          'file_count': len(LOG_ред), 'ascii_filename_count': sum(внес_VALUE['ascii_filename'] for внес_VALUE in LOG_ред),
          'python_files_with_ascii_declarations': sum(bool(внес_VALUE.get('ascii_python_declarations')) for внес_VALUE in LOG_ред),
          'all_repository_identifiers_korean': False,
          'note': '표준 Врзи_се 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    одредиште_VALUE = Project_корен/'build/verification/naming'; одредиште_VALUE.mkdir(parents=True, exist_ok=True)
    (одредиште_VALUE/'source-review.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2)+'\n')
    print('ИЗВОР', мерка['file_count'], '개; ASCII датотека_име_СМС', мерка['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Датотека', мерка['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Изврши_2()
