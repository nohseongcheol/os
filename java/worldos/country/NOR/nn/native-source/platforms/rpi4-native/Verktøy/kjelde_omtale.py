#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. ekstern_VALUE/generere 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

spegle_rot = Path(__file__).resolve().parents[1]
저장소 = spegle_rot.parents[1]

def Køyr_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_rad = []
    for katalog_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Namn for Namn in 하위들 if Namn not in 제외)
        for Namn in sorted(파일들):
            STIGE = Path(katalog_VALUE)/Namn
            if STIGE.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = STIGE.read_bytes()
            oppføring_VALUE = {'path': str(STIGE.relative_to(저장소)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(teikn_VALUE)<128 for teikn_VALUE in STIGE.stem)}
            if STIGE.suffix == '.py':
                남은선언 = []
                try:
                    for node_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VALUE.name
                        elif isinstance(node_VALUE, ast.arg): 낱말 = node_VALUE.arg
                        elif isinstance(node_VALUE, ast.Name) and isinstance(node_VALUE.ctx, ast.Store): 낱말 = node_VALUE.id
                        if 낱말 and all(ord(teikn_VALUE)<128 for teikn_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VALUE.lineno})
                    oppføring_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as FEIL:
                    oppføring_VALUE['parse_error'] = str(FEIL)
            LOG_rad.append(oppføring_VALUE)
    forretningsmål = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_rad,
          'file_count': len(LOG_rad), 'ascii_filename_count': sum(oppføring_VALUE['ascii_filename'] for oppføring_VALUE in LOG_rad),
          'python_files_with_ascii_declarations': sum(bool(oppføring_VALUE.get('ascii_python_declarations')) for oppføring_VALUE in LOG_rad),
          'all_repository_identifiers_korean': False,
          'note': '표준 Kopla_til 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    mål_VALUE = spegle_rot/'build/verification/naming'; mål_VALUE.mkdir(parents=True, exist_ok=True)
    (mål_VALUE/'source-review.json').write_text(json.dumps(forretningsmål, ensure_ascii=False, indent=2)+'\n')
    print('KJELDE', forretningsmål['file_count'], '개; ASCII fil_namn_SMS', forretningsmål['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fil', forretningsmål['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Køyr_2()
