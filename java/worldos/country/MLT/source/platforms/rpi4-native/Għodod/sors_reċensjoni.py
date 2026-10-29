#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/iġġenera 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

pprojetta_għerq = Path(__file__).resolve().parents[1]
저장소 = pprojetta_għerq.parents[1]

def serje():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_RECORD = []
    for direttorju_VALUE, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(isem for isem in 하위들 if isem not in 제외)
        for isem in sorted(파일들):
            mogħdija = Path(direttorju_VALUE)/isem
            if mogħdija.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = mogħdija.read_bytes()
            entrata_VALUE = {'path': str(mogħdija.relative_to(저장소)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(karattru_VALUE)<128 for karattru_VALUE in mogħdija.stem)}
            if mogħdija.suffix == '.py':
                남은선언 = []
                try:
                    for node_VALUE in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VALUE, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VALUE.name
                        elif isinstance(node_VALUE, ast.arg): 낱말 = node_VALUE.arg
                        elif isinstance(node_VALUE, ast.Name) and isinstance(node_VALUE.ctx, ast.Store): 낱말 = node_VALUE.id
                        if 낱말 and all(ord(karattru_VALUE)<128 for karattru_VALUE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VALUE.lineno})
                    entrata_VALUE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as żball:
                    entrata_VALUE['parse_error'] = str(żball)
            LOG_RECORD.append(entrata_VALUE)
    miżura = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_RECORD,
          'file_count': len(LOG_RECORD), 'ascii_filename_count': sum(entrata_VALUE['ascii_filename'] for entrata_VALUE in LOG_RECORD),
          'python_files_with_ascii_declarations': sum(bool(entrata_VALUE.get('ascii_python_declarations')) for entrata_VALUE in LOG_RECORD),
          'all_repository_identifiers_korean': False,
          'note': '표준 AQBAD 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destinazzjoni_VALUE = pprojetta_għerq/'build/verification/naming'; destinazzjoni_VALUE.mkdir(parents=True, exist_ok=True)
    (destinazzjoni_VALUE/'source-review.json').write_text(json.dumps(miżura, ensure_ascii=False, indent=2)+'\n')
    print('sors', miżura['file_count'], '개; ASCII fajl_isem_SMS', miżura['ascii_filename_count'],
          '개; 영어 선언이 남은 Python fajl', miżura['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': serje()
