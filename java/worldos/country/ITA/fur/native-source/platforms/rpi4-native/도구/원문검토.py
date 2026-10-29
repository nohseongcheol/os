#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Eseguis():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    기록 = []
    for 폴더, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Nom for Nom in 하위들 if Nom not in 제외)
        for Nom in sorted(파일들):
            Percors = Path(폴더)/Nom
            if Percors.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            자료 = Percors.read_bytes()
            항목 = {'path': str(Percors.relative_to(저장소)), 'sha256': hashlib.sha256(자료).hexdigest(),
                  'ascii_filename': all(ord(글자)<128 for 글자 in Percors.stem)}
            if Percors.suffix == '.py':
                남은선언 = []
                try:
                    for 마디 in ast.walk(ast.parse(자료.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(마디, (ast.FunctionDef, ast.ClassDef)): 낱말 = 마디.name
                        elif isinstance(마디, ast.arg): 낱말 = 마디.arg
                        elif isinstance(마디, ast.Name) and isinstance(마디.ctx, ast.Store): 낱말 = 마디.id
                        if 낱말 and all(ord(글자)<128 for 글자 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': 마디.lineno})
                    항목['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Erôr:
                    항목['parse_error'] = str(Erôr)
            기록.append(항목)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': 기록,
          'file_count': len(기록), 'ascii_filename_count': sum(항목['ascii_filename'] for 항목 in 기록),
          'python_files_with_ascii_declarations': sum(bool(항목.get('ascii_python_declarations')) for 항목 in 기록),
          'all_repository_identifiers_korean': False,
          'note': '표준 Conetiti 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    목적 = 기준/'build/verification/naming'; 목적.mkdir(parents=True, exist_ok=True)
    (목적/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('원문', 결과['file_count'], '개; ASCII 파일명', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python 파일', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Eseguis()
