#!/usr/bin/env python3
"""مستودع_جذر 전체의 ذاتي 원문을 목록화한다. خارجي_قيمة/إنشاء 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

يعرض_جذر = Path(__file__).resolve().parents[1]
مستودع_جذر = يعرض_جذر.parents[1]

def تشغيل():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    سجل_سجل = []
    for دليل_قيمة, 하위들, 파일들 in os.walk(str(مستودع_جذر)):
        하위들[:] = sorted(اسم for اسم in 하위들 if اسم not in 제외)
        for اسم in sorted(파일들):
            مسار = Path(دليل_قيمة)/اسم
            if مسار.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            بيانات = مسار.read_bytes()
            إدخال_قيمة_962f286b = {'path': str(مسار.relative_to(مستودع_جذر)), 'sha256': hashlib.sha256(بيانات).hexdigest(),
                  'ascii_filename': all(ord(حرف_قيمة)<128 for حرف_قيمة in مسار.stem)}
            if مسار.suffix == '.py':
                남은선언 = []
                try:
                    for عقدة_قيمة in ast.walk(ast.parse(بيانات.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(عقدة_قيمة, (ast.FunctionDef, ast.ClassDef)): 낱말 = عقدة_قيمة.name
                        elif isinstance(عقدة_قيمة, ast.arg): 낱말 = عقدة_قيمة.arg
                        elif isinstance(عقدة_قيمة, ast.Name) and isinstance(عقدة_قيمة.ctx, ast.Store): 낱말 = عقدة_قيمة.id
                        if 낱말 and all(ord(حرف_قيمة)<128 for حرف_قيمة in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': عقدة_قيمة.lineno})
                    إدخال_قيمة_962f286b['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as خطأ:
                    إدخال_قيمة_962f286b['parse_error'] = str(خطأ)
            سجل_سجل.append(إدخال_قيمة_962f286b)
    نتيجة = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': سجل_سجل,
          'file_count': len(سجل_سجل), 'ascii_filename_count': sum(إدخال_قيمة_962f286b['ascii_filename'] for إدخال_قيمة_962f286b in سجل_سجل),
          'python_files_with_ascii_declarations': sum(bool(إدخال_قيمة_962f286b.get('ascii_python_declarations')) for إدخال_قيمة_962f286b in سجل_سجل),
          'all_repository_identifiers_korean': False,
          'note': '표준 اتصال 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    وجهة_قيمة = يعرض_جذر/'build/verification/naming'; وجهة_قيمة.mkdir(parents=True, exist_ok=True)
    (وجهة_قيمة/'source-review.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2)+'\n')
    print('مصدر', نتيجة['file_count'], '개; ASCII اسم_الملف_نص', نتيجة['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ملف', نتيجة['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': تشغيل()
