#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/সৃষ্টি_কৰক 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def সঞ্চালন():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    লগ_শাৰী = []
    for ডাইৰেক্টৰী_মান, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(নাম for নাম in 하위들 if নাম not in 제외)
        for নাম in sorted(파일들):
            পথ = Path(ডাইৰেক্টৰী_মান)/নাম
            if পথ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ডাটা = পথ.read_bytes()
            প্রবিষ্ট_মান = {'path': str(পথ.relative_to(저장소)), 'sha256': hashlib.sha256(ডাটা).hexdigest(),
                  'ascii_filename': all(ord(বৰ্ণ_মান)<128 for বৰ্ণ_মান in পথ.stem)}
            if পথ.suffix == '.py':
                남은선언 = []
                try:
                    for নোড_মান in ast.walk(ast.parse(ডাটা.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(নোড_মান, (ast.FunctionDef, ast.ClassDef)): 낱말 = নোড_মান.name
                        elif isinstance(নোড_মান, ast.arg): 낱말 = নোড_মান.arg
                        elif isinstance(নোড_মান, ast.Name) and isinstance(নোড_মান.ctx, ast.Store): 낱말 = নোড_মান.id
                        if 낱말 and all(ord(বৰ্ণ_মান)<128 for বৰ্ণ_মান in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': নোড_মান.lineno})
                    প্রবিষ্ট_মান['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ত্ৰুটি:
                    প্রবিষ্ট_মান['parse_error'] = str(ত্ৰুটি)
            লগ_শাৰী.append(প্রবিষ্ট_মান)
    পৰিমাপ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': লগ_শাৰী,
          'file_count': len(লগ_শাৰী), 'ascii_filename_count': sum(প্রবিষ্ট_মান['ascii_filename'] for প্রবিষ্ট_মান in লগ_শাৰী),
          'python_files_with_ascii_declarations': sum(bool(প্রবিষ্ট_মান.get('ascii_python_declarations')) for প্রবিষ্ট_মান in লগ_শাৰী),
          'all_repository_identifiers_korean': False,
          'note': '표준 সংযোগ_স্থাপনা 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    গন্তব্য_স্থান_মান = 기준/'build/verification/naming'; গন্তব্য_স্থান_মান.mkdir(parents=True, exist_ok=True)
    (গন্তব্য_স্থান_মান/'source-review.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2)+'\n')
    print('উৎস', পৰিমাপ['file_count'], '개; ASCII ফাইল_নাম_পাঠ', পৰিমাপ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python নথিপত্ৰ', পৰিমাপ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': সঞ্চালন()
