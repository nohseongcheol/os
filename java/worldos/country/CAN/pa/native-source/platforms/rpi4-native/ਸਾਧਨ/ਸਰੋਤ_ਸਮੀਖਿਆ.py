#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/ਜਨਰੇਟ_ਕਰੋ 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
저장소 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]

def ਚਲਾਓ_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ਲੌਗ_ਕਤਾਰ = []
    for ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ਨਾਂ for ਨਾਂ in 하위들 if ਨਾਂ not in 제외)
        for ਨਾਂ in sorted(파일들):
            ਮਾਰਗ = Path(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)/ਨਾਂ
            if ਮਾਰਗ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ਸਮੱਗਰੀ = ਮਾਰਗ.read_bytes()
            ਦਾਖਲਾ_ਕੀਮਤ = {'path': str(ਮਾਰਗ.relative_to(저장소)), 'sha256': hashlib.sha256(ਸਮੱਗਰੀ).hexdigest(),
                  'ascii_filename': all(ord(ਵਰਣ_ਕੀਮਤ)<128 for ਵਰਣ_ਕੀਮਤ in ਮਾਰਗ.stem)}
            if ਮਾਰਗ.suffix == '.py':
                남은선언 = []
                try:
                    for ਨੋਡ_ਕੀਮਤ in ast.walk(ast.parse(ਸਮੱਗਰੀ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ਨੋਡ_ਕੀਮਤ, (ast.FunctionDef, ast.ClassDef)): 낱말 = ਨੋਡ_ਕੀਮਤ.name
                        elif isinstance(ਨੋਡ_ਕੀਮਤ, ast.arg): 낱말 = ਨੋਡ_ਕੀਮਤ.arg
                        elif isinstance(ਨੋਡ_ਕੀਮਤ, ast.Name) and isinstance(ਨੋਡ_ਕੀਮਤ.ctx, ast.Store): 낱말 = ਨੋਡ_ਕੀਮਤ.id
                        if 낱말 and all(ord(ਵਰਣ_ਕੀਮਤ)<128 for ਵਰਣ_ਕੀਮਤ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ਨੋਡ_ਕੀਮਤ.lineno})
                    ਦਾਖਲਾ_ਕੀਮਤ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ਗਲਤੀ:
                    ਦਾਖਲਾ_ਕੀਮਤ['parse_error'] = str(ਗਲਤੀ)
            ਲੌਗ_ਕਤਾਰ.append(ਦਾਖਲਾ_ਕੀਮਤ)
    ਮਾਪ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ਲੌਗ_ਕਤਾਰ,
          'file_count': len(ਲੌਗ_ਕਤਾਰ), 'ascii_filename_count': sum(ਦਾਖਲਾ_ਕੀਮਤ['ascii_filename'] for ਦਾਖਲਾ_ਕੀਮਤ in ਲੌਗ_ਕਤਾਰ),
          'python_files_with_ascii_declarations': sum(bool(ਦਾਖਲਾ_ਕੀਮਤ.get('ascii_python_declarations')) for ਦਾਖਲਾ_ਕੀਮਤ in ਲੌਗ_ਕਤਾਰ),
          'all_repository_identifiers_korean': False,
          'note': '표준 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ਮੰਜਿਲ_ਕੀਮਤ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/naming'; ਮੰਜਿਲ_ਕੀਮਤ.mkdir(parents=True, exist_ok=True)
    (ਮੰਜਿਲ_ਕੀਮਤ/'source-review.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2)+'\n')
    print('ਸਰੋਤ', ਮਾਪ['file_count'], '개; ASCII ਲਿਖਤ_ਪੱਤਰ_ਨਾਮ_ਪਾਠ', ਮਾਪ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ਫਾਇਲ', ਮਾਪ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ਚਲਾਓ_2()
