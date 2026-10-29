#!/usr/bin/env python3
"""gagnageymsla_rót 전체의 eigin 원문을 목록화한다. 외부/skapa 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

verk_rót = Path(__file__).resolve().parents[1]
gagnageymsla_rót = verk_rót.parents[1]

def Keyra_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_lína = []
    for skráasafn_VALUE, 하위들, 파일들 in os.walk(str(gagnageymsla_rót)):
        하위들[:] = sorted(Heiti for Heiti in 하위들 if Heiti not in 제외)
        for Heiti in sorted(파일들):
            SLÓÐ = Path(skráasafn_VALUE)/Heiti
            if SLÓÐ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            gögn = SLÓÐ.read_bytes()
            færsla_VALUE = {'path': str(SLÓÐ.relative_to(gagnageymsla_rót)), 'sha256': hashlib.sha256(gögn).hexdigest(),
                  'ascii_filename': all(ord(stafur_VALUE)<128 for stafur_VALUE in SLÓÐ.stem)}
            if SLÓÐ.suffix == '.py':
                남은선언 = []
                try:
                    for hnútur_VALUE in ast.walk(ast.parse(gögn.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(hnútur_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = hnútur_VALUE.name
                        elif isinstance(hnútur_VALUE, ast.arg): 낱말 = hnútur_VALUE.arg
                        elif isinstance(hnútur_VALUE, ast.Name) and isinstance(hnútur_VALUE.ctx, ast.Store): 낱말 = hnútur_VALUE.id
                        if 낱말 and all(ord(stafur_VALUE)<128 for stafur_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': hnútur_VALUE.lineno})
                    færsla_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Villa:
                    færsla_VALUE['parse_error'] = str(Villa)
            LOG_lína.append(færsla_VALUE)
    NIÐURSTAÐA = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_lína,
          'file_count': len(LOG_lína), 'ascii_filename_count': sum(færsla_VALUE['ascii_filename'] for færsla_VALUE in LOG_lína),
          'python_files_with_ascii_declarations': sum(bool(færsla_VALUE.get('ascii_python_declarations')) for færsla_VALUE in LOG_lína),
          'all_repository_identifiers_korean': False,
          'note': '표준 Tengjast 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    endastaður_VALUE = verk_rót/'build/verification/naming'; endastaður_VALUE.mkdir(parents=True, exist_ok=True)
    (endastaður_VALUE/'source-review.json').write_text(json.dumps(NIÐURSTAÐA, ensure_ascii=False, indent=2)+'\n')
    print('Uppruni', NIÐURSTAÐA['file_count'], '개; ASCII skrá_heiti_SMS', NIÐURSTAÐA['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Skrá', NIÐURSTAÐA['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Keyra_2()
