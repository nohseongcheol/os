#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/булдыру 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]
저장소 = экранга_җибәрү_тамыр.parents[1]

def эшләтү():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_юл = []
    for каталог_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(исем for исем in 하위들 if исем not in 제외)
        for исем in sorted(파일들):
            Yul = Path(каталог_VALUE)/исем
            if Yul.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            мәгълүмат = Yul.read_bytes()
            кертү_VALUE = {'path': str(Yul.relative_to(저장소)), 'sha256': hashlib.sha256(мәгълүмат).hexdigest(),
                  'ascii_filename': all(ord(символ_VALUE_068c2631)<128 for символ_VALUE_068c2631 in Yul.stem)}
            if Yul.suffix == '.py':
                남은선언 = []
                try:
                    for төен_VALUE in ast.walk(ast.parse(мәгълүмат.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(төен_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = төен_VALUE.name
                        elif isinstance(төен_VALUE, ast.arg): 낱말 = төен_VALUE.arg
                        elif isinstance(төен_VALUE, ast.Name) and isinstance(төен_VALUE.ctx, ast.Store): 낱말 = төен_VALUE.id
                        if 낱말 and all(ord(символ_VALUE_068c2631)<128 for символ_VALUE_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': төен_VALUE.lineno})
                    кертү_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Хата:
                    кертү_VALUE['parse_error'] = str(Хата)
            LOG_юл.append(кертү_VALUE)
    үлчәм = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_юл,
          'file_count': len(LOG_юл), 'ascii_filename_count': sum(кертү_VALUE['ascii_filename'] for кертү_VALUE in LOG_юл),
          'python_files_with_ascii_declarations': sum(bool(кертү_VALUE.get('ascii_python_declarations')) for кертү_VALUE in LOG_юл),
          'all_repository_identifiers_korean': False,
          'note': '표준 ялгау 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    күчерү_урыны_VALUE = экранга_җибәрү_тамыр/'build/verification/naming'; күчерү_урыны_VALUE.mkdir(parents=True, exist_ok=True)
    (күчерү_урыны_VALUE/'source-review.json').write_text(json.dumps(үлчәм, ensure_ascii=False, indent=2)+'\n')
    print('чыганак', үлчәм['file_count'], '개; ASCII файл_исем_СМС', үлчәм['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Birem', үлчәм['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': эшләтү()
