#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Tafiyar_da():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    logu_naɗa = []
    for ma_ajiya_Daraja, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Suna for Suna in 하위들 if Suna not in 제외)
        for Suna in sorted(파일들):
            Hanyar_shiga = Path(ma_ajiya_Daraja)/Suna
            if Hanyar_shiga.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            Tarin_bayani = Hanyar_shiga.read_bytes()
            Mashigar_bayanai_Daraja = {'path': str(Hanyar_shiga.relative_to(저장소)), 'sha256': hashlib.sha256(Tarin_bayani).hexdigest(),
                  'ascii_filename': all(ord(Harafi_Daraja)<128 for Harafi_Daraja in Hanyar_shiga.stem)}
            if Hanyar_shiga.suffix == '.py':
                남은선언 = []
                try:
                    for Gwafa_Daraja in ast.walk(ast.parse(Tarin_bayani.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(Gwafa_Daraja, (ast.FunctionDef, ast.ClassDef)): 낱말 = Gwafa_Daraja.name
                        elif isinstance(Gwafa_Daraja, ast.arg): 낱말 = Gwafa_Daraja.arg
                        elif isinstance(Gwafa_Daraja, ast.Name) and isinstance(Gwafa_Daraja.ctx, ast.Store): 낱말 = Gwafa_Daraja.id
                        if 낱말 and all(ord(Harafi_Daraja)<128 for Harafi_Daraja in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': Gwafa_Daraja.lineno})
                    Mashigar_bayanai_Daraja['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Kuskure:
                    Mashigar_bayanai_Daraja['parse_error'] = str(Kuskure)
            logu_naɗa.append(Mashigar_bayanai_Daraja)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': logu_naɗa,
          'file_count': len(logu_naɗa), 'ascii_filename_count': sum(Mashigar_bayanai_Daraja['ascii_filename'] for Mashigar_bayanai_Daraja in logu_naɗa),
          'python_files_with_ascii_declarations': sum(bool(Mashigar_bayanai_Daraja.get('ascii_python_declarations')) for Mashigar_bayanai_Daraja in logu_naɗa),
          'all_repository_identifiers_korean': False,
          'note': '표준 Haɗi 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    Zangon_ƙarshe_Daraja = 기준/'build/verification/naming'; Zangon_ƙarshe_Daraja.mkdir(parents=True, exist_ok=True)
    (Zangon_ƙarshe_Daraja/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('tushe', 결과['file_count'], '개; ASCII Fayil_Suna_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fayil', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Tafiyar_da()
