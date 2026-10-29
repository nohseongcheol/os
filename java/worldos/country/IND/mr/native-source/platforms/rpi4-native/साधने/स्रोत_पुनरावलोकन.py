#!/usr/bin/env python3
"""भांडार_मूळ 전체의 स्वकीय 원문을 목록화한다. बाह्य_मूल्य/तयार_करा 코드는 मोजणी_मूल्य 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]
भांडार_मूळ = प्रोजेक्ट_मूळ.parents[1]

def सुरू_करा():
    वगळा_मूल्य = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    लॉग_नोंद = []
    for निर्देशिका_मूल्य, अपत्ये_यादी, संचिका_नोंदी in os.walk(str(भांडार_मूळ)):
        अपत्ये_यादी[:] = sorted(नाव for नाव in अपत्ये_यादी if नाव not in वगळा_मूल्य)
        for नाव in sorted(संचिका_नोंदी):
            मार्ग = Path(निर्देशिका_मूल्य)/नाव
            if मार्ग.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            डेटा = मार्ग.read_bytes()
            प्रविष्टी_मूल्य = {'path': str(मार्ग.relative_to(भांडार_मूळ)), 'sha256': hashlib.sha256(डेटा).hexdigest(),
                  'ascii_filename': all(ord(वर्ण_मूल्य)<128 for वर्ण_मूल्य in मार्ग.stem)}
            if मार्ग.suffix == '.py':
                उर्वरित_घोषणा = []
                try:
                    for नोड_मूल्य in ast.walk(ast.parse(डेटा.decode('utf-8-sig'))):
                        शाब्दिक_शब्द = ''
                        if isinstance(नोड_मूल्य, (ast.FunctionDef, ast.ClassDef)): शाब्दिक_शब्द = नोड_मूल्य.name
                        elif isinstance(नोड_मूल्य, ast.arg): शाब्दिक_शब्द = नोड_मूल्य.arg
                        elif isinstance(नोड_मूल्य, ast.Name) and isinstance(नोड_मूल्य.ctx, ast.Store): शाब्दिक_शब्द = नोड_मूल्य.id
                        if शाब्दिक_शब्द and all(ord(वर्ण_मूल्य)<128 for वर्ण_मूल्य in शाब्दिक_शब्द) and शाब्दिक_शब्द != '_' and not शाब्दिक_शब्द.startswith('__'):
                            उर्वरित_घोषणा.append({'name': शाब्दिक_शब्द, 'line': नोड_मूल्य.lineno})
                    प्रविष्टी_मूल्य['ascii_python_declarations'] = उर्वरित_घोषणा
                except (SyntaxError, UnicodeError) as त्रुटी:
                    प्रविष्टी_मूल्य['parse_error'] = str(त्रुटी)
            लॉग_नोंद.append(प्रविष्टी_मूल्य)
    मोजमाप = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(वगळा_मूल्य), 'files': लॉग_नोंद,
          'file_count': len(लॉग_नोंद), 'ascii_filename_count': sum(प्रविष्टी_मूल्य['ascii_filename'] for प्रविष्टी_मूल्य in लॉग_नोंद),
          'python_files_with_ascii_declarations': sum(bool(प्रविष्टी_मूल्य.get('ascii_python_declarations')) for प्रविष्टी_मूल्य in लॉग_नोंद),
          'all_repository_identifiers_korean': False,
          'note': '표준 जोडा 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    गंतव्यस्थान_मूल्य = प्रोजेक्ट_मूळ/'build/verification/naming'; गंतव्यस्थान_मूल्य.mkdir(parents=True, exist_ok=True)
    (गंतव्यस्थान_मूल्य/'source-review.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2)+'\n')
    print('स्रोत', मोजमाप['file_count'], '개; ASCII संचिका_नाव_मजकूर', मोजमाप['ascii_filename_count'],
          '개; 영어 선언이 남은 Python फाइल', मोजमाप['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': सुरू_करा()
