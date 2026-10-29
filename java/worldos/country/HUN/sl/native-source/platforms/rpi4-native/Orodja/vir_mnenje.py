#!/usr/bin/env python3
"""shramba_koren 전체의 lastno 원문을 목록화한다. zunanji_VALUE/ustvariti 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

pobuda_koren = Path(__file__).resolve().parents[1]
shramba_koren = pobuda_koren.parents[1]

def Zaženi():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_zapis = []
    for Imenik_VALUE, 하위들, 파일들 in os.walk(str(shramba_koren)):
        하위들[:] = sorted(Ime for Ime in 하위들 if Ime not in 제외)
        for Ime in sorted(파일들):
            POT = Path(Imenik_VALUE)/Ime
            if POT.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            podatki = POT.read_bytes()
            vnos_VALUE = {'path': str(POT.relative_to(shramba_koren)), 'sha256': hashlib.sha256(podatki).hexdigest(),
                  'ascii_filename': all(ord(znak_VALUE)<128 for znak_VALUE in POT.stem)}
            if POT.suffix == '.py':
                남은선언 = []
                try:
                    for vozlišče_VALUE in ast.walk(ast.parse(podatki.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(vozlišče_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = vozlišče_VALUE.name
                        elif isinstance(vozlišče_VALUE, ast.arg): 낱말 = vozlišče_VALUE.arg
                        elif isinstance(vozlišče_VALUE, ast.Name) and isinstance(vozlišče_VALUE.ctx, ast.Store): 낱말 = vozlišče_VALUE.id
                        if 낱말 and all(ord(znak_VALUE)<128 for znak_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': vozlišče_VALUE.lineno})
                    vnos_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as NAPAKA:
                    vnos_VALUE['parse_error'] = str(NAPAKA)
            LOG_zapis.append(vnos_VALUE)
    REZULTAT = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_zapis,
          'file_count': len(LOG_zapis), 'ascii_filename_count': sum(vnos_VALUE['ascii_filename'] for vnos_VALUE in LOG_zapis),
          'python_files_with_ascii_declarations': sum(bool(vnos_VALUE.get('ascii_python_declarations')) for vnos_VALUE in LOG_zapis),
          'all_repository_identifiers_korean': False,
          'note': '표준 Poveži 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    cilj_VALUE = pobuda_koren/'build/verification/naming'; cilj_VALUE.mkdir(parents=True, exist_ok=True)
    (cilj_VALUE/'source-review.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2)+'\n')
    print('VIR', REZULTAT['file_count'], '개; ASCII ime_datoteke_SMS', REZULTAT['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Datoteka', REZULTAT['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Zaženi()
