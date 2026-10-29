#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Выканаць():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    журнал_запіс = []
    for каталог_значэнне, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Назва for Назва in 하위들 if Назва not in 제외)
        for Назва in sorted(파일들):
            ШЛЯХ = Path(каталог_значэнне)/Назва
            if ШЛЯХ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            дадзеныя = ШЛЯХ.read_bytes()
            увядзенне_значэнне = {'path': str(ШЛЯХ.relative_to(저장소)), 'sha256': hashlib.sha256(дадзеныя).hexdigest(),
                  'ascii_filename': all(ord(сімвал_значэнне_068c2631)<128 for сімвал_значэнне_068c2631 in ШЛЯХ.stem)}
            if ШЛЯХ.suffix == '.py':
                남은선언 = []
                try:
                    for вузел_значэнне in ast.walk(ast.parse(дадзеныя.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(вузел_значэнне, (ast.FunctionDef, ast.ClassDef)): 낱말 = вузел_значэнне.name
                        elif isinstance(вузел_значэнне, ast.arg): 낱말 = вузел_значэнне.arg
                        elif isinstance(вузел_значэнне, ast.Name) and isinstance(вузел_значэнне.ctx, ast.Store): 낱말 = вузел_значэнне.id
                        if 낱말 and all(ord(сімвал_значэнне_068c2631)<128 for сімвал_значэнне_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': вузел_значэнне.lineno})
                    увядзенне_значэнне['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ПАМЫЛКА:
                    увядзенне_значэнне['parse_error'] = str(ПАМЫЛКА)
            журнал_запіс.append(увядзенне_значэнне)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': журнал_запіс,
          'file_count': len(журнал_запіс), 'ascii_filename_count': sum(увядзенне_значэнне['ascii_filename'] for увядзенне_значэнне in журнал_запіс),
          'python_files_with_ascii_declarations': sum(bool(увядзенне_значэнне.get('ascii_python_declarations')) for увядзенне_значэнне in журнал_запіс),
          'all_repository_identifiers_korean': False,
          'note': '표준 Злучыцца 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    прызначэнне_значэнне_a0fbc067 = 기준/'build/verification/naming'; прызначэнне_значэнне_a0fbc067.mkdir(parents=True, exist_ok=True)
    (прызначэнне_значэнне_a0fbc067/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('КРЫНІЦА', 결과['file_count'], '개; ASCII файл_імя_Тэкст', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Файл', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Выканаць()
