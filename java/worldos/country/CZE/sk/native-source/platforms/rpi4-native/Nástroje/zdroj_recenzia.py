#!/usr/bin/env python3
"""odkladací_priestor_koreň 전체의 vlastné 원문을 목록화한다. externý_VALUE/generovať 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

akcia_koreň = Path(__file__).resolve().parents[1]
odkladací_priestor_koreň = akcia_koreň.parents[1]

def Spustiť_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for Adresár_VALUE, 하위들, 파일들 in os.walk(str(odkladací_priestor_koreň)):
        하위들[:] = sorted(Názov for Názov in 하위들 if Názov not in 제외)
        for Názov in sorted(파일들):
            Cesta = Path(Adresár_VALUE)/Názov
            if Cesta.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            údaje = Cesta.read_bytes()
            položka_VALUE = {'path': str(Cesta.relative_to(odkladací_priestor_koreň)), 'sha256': hashlib.sha256(údaje).hexdigest(),
                  'ascii_filename': all(ord(znak_VALUE)<128 for znak_VALUE in Cesta.stem)}
            if Cesta.suffix == '.py':
                남은선언 = []
                try:
                    for uzol_VALUE in ast.walk(ast.parse(údaje.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(uzol_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = uzol_VALUE.name
                        elif isinstance(uzol_VALUE, ast.arg): 낱말 = uzol_VALUE.arg
                        elif isinstance(uzol_VALUE, ast.Name) and isinstance(uzol_VALUE.ctx, ast.Store): 낱말 = uzol_VALUE.id
                        if 낱말 and all(ord(znak_VALUE)<128 for znak_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': uzol_VALUE.lineno})
                    položka_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as chyba:
                    položka_VALUE['parse_error'] = str(chyba)
            LOG_RECORD.append(položka_VALUE)
    KR = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(položka_VALUE['ascii_filename'] for položka_VALUE in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(položka_VALUE.get('ascii_python_declarations')) for položka_VALUE in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Pripojiť 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    cieľ_VALUE = akcia_koreň/'build/verification/naming'; cieľ_VALUE.mkdir(parents=True, exist_ok=True)
    (cieľ_VALUE/'source-review.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2)+'\n')
    print('ZDROJ', KR['file_count'], '개; ASCII názov_súboru_SMS', KR['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Súbor', KR['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Spustiť_2()
