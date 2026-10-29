#!/usr/bin/env python3
"""depo_kök 전체의 Öz 원문을 목록화한다. dış_değer/oluşturmak 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

işlem_kök = Path(__file__).resolve().parents[1]
depo_kök = işlem_kök.parents[1]

def çalıştır():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_KAYIT = []
    for dizin_değer, 하위들, 파일들 in os.walk(str(depo_kök)):
        하위들[:] = sorted(İsim for İsim in 하위들 if İsim not in 제외)
        for İsim in sorted(파일들):
            yol = Path(dizin_değer)/İsim
            if yol.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            veri = yol.read_bytes()
            girdi_değer = {'path': str(yol.relative_to(depo_kök)), 'sha256': hashlib.sha256(veri).hexdigest(),
                  'ascii_filename': all(ord(karakter_değer)<128 for karakter_değer in yol.stem)}
            if yol.suffix == '.py':
                남은선언 = []
                try:
                    for düğüm_değer in ast.walk(ast.parse(veri.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(düğüm_değer, (ast.FunctionDef, ast.ClassDef)): 낱말 = düğüm_değer.name
                        elif isinstance(düğüm_değer, ast.arg): 낱말 = düğüm_değer.arg
                        elif isinstance(düğüm_değer, ast.Name) and isinstance(düğüm_değer.ctx, ast.Store): 낱말 = düğüm_değer.id
                        if 낱말 and all(ord(karakter_değer)<128 for karakter_değer in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': düğüm_değer.lineno})
                    girdi_değer['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as hata:
                    girdi_değer['parse_error'] = str(hata)
            LOG_KAYIT.append(girdi_değer)
    sonuç = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_KAYIT,
          'file_count': len(LOG_KAYIT), 'ascii_filename_count': sum(girdi_değer['ascii_filename'] for girdi_değer in LOG_KAYIT),
          'python_files_with_ascii_declarations': sum(bool(girdi_değer.get('ascii_python_declarations')) for girdi_değer in LOG_KAYIT),
          'all_repository_identifiers_korean': False,
          'note': '표준 Bağlan 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    hedef_değer = işlem_kök/'build/verification/naming'; hedef_değer.mkdir(parents=True, exist_ok=True)
    (hedef_değer/'source-review.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2)+'\n')
    print('kaynakKod', sonuç['file_count'], '개; ASCII dosya_adı_SMS', sonuç['ascii_filename_count'],
          '개; 영어 선언이 남은 Python dosya', sonuç['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': çalıştır()
