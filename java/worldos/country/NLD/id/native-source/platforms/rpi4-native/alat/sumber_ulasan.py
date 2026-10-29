#!/usr/bin/env python3
"""repositori_akar 전체의 Asli 원문을 목록화한다. eksternal_VALUE/buat 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Tugas_akar = Path(__file__).resolve().parents[1]
repositori_akar = Tugas_akar.parents[1]

def jalankan():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_baris = []
    for Direktori_VALUE, 하위들, 파일들 in os.walk(str(repositori_akar)):
        하위들[:] = sorted(Nama_2 for Nama_2 in 하위들 if Nama_2 not in 제외)
        for Nama_2 in sorted(파일들):
            jalur = Path(Direktori_VALUE)/Nama_2
            if jalur.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = jalur.read_bytes()
            entri_VALUE = {'path': str(jalur.relative_to(repositori_akar)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(karakter_VALUE)<128 for karakter_VALUE in jalur.stem)}
            if jalur.suffix == '.py':
                남은선언 = []
                try:
                    for node_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VALUE.name
                        elif isinstance(node_VALUE, ast.arg): 낱말 = node_VALUE.arg
                        elif isinstance(node_VALUE, ast.Name) and isinstance(node_VALUE.ctx, ast.Store): 낱말 = node_VALUE.id
                        if 낱말 and all(ord(karakter_VALUE)<128 for karakter_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VALUE.lineno})
                    entri_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as galat:
                    entri_VALUE['parse_error'] = str(galat)
            LOG_baris.append(entri_VALUE)
    hasil = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_baris,
          'file_count': len(LOG_baris), 'ascii_filename_count': sum(entri_VALUE['ascii_filename'] for entri_VALUE in LOG_baris),
          'python_files_with_ascii_declarations': sum(bool(entri_VALUE.get('ascii_python_declarations')) for entri_VALUE in LOG_baris),
          'all_repository_identifiers_korean': False,
          'note': '표준 Sambung 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    tujuan_VALUE = Tugas_akar/'build/verification/naming'; tujuan_VALUE.mkdir(parents=True, exist_ok=True)
    (tujuan_VALUE/'source-review.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2)+'\n')
    print('kodeSumber', hasil['file_count'], '개; ASCII nama_file_SMS', hasil['ascii_filename_count'],
          '개; 영어 선언이 남은 Python berkas', hasil['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': jalankan()
