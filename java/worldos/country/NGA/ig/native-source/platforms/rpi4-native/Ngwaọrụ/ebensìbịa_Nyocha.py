#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Bido():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ndekọ_NDEKỌ = []
    for dàịrektrị_valuu, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Aha for Aha in 하위들 if Aha not in 제외)
        for Aha in sorted(파일들):
            ụzọ_ozi = Path(dàịrektrị_valuu)/Aha
            if ụzọ_ozi.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            datà = ụzọ_ozi.read_bytes()
            ndebà_valuu = {'path': str(ụzọ_ozi.relative_to(저장소)), 'sha256': hashlib.sha256(datà).hexdigest(),
                  'ascii_filename': all(ord(mkpụrụedemede_valuu)<128 for mkpụrụedemede_valuu in ụzọ_ozi.stem)}
            if ụzọ_ozi.suffix == '.py':
                남은선언 = []
                try:
                    for akpụ_valuu in ast.walk(ast.parse(datà.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(akpụ_valuu, (ast.FunctionDef, ast.ClassDef)): 낱말 = akpụ_valuu.name
                        elif isinstance(akpụ_valuu, ast.arg): 낱말 = akpụ_valuu.arg
                        elif isinstance(akpụ_valuu, ast.Name) and isinstance(akpụ_valuu.ctx, ast.Store): 낱말 = akpụ_valuu.id
                        if 낱말 and all(ord(mkpụrụedemede_valuu)<128 for mkpụrụedemede_valuu in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': akpụ_valuu.lineno})
                    ndebà_valuu['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as mmejọ:
                    ndebà_valuu['parse_error'] = str(mmejọ)
            ndekọ_NDEKỌ.append(ndebà_valuu)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ndekọ_NDEKỌ,
          'file_count': len(ndekọ_NDEKỌ), 'ascii_filename_count': sum(ndebà_valuu['ascii_filename'] for ndebà_valuu in ndekọ_NDEKỌ),
          'python_files_with_ascii_declarations': sum(bool(ndebà_valuu.get('ascii_python_declarations')) for ndebà_valuu in ndekọ_NDEKỌ),
          'all_repository_identifiers_korean': False,
          'note': '표준 Banye 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ebemwèga_valuu = 기준/'build/verification/naming'; ebemwèga_valuu.mkdir(parents=True, exist_ok=True)
    (ebemwèga_valuu/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ebensìbịa', 결과['file_count'], '개; ASCII ọbọakwụkwọ_akara_ahà_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Faịlụ', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Bido()
