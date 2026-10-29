#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def endesha():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    batli_REKODI = []
    for Saraka_thamani, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Jina for Jina in 하위들 if Jina not in 제외)
        for Jina in sorted(파일들):
            njia = Path(Saraka_thamani)/Jina
            if njia.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = njia.read_bytes()
            ingizo_thamani = {'path': str(njia.relative_to(저장소)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(kibambo_thamani)<128 for kibambo_thamani in njia.stem)}
            if njia.suffix == '.py':
                남은선언 = []
                try:
                    for fundo_thamani in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(fundo_thamani, (ast.FunctionDef, ast.ClassDef)): 낱말 = fundo_thamani.name
                        elif isinstance(fundo_thamani, ast.arg): 낱말 = fundo_thamani.arg
                        elif isinstance(fundo_thamani, ast.Name) and isinstance(fundo_thamani.ctx, ast.Store): 낱말 = fundo_thamani.id
                        if 낱말 and all(ord(kibambo_thamani)<128 for kibambo_thamani in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': fundo_thamani.lineno})
                    ingizo_thamani['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as kosa:
                    ingizo_thamani['parse_error'] = str(kosa)
            batli_REKODI.append(ingizo_thamani)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': batli_REKODI,
          'file_count': len(batli_REKODI), 'ascii_filename_count': sum(ingizo_thamani['ascii_filename'] for ingizo_thamani in batli_REKODI),
          'python_files_with_ascii_declarations': sum(bool(ingizo_thamani.get('ascii_python_declarations')) for ingizo_thamani in batli_REKODI),
          'all_repository_identifiers_korean': False,
          'note': '표준 UNGANISHA 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    fikio_thamani = 기준/'build/verification/naming'; fikio_thamani.mkdir(parents=True, exist_ok=True)
    (fikio_thamani/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('chanzo', 결과['file_count'], '개; ASCII faili_jina_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python faili', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': endesha()
