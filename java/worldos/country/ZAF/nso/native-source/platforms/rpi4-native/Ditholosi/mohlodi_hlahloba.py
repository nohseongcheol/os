#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Diriša():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    pego_rei = []
    for lelokelelo_boleng, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Leina for Leina in 하위들 if Leina not in 제외)
        for Leina in sorted(파일들):
            Tsejana = Path(lelokelelo_boleng)/Leina
            if Tsejana.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = Tsejana.read_bytes()
            go_tsenya_tshedimošo_boleng = {'path': str(Tsejana.relative_to(저장소)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(tlhaka_boleng)<128 for tlhaka_boleng in Tsejana.stem)}
            if Tsejana.suffix == '.py':
                남은선언 = []
                try:
                    for noute_boleng in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(noute_boleng, (ast.FunctionDef, ast.ClassDef)): 낱말 = noute_boleng.name
                        elif isinstance(noute_boleng, ast.arg): 낱말 = noute_boleng.arg
                        elif isinstance(noute_boleng, ast.Name) and isinstance(noute_boleng.ctx, ast.Store): 낱말 = noute_boleng.id
                        if 낱말 and all(ord(tlhaka_boleng)<128 for tlhaka_boleng in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': noute_boleng.lineno})
                    go_tsenya_tshedimošo_boleng['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Phošo:
                    go_tsenya_tshedimošo_boleng['parse_error'] = str(Phošo)
            pego_rei.append(go_tsenya_tshedimošo_boleng)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': pego_rei,
          'file_count': len(pego_rei), 'ascii_filename_count': sum(go_tsenya_tshedimošo_boleng['ascii_filename'] for go_tsenya_tshedimošo_boleng in pego_rei),
          'python_files_with_ascii_declarations': sum(bool(go_tsenya_tshedimošo_boleng.get('ascii_python_declarations')) for go_tsenya_tshedimošo_boleng in pego_rei),
          'all_repository_identifiers_korean': False,
          'note': '표준 Ikgokaganye 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    boyo_boleng = 기준/'build/verification/naming'; boyo_boleng.mkdir(parents=True, exist_ok=True)
    (boyo_boleng/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('mohlodi', 결과['file_count'], '개; ASCII faele_leina_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Faele', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Diriša()
