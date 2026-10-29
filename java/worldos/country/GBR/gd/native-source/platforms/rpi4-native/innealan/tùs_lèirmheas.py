#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/gin 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

tilg_freumh = Path(__file__).resolve().parents[1]
저장소 = tilg_freumh.parents[1]

def ruith():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_ràgh = []
    for eòlaire_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Ainm for Ainm in 하위들 if Ainm not in 제외)
        for Ainm in sorted(파일들):
            Slighe = Path(eòlaire_VALUE)/Ainm
            if Slighe.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            dàta = Slighe.read_bytes()
            cur_a_steach_VALUE = {'path': str(Slighe.relative_to(저장소)), 'sha256': hashlib.sha256(dàta).hexdigest(),
                  'ascii_filename': all(ord(caractar_VALUE)<128 for caractar_VALUE in Slighe.stem)}
            if Slighe.suffix == '.py':
                남은선언 = []
                try:
                    for nòd_VALUE in ast.walk(ast.parse(dàta.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nòd_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nòd_VALUE.name
                        elif isinstance(nòd_VALUE, ast.arg): 낱말 = nòd_VALUE.arg
                        elif isinstance(nòd_VALUE, ast.Name) and isinstance(nòd_VALUE.ctx, ast.Store): 낱말 = nòd_VALUE.id
                        if 낱말 and all(ord(caractar_VALUE)<128 for caractar_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nòd_VALUE.lineno})
                    cur_a_steach_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Mearachd:
                    cur_a_steach_VALUE['parse_error'] = str(Mearachd)
            LOG_ràgh.append(cur_a_steach_VALUE)
    tomhas = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_ràgh,
          'file_count': len(LOG_ràgh), 'ascii_filename_count': sum(cur_a_steach_VALUE['ascii_filename'] for cur_a_steach_VALUE in LOG_ràgh),
          'python_files_with_ascii_declarations': sum(bool(cur_a_steach_VALUE.get('ascii_python_declarations')) for cur_a_steach_VALUE in LOG_ràgh),
          'all_repository_identifiers_korean': False,
          'note': '표준 CONNECT 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ceann_uidhe_VALUE = tilg_freumh/'build/verification/naming'; ceann_uidhe_VALUE.mkdir(parents=True, exist_ok=True)
    (ceann_uidhe_VALUE/'source-review.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2)+'\n')
    print('tùs', tomhas['file_count'], '개; ASCII faidhle_ainm_SMS', tomhas['ascii_filename_count'],
          '개; 영어 선언이 남은 Python faidhle', tomhas['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ruith()
