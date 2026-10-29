#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Sebenzisa():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    loga_umugqa = []
    for umkhombandlela_inani, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Igama for Igama in 하위들 if Igama not in 제외)
        for Igama in sorted(파일들):
            Indlela_2 = Path(umkhombandlela_inani)/Igama
            if Indlela_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            imininingwane = Indlela_2.read_bytes()
            okufakwayo_inani = {'path': str(Indlela_2.relative_to(저장소)), 'sha256': hashlib.sha256(imininingwane).hexdigest(),
                  'ascii_filename': all(ord(uhlamvusimo_inani)<128 for uhlamvusimo_inani in Indlela_2.stem)}
            if Indlela_2.suffix == '.py':
                남은선언 = []
                try:
                    for iqupha_inani in ast.walk(ast.parse(imininingwane.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(iqupha_inani, (ast.FunctionDef, ast.ClassDef)): 낱말 = iqupha_inani.name
                        elif isinstance(iqupha_inani, ast.arg): 낱말 = iqupha_inani.arg
                        elif isinstance(iqupha_inani, ast.Name) and isinstance(iqupha_inani.ctx, ast.Store): 낱말 = iqupha_inani.id
                        if 낱말 and all(ord(uhlamvusimo_inani)<128 for uhlamvusimo_inani in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': iqupha_inani.lineno})
                    okufakwayo_inani['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Iphutha:
                    okufakwayo_inani['parse_error'] = str(Iphutha)
            loga_umugqa.append(okufakwayo_inani)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': loga_umugqa,
          'file_count': len(loga_umugqa), 'ascii_filename_count': sum(okufakwayo_inani['ascii_filename'] for okufakwayo_inani in loga_umugqa),
          'python_files_with_ascii_declarations': sum(bool(okufakwayo_inani.get('ascii_python_declarations')) for okufakwayo_inani in loga_umugqa),
          'all_repository_identifiers_korean': False,
          'note': '표준 Xhumanisa 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    isikhumulo_inani = 기준/'build/verification/naming'; isikhumulo_inani.mkdir(parents=True, exist_ok=True)
    (isikhumulo_inani/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('umthombo', 결과['file_count'], '개; ASCII ifayela_igama_I_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Ihele', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Sebenzisa()
