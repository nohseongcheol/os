#!/usr/bin/env python3
"""säilö_juuri 전체의 oma 원문을 목록화한다. ulkoinen_ARVO/generoida 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

aloite_juuri = Path(__file__).resolve().parents[1]
säilö_juuri = aloite_juuri.parents[1]

def Suorita_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_TIETUE = []
    for Directory_ARVO, 하위들, 파일들 in os.walk(str(säilö_juuri)):
        하위들[:] = sorted(Nimi for Nimi in 하위들 if Nimi not in 제외)
        for Nimi in sorted(파일들):
            polku_2 = Path(Directory_ARVO)/Nimi
            if polku_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = polku_2.read_bytes()
            merkintä_ARVO_962f286b = {'path': str(polku_2.relative_to(säilö_juuri)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(merkki_ARVO)<128 for merkki_ARVO in polku_2.stem)}
            if polku_2.suffix == '.py':
                남은선언 = []
                try:
                    for solmu_ARVO in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(solmu_ARVO, (ast.FunctionDef, ast.ClassDef)): 낱말 = solmu_ARVO.name
                        elif isinstance(solmu_ARVO, ast.arg): 낱말 = solmu_ARVO.arg
                        elif isinstance(solmu_ARVO, ast.Name) and isinstance(solmu_ARVO.ctx, ast.Store): 낱말 = solmu_ARVO.id
                        if 낱말 and all(ord(merkki_ARVO)<128 for merkki_ARVO in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': solmu_ARVO.lineno})
                    merkintä_ARVO_962f286b['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as VIRHE:
                    merkintä_ARVO_962f286b['parse_error'] = str(VIRHE)
            LOG_TIETUE.append(merkintä_ARVO_962f286b)
    TULOS = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_TIETUE,
          'file_count': len(LOG_TIETUE), 'ascii_filename_count': sum(merkintä_ARVO_962f286b['ascii_filename'] for merkintä_ARVO_962f286b in LOG_TIETUE),
          'python_files_with_ascii_declarations': sum(bool(merkintä_ARVO_962f286b.get('ascii_python_declarations')) for merkintä_ARVO_962f286b in LOG_TIETUE),
          'all_repository_identifiers_korean': False,
          'note': '표준 Yhdistä 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    kohde_ARVO = aloite_juuri/'build/verification/naming'; kohde_ARVO.mkdir(parents=True, exist_ok=True)
    (kohde_ARVO/'source-review.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2)+'\n')
    print('lähdetiedosto', TULOS['file_count'], '개; ASCII tiedostonimi_SMS', TULOS['ascii_filename_count'],
          '개; 영어 선언이 남은 Python tiedoston_nimi', TULOS['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Suorita_2()
