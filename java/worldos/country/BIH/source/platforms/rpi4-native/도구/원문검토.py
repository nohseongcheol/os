#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def 시작():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    дневник_рада_ред = []
    for директориј_вриједност, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(назив for назив in 하위들 if назив not in 제외)
        for назив in sorted(파일들):
            пут = Path(директориј_вриједност)/назив
            if пут.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            подаци = пут.read_bytes()
            унос_вриједност = {'path': str(пут.relative_to(저장소)), 'sha256': hashlib.sha256(подаци).hexdigest(),
                  'ascii_filename': all(ord(знак_вриједност)<128 for знак_вриједност in пут.stem)}
            if пут.suffix == '.py':
                남은선언 = []
                try:
                    for чвор_вриједност in ast.walk(ast.parse(подаци.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(чвор_вриједност, (ast.FunctionDef, ast.ClassDef)): 낱말 = чвор_вриједност.name
                        elif isinstance(чвор_вриједност, ast.arg): 낱말 = чвор_вриједност.arg
                        elif isinstance(чвор_вриједност, ast.Name) and isinstance(чвор_вриједност.ctx, ast.Store): 낱말 = чвор_вриједност.id
                        if 낱말 and all(ord(знак_вриједност)<128 for знак_вриједност in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': чвор_вриједност.lineno})
                    унос_вриједност['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as грешка:
                    унос_вриједност['parse_error'] = str(грешка)
            дневник_рада_ред.append(унос_вриједност)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': дневник_рада_ред,
          'file_count': len(дневник_рада_ред), 'ascii_filename_count': sum(унос_вриједност['ascii_filename'] for унос_вриједност in дневник_рада_ред),
          'python_files_with_ascii_declarations': sum(bool(унос_вриједност.get('ascii_python_declarations')) for унос_вриједност in дневник_рада_ред),
          'all_repository_identifiers_korean': False,
          'note': '표준 повезати 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    одредиште_вриједност = 기준/'build/verification/naming'; одредиште_вриједност.mkdir(parents=True, exist_ok=True)
    (одредиште_вриједност/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('извор', 결과['file_count'], '개; ASCII фајл_назив_текст', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python фајл', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': 시작()
