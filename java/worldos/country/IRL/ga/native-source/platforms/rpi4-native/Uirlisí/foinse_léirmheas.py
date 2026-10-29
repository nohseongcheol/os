#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/giniúint 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

teilgean_fréamh = Path(__file__).resolve().parents[1]
저장소 = teilgean_fréamh.parents[1]

def Rith_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_ró = []
    for eolaire_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Ainm for Ainm in 하위들 if Ainm not in 제외)
        for Ainm in sorted(파일들):
            CONAIR = Path(eolaire_VALUE)/Ainm
            if CONAIR.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            sonraí = CONAIR.read_bytes()
            iontráil_VALUE = {'path': str(CONAIR.relative_to(저장소)), 'sha256': hashlib.sha256(sonraí).hexdigest(),
                  'ascii_filename': all(ord(carachtar_VALUE)<128 for carachtar_VALUE in CONAIR.stem)}
            if CONAIR.suffix == '.py':
                남은선언 = []
                try:
                    for nód_VALUE in ast.walk(ast.parse(sonraí.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nód_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nód_VALUE.name
                        elif isinstance(nód_VALUE, ast.arg): 낱말 = nód_VALUE.arg
                        elif isinstance(nód_VALUE, ast.Name) and isinstance(nód_VALUE.ctx, ast.Store): 낱말 = nód_VALUE.id
                        if 낱말 and all(ord(carachtar_VALUE)<128 for carachtar_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nód_VALUE.lineno})
                    iontráil_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ERREÁID:
                    iontráil_VALUE['parse_error'] = str(ERREÁID)
            LOG_ró.append(iontráil_VALUE)
    tomhas = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_ró,
          'file_count': len(LOG_ró), 'ascii_filename_count': sum(iontráil_VALUE['ascii_filename'] for iontráil_VALUE in LOG_ró),
          'python_files_with_ascii_declarations': sum(bool(iontráil_VALUE.get('ascii_python_declarations')) for iontráil_VALUE in LOG_ró),
          'all_repository_identifiers_korean': False,
          'note': '표준 Nasc 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    sprioc_VALUE = teilgean_fréamh/'build/verification/naming'; sprioc_VALUE.mkdir(parents=True, exist_ok=True)
    (sprioc_VALUE/'source-review.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2)+'\n')
    print('FOINSE', tomhas['file_count'], '개; ASCII comhad_ainm_SMS', tomhas['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Comhad', tomhas['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Rith_2()
