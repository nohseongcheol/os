#!/usr/bin/env python3
"""repository_root 전체의 자체 원문을 목록화한다. 외부/mag_generate 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_root = Path(__file__).resolve().parents[1]
repository_root = Project_root.parents[1]

def run():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_hanay = []
    for Directory_VALUE, 하위들, 파일들 in os.walk(str(repository_root)):
        하위들[:] = sorted(pangalan for pangalan in 하위들 if pangalan not in 제외)
        for pangalan in sorted(파일들):
            path = Path(Directory_VALUE)/pangalan
            if path.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = path.read_bytes()
            pagpasok_VALUE = {'path': str(path.relative_to(repository_root)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(karakter_VALUE)<128 for karakter_VALUE in path.stem)}
            if path.suffix == '.py':
                남은선언 = []
                try:
                    for node_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VALUE.name
                        elif isinstance(node_VALUE, ast.arg): 낱말 = node_VALUE.arg
                        elif isinstance(node_VALUE, ast.Name) and isinstance(node_VALUE.ctx, ast.Store): 낱말 = node_VALUE.id
                        if 낱말 and all(ord(karakter_VALUE)<128 for karakter_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VALUE.lineno})
                    pagpasok_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as error:
                    pagpasok_VALUE['parse_error'] = str(error)
            LOG_hanay.append(pagpasok_VALUE)
    sukat = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_hanay,
          'file_count': len(LOG_hanay), 'ascii_filename_count': sum(pagpasok_VALUE['ascii_filename'] for pagpasok_VALUE in LOG_hanay),
          'python_files_with_ascii_declarations': sum(bool(pagpasok_VALUE.get('ascii_python_declarations')) for pagpasok_VALUE in LOG_hanay),
          'all_repository_identifiers_korean': False,
          'note': '표준 CONNECT 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    patutunguhan_VALUE = Project_root/'build/verification/naming'; patutunguhan_VALUE.mkdir(parents=True, exist_ok=True)
    (patutunguhan_VALUE/'source-review.json').write_text(json.dumps(sukat, ensure_ascii=False, indent=2)+'\n')
    print('pinagmulan', sukat['file_count'], '개; ASCII file_pangalan_SMS', sukat['ascii_filename_count'],
          '개; 영어 선언이 남은 Python file', sukat['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': run()
