#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Rọ́ọ̀nù():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    àkọsílẹ̀_ìṣe_ìlà_ìbú = []
    for àkójọpọ̀_fáìlì_iye, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Orúkọ for Orúkọ in 하위들 if Orúkọ not in 제외)
        for Orúkọ in sorted(파일들):
            ọ̀nà = Path(àkójọpọ̀_fáìlì_iye)/Orúkọ
            if ọ̀nà.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            détà = ọ̀nà.read_bytes()
            ìgbéwọlé_iye = {'path': str(ọ̀nà.relative_to(저장소)), 'sha256': hashlib.sha256(détà).hexdigest(),
                  'ascii_filename': all(ord(ẹyọ_ọ̀rọ̀_iye)<128 for ẹyọ_ọ̀rọ̀_iye in ọ̀nà.stem)}
            if ọ̀nà.suffix == '.py':
                남은선언 = []
                try:
                    for apẹka_iye in ast.walk(ast.parse(détà.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(apẹka_iye, (ast.FunctionDef, ast.ClassDef)): 낱말 = apẹka_iye.name
                        elif isinstance(apẹka_iye, ast.arg): 낱말 = apẹka_iye.arg
                        elif isinstance(apẹka_iye, ast.Name) and isinstance(apẹka_iye.ctx, ast.Store): 낱말 = apẹka_iye.id
                        if 낱말 and all(ord(ẹyọ_ọ̀rọ̀_iye)<128 for ẹyọ_ọ̀rọ̀_iye in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': apẹka_iye.lineno})
                    ìgbéwọlé_iye['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as àṣìṣe:
                    ìgbéwọlé_iye['parse_error'] = str(àṣìṣe)
            àkọsílẹ̀_ìṣe_ìlà_ìbú.append(ìgbéwọlé_iye)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': àkọsílẹ̀_ìṣe_ìlà_ìbú,
          'file_count': len(àkọsílẹ̀_ìṣe_ìlà_ìbú), 'ascii_filename_count': sum(ìgbéwọlé_iye['ascii_filename'] for ìgbéwọlé_iye in àkọsílẹ̀_ìṣe_ìlà_ìbú),
          'python_files_with_ascii_declarations': sum(bool(ìgbéwọlé_iye.get('ascii_python_declarations')) for ìgbéwọlé_iye in àkọsílẹ̀_ìṣe_ìlà_ìbú),
          'all_repository_identifiers_korean': False,
          'note': '표준 Darapọ̀ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    èbúté_iye = 기준/'build/verification/naming'; èbúté_iye.mkdir(parents=True, exist_ok=True)
    (èbúté_iye/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('orísun', 결과['file_count'], '개; ASCII fáìlì_orúkọ_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fáìlì', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Rọ́ọ̀nù()
