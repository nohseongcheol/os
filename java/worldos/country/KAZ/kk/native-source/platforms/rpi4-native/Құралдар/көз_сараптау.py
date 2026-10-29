#!/usr/bin/env python3
"""репозиторий_түбір 전체의 자체 원문을 목록화한다. сыртқы_мән/жасау 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

жоба_түбір = Path(__file__).resolve().parents[1]
репозиторий_түбір = жоба_түбір.parents[1]

def Орындау_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    журнал_жол = []
    for каталог_мән, 하위들, 파일들 in os.walk(str(репозиторий_түбір)):
        하위들[:] = sorted(Аты for Аты in 하위들 if Аты not in 제외)
        for Аты in sorted(파일들):
            Жол_2 = Path(каталог_мән)/Аты
            if Жол_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            деректер = Жол_2.read_bytes()
            енгізу_мән = {'path': str(Жол_2.relative_to(репозиторий_түбір)), 'sha256': hashlib.sha256(деректер).hexdigest(),
                  'ascii_filename': all(ord(таңба_мән)<128 for таңба_мән in Жол_2.stem)}
            if Жол_2.suffix == '.py':
                남은선언 = []
                try:
                    for түйін_мән in ast.walk(ast.parse(деректер.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(түйін_мән, (ast.FunctionDef, ast.ClassDef)): 낱말 = түйін_мән.name
                        elif isinstance(түйін_мән, ast.arg): 낱말 = түйін_мән.arg
                        elif isinstance(түйін_мән, ast.Name) and isinstance(түйін_мән.ctx, ast.Store): 낱말 = түйін_мән.id
                        if 낱말 and all(ord(таңба_мән)<128 for таңба_мән in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': түйін_мән.lineno})
                    енгізу_мән['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Қате:
                    енгізу_мән['parse_error'] = str(Қате)
            журнал_жол.append(енгізу_мән)
    НӘТИЖЕ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': журнал_жол,
          'file_count': len(журнал_жол), 'ascii_filename_count': sum(енгізу_мән['ascii_filename'] for енгізу_мән in журнал_жол),
          'python_files_with_ascii_declarations': sum(bool(енгізу_мән.get('ascii_python_declarations')) for енгізу_мән in журнал_жол),
          'all_repository_identifiers_korean': False,
          'note': '표준 Байланысу 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    тағайындау_мән = жоба_түбір/'build/verification/naming'; тағайындау_мән.mkdir(parents=True, exist_ok=True)
    (тағайындау_мән/'source-review.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2)+'\n')
    print('Неден', НӘТИЖЕ['file_count'], '개; ASCII файл_атауы_Мәтін', НӘТИЖЕ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Файл', НӘТИЖЕ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Орындау_2()
