#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/generéieren 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

projezéieren_Racinn = Path(__file__).resolve().parents[1]
저장소 = projezéieren_Racinn.parents[1]

def Laf():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_Rei = []
    for Verzeechnes_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Numm for Numm in 하위들 if Numm not in 제외)
        for Numm in sorted(파일들):
            Wee = Path(Verzeechnes_VALUE)/Numm
            if Wee.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            Daten = Wee.read_bytes()
            Agab_VALUE = {'path': str(Wee.relative_to(저장소)), 'sha256': hashlib.sha256(Daten).hexdigest(),
                  'ascii_filename': all(ord(Zeechen_VALUE)<128 for Zeechen_VALUE in Wee.stem)}
            if Wee.suffix == '.py':
                남은선언 = []
                try:
                    for Knuet_VALUE in ast.walk(ast.parse(Daten.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(Knuet_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = Knuet_VALUE.name
                        elif isinstance(Knuet_VALUE, ast.arg): 낱말 = Knuet_VALUE.arg
                        elif isinstance(Knuet_VALUE, ast.Name) and isinstance(Knuet_VALUE.ctx, ast.Store): 낱말 = Knuet_VALUE.id
                        if 낱말 and all(ord(Zeechen_VALUE)<128 for Zeechen_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': Knuet_VALUE.lineno})
                    Agab_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Feeler:
                    Agab_VALUE['parse_error'] = str(Feeler)
            LOG_Rei.append(Agab_VALUE)
    Mooss = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_Rei,
          'file_count': len(LOG_Rei), 'ascii_filename_count': sum(Agab_VALUE['ascii_filename'] for Agab_VALUE in LOG_Rei),
          'python_files_with_ascii_declarations': sum(bool(Agab_VALUE.get('ascii_python_declarations')) for Agab_VALUE in LOG_Rei),
          'all_repository_identifiers_korean': False,
          'note': '표준 Verbannen 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    Zil_VALUE = projezéieren_Racinn/'build/verification/naming'; Zil_VALUE.mkdir(parents=True, exist_ok=True)
    (Zil_VALUE/'source-review.json').write_text(json.dumps(Mooss, ensure_ascii=False, indent=2)+'\n')
    print('Quell', Mooss['file_count'], '개; ASCII Fichier_Numm_SMS', Mooss['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fichier', Mooss['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Laf()
