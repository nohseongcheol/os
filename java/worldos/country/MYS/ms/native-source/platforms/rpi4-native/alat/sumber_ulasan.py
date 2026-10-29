#!/usr/bin/env python3
"""repositori_akar 전체의 Asli 원문을 목록화한다. 외부/jana 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

projek_akar = Path(__file__).resolve().parents[1]
repositori_akar = projek_akar.parents[1]

def Jalan():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_baris = []
    for direktori_VALUE, 하위들, 파일들 in os.walk(str(repositori_akar)):
        하위들[:] = sorted(Nama for Nama in 하위들 if Nama not in 제외)
        for Nama in sorted(파일들):
            LALUAN = Path(direktori_VALUE)/Nama
            if LALUAN.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = LALUAN.read_bytes()
            pemasukan_VALUE = {'path': str(LALUAN.relative_to(repositori_akar)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(aksara_VALUE)<128 for aksara_VALUE in LALUAN.stem)}
            if LALUAN.suffix == '.py':
                남은선언 = []
                try:
                    for nod_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nod_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nod_VALUE.name
                        elif isinstance(nod_VALUE, ast.arg): 낱말 = nod_VALUE.arg
                        elif isinstance(nod_VALUE, ast.Name) and isinstance(nod_VALUE.ctx, ast.Store): 낱말 = nod_VALUE.id
                        if 낱말 and all(ord(aksara_VALUE)<128 for aksara_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nod_VALUE.lineno})
                    pemasukan_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as RALAT:
                    pemasukan_VALUE['parse_error'] = str(RALAT)
            LOG_baris.append(pemasukan_VALUE)
    ukuran = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_baris,
          'file_count': len(LOG_baris), 'ascii_filename_count': sum(pemasukan_VALUE['ascii_filename'] for pemasukan_VALUE in LOG_baris),
          'python_files_with_ascii_declarations': sum(bool(pemasukan_VALUE.get('ascii_python_declarations')) for pemasukan_VALUE in LOG_baris),
          'all_repository_identifiers_korean': False,
          'note': '표준 Sambung 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destinasi_VALUE = projek_akar/'build/verification/naming'; destinasi_VALUE.mkdir(parents=True, exist_ok=True)
    (destinasi_VALUE/'source-review.json').write_text(json.dumps(ukuran, ensure_ascii=False, indent=2)+'\n')
    print('SUMBER', ukuran['file_count'], '개; ASCII nama_fail_SMS', ukuran['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fail', ukuran['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Jalan()
