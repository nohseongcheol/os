#!/usr/bin/env python3
"""repositorium_rot 전체의 eget 원문을 목록화한다. ekstern_VERDI/generere 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

speile_rot = Path(__file__).resolve().parents[1]
repositorium_rot = speile_rot.parents[1]

def Kjør_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_POST = []
    for katalog_VERDI, 하위들, 파일들 in os.walk(str(repositorium_rot)):
        하위들[:] = sorted(Navn for Navn in 하위들 if Navn not in 제외)
        for Navn in sorted(파일들):
            Sti = Path(katalog_VERDI)/Navn
            if Sti.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = Sti.read_bytes()
            oppføring_VERDI = {'path': str(Sti.relative_to(repositorium_rot)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(tegn_VERDI)<128 for tegn_VERDI in Sti.stem)}
            if Sti.suffix == '.py':
                남은선언 = []
                try:
                    for node_VERDI in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VERDI, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VERDI.name
                        elif isinstance(node_VERDI, ast.arg): 낱말 = node_VERDI.arg
                        elif isinstance(node_VERDI, ast.Name) and isinstance(node_VERDI.ctx, ast.Store): 낱말 = node_VERDI.id
                        if 낱말 and all(ord(tegn_VERDI)<128 for tegn_VERDI in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VERDI.lineno})
                    oppføring_VERDI['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as feil:
                    oppføring_VERDI['parse_error'] = str(feil)
            LOG_POST.append(oppføring_VERDI)
    KR = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_POST,
          'file_count': len(LOG_POST), 'ascii_filename_count': sum(oppføring_VERDI['ascii_filename'] for oppføring_VERDI in LOG_POST),
          'python_files_with_ascii_declarations': sum(bool(oppføring_VERDI.get('ascii_python_declarations')) for oppføring_VERDI in LOG_POST),
          'all_repository_identifiers_korean': False,
          'note': '표준 Koble_til 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    mål_VERDI = speile_rot/'build/verification/naming'; mål_VERDI.mkdir(parents=True, exist_ok=True)
    (mål_VERDI/'source-review.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2)+'\n')
    print('KILDE', KR['file_count'], '개; ASCII filnavn_SMS', KR['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fil', KR['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Kjør_2()
