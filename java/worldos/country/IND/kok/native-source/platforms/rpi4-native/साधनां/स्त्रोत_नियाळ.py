#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/तयार_करचें 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
저장소 = प्रॉजॅक्ट_रूट.parents[1]

def चलोवप():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_नोंद = []
    for नामावळ_मोल, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(नांव for नांव in 하위들 if नांव not in 제외)
        for नांव in sorted(파일들):
            पाथ = Path(नामावळ_मोल)/नांव
            if पाथ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            डेटा = पाथ.read_bytes()
            प्रवेश_मोल = {'path': str(पाथ.relative_to(저장소)), 'sha256': hashlib.sha256(डेटा).hexdigest(),
                  'ascii_filename': all(ord(वर्ण_मोल)<128 for वर्ण_मोल in पाथ.stem)}
            if पाथ.suffix == '.py':
                남은선언 = []
                try:
                    for नोड_मोल in ast.walk(ast.parse(डेटा.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(नोड_मोल, (ast.FunctionDef, ast.ClassDef)): 낱말 = नोड_मोल.name
                        elif isinstance(नोड_मोल, ast.arg): 낱말 = नोड_मोल.arg
                        elif isinstance(नोड_मोल, ast.Name) and isinstance(नोड_मोल.ctx, ast.Store): 낱말 = नोड_मोल.id
                        if 낱말 and all(ord(वर्ण_मोल)<128 for वर्ण_मोल in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': नोड_मोल.lineno})
                    प्रवेश_मोल['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as चूक:
                    प्रवेश_मोल['parse_error'] = str(चूक)
            LOG_नोंद.append(प्रवेश_मोल)
    मेजप = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_नोंद,
          'file_count': len(LOG_नोंद), 'ascii_filename_count': sum(प्रवेश_मोल['ascii_filename'] for प्रवेश_मोल in LOG_नोंद),
          'python_files_with_ascii_declarations': sum(bool(प्रवेश_मोल.get('ascii_python_declarations')) for प्रवेश_मोल in LOG_नोंद),
          'all_repository_identifiers_korean': False,
          'note': '표준 कनॅक्ट 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    नियुक्त_स्थान_मोल = प्रॉजॅक्ट_रूट/'build/verification/naming'; नियुक्त_स्थान_मोल.mkdir(parents=True, exist_ok=True)
    (नियुक्त_स्थान_मोल/'source-review.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2)+'\n')
    print('स्त्रोत', मेजप['file_count'], '개; ASCII फायल_नांव_SMS', मेजप['ascii_filename_count'],
          '개; 영어 선언이 남은 Python फायल', मेजप['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': चलोवप()
