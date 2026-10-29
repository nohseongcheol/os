#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def 시작():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    aa_innachikimaajatü_aparatsee = []
    for anaajaalee_ajutuu, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(이름 for 이름 in 하위들 if 이름 not in 제외)
        for 이름 in sorted(파일들):
            wopu_a_ttaaleemüin = Path(anaajaalee_ajutuu)/이름
            if wopu_a_ttaaleemüin.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            atijaaya = wopu_a_ttaaleemüin.read_bytes()
            ekeroliaa_ajutuu = {'path': str(wopu_a_ttaaleemüin.relative_to(저장소)), 'sha256': hashlib.sha256(atijaaya).hexdigest(),
                  'ascii_filename': all(ord(jeerü_ajutuu)<128 for jeerü_ajutuu in wopu_a_ttaaleemüin.stem)}
            if wopu_a_ttaaleemüin.suffix == '.py':
                남은선언 = []
                try:
                    for asho_oo_ajutuu in ast.walk(ast.parse(atijaaya.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(asho_oo_ajutuu, (ast.FunctionDef, ast.ClassDef)): 낱말 = asho_oo_ajutuu.name
                        elif isinstance(asho_oo_ajutuu, ast.arg): 낱말 = asho_oo_ajutuu.arg
                        elif isinstance(asho_oo_ajutuu, ast.Name) and isinstance(asho_oo_ajutuu.ctx, ast.Store): 낱말 = asho_oo_ajutuu.id
                        if 낱말 and all(ord(jeerü_ajutuu)<128 for jeerü_ajutuu in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': asho_oo_ajutuu.lineno})
                    ekeroliaa_ajutuu['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ajachitia:
                    ekeroliaa_ajutuu['parse_error'] = str(ajachitia)
            aa_innachikimaajatü_aparatsee.append(ekeroliaa_ajutuu)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': aa_innachikimaajatü_aparatsee,
          'file_count': len(aa_innachikimaajatü_aparatsee), 'ascii_filename_count': sum(ekeroliaa_ajutuu['ascii_filename'] for ekeroliaa_ajutuu in aa_innachikimaajatü_aparatsee),
          'python_files_with_ascii_declarations': sum(bool(ekeroliaa_ajutuu.get('ascii_python_declarations')) for ekeroliaa_ajutuu in aa_innachikimaajatü_aparatsee),
          'all_repository_identifiers_korean': False,
          'note': '표준 a_ataa 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    jalamüinjatü_ajutuu = 기준/'build/verification/naming'; jalamüinjatü_ajutuu.mkdir(parents=True, exist_ok=True)
    (jalamüinjatü_ajutuu/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('eejeejetülein', 결과['file_count'], '개; ASCII 파일명', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python anaajaalaa', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': 시작()
