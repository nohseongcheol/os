#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def порча():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    сабт_кардан_сабт = []
    for директория_қимат, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Ном for Ном in 하위들 if Ном not in 제외)
        for Ном in sorted(파일들):
            масир = Path(директория_қимат)/Ном
            if масир.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            иттилоот = масир.read_bytes()
            ворида_қимат = {'path': str(масир.relative_to(저장소)), 'sha256': hashlib.sha256(иттилоот).hexdigest(),
                  'ascii_filename': all(ord(аломат_қимат_068c2631)<128 for аломат_қимат_068c2631 in масир.stem)}
            if масир.suffix == '.py':
                남은선언 = []
                try:
                    for гиреҳ_қимат in ast.walk(ast.parse(иттилоот.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(гиреҳ_қимат, (ast.FunctionDef, ast.ClassDef)): 낱말 = гиреҳ_қимат.name
                        elif isinstance(гиреҳ_қимат, ast.arg): 낱말 = гиреҳ_қимат.arg
                        elif isinstance(гиреҳ_қимат, ast.Name) and isinstance(гиреҳ_қимат.ctx, ast.Store): 낱말 = гиреҳ_қимат.id
                        if 낱말 and all(ord(аломат_қимат_068c2631)<128 for аломат_қимат_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': гиреҳ_қимат.lineno})
                    ворида_қимат['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Хато:
                    ворида_қимат['parse_error'] = str(Хато)
            сабт_кардан_сабт.append(ворида_қимат)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': сабт_кардан_сабт,
          'file_count': len(сабт_кардан_сабт), 'ascii_filename_count': sum(ворида_қимат['ascii_filename'] for ворида_қимат in сабт_кардан_сабт),
          'python_files_with_ascii_declarations': sum(bool(ворида_қимат.get('ascii_python_declarations')) for ворида_қимат in сабт_кардан_сабт),
          'all_repository_identifiers_korean': False,
          'note': '표준 ПАЙВАСТ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ҷои_таъинот_қимат = 기준/'build/verification/naming'; ҷои_таъинот_қимат.mkdir(parents=True, exist_ok=True)
    (ҷои_таъинот_қимат/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('манбаъ', 결과['file_count'], '개; ASCII файл_ном_Матн', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Файл', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': порча()
