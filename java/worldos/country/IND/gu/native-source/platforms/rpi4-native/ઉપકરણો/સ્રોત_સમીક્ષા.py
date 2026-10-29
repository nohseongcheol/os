#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/જનરેટ_કરો 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
저장소 = પ્રોજેક્ટ_રૂટ.parents[1]

def ચલાવો_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    લૉગ_પંક્તિ = []
    for નિર્દેશિકા_મૂલ્ય, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(નામ for નામ in 하위들 if નામ not in 제외)
        for નામ in sorted(파일들):
            પથ = Path(નિર્દેશિકા_મૂલ્ય)/નામ
            if પથ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ડેટા = પથ.read_bytes()
            પ્રવેશ_મૂલ્ય = {'path': str(પથ.relative_to(저장소)), 'sha256': hashlib.sha256(ડેટા).hexdigest(),
                  'ascii_filename': all(ord(વર્ણ_મૂલ્ય)<128 for વર્ણ_મૂલ્ય in પથ.stem)}
            if પથ.suffix == '.py':
                남은선언 = []
                try:
                    for નોડ_મૂલ્ય in ast.walk(ast.parse(ડેટા.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(નોડ_મૂલ્ય, (ast.FunctionDef, ast.ClassDef)): 낱말 = નોડ_મૂલ્ય.name
                        elif isinstance(નોડ_મૂલ્ય, ast.arg): 낱말 = નોડ_મૂલ્ય.arg
                        elif isinstance(નોડ_મૂલ્ય, ast.Name) and isinstance(નોડ_મૂલ્ય.ctx, ast.Store): 낱말 = નોડ_મૂલ્ય.id
                        if 낱말 and all(ord(વર્ણ_મૂલ્ય)<128 for વર્ણ_મૂલ્ય in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': નોડ_મૂલ્ય.lineno})
                    પ્રવેશ_મૂલ્ય['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ભૂલ:
                    પ્રવેશ_મૂલ્ય['parse_error'] = str(ભૂલ)
            લૉગ_પંક્તિ.append(પ્રવેશ_મૂલ્ય)
    પરિમાણ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': લૉગ_પંક્તિ,
          'file_count': len(લૉગ_પંક્તિ), 'ascii_filename_count': sum(પ્રવેશ_મૂલ્ય['ascii_filename'] for પ્રવેશ_મૂલ્ય in લૉગ_પંક્તિ),
          'python_files_with_ascii_declarations': sum(bool(પ્રવેશ_મૂલ્ય.get('ascii_python_declarations')) for પ્રવેશ_મૂલ્ય in લૉગ_પંક્તિ),
          'all_repository_identifiers_korean': False,
          'note': '표준 સંપર્ક_કરો 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ગંતવ્ય_મૂલ્ય = પ્રોજેક્ટ_રૂટ/'build/verification/naming'; ગંતવ્ય_મૂલ્ય.mkdir(parents=True, exist_ok=True)
    (ગંતવ્ય_મૂલ્ય/'source-review.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2)+'\n')
    print('સ્રોત', પરિમાણ['file_count'], '개; ASCII ફાઇલ_નામ_પાઠ', પરિમાણ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ફાઈલ', પરિમાણ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ચલાવો_2()
