#!/usr/bin/env python3
"""ablageWurzel 전체의 eigen 원문을 목록화한다. externWert/generieren 코드는 zählendWert 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

projektWurzel = Path(__file__).resolve().parents[1]
ablageWurzel = projektWurzel.parents[1]

def ausführenVorgang():
    ausschließenWert = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    protokolldateiAufzeichnung = []
    for verzeichnisWert, kinderListe, dateiEinträge in os.walk(str(ablageWurzel)):
        kinderListe[:] = sorted(Name for Name in kinderListe if Name not in ausschließenWert)
        for Name in sorted(dateiEinträge):
            pfad = Path(verzeichnisWert)/Name
            if pfad.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            Daten = pfad.read_bytes()
            eintragWert = {'path': str(pfad.relative_to(ablageWurzel)), 'sha256': hashlib.sha256(Daten).hexdigest(),
                  'ascii_filename': all(ord(zeichenWert)<128 for zeichenWert in pfad.stem)}
            if pfad.suffix == '.py':
                verbleibendDeklarationen = []
                try:
                    for knotenWert in ast.walk(ast.parse(Daten.decode('utf-8-sig'))):
                        lexikalischMaschinenwort = ''
                        if isinstance(knotenWert, (ast.FunctionDef, ast.ClassDef)): lexikalischMaschinenwort = knotenWert.name
                        elif isinstance(knotenWert, ast.arg): lexikalischMaschinenwort = knotenWert.arg
                        elif isinstance(knotenWert, ast.Name) and isinstance(knotenWert.ctx, ast.Store): lexikalischMaschinenwort = knotenWert.id
                        if lexikalischMaschinenwort and all(ord(zeichenWert)<128 for zeichenWert in lexikalischMaschinenwort) and lexikalischMaschinenwort != '_' and not lexikalischMaschinenwort.startswith('__'):
                            verbleibendDeklarationen.append({'name': lexikalischMaschinenwort, 'line': knotenWert.lineno})
                    eintragWert['ascii_python_declarations'] = verbleibendDeklarationen
                except (SyntaxError, UnicodeError) as fehler:
                    eintragWert['parse_error'] = str(fehler)
            protokolldateiAufzeichnung.append(eintragWert)
    ergebnis = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(ausschließenWert), 'files': protokolldateiAufzeichnung,
          'file_count': len(protokolldateiAufzeichnung), 'ascii_filename_count': sum(eintragWert['ascii_filename'] for eintragWert in protokolldateiAufzeichnung),
          'python_files_with_ascii_declarations': sum(bool(eintragWert.get('ascii_python_declarations')) for eintragWert in protokolldateiAufzeichnung),
          'all_repository_identifiers_korean': False,
          'note': '표준 verbinden 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    zielWert = projektWurzel/'build/verification/naming'; zielWert.mkdir(parents=True, exist_ok=True)
    (zielWert/'source-review.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2)+'\n')
    print('Quelltext', ergebnis['file_count'], '개; ASCII dateiNameText', ergebnis['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Datei', ergebnis['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ausführenVorgang()
