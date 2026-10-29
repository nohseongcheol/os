#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ኣኺድ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ምዝጉብ_ሪጋ = []
    for ሓባሪ_ማህደር_ዋጋ, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ሽም for ሽም in 하위들 if ሽም not in 제외)
        for ሽም in sorted(파일들):
            መገዲ = Path(ሓባሪ_ማህደር_ዋጋ)/ሽም
            if መገዲ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ሓበሬታ = መገዲ.read_bytes()
            ምእታው_ዋጋ = {'path': str(መገዲ.relative_to(저장소)), 'sha256': hashlib.sha256(ሓበሬታ).hexdigest(),
                  'ascii_filename': all(ord(ፊደል_ዋጋ)<128 for ፊደል_ዋጋ in መገዲ.stem)}
            if መገዲ.suffix == '.py':
                남은선언 = []
                try:
                    for ጨንፈር_ዋጋ_2fb0eaf6 in ast.walk(ast.parse(ሓበሬታ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ጨንፈር_ዋጋ_2fb0eaf6, (ast.FunctionDef, ast.ClassDef)): 낱말 = ጨንፈር_ዋጋ_2fb0eaf6.name
                        elif isinstance(ጨንፈር_ዋጋ_2fb0eaf6, ast.arg): 낱말 = ጨንፈር_ዋጋ_2fb0eaf6.arg
                        elif isinstance(ጨንፈር_ዋጋ_2fb0eaf6, ast.Name) and isinstance(ጨንፈር_ዋጋ_2fb0eaf6.ctx, ast.Store): 낱말 = ጨንፈር_ዋጋ_2fb0eaf6.id
                        if 낱말 and all(ord(ፊደል_ዋጋ)<128 for ፊደል_ዋጋ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ጨንፈር_ዋጋ_2fb0eaf6.lineno})
                    ምእታው_ዋጋ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ጌጋ:
                    ምእታው_ዋጋ['parse_error'] = str(ጌጋ)
            ምዝጉብ_ሪጋ.append(ምእታው_ዋጋ)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ምዝጉብ_ሪጋ,
          'file_count': len(ምዝጉብ_ሪጋ), 'ascii_filename_count': sum(ምእታው_ዋጋ['ascii_filename'] for ምእታው_ዋጋ in ምዝጉብ_ሪጋ),
          'python_files_with_ascii_declarations': sum(bool(ምእታው_ዋጋ.get('ascii_python_declarations')) for ምእታው_ዋጋ in ምዝጉብ_ሪጋ),
          'all_repository_identifiers_korean': False,
          'note': '표준 ኣላግብ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    መዓልቦ_ዋጋ = 기준/'build/verification/naming'; መዓልቦ_ዋጋ.mkdir(parents=True, exist_ok=True)
    (መዓልቦ_ዋጋ/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ምንጪ', 결과['file_count'], '개; ASCII ፋይል_ሽም_ጽሑፍ', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ፋይል', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ኣኺድ()
