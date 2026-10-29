#!/usr/bin/env python3
"""centrallager_rot 전체의 eget 원문을 목록화한다. extern_värde/generera 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

åtgärd_rot = Path(__file__).resolve().parents[1]
centrallager_rot = åtgärd_rot.parents[1]

def Kör():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_POST = []
    for Katalog_värde, 하위들, 파일들 in os.walk(str(centrallager_rot)):
        하위들[:] = sorted(Namn for Namn in 하위들 if Namn not in 제외)
        for Namn in sorted(파일들):
            sökväg_2 = Path(Katalog_värde)/Namn
            if sökväg_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = sökväg_2.read_bytes()
            post_värde = {'path': str(sökväg_2.relative_to(centrallager_rot)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(tecken_värde)<128 for tecken_värde in sökväg_2.stem)}
            if sökväg_2.suffix == '.py':
                남은선언 = []
                try:
                    for nod_värde in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nod_värde, (ast.FunctionDef, ast.ClassDef)): 낱말 = nod_värde.name
                        elif isinstance(nod_värde, ast.arg): 낱말 = nod_värde.arg
                        elif isinstance(nod_värde, ast.Name) and isinstance(nod_värde.ctx, ast.Store): 낱말 = nod_värde.id
                        if 낱말 and all(ord(tecken_värde)<128 for tecken_värde in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nod_värde.lineno})
                    post_värde['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as fel:
                    post_värde['parse_error'] = str(fel)
            LOG_POST.append(post_värde)
    RESULTAT = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_POST,
          'file_count': len(LOG_POST), 'ascii_filename_count': sum(post_värde['ascii_filename'] for post_värde in LOG_POST),
          'python_files_with_ascii_declarations': sum(bool(post_värde.get('ascii_python_declarations')) for post_värde in LOG_POST),
          'all_repository_identifiers_korean': False,
          'note': '표준 Anslut 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    mål_värde = åtgärd_rot/'build/verification/naming'; mål_värde.mkdir(parents=True, exist_ok=True)
    (mål_värde/'source-review.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2)+'\n')
    print('källfil', RESULTAT['file_count'], '개; ASCII filnamn_SMS', RESULTAT['ascii_filename_count'],
          '개; 영어 선언이 남은 Python filnamn', RESULTAT['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Kör()
