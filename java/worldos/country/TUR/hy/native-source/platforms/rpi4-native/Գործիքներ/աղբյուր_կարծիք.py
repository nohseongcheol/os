#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/արտադրել 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

արձակել_արմատ = Path(__file__).resolve().parents[1]
저장소 = արձակել_արմատ.parents[1]

def Գործարկել():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    մատյան_տող = []
    for գրացուցակ_արժեք, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Անուն for Անուն in 하위들 if Անուն not in 제외)
        for Անուն in sorted(파일들):
            Ճանապարհ = Path(գրացուցակ_արժեք)/Անուն
            if Ճանապարհ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            տվյալ = Ճանապարհ.read_bytes()
            մուտքագրում_արժեք = {'path': str(Ճանապարհ.relative_to(저장소)), 'sha256': hashlib.sha256(տվյալ).hexdigest(),
                  'ascii_filename': all(ord(գրանշան_արժեք)<128 for գրանշան_արժեք in Ճանապարհ.stem)}
            if Ճանապարհ.suffix == '.py':
                남은선언 = []
                try:
                    for հանգույց_արժեք in ast.walk(ast.parse(տվյալ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(հանգույց_արժեք, (ast.FunctionDef, ast.ClassDef)): 낱말 = հանգույց_արժեք.name
                        elif isinstance(հանգույց_արժեք, ast.arg): 낱말 = հանգույց_արժեք.arg
                        elif isinstance(հանգույց_արժեք, ast.Name) and isinstance(հանգույց_արժեք.ctx, ast.Store): 낱말 = հանգույց_արժեք.id
                        if 낱말 and all(ord(գրանշան_արժեք)<128 for գրանշան_արժեք in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': հանգույց_արժեք.lineno})
                    մուտքագրում_արժեք['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Սխալ:
                    մուտքագրում_արժեք['parse_error'] = str(Սխալ)
            մատյան_տող.append(մուտքագրում_արժեք)
    չափ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': մատյան_տող,
          'file_count': len(մատյան_տող), 'ascii_filename_count': sum(մուտքագրում_արժեք['ascii_filename'] for մուտքագրում_արժեք in մատյան_տող),
          'python_files_with_ascii_declarations': sum(bool(մուտքագրում_արժեք.get('ascii_python_declarations')) for մուտքագրում_արժեք in մատյան_տող),
          'all_repository_identifiers_korean': False,
          'note': '표준 Միացնել 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    նպատակակետ_արժեք = արձակել_արմատ/'build/verification/naming'; նպատակակետ_արժեք.mkdir(parents=True, exist_ok=True)
    (նպատակակետ_արժեք/'source-review.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2)+'\n')
    print('ԱՂԲՅՈՒՐ', չափ['file_count'], '개; ASCII նիշք_անուն_Գրվածք', չափ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Ֆայլ', չափ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Գործարկել()
