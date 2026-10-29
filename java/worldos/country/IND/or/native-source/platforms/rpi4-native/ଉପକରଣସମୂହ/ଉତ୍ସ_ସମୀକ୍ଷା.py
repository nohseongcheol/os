#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/ସୃଷ୍ଟି_କରିବା 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
저장소 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]

def ଚଳାନ୍ତୁ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ଲଗ୍_ଧାଡ଼ି = []
    for ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ନାମ for ନାମ in 하위들 if ନାମ not in 제외)
        for ନାମ in sorted(파일들):
            ପଥ = Path(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)/ନାମ
            if ପଥ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ଡାଟା = ପଥ.read_bytes()
            ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = {'path': str(ପଥ.relative_to(저장소)), 'sha256': hashlib.sha256(ଡାଟା).hexdigest(),
                  'ascii_filename': all(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)<128 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ପଥ.stem)}
            if ପଥ.suffix == '.py':
                남은선언 = []
                try:
                    for ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ in ast.walk(ast.parse(ଡାଟା.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ, (ast.FunctionDef, ast.ClassDef)): 낱말 = ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ.name
                        elif isinstance(ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ, ast.arg): 낱말 = ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ.arg
                        elif isinstance(ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ, ast.Name) and isinstance(ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ.ctx, ast.Store): 낱말 = ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ.id
                        if 낱말 and all(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)<128 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ସଂଯୋଗ_ବିନ୍ଦୁ_ମୂଲ୍ୟ.lineno})
                    ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ତ୍ରୁଟି:
                    ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['parse_error'] = str(ତ୍ରୁଟି)
            ଲଗ୍_ଧାଡ଼ି.append(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)
    ମାପ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ଲଗ୍_ଧାଡ଼ି,
          'file_count': len(ଲଗ୍_ଧାଡ଼ି), 'ascii_filename_count': sum(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['ascii_filename'] for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ଲଗ୍_ଧାଡ଼ି),
          'python_files_with_ascii_declarations': sum(bool(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.get('ascii_python_declarations')) for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ଲଗ୍_ଧାଡ଼ି),
          'all_repository_identifiers_korean': False,
          'note': '표준 ସଂଯୋଗ_କରନ୍ତୁ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/naming'; ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.mkdir(parents=True, exist_ok=True)
    (ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'source-review.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2)+'\n')
    print('ଉତ୍ସ', ମାପ['file_count'], '개; ASCII ଫାଇଲ୍_ନାମ_ପାଠ', ମାପ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ଫାଇଲ', ମାପ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ଚଳାନ୍ତୁ()
