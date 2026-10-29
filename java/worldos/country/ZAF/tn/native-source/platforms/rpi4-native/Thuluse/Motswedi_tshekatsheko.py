#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def dirisa():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    rekota_mola = []
    for Lenaneofaele_Boleng, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(leina for leina in 하위들 if leina not in 제외)
        for leina in sorted(파일들):
            tsela = Path(Lenaneofaele_Boleng)/leina
            if tsela.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            tshedimosetso = tsela.read_bytes()
            tsenyo_Boleng = {'path': str(tsela.relative_to(저장소)), 'sha256': hashlib.sha256(tshedimosetso).hexdigest(),
                  'ascii_filename': all(ord(Letshwao_Boleng)<128 for Letshwao_Boleng in tsela.stem)}
            if tsela.suffix == '.py':
                남은선언 = []
                try:
                    for sekopanyamafaratlhatlha_Boleng in ast.walk(ast.parse(tshedimosetso.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(sekopanyamafaratlhatlha_Boleng, (ast.FunctionDef, ast.ClassDef)): 낱말 = sekopanyamafaratlhatlha_Boleng.name
                        elif isinstance(sekopanyamafaratlhatlha_Boleng, ast.arg): 낱말 = sekopanyamafaratlhatlha_Boleng.arg
                        elif isinstance(sekopanyamafaratlhatlha_Boleng, ast.Name) and isinstance(sekopanyamafaratlhatlha_Boleng.ctx, ast.Store): 낱말 = sekopanyamafaratlhatlha_Boleng.id
                        if 낱말 and all(ord(Letshwao_Boleng)<128 for Letshwao_Boleng in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': sekopanyamafaratlhatlha_Boleng.lineno})
                    tsenyo_Boleng['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as phoso:
                    tsenyo_Boleng['parse_error'] = str(phoso)
            rekota_mola.append(tsenyo_Boleng)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': rekota_mola,
          'file_count': len(rekota_mola), 'ascii_filename_count': sum(tsenyo_Boleng['ascii_filename'] for tsenyo_Boleng in rekota_mola),
          'python_files_with_ascii_declarations': sum(bool(tsenyo_Boleng.get('ascii_python_declarations')) for tsenyo_Boleng in rekota_mola),
          'all_repository_identifiers_korean': False,
          'note': '표준 Golaganya 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    bogorogelo_Boleng = 기준/'build/verification/naming'; bogorogelo_Boleng.mkdir(parents=True, exist_ok=True)
    (bogorogelo_Boleng/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('Motswedi', 결과['file_count'], '개; ASCII faele_leina_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python faele', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': dirisa()
