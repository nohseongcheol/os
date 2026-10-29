#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def huutoraade():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    suurnal_winndande = []
    for mooftordu_njaru, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(innde for innde in 하위들 if innde not in 제외)
        for innde in sorted(파일들):
            laawol = Path(mooftordu_njaru)/innde
            if laawol.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            keɓe = laawol.read_bytes()
            naatnugol_njaru = {'path': str(laawol.relative_to(저장소)), 'sha256': hashlib.sha256(keɓe).hexdigest(),
                  'ascii_filename': all(ord(alkulal_njaru)<128 for alkulal_njaru in laawol.stem)}
            if laawol.suffix == '.py':
                남은선언 = []
                try:
                    for piɓol_njaru in ast.walk(ast.parse(keɓe.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(piɓol_njaru, (ast.FunctionDef, ast.ClassDef)): 낱말 = piɓol_njaru.name
                        elif isinstance(piɓol_njaru, ast.arg): 낱말 = piɓol_njaru.arg
                        elif isinstance(piɓol_njaru, ast.Name) and isinstance(piɓol_njaru.ctx, ast.Store): 낱말 = piɓol_njaru.id
                        if 낱말 and all(ord(alkulal_njaru)<128 for alkulal_njaru in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': piɓol_njaru.lineno})
                    naatnugol_njaru['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as juumre:
                    naatnugol_njaru['parse_error'] = str(juumre)
            suurnal_winndande.append(naatnugol_njaru)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': suurnal_winndande,
          'file_count': len(suurnal_winndande), 'ascii_filename_count': sum(naatnugol_njaru['ascii_filename'] for naatnugol_njaru in suurnal_winndande),
          'python_files_with_ascii_declarations': sum(bool(naatnugol_njaru.get('ascii_python_declarations')) for naatnugol_njaru in suurnal_winndande),
          'all_repository_identifiers_korean': False,
          'note': '표준 seŋaade 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    tiindaare_njaru = 기준/'build/verification/naming'; tiindaare_njaru.mkdir(parents=True, exist_ok=True)
    (tiindaare_njaru/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('sewnde', 결과['file_count'], '개; ASCII fiilde_innde_binndi', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python fiilde', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': huutoraade()
