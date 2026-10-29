#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. iz_eksternog_izvora_VALUE/generirati 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

projicirati_koijen = Path(__file__).resolve().parents[1]
저장소 = projicirati_koijen.parents[1]

def Pokreni():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_red = []
    for Direktorij_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Naziv for Naziv in 하위들 if Naziv not in 제외)
        for Naziv in sorted(파일들):
            Putanja = Path(Direktorij_VALUE)/Naziv
            if Putanja.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            podaci = Putanja.read_bytes()
            unos_VALUE = {'path': str(Putanja.relative_to(저장소)), 'sha256': hashlib.sha256(podaci).hexdigest(),
                  'ascii_filename': all(ord(znak_VALUE)<128 for znak_VALUE in Putanja.stem)}
            if Putanja.suffix == '.py':
                남은선언 = []
                try:
                    for čvor_VALUE in ast.walk(ast.parse(podaci.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(čvor_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = čvor_VALUE.name
                        elif isinstance(čvor_VALUE, ast.arg): 낱말 = čvor_VALUE.arg
                        elif isinstance(čvor_VALUE, ast.Name) and isinstance(čvor_VALUE.ctx, ast.Store): 낱말 = čvor_VALUE.id
                        if 낱말 and all(ord(znak_VALUE)<128 for znak_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': čvor_VALUE.lineno})
                    unos_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as GRESKA:
                    unos_VALUE['parse_error'] = str(GRESKA)
            LOG_red.append(unos_VALUE)
    mjera = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_red,
          'file_count': len(LOG_red), 'ascii_filename_count': sum(unos_VALUE['ascii_filename'] for unos_VALUE in LOG_red),
          'python_files_with_ascii_declarations': sum(bool(unos_VALUE.get('ascii_python_declarations')) for unos_VALUE in LOG_red),
          'all_repository_identifiers_korean': False,
          'note': '표준 Spoji_se 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    odredište_VALUE = projicirati_koijen/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'source-review.json').write_text(json.dumps(mjera, ensure_ascii=False, indent=2)+'\n')
    print('IZVOR', mjera['file_count'], '개; ASCII fajl_naziv_SMS', mjera['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fajl', mjera['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Pokreni()
