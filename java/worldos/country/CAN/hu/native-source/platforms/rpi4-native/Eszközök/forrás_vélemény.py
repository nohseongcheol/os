#!/usr/bin/env python3
"""adattár_gyök 전체의 saját 원문을 목록화한다. külső_ÉRTÉK/generálás 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

teendő_gyök = Path(__file__).resolve().parents[1]
adattár_gyök = teendő_gyök.parents[1]

def Futtatás():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_REKORD = []
    for címtár_ÉRTÉK, 하위들, 파일들 in os.walk(str(adattár_gyök)):
        하위들[:] = sorted(Név for Név in 하위들 if Név not in 제외)
        for Név in sorted(파일들):
            ÚTVONAL = Path(címtár_ÉRTÉK)/Név
            if ÚTVONAL.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            adat = ÚTVONAL.read_bytes()
            bejegyzés_ÉRTÉK = {'path': str(ÚTVONAL.relative_to(adattár_gyök)), 'sha256': hashlib.sha256(adat).hexdigest(),
                  'ascii_filename': all(ord(karakter_ÉRTÉK)<128 for karakter_ÉRTÉK in ÚTVONAL.stem)}
            if ÚTVONAL.suffix == '.py':
                남은선언 = []
                try:
                    for csomópont_ÉRTÉK in ast.walk(ast.parse(adat.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(csomópont_ÉRTÉK, (ast.FunctionDef, ast.ClassDef)): 낱말 = csomópont_ÉRTÉK.name
                        elif isinstance(csomópont_ÉRTÉK, ast.arg): 낱말 = csomópont_ÉRTÉK.arg
                        elif isinstance(csomópont_ÉRTÉK, ast.Name) and isinstance(csomópont_ÉRTÉK.ctx, ast.Store): 낱말 = csomópont_ÉRTÉK.id
                        if 낱말 and all(ord(karakter_ÉRTÉK)<128 for karakter_ÉRTÉK in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': csomópont_ÉRTÉK.lineno})
                    bejegyzés_ÉRTÉK['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as HIBA:
                    bejegyzés_ÉRTÉK['parse_error'] = str(HIBA)
            LOG_REKORD.append(bejegyzés_ÉRTÉK)
    KR = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_REKORD,
          'file_count': len(LOG_REKORD), 'ascii_filename_count': sum(bejegyzés_ÉRTÉK['ascii_filename'] for bejegyzés_ÉRTÉK in LOG_REKORD),
          'python_files_with_ascii_declarations': sum(bool(bejegyzés_ÉRTÉK.get('ascii_python_declarations')) for bejegyzés_ÉRTÉK in LOG_REKORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 Kapcsolódás 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    cél_ÉRTÉK = teendő_gyök/'build/verification/naming'; cél_ÉRTÉK.mkdir(parents=True, exist_ok=True)
    (cél_ÉRTÉK/'source-review.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2)+'\n')
    print('FORRÁS', KR['file_count'], '개; ASCII fájlnév_SMS', KR['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fájl', KR['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Futtatás()
