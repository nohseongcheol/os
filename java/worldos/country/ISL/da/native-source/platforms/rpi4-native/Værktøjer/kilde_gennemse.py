#!/usr/bin/env python3
"""lager_rod 전체의 eget 원문을 목록화한다. ekstern_VÆRDI/generere 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

To_do_rod = Path(__file__).resolve().parents[1]
lager_rod = To_do_rod.parents[1]

def Kør_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_post = []
    for mappe_VÆRDI, 하위들, 파일들 in os.walk(str(lager_rod)):
        하위들[:] = sorted(Navn for Navn in 하위들 if Navn not in 제외)
        for Navn in sorted(파일들):
            Sti = Path(mappe_VÆRDI)/Navn
            if Sti.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = Sti.read_bytes()
            post_VÆRDI_962f286b = {'path': str(Sti.relative_to(lager_rod)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(tegn_VÆRDI)<128 for tegn_VÆRDI in Sti.stem)}
            if Sti.suffix == '.py':
                남은선언 = []
                try:
                    for node_VÆRDI in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VÆRDI, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VÆRDI.name
                        elif isinstance(node_VÆRDI, ast.arg): 낱말 = node_VÆRDI.arg
                        elif isinstance(node_VÆRDI, ast.Name) and isinstance(node_VÆRDI.ctx, ast.Store): 낱말 = node_VÆRDI.id
                        if 낱말 and all(ord(tegn_VÆRDI)<128 for tegn_VÆRDI in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VÆRDI.lineno})
                    post_VÆRDI_962f286b['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as fejl:
                    post_VÆRDI_962f286b['parse_error'] = str(fejl)
            LOG_post.append(post_VÆRDI_962f286b)
    KR = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_post,
          'file_count': len(LOG_post), 'ascii_filename_count': sum(post_VÆRDI_962f286b['ascii_filename'] for post_VÆRDI_962f286b in LOG_post),
          'python_files_with_ascii_declarations': sum(bool(post_VÆRDI_962f286b.get('ascii_python_declarations')) for post_VÆRDI_962f286b in LOG_post),
          'all_repository_identifiers_korean': False,
          'note': '표준 Tilslut 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destination_VÆRDI = To_do_rod/'build/verification/naming'; destination_VÆRDI.mkdir(parents=True, exist_ok=True)
    (destination_VÆRDI/'source-review.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2)+'\n')
    print('KILDE', KR['file_count'], '개; ASCII filnavn_sms', KR['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fil', KR['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Kør_2()
