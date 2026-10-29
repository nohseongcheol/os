#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Bitir():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    hasaba_alyş_setir = []
    for katalog_baha, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Ad for Ad in 하위들 if Ad not in 제외)
        for Ad in sorted(파일들):
            Ýol = Path(katalog_baha)/Ad
            if Ýol.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            maglumat = Ýol.read_bytes()
            girizmeklik_baha = {'path': str(Ýol.relative_to(저장소)), 'sha256': hashlib.sha256(maglumat).hexdigest(),
                  'ascii_filename': all(ord(nyşan_baha_068c2631)<128 for nyşan_baha_068c2631 in Ýol.stem)}
            if Ýol.suffix == '.py':
                남은선언 = []
                try:
                    for düwün_baha in ast.walk(ast.parse(maglumat.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(düwün_baha, (ast.FunctionDef, ast.ClassDef)): 낱말 = düwün_baha.name
                        elif isinstance(düwün_baha, ast.arg): 낱말 = düwün_baha.arg
                        elif isinstance(düwün_baha, ast.Name) and isinstance(düwün_baha.ctx, ast.Store): 낱말 = düwün_baha.id
                        if 낱말 and all(ord(nyşan_baha_068c2631)<128 for nyşan_baha_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': düwün_baha.lineno})
                    girizmeklik_baha['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Hata:
                    girizmeklik_baha['parse_error'] = str(Hata)
            hasaba_alyş_setir.append(girizmeklik_baha)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': hasaba_alyş_setir,
          'file_count': len(hasaba_alyş_setir), 'ascii_filename_count': sum(girizmeklik_baha['ascii_filename'] for girizmeklik_baha in hasaba_alyş_setir),
          'python_files_with_ascii_declarations': sum(bool(girizmeklik_baha.get('ascii_python_declarations')) for girizmeklik_baha in hasaba_alyş_setir),
          'all_repository_identifiers_korean': False,
          'note': '표준 Birikme 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    barylmaly_ýer_baha = 기준/'build/verification/naming'; barylmaly_ýer_baha.mkdir(parents=True, exist_ok=True)
    (barylmaly_ýer_baha/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('Çeşme', 결과['file_count'], '개; ASCII faýl_at_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Faýl', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Bitir()
