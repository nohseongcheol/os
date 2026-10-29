#!/usr/bin/env python3
"""مخزن_جذر 전체의 بومی 원문을 목록화한다. 외부/ایجاد 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
مخزن_جذر = نمایش_دادن_جذر.parents[1]

def اجرا_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    واقعه_نگار_ردیف = []
    for فهرست_مقدار_e5561a2b, 하위들, 파일들 in os.walk(str(مخزن_جذر)):
        하위들[:] = sorted(نام for نام in 하위들 if نام not in 제외)
        for نام in sorted(파일들):
            مسیر = Path(فهرست_مقدار_e5561a2b)/نام
            if مسیر.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            داده_ها = مسیر.read_bytes()
            ورودی_مقدار = {'path': str(مسیر.relative_to(مخزن_جذر)), 'sha256': hashlib.sha256(داده_ها).hexdigest(),
                  'ascii_filename': all(ord(نویسه_مقدار)<128 for نویسه_مقدار in مسیر.stem)}
            if مسیر.suffix == '.py':
                남은선언 = []
                try:
                    for گره_مقدار in ast.walk(ast.parse(داده_ها.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(گره_مقدار, (ast.FunctionDef, ast.ClassDef)): 낱말 = گره_مقدار.name
                        elif isinstance(گره_مقدار, ast.arg): 낱말 = گره_مقدار.arg
                        elif isinstance(گره_مقدار, ast.Name) and isinstance(گره_مقدار.ctx, ast.Store): 낱말 = گره_مقدار.id
                        if 낱말 and all(ord(نویسه_مقدار)<128 for نویسه_مقدار in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': گره_مقدار.lineno})
                    ورودی_مقدار['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as خطا:
                    ورودی_مقدار['parse_error'] = str(خطا)
            واقعه_نگار_ردیف.append(ورودی_مقدار)
    سنجش = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': واقعه_نگار_ردیف,
          'file_count': len(واقعه_نگار_ردیف), 'ascii_filename_count': sum(ورودی_مقدار['ascii_filename'] for ورودی_مقدار in واقعه_نگار_ردیف),
          'python_files_with_ascii_declarations': sum(bool(ورودی_مقدار.get('ascii_python_declarations')) for ورودی_مقدار in واقعه_نگار_ردیف),
          'all_repository_identifiers_korean': False,
          'note': '표준 اتصال 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    مقصد_مقدار = نمایش_دادن_جذر/'build/verification/naming'; مقصد_مقدار.mkdir(parents=True, exist_ok=True)
    (مقصد_مقدار/'source-review.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2)+'\n')
    print('مبداء', سنجش['file_count'], '개; ASCII فایل_نام_متن', سنجش['ascii_filename_count'],
          '개; 영어 선언이 남은 Python پرونده', سنجش['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': اجرا_2()
