#!/usr/bin/env python3
"""saugykla_šaknis 전체의 savas 원문을 목록화한다. išorinis_VALUE/generuoti 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_šaknis = Path(__file__).resolve().parents[1]
saugykla_šaknis = Project_šaknis.parents[1]

def Paleisti():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for Katalogas_VALUE, 하위들, 파일들 in os.walk(str(saugykla_šaknis)):
        하위들[:] = sorted(Pavadinimas_2 for Pavadinimas_2 in 하위들 if Pavadinimas_2 not in 제외)
        for Pavadinimas_2 in sorted(파일들):
            KELIAS = Path(Katalogas_VALUE)/Pavadinimas_2
            if KELIAS.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            duomenys = KELIAS.read_bytes()
            įrašas_VALUE = {'path': str(KELIAS.relative_to(saugykla_šaknis)), 'sha256': hashlib.sha256(duomenys).hexdigest(),
                  'ascii_filename': all(ord(simbolis_VALUE_068c2631)<128 for simbolis_VALUE_068c2631 in KELIAS.stem)}
            if KELIAS.suffix == '.py':
                남은선언 = []
                try:
                    for mazgas_VALUE in ast.walk(ast.parse(duomenys.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(mazgas_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = mazgas_VALUE.name
                        elif isinstance(mazgas_VALUE, ast.arg): 낱말 = mazgas_VALUE.arg
                        elif isinstance(mazgas_VALUE, ast.Name) and isinstance(mazgas_VALUE.ctx, ast.Store): 낱말 = mazgas_VALUE.id
                        if 낱말 and all(ord(simbolis_VALUE_068c2631)<128 for simbolis_VALUE_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': mazgas_VALUE.lineno})
                    įrašas_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as KLAIDA:
                    įrašas_VALUE['parse_error'] = str(KLAIDA)
            LOG_RECORD.append(įrašas_VALUE)
    REZULTATAS = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(įrašas_VALUE['ascii_filename'] for įrašas_VALUE in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(įrašas_VALUE.get('ascii_python_declarations')) for įrašas_VALUE in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Prisijungti 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    vieta_VALUE = Project_šaknis/'build/verification/naming'; vieta_VALUE.mkdir(parents=True, exist_ok=True)
    (vieta_VALUE/'source-review.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2)+'\n')
    print('ŠALTINIS', REZULTATAS['file_count'], '개; ASCII failo_vardas_SMS', REZULTATAS['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Failas', REZULTATAS['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Paleisti()
