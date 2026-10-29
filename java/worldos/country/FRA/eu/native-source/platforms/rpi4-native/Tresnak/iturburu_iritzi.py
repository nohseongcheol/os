#!/usr/bin/env python3
"""biltegi_erro 전체의 자체 원문을 목록화한다. 외부/sortu 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_erro = Path(__file__).resolve().parents[1]
biltegi_erro = Project_erro.parents[1]

def Exekutatu_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_marka = []
    for direktorio_balio, 하위들, 파일들 in os.walk(str(biltegi_erro)):
        하위들[:] = sorted(Izena for Izena in 하위들 if Izena not in 제외)
        for Izena in sorted(파일들):
            Bide_izena = Path(direktorio_balio)/Izena
            if Bide_izena.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            datuak = Bide_izena.read_bytes()
            sarrera_balio = {'path': str(Bide_izena.relative_to(biltegi_erro)), 'sha256': hashlib.sha256(datuak).hexdigest(),
                  'ascii_filename': all(ord(karaktere_balio)<128 for karaktere_balio in Bide_izena.stem)}
            if Bide_izena.suffix == '.py':
                남은선언 = []
                try:
                    for nodo_balio in ast.walk(ast.parse(datuak.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nodo_balio, (ast.FunctionDef, ast.ClassDef)): 낱말 = nodo_balio.name
                        elif isinstance(nodo_balio, ast.arg): 낱말 = nodo_balio.arg
                        elif isinstance(nodo_balio, ast.Name) and isinstance(nodo_balio.ctx, ast.Store): 낱말 = nodo_balio.id
                        if 낱말 and all(ord(karaktere_balio)<128 for karaktere_balio in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nodo_balio.lineno})
                    sarrera_balio['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as errorea:
                    sarrera_balio['parse_error'] = str(errorea)
            LOG_marka.append(sarrera_balio)
    EMAITZA = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_marka,
          'file_count': len(LOG_marka), 'ascii_filename_count': sum(sarrera_balio['ascii_filename'] for sarrera_balio in LOG_marka),
          'python_files_with_ascii_declarations': sum(bool(sarrera_balio.get('ascii_python_declarations')) for sarrera_balio in LOG_marka),
          'all_repository_identifiers_korean': False,
          'note': '표준 Konektatu 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    helburu_balio_a0fbc067 = Project_erro/'build/verification/naming'; helburu_balio_a0fbc067.mkdir(parents=True, exist_ok=True)
    (helburu_balio_a0fbc067/'source-review.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2)+'\n')
    print('ITURBURUA', EMAITZA['file_count'], '개; ASCII fitxategi_izen_SMS', EMAITZA['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fitxategia', EMAITZA['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Exekutatu_2()
