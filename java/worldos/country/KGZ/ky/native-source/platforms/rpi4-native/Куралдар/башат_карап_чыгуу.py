#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Жүргүзүү():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    жазуу_катар = []
    for каталог_маани, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Аты for Аты in 하위들 if Аты not in 제외)
        for Аты in sorted(파일들):
            ЖОЛ = Path(каталог_маани)/Аты
            if ЖОЛ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            берилмелер = ЖОЛ.read_bytes()
            киргизме_жазуу_маани = {'path': str(ЖОЛ.relative_to(저장소)), 'sha256': hashlib.sha256(берилмелер).hexdigest(),
                  'ascii_filename': all(ord(символ_маани_068c2631)<128 for символ_маани_068c2631 in ЖОЛ.stem)}
            if ЖОЛ.suffix == '.py':
                남은선언 = []
                try:
                    for түйүн_маани in ast.walk(ast.parse(берилмелер.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(түйүн_маани, (ast.FunctionDef, ast.ClassDef)): 낱말 = түйүн_маани.name
                        elif isinstance(түйүн_маани, ast.arg): 낱말 = түйүн_маани.arg
                        elif isinstance(түйүн_маани, ast.Name) and isinstance(түйүн_маани.ctx, ast.Store): 낱말 = түйүн_маани.id
                        if 낱말 and all(ord(символ_маани_068c2631)<128 for символ_маани_068c2631 in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': түйүн_маани.lineno})
                    киргизме_жазуу_маани['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Ката:
                    киргизме_жазуу_маани['parse_error'] = str(Ката)
            жазуу_катар.append(киргизме_жазуу_маани)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': жазуу_катар,
          'file_count': len(жазуу_катар), 'ascii_filename_count': sum(киргизме_жазуу_маани['ascii_filename'] for киргизме_жазуу_маани in жазуу_катар),
          'python_files_with_ascii_declarations': sum(bool(киргизме_жазуу_маани.get('ascii_python_declarations')) for киргизме_жазуу_маани in жазуу_катар),
          'all_repository_identifiers_korean': False,
          'note': '표준 Туташуу 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    көздөө_жайы_маани = 기준/'build/verification/naming'; көздөө_жайы_маани.mkdir(parents=True, exist_ok=True)
    (көздөө_жайы_маани/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('Булак', 결과['file_count'], '개; ASCII файл_аты_СМС', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Файл', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Жүргүзүү()
