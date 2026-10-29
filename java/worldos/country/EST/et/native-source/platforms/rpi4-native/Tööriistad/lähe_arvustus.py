#!/usr/bin/env python3
"""hoidla_juur 전체의 oma 원문을 목록화한다. väline_VALUE/genereerima 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_juur = Path(__file__).resolve().parents[1]
hoidla_juur = Project_juur.parents[1]

def Käivita_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_kirje = []
    for kaust_VALUE, 하위들, 파일들 in os.walk(str(hoidla_juur)):
        하위들[:] = sorted(Nimi_2 for Nimi_2 in 하위들 if Nimi_2 not in 제외)
        for Nimi_2 in sorted(파일들):
            RADA = Path(kaust_VALUE)/Nimi_2
            if RADA.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            andmed = RADA.read_bytes()
            kirje_VALUE = {'path': str(RADA.relative_to(hoidla_juur)), 'sha256': hashlib.sha256(andmed).hexdigest(),
                  'ascii_filename': all(ord(märk_VALUE)<128 for märk_VALUE in RADA.stem)}
            if RADA.suffix == '.py':
                남은선언 = []
                try:
                    for sõlm_VALUE in ast.walk(ast.parse(andmed.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(sõlm_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = sõlm_VALUE.name
                        elif isinstance(sõlm_VALUE, ast.arg): 낱말 = sõlm_VALUE.arg
                        elif isinstance(sõlm_VALUE, ast.Name) and isinstance(sõlm_VALUE.ctx, ast.Store): 낱말 = sõlm_VALUE.id
                        if 낱말 and all(ord(märk_VALUE)<128 for märk_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': sõlm_VALUE.lineno})
                    kirje_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as VIGA:
                    kirje_VALUE['parse_error'] = str(VIGA)
            LOG_kirje.append(kirje_VALUE)
    TULEMUS = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_kirje,
          'file_count': len(LOG_kirje), 'ascii_filename_count': sum(kirje_VALUE['ascii_filename'] for kirje_VALUE in LOG_kirje),
          'python_files_with_ascii_declarations': sum(bool(kirje_VALUE.get('ascii_python_declarations')) for kirje_VALUE in LOG_kirje),
          'all_repository_identifiers_korean': False,
          'note': '표준 Ühendu 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    sihtkoht_VALUE = Project_juur/'build/verification/naming'; sihtkoht_VALUE.mkdir(parents=True, exist_ok=True)
    (sihtkoht_VALUE/'source-review.json').write_text(json.dumps(TULEMUS, ensure_ascii=False, indent=2)+'\n')
    print('ALLIKAS', TULEMUS['file_count'], '개; ASCII failinimi_SMS', TULEMUS['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fail', TULEMUS['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Käivita_2()
