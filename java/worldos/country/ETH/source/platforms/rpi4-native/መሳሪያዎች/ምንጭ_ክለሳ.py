#!/usr/bin/env python3
"""ማከማቻ_ስር 전체의 자체 원문을 목록화한다. 외부/አዘጋጅ 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

አሳይ_ስር = Path(__file__).resolve().parents[1]
ማከማቻ_ስር = አሳይ_ስር.parents[1]

def ማስኬጃ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    መዝግብ_ረድፍ = []
    for ማውጫ_እሴት, 하위들, 파일들 in os.walk(str(ማከማቻ_ስር)):
        하위들[:] = sorted(ስም for ስም in 하위들 if ስም not in 제외)
        for ስም in sorted(파일들):
            መተላለፊያ = Path(ማውጫ_እሴት)/ስም
            if መተላለፊያ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ውሂብ = መተላለፊያ.read_bytes()
            ምዝግብ_እሴት = {'path': str(መተላለፊያ.relative_to(ማከማቻ_ስር)), 'sha256': hashlib.sha256(ውሂብ).hexdigest(),
                  'ascii_filename': all(ord(ቁምፊ_እሴት)<128 for ቁምፊ_እሴት in መተላለፊያ.stem)}
            if መተላለፊያ.suffix == '.py':
                남은선언 = []
                try:
                    for ዓፅቅ_እሴት in ast.walk(ast.parse(ውሂብ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ዓፅቅ_እሴት, (ast.FunctionDef, ast.ClassDef)): 낱말 = ዓፅቅ_እሴት.name
                        elif isinstance(ዓፅቅ_እሴት, ast.arg): 낱말 = ዓፅቅ_እሴት.arg
                        elif isinstance(ዓፅቅ_እሴት, ast.Name) and isinstance(ዓፅቅ_እሴት.ctx, ast.Store): 낱말 = ዓፅቅ_እሴት.id
                        if 낱말 and all(ord(ቁምፊ_እሴት)<128 for ቁምፊ_እሴት in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ዓፅቅ_እሴት.lineno})
                    ምዝግብ_እሴት['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ስህተት:
                    ምዝግብ_እሴት['parse_error'] = str(ስህተት)
            መዝግብ_ረድፍ.append(ምዝግብ_እሴት)
    ልኬት = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': መዝግብ_ረድፍ,
          'file_count': len(መዝግብ_ረድፍ), 'ascii_filename_count': sum(ምዝግብ_እሴት['ascii_filename'] for ምዝግብ_እሴት in መዝግብ_ረድፍ),
          'python_files_with_ascii_declarations': sum(bool(ምዝግብ_እሴት.get('ascii_python_declarations')) for ምዝግብ_እሴት in መዝግብ_ረድፍ),
          'all_repository_identifiers_korean': False,
          'note': '표준 መገናኛ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    መድረሻ_እሴት = አሳይ_ስር/'build/verification/naming'; መድረሻ_እሴት.mkdir(parents=True, exist_ok=True)
    (መድረሻ_እሴት/'source-review.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2)+'\n')
    print('ምንጭ', ልኬት['file_count'], '개; ASCII ፋይል_ስም_ጽሁፍ', ልኬት['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ፋይል', ልኬት['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ማስኬጃ()
