#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/დაგენერირება 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]
저장소 = პროეცირება_ფესვი.parents[1]

def გაშვება():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ჟურნალი_ჩაწერა = []
    for საქაღალდე_მნიშვნელობა, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(სახელი for სახელი in 하위들 if სახელი not in 제외)
        for სახელი in sorted(파일들):
            გეზი = Path(საქაღალდე_მნიშვნელობა)/სახელი
            if გეზი.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            მონაცემები = გეზი.read_bytes()
            შენატანი_მნიშვნელობა = {'path': str(გეზი.relative_to(저장소)), 'sha256': hashlib.sha256(მონაცემები).hexdigest(),
                  'ascii_filename': all(ord(სიმბოლო_მნიშვნელობა_068c2631)<128 for სიმბოლო_მნიშვნელობა_068c2631 in გეზი.stem)}
            if გეზი.suffix == '.py':
                남은선언 = []
                try:
                    for კვანძი_მნიშვნელობა in ast.walk(ast.parse(მონაცემები.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(კვანძი_მნიშვნელობა, (ast.FunctionDef, ast.ClassDef)): 낱말 = კვანძი_მნიშვნელობა.name
                        elif isinstance(კვანძი_მნიშვნელობა, ast.arg): 낱말 = კვანძი_მნიშვნელობა.arg
                        elif isinstance(კვანძი_მნიშვნელობა, ast.Name) and isinstance(კვანძი_მნიშვნელობა.ctx, ast.Store): 낱말 = კვანძი_მნიშვნელობა.id
                        if 낱말 and all(ord(სიმბოლო_მნიშვნელობა_068c2631)<128 for სიმბოლო_მნიშვნელობა_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': კვანძი_მნიშვნელობა.lineno})
                    შენატანი_მნიშვნელობა['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as შეცდომა:
                    შენატანი_მნიშვნელობა['parse_error'] = str(შეცდომა)
            ჟურნალი_ჩაწერა.append(შენატანი_მნიშვნელობა)
    გაზომვა = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ჟურნალი_ჩაწერა,
          'file_count': len(ჟურნალი_ჩაწერა), 'ascii_filename_count': sum(შენატანი_მნიშვნელობა['ascii_filename'] for შენატანი_მნიშვნელობა in ჟურნალი_ჩაწერა),
          'python_files_with_ascii_declarations': sum(bool(შენატანი_მნიშვნელობა.get('ascii_python_declarations')) for შენატანი_მნიშვნელობა in ჟურნალი_ჩაწერა),
          'all_repository_identifiers_korean': False,
          'note': '표준 დაკავშირება 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    მიმართულება_მნიშვნელობა = პროეცირება_ფესვი/'build/verification/naming'; მიმართულება_მნიშვნელობა.mkdir(parents=True, exist_ok=True)
    (მიმართულება_მნიშვნელობა/'source-review.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2)+'\n')
    print('წყარო', გაზომვა['file_count'], '개; ASCII ფაილი_სახელი_ტექსტი', გაზომვა['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ფაილი', გაზომვა['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': გაშვება()
