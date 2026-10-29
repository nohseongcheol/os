#!/usr/bin/env python3
"""저장소 전체의 निज 원문을 목록화한다. 외부/सिर्जना_गर्नुहोस् 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

परियोजना_रूट = Path(__file__).resolve().parents[1]
저장소 = परियोजना_रूट.parents[1]

def चलाउनुहोस्():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    लग_रेकर्ड = []
    for डाइरेक्टरी_मान, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(नाम for नाम in 하위들 if नाम not in 제외)
        for नाम in sorted(파일들):
            मार्ग = Path(डाइरेक्टरी_मान)/नाम
            if मार्ग.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            लगत = मार्ग.read_bytes()
            प्रविष्टि_मान = {'path': str(मार्ग.relative_to(저장소)), 'sha256': hashlib.sha256(लगत).hexdigest(),
                  'ascii_filename': all(ord(वर्ण_मान)<128 for वर्ण_मान in मार्ग.stem)}
            if मार्ग.suffix == '.py':
                남은선언 = []
                try:
                    for नोड_मान in ast.walk(ast.parse(लगत.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(नोड_मान, (ast.FunctionDef, ast.ClassDef)): 낱말 = नोड_मान.name
                        elif isinstance(नोड_मान, ast.arg): 낱말 = नोड_मान.arg
                        elif isinstance(नोड_मान, ast.Name) and isinstance(नोड_मान.ctx, ast.Store): 낱말 = नोड_मान.id
                        if 낱말 and all(ord(वर्ण_मान)<128 for वर्ण_मान in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': नोड_मान.lineno})
                    प्रविष्टि_मान['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as त्रुटि:
                    प्रविष्टि_मान['parse_error'] = str(त्रुटि)
            लग_रेकर्ड.append(प्रविष्टि_मान)
    मापन = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': लग_रेकर्ड,
          'file_count': len(लग_रेकर्ड), 'ascii_filename_count': sum(प्रविष्टि_मान['ascii_filename'] for प्रविष्टि_मान in लग_रेकर्ड),
          'python_files_with_ascii_declarations': sum(bool(प्रविष्टि_मान.get('ascii_python_declarations')) for प्रविष्टि_मान in लग_रेकर्ड),
          'all_repository_identifiers_korean': False,
          'note': '표준 जडान 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    गन्तव्य_मान = परियोजना_रूट/'build/verification/naming'; गन्तव्य_मान.mkdir(parents=True, exist_ok=True)
    (गन्तव्य_मान/'source-review.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2)+'\n')
    print('स्रोत', मापन['file_count'], '개; ASCII फाइल_नाम_पाठ', मापन['ascii_filename_count'],
          '개; 영어 선언이 남은 Python फाइल', मापन['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': चलाउनुहोस्()
