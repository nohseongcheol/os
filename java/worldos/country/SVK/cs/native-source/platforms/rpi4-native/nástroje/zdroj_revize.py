#!/usr/bin/env python3
"""úložiště_kořen 전체의 vlastní 원문을 목록화한다. externí_HODNOTA/generovat 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

akce_kořen = Path(__file__).resolve().parents[1]
úložiště_kořen = akce_kořen.parents[1]

def Spustit_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOGZ_ZÁZNAM = []
    for Adresář_HODNOTA, 하위들, 파일들 in os.walk(str(úložiště_kořen)):
        하위들[:] = sorted(Název for Název in 하위들 if Název not in 제외)
        for Název in sorted(파일들):
            cesta_2 = Path(Adresář_HODNOTA)/Název
            if cesta_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = cesta_2.read_bytes()
            položka_HODNOTA = {'path': str(cesta_2.relative_to(úložiště_kořen)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(znak_HODNOTA)<128 for znak_HODNOTA in cesta_2.stem)}
            if cesta_2.suffix == '.py':
                남은선언 = []
                try:
                    for uzel_HODNOTA in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(uzel_HODNOTA, (ast.FunctionDef, ast.ClassDef)): 낱말 = uzel_HODNOTA.name
                        elif isinstance(uzel_HODNOTA, ast.arg): 낱말 = uzel_HODNOTA.arg
                        elif isinstance(uzel_HODNOTA, ast.Name) and isinstance(uzel_HODNOTA.ctx, ast.Store): 낱말 = uzel_HODNOTA.id
                        if 낱말 and all(ord(znak_HODNOTA)<128 for znak_HODNOTA in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': uzel_HODNOTA.lineno})
                    položka_HODNOTA['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as chyba:
                    položka_HODNOTA['parse_error'] = str(chyba)
            LOGZ_ZÁZNAM.append(položka_HODNOTA)
    VÝSLEDEK = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOGZ_ZÁZNAM,
          'file_count': len(LOGZ_ZÁZNAM), 'ascii_filename_count': sum(položka_HODNOTA['ascii_filename'] for položka_HODNOTA in LOGZ_ZÁZNAM),
          'python_files_with_ascii_declarations': sum(bool(položka_HODNOTA.get('ascii_python_declarations')) for položka_HODNOTA in LOGZ_ZÁZNAM),
          'all_repository_identifiers_korean': False,
          'note': '표준 Připojit 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    cíl_HODNOTA = akce_kořen/'build/verification/naming'; cíl_HODNOTA.mkdir(parents=True, exist_ok=True)
    (cíl_HODNOTA/'source-review.json').write_text(json.dumps(VÝSLEDEK, ensure_ascii=False, indent=2)+'\n')
    print('zdrojový_soubor', VÝSLEDEK['file_count'], '개; ASCII název_souboru_SMS', VÝSLEDEK['ascii_filename_count'],
          '개; 영어 선언이 남은 Python název_souboru', VÝSLEDEK['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Spustit_2()
