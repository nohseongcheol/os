#!/usr/bin/env python3
"""ಸಂಗ್ರಹಣೆ_ಮೂಲ 전체의 자체 원문을 목록화한다. 외부/ರಚಿಸಿ 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
ಸಂಗ್ರಹಣೆ_ಮೂಲ = ಬಿಂಬಿಸು_ಮೂಲ.parents[1]

def ಚಲಾಯಿಸು_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ಲಾಗ್_ದಾಖಲೆ = []
    for ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ, 하위들, 파일들 in os.walk(str(ಸಂಗ್ರಹಣೆ_ಮೂಲ)):
        하위들[:] = sorted(ಹೆಸರು for ಹೆಸರು in 하위들 if ಹೆಸರು not in 제외)
        for ಹೆಸರು in sorted(파일들):
            ಮಾರ್ಗ = Path(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)/ಹೆಸರು
            if ಮಾರ್ಗ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ಡೇಟಾ = ಮಾರ್ಗ.read_bytes()
            ನಮೂದು_ಮೌಲ್ಯ = {'path': str(ಮಾರ್ಗ.relative_to(ಸಂಗ್ರಹಣೆ_ಮೂಲ)), 'sha256': hashlib.sha256(ಡೇಟಾ).hexdigest(),
                  'ascii_filename': all(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)<128 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಮಾರ್ಗ.stem)}
            if ಮಾರ್ಗ.suffix == '.py':
                남은선언 = []
                try:
                    for ನೋಡ್_ಮೌಲ್ಯ in ast.walk(ast.parse(ಡೇಟಾ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ನೋಡ್_ಮೌಲ್ಯ, (ast.FunctionDef, ast.ClassDef)): 낱말 = ನೋಡ್_ಮೌಲ್ಯ.name
                        elif isinstance(ನೋಡ್_ಮೌಲ್ಯ, ast.arg): 낱말 = ನೋಡ್_ಮೌಲ್ಯ.arg
                        elif isinstance(ನೋಡ್_ಮೌಲ್ಯ, ast.Name) and isinstance(ನೋಡ್_ಮೌಲ್ಯ.ctx, ast.Store): 낱말 = ನೋಡ್_ಮೌಲ್ಯ.id
                        if 낱말 and all(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)<128 for ಅಕ್ಷರ_ಮೌಲ್ಯ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ನೋಡ್_ಮೌಲ್ಯ.lineno})
                    ನಮೂದು_ಮೌಲ್ಯ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ದೋಷ:
                    ನಮೂದು_ಮೌಲ್ಯ['parse_error'] = str(ದೋಷ)
            ಲಾಗ್_ದಾಖಲೆ.append(ನಮೂದು_ಮೌಲ್ಯ)
    ಮಾಪನ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ಲಾಗ್_ದಾಖಲೆ,
          'file_count': len(ಲಾಗ್_ದಾಖಲೆ), 'ascii_filename_count': sum(ನಮೂದು_ಮೌಲ್ಯ['ascii_filename'] for ನಮೂದು_ಮೌಲ್ಯ in ಲಾಗ್_ದಾಖಲೆ),
          'python_files_with_ascii_declarations': sum(bool(ನಮೂದು_ಮೌಲ್ಯ.get('ascii_python_declarations')) for ನಮೂದು_ಮೌಲ್ಯ in ಲಾಗ್_ದಾಖಲೆ),
          'all_repository_identifiers_korean': False,
          'note': '표준 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/naming'; ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.mkdir(parents=True, exist_ok=True)
    (ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'source-review.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2)+'\n')
    print('ಮೂಲ', ಮಾಪನ['file_count'], '개; ASCII ಫೈಲ್_ಹೆಸರು_ಪಠ್ಯ', ಮಾಪನ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ಕಡತ', ಮಾಪನ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ಚಲಾಯಿಸು_2()
