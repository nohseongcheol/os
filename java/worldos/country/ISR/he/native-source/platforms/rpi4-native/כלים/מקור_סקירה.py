#!/usr/bin/env python3
"""מאגר_בסיס 전체의 עצמי 원문을 목록화한다. חיצוני_ערך/יצר 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

לשקף_בסיס = Path(__file__).resolve().parents[1]
מאגר_בסיס = לשקף_בסיס.parents[1]

def הפעלה():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    לרשום_שיא = []
    for מדריך_ערך, 하위들, 파일들 in os.walk(str(מאגר_בסיס)):
        하위들[:] = sorted(שם for שם in 하위들 if שם not in 제외)
        for שם in sorted(파일들):
            נתיב = Path(מדריך_ערך)/שם
            if נתיב.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            נתונים = נתיב.read_bytes()
            ערך_ערך = {'path': str(נתיב.relative_to(מאגר_בסיס)), 'sha256': hashlib.sha256(נתונים).hexdigest(),
                  'ascii_filename': all(ord(תו_ערך)<128 for תו_ערך in נתיב.stem)}
            if נתיב.suffix == '.py':
                남은선언 = []
                try:
                    for צומת_ערך in ast.walk(ast.parse(נתונים.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(צומת_ערך, (ast.FunctionDef, ast.ClassDef)): 낱말 = צומת_ערך.name
                        elif isinstance(צומת_ערך, ast.arg): 낱말 = צומת_ערך.arg
                        elif isinstance(צומת_ערך, ast.Name) and isinstance(צומת_ערך.ctx, ast.Store): 낱말 = צומת_ערך.id
                        if 낱말 and all(ord(תו_ערך)<128 for תו_ערך in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': צומת_ערך.lineno})
                    ערך_ערך['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as שגיאה:
                    ערך_ערך['parse_error'] = str(שגיאה)
            לרשום_שיא.append(ערך_ערך)
    תוצאה = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': לרשום_שיא,
          'file_count': len(לרשום_שיא), 'ascii_filename_count': sum(ערך_ערך['ascii_filename'] for ערך_ערך in לרשום_שיא),
          'python_files_with_ascii_declarations': sum(bool(ערך_ערך.get('ascii_python_declarations')) for ערך_ערך in לרשום_שיא),
          'all_repository_identifiers_korean': False,
          'note': '표준 חיבור 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    יעד_ערך = לשקף_בסיס/'build/verification/naming'; יעד_ערך.mkdir(parents=True, exist_ok=True)
    (יעד_ערך/'source-review.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2)+'\n')
    print('קודמקור', תוצאה['file_count'], '개; ASCII שם_קובץ_טקסט', תוצאה['ascii_filename_count'],
          '개; 영어 선언이 남은 Python קובץ', תוצאה['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': הפעלה()
