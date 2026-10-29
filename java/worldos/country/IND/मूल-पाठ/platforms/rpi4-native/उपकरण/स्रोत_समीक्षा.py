#!/usr/bin/env python3
"""संग्रह_मूल 전체의 निज 원문을 목록화한다. बाहरी_मान/जनरेट_करें 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]
संग्रह_मूल = प्रोजेक्ट_करें_मूल.parents[1]

def चलाएँ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    लॉग_रिकॉर्ड = []
    for डायरेक्टरी_मान, 하위들, 파일들 in os.walk(str(संग्रह_मूल)):
        하위들[:] = sorted(नाम for नाम in 하위들 if नाम not in 제외)
        for नाम in sorted(파일들):
            पथ = Path(डायरेक्टरी_मान)/नाम
            if पथ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            आँकड़े = पथ.read_bytes()
            एन्ट्री_मान = {'path': str(पथ.relative_to(संग्रह_मूल)), 'sha256': hashlib.sha256(आँकड़े).hexdigest(),
                  'ascii_filename': all(ord(कैरेक्टर_मान)<128 for कैरेक्टर_मान in पथ.stem)}
            if पथ.suffix == '.py':
                남은선언 = []
                try:
                    for नोड_मान in ast.walk(ast.parse(आँकड़े.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(नोड_मान, (ast.FunctionDef, ast.ClassDef)): 낱말 = नोड_मान.name
                        elif isinstance(नोड_मान, ast.arg): 낱말 = नोड_मान.arg
                        elif isinstance(नोड_मान, ast.Name) and isinstance(नोड_मान.ctx, ast.Store): 낱말 = नोड_मान.id
                        if 낱말 and all(ord(कैरेक्टर_मान)<128 for कैरेक्टर_मान in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': नोड_मान.lineno})
                    एन्ट्री_मान['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as त्रुटि:
                    एन्ट्री_मान['parse_error'] = str(त्रुटि)
            लॉग_रिकॉर्ड.append(एन्ट्री_मान)
    परिणाम = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': लॉग_रिकॉर्ड,
          'file_count': len(लॉग_रिकॉर्ड), 'ascii_filename_count': sum(एन्ट्री_मान['ascii_filename'] for एन्ट्री_मान in लॉग_रिकॉर्ड),
          'python_files_with_ascii_declarations': sum(bool(एन्ट्री_मान.get('ascii_python_declarations')) for एन्ट्री_मान in लॉग_रिकॉर्ड),
          'all_repository_identifiers_korean': False,
          'note': '표준 जोड़ना 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    गंतव्य_मान = प्रोजेक्ट_करें_मूल/'build/verification/naming'; गंतव्य_मान.mkdir(parents=True, exist_ok=True)
    (गंतव्य_मान/'source-review.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2)+'\n')
    print('स्रोत', परिणाम['file_count'], '개; ASCII फ़ाइल_नाम_पाठ', परिणाम['ascii_filename_count'],
          '개; 영어 선언이 남은 Python संचिका', परिणाम['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': चलाएँ()
