#!/usr/bin/env python3
"""সংগ্রহস্থলের_মূল 전체의 নিজ 원문을 목록화한다. 외부/সৃষ্টি_করুন 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
সংগ্রহস্থলের_মূল = প্রকল্প_মূল.parents[1]

def চালনা():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    লগ_সারি = []
    for ডিরেক্টরি_মান, 하위들, 파일들 in os.walk(str(সংগ্রহস্থলের_মূল)):
        하위들[:] = sorted(নাম for নাম in 하위들 if নাম not in 제외)
        for নাম in sorted(파일들):
            পথ_2 = Path(ডিরেক্টরি_মান)/নাম
            if পথ_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ডাটা = পথ_2.read_bytes()
            ভুক্তি_মান = {'path': str(পথ_2.relative_to(সংগ্রহস্থলের_মূল)), 'sha256': hashlib.sha256(ডাটা).hexdigest(),
                  'ascii_filename': all(ord(অক্ষর_মান)<128 for অক্ষর_মান in পথ_2.stem)}
            if পথ_2.suffix == '.py':
                남은선언 = []
                try:
                    for নোড_মান in ast.walk(ast.parse(ডাটা.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(নোড_মান, (ast.FunctionDef, ast.ClassDef)): 낱말 = নোড_মান.name
                        elif isinstance(নোড_মান, ast.arg): 낱말 = নোড_মান.arg
                        elif isinstance(নোড_মান, ast.Name) and isinstance(নোড_মান.ctx, ast.Store): 낱말 = নোড_মান.id
                        if 낱말 and all(ord(অক্ষর_মান)<128 for অক্ষর_মান in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': নোড_মান.lineno})
                    ভুক্তি_মান['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ত্রুটি:
                    ভুক্তি_মান['parse_error'] = str(ত্রুটি)
            লগ_সারি.append(ভুক্তি_মান)
    পরিমাপ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': লগ_সারি,
          'file_count': len(লগ_সারি), 'ascii_filename_count': sum(ভুক্তি_মান['ascii_filename'] for ভুক্তি_মান in লগ_সারি),
          'python_files_with_ascii_declarations': sum(bool(ভুক্তি_মান.get('ascii_python_declarations')) for ভুক্তি_মান in লগ_সারি),
          'all_repository_identifiers_korean': False,
          'note': '표준 সংযোগ_স্থাপনা 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    গন্তব্য_মান = প্রকল্প_মূল/'build/verification/naming'; গন্তব্য_মান.mkdir(parents=True, exist_ok=True)
    (গন্তব্য_মান/'source-review.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2)+'\n')
    print('উৎস_নথি', পরিমাপ['file_count'], '개; ASCII ফাইল_নাম_পাঠ', পরিমাপ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python নথির_নাম', পরিমাপ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': চালনা()
