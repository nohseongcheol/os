#!/usr/bin/env python3
"""anbar_kök 전체의 자체 원문을 목록화한다. 외부/yarat 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_kök = Path(__file__).resolve().parents[1]
anbar_kök = Project_kök.parents[1]

def İcra_Et():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_yaz = []
    for kataloq_VALUE, 하위들, 파일들 in os.walk(str(anbar_kök)):
        하위들[:] = sorted(Ad for Ad in 하위들 if Ad not in 제외)
        for Ad in sorted(파일들):
            Cığır = Path(kataloq_VALUE)/Ad
            if Cığır.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            verilənlər = Cığır.read_bytes()
            daxiletmə_VALUE = {'path': str(Cığır.relative_to(anbar_kök)), 'sha256': hashlib.sha256(verilənlər).hexdigest(),
                  'ascii_filename': all(ord(simvol_VALUE_068c2631)<128 for simvol_VALUE_068c2631 in Cığır.stem)}
            if Cığır.suffix == '.py':
                남은선언 = []
                try:
                    for qovşaq_VALUE in ast.walk(ast.parse(verilənlər.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(qovşaq_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = qovşaq_VALUE.name
                        elif isinstance(qovşaq_VALUE, ast.arg): 낱말 = qovşaq_VALUE.arg
                        elif isinstance(qovşaq_VALUE, ast.Name) and isinstance(qovşaq_VALUE.ctx, ast.Store): 낱말 = qovşaq_VALUE.id
                        if 낱말 and all(ord(simvol_VALUE_068c2631)<128 for simvol_VALUE_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': qovşaq_VALUE.lineno})
                    daxiletmə_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as XƏTA:
                    daxiletmə_VALUE['parse_error'] = str(XƏTA)
            LOG_yaz.append(daxiletmə_VALUE)
    ölçü = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_yaz,
          'file_count': len(LOG_yaz), 'ascii_filename_count': sum(daxiletmə_VALUE['ascii_filename'] for daxiletmə_VALUE in LOG_yaz),
          'python_files_with_ascii_declarations': sum(bool(daxiletmə_VALUE.get('ascii_python_declarations')) for daxiletmə_VALUE in LOG_yaz),
          'all_repository_identifiers_korean': False,
          'note': '표준 Bağlan 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    təyinat_VALUE_a0fbc067 = Project_kök/'build/verification/naming'; təyinat_VALUE_a0fbc067.mkdir(parents=True, exist_ok=True)
    (təyinat_VALUE_a0fbc067/'source-review.json').write_text(json.dumps(ölçü, ensure_ascii=False, indent=2)+'\n')
    print('QAYNAQ', ölçü['file_count'], '개; ASCII fayl_ad_SMS', ölçü['ascii_filename_count'],
          '개; 영어 선언이 남은 Python FAYL', ölçü['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': İcra_Et()
