#!/usr/bin/env python3
"""repozitoriy_ildiz 전체의 자체 원문을 목록화한다. 외부/generatsiiyalash 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_ildiz = Path(__file__).resolve().parents[1]
repozitoriy_ildiz = Project_ildiz.parents[1]

def Bajarish():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_satr = []
    for katalog_VALUE, 하위들, 파일들 in os.walk(str(repozitoriy_ildiz)):
        하위들[:] = sorted(Nomi for Nomi in 하위들 if Nomi not in 제외)
        for Nomi in sorted(파일들):
            yo_l = Path(katalog_VALUE)/Nomi
            if yo_l.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ma_lumotlar = yo_l.read_bytes()
            kiritish_VALUE = {'path': str(yo_l.relative_to(repozitoriy_ildiz)), 'sha256': hashlib.sha256(ma_lumotlar).hexdigest(),
                  'ascii_filename': all(ord(belgi_VALUE)<128 for belgi_VALUE in yo_l.stem)}
            if yo_l.suffix == '.py':
                남은선언 = []
                try:
                    for bog_lama_VALUE in ast.walk(ast.parse(ma_lumotlar.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(bog_lama_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = bog_lama_VALUE.name
                        elif isinstance(bog_lama_VALUE, ast.arg): 낱말 = bog_lama_VALUE.arg
                        elif isinstance(bog_lama_VALUE, ast.Name) and isinstance(bog_lama_VALUE.ctx, ast.Store): 낱말 = bog_lama_VALUE.id
                        if 낱말 and all(ord(belgi_VALUE)<128 for belgi_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': bog_lama_VALUE.lineno})
                    kiritish_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Xato:
                    kiritish_VALUE['parse_error'] = str(Xato)
            LOG_satr.append(kiritish_VALUE)
    o_lchov = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_satr,
          'file_count': len(LOG_satr), 'ascii_filename_count': sum(kiritish_VALUE['ascii_filename'] for kiritish_VALUE in LOG_satr),
          'python_files_with_ascii_declarations': sum(bool(kiritish_VALUE.get('ascii_python_declarations')) for kiritish_VALUE in LOG_satr),
          'all_repository_identifiers_korean': False,
          'note': '표준 Ulanish 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ko_chirish_joyi_VALUE = Project_ildiz/'build/verification/naming'; ko_chirish_joyi_VALUE.mkdir(parents=True, exist_ok=True)
    (ko_chirish_joyi_VALUE/'source-review.json').write_text(json.dumps(o_lchov, ensure_ascii=False, indent=2)+'\n')
    print('manba', o_lchov['file_count'], '개; ASCII fayl_nom_SMS', o_lchov['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fayl', o_lchov['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Bajarish()
