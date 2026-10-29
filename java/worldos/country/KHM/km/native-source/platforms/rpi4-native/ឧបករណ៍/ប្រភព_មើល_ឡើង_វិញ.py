#!/usr/bin/env python3
"""ឃ្លាំង_ផ្ទុក_ឬស 전체의 자체 원문을 목록화한다. 외부/បង្កើត 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
ឃ្លាំង_ផ្ទុក_ឬស = បញ្ចាំង_ឬស.parents[1]

def រត់():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    កំណត់_ហេតុ_ថត = []
    for បញ្ជី_តំលៃ, 하위들, 파일들 in os.walk(str(ឃ្លាំង_ផ្ទុក_ឬស)):
        하위들[:] = sorted(ឈ្មោះ for ឈ្មោះ in 하위들 if ឈ្មោះ not in 제외)
        for ឈ្មោះ in sorted(파일들):
            ផ្លូវ = Path(បញ្ជី_តំលៃ)/ឈ្មោះ
            if ផ្លូវ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ទិន្នន័យ = ផ្លូវ.read_bytes()
            ការបញ្ចូល_តំលៃ = {'path': str(ផ្លូវ.relative_to(ឃ្លាំង_ផ្ទុក_ឬស)), 'sha256': hashlib.sha256(ទិន្នន័យ).hexdigest(),
                  'ascii_filename': all(ord(តួអក្សរ_តំលៃ)<128 for តួអក្សរ_តំលៃ in ផ្លូវ.stem)}
            if ផ្លូវ.suffix == '.py':
                남은선언 = []
                try:
                    for ណូត_តំលៃ in ast.walk(ast.parse(ទិន្នន័យ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ណូត_តំលៃ, (ast.FunctionDef, ast.ClassDef)): 낱말 = ណូត_តំលៃ.name
                        elif isinstance(ណូត_តំលៃ, ast.arg): 낱말 = ណូត_តំលៃ.arg
                        elif isinstance(ណូត_តំលៃ, ast.Name) and isinstance(ណូត_តំលៃ.ctx, ast.Store): 낱말 = ណូត_តំលៃ.id
                        if 낱말 and all(ord(តួអក្សរ_តំលៃ)<128 for តួអក្សរ_តំលៃ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ណូត_តំលៃ.lineno})
                    ការបញ្ចូល_តំលៃ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as កំហុស:
                    ការបញ្ចូល_តំលៃ['parse_error'] = str(កំហុស)
            កំណត់_ហេតុ_ថត.append(ការបញ្ចូល_តំលៃ)
    ការវាស់វែង = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': កំណត់_ហេតុ_ថត,
          'file_count': len(កំណត់_ហេតុ_ថត), 'ascii_filename_count': sum(ការបញ្ចូល_តំលៃ['ascii_filename'] for ការបញ្ចូល_តំលៃ in កំណត់_ហេតុ_ថត),
          'python_files_with_ascii_declarations': sum(bool(ការបញ្ចូល_តំលៃ.get('ascii_python_declarations')) for ការបញ្ចូល_តំលៃ in កំណត់_ហេតុ_ថត),
          'all_repository_identifiers_korean': False,
          'note': '표준 ភ្ជាប់ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ទិសដៅ_តំលៃ = បញ្ចាំង_ឬស/'build/verification/naming'; ទិសដៅ_តំលៃ.mkdir(parents=True, exist_ok=True)
    (ទិសដៅ_តំលៃ/'source-review.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2)+'\n')
    print('ប្រភព', ការវាស់វែង['file_count'], '개; ASCII ឯកសារ_ឈ្មោះ_អត្ថបទ', ការវាស់វែង['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ឯកសារ', ការវាស់វែង['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': រត់()
