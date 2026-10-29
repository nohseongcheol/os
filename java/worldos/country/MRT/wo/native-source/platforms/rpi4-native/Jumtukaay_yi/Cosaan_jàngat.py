#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def daw():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    làq_Dënk = []
    for dàmb_xëyma, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(tur_253d1510 for tur_253d1510 in 하위들 if tur_253d1510 not in 제외)
        for tur_253d1510 in sorted(파일들):
            Yoonu_jëmale = Path(dàmb_xëyma)/tur_253d1510
            if Yoonu_jëmale.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            mbir = Yoonu_jëmale.read_bytes()
            dugal_xabaar_xëyma = {'path': str(Yoonu_jëmale.relative_to(저장소)), 'sha256': hashlib.sha256(mbir).hexdigest(),
                  'ascii_filename': all(ord(Araf_xëyma)<128 for Araf_xëyma in Yoonu_jëmale.stem)}
            if Yoonu_jëmale.suffix == '.py':
                남은선언 = []
                try:
                    for lëkk_lëkk_xëyma in ast.walk(ast.parse(mbir.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(lëkk_lëkk_xëyma, (ast.FunctionDef, ast.ClassDef)): 낱말 = lëkk_lëkk_xëyma.name
                        elif isinstance(lëkk_lëkk_xëyma, ast.arg): 낱말 = lëkk_lëkk_xëyma.arg
                        elif isinstance(lëkk_lëkk_xëyma, ast.Name) and isinstance(lëkk_lëkk_xëyma.ctx, ast.Store): 낱말 = lëkk_lëkk_xëyma.id
                        if 낱말 and all(ord(Araf_xëyma)<128 for Araf_xëyma in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': lëkk_lëkk_xëyma.lineno})
                    dugal_xabaar_xëyma['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as njumte:
                    dugal_xabaar_xëyma['parse_error'] = str(njumte)
            làq_Dënk.append(dugal_xabaar_xëyma)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': làq_Dënk,
          'file_count': len(làq_Dënk), 'ascii_filename_count': sum(dugal_xabaar_xëyma['ascii_filename'] for dugal_xabaar_xëyma in làq_Dënk),
          'python_files_with_ascii_declarations': sum(bool(dugal_xabaar_xëyma.get('ascii_python_declarations')) for dugal_xabaar_xëyma in làq_Dënk),
          'all_repository_identifiers_korean': False,
          'note': '표준 JOKKOO 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    jëmmukaay_xëyma = 기준/'build/verification/naming'; jëmmukaay_xëyma.mkdir(parents=True, exist_ok=True)
    (jëmmukaay_xëyma/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('Cosaan', 결과['file_count'], '개; ASCII bara_denc_tur_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python bara_denc', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': daw()
