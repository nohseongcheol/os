#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/cynhyrchu 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

prosiect_gwraidd = Path(__file__).resolve().parents[1]
저장소 = prosiect_gwraidd.parents[1]

def Gweithredu_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_rhes = []
    for cyfeiriadur_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Enw for Enw in 하위들 if Enw not in 제외)
        for Enw in sorted(파일들):
            LLWYBR = Path(cyfeiriadur_VALUE)/Enw
            if LLWYBR.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = LLWYBR.read_bytes()
            cofnod_VALUE = {'path': str(LLWYBR.relative_to(저장소)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(nod_VALUE)<128 for nod_VALUE in LLWYBR.stem)}
            if LLWYBR.suffix == '.py':
                남은선언 = []
                try:
                    for cwgn_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(cwgn_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = cwgn_VALUE.name
                        elif isinstance(cwgn_VALUE, ast.arg): 낱말 = cwgn_VALUE.arg
                        elif isinstance(cwgn_VALUE, ast.Name) and isinstance(cwgn_VALUE.ctx, ast.Store): 낱말 = cwgn_VALUE.id
                        if 낱말 and all(ord(nod_VALUE)<128 for nod_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': cwgn_VALUE.lineno})
                    cofnod_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Gwall:
                    cofnod_VALUE['parse_error'] = str(Gwall)
            LOG_rhes.append(cofnod_VALUE)
    mesur = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_rhes,
          'file_count': len(LOG_rhes), 'ascii_filename_count': sum(cofnod_VALUE['ascii_filename'] for cofnod_VALUE in LOG_rhes),
          'python_files_with_ascii_declarations': sum(bool(cofnod_VALUE.get('ascii_python_declarations')) for cofnod_VALUE in LOG_rhes),
          'all_repository_identifiers_korean': False,
          'note': '표준 Cysylltu 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    cyrchfan_VALUE = prosiect_gwraidd/'build/verification/naming'; cyrchfan_VALUE.mkdir(parents=True, exist_ok=True)
    (cyrchfan_VALUE/'source-review.json').write_text(json.dumps(mesur, ensure_ascii=False, indent=2)+'\n')
    print('FFYNHONNELL', mesur['file_count'], '개; ASCII ffeil_enw_SMS', mesur['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Ffeil', mesur['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Gweithredu_2()
