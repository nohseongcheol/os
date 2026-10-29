#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/waihanga 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

whakaatu_pūtake = Path(__file__).resolve().parents[1]
저장소 = whakaatu_pūtake.parents[1]

def whakahaere():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for whaiaronga_uara, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Ingoa for Ingoa in 하위들 if Ingoa not in 제외)
        for Ingoa in sorted(파일들):
            ara = Path(whaiaronga_uara)/Ingoa
            if ara.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            raraunga = ara.read_bytes()
            tāurunga_uara = {'path': str(ara.relative_to(저장소)), 'sha256': hashlib.sha256(raraunga).hexdigest(),
                  'ascii_filename': all(ord(pūāhua_uara)<128 for pūāhua_uara in ara.stem)}
            if ara.suffix == '.py':
                남은선언 = []
                try:
                    for kōpuku_uara in ast.walk(ast.parse(raraunga.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(kōpuku_uara, (ast.FunctionDef, ast.ClassDef)): 낱말 = kōpuku_uara.name
                        elif isinstance(kōpuku_uara, ast.arg): 낱말 = kōpuku_uara.arg
                        elif isinstance(kōpuku_uara, ast.Name) and isinstance(kōpuku_uara.ctx, ast.Store): 낱말 = kōpuku_uara.id
                        if 낱말 and all(ord(pūāhua_uara)<128 for pūāhua_uara in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': kōpuku_uara.lineno})
                    tāurunga_uara['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Pōhēhē:
                    tāurunga_uara['parse_error'] = str(Pōhēhē)
            LOG_RECORD.append(tāurunga_uara)
    mēhua = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(tāurunga_uara['ascii_filename'] for tāurunga_uara in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(tāurunga_uara.get('ascii_python_declarations')) for tāurunga_uara in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 TŪHONO 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ūnga_uara = whakaatu_pūtake/'build/verification/naming'; ūnga_uara.mkdir(parents=True, exist_ok=True)
    (ūnga_uara/'source-review.json').write_text(json.dumps(mēhua, ensure_ascii=False, indent=2)+'\n')
    print('pūtake', mēhua['file_count'], '개; ASCII kōnae_ingoa_TEXT', mēhua['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Kōnae', mēhua['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': whakahaere()
