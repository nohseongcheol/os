#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/ھاسىل_قىلىش 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]
저장소 = كۆرسىتىش_يىلتىز.parents[1]

def ئىجرا_قىل_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    خاتىرە_قۇر = []
    for مۇندەرىجە_قىممىتى, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ئاتى for ئاتى in 하위들 if ئاتى not in 제외)
        for ئاتى in sorted(파일들):
            يول = Path(مۇندەرىجە_قىممىتى)/ئاتى
            if يول.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            مەلۇمات = يول.read_bytes()
            كىرگۈزۈش_قىممىتى = {'path': str(يول.relative_to(저장소)), 'sha256': hashlib.sha256(مەلۇمات).hexdigest(),
                  'ascii_filename': all(ord(ھەرپ_بەلگە_قىممىتى)<128 for ھەرپ_بەلگە_قىممىتى in يول.stem)}
            if يول.suffix == '.py':
                남은선언 = []
                try:
                    for تۈگۈن_قىممىتى in ast.walk(ast.parse(مەلۇمات.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(تۈگۈن_قىممىتى, (ast.FunctionDef, ast.ClassDef)): 낱말 = تۈگۈن_قىممىتى.name
                        elif isinstance(تۈگۈن_قىممىتى, ast.arg): 낱말 = تۈگۈن_قىممىتى.arg
                        elif isinstance(تۈگۈن_قىممىتى, ast.Name) and isinstance(تۈگۈن_قىممىتى.ctx, ast.Store): 낱말 = تۈگۈن_قىممىتى.id
                        if 낱말 and all(ord(ھەرپ_بەلگە_قىممىتى)<128 for ھەرپ_بەلگە_قىممىتى in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': تۈگۈن_قىممىتى.lineno})
                    كىرگۈزۈش_قىممىتى['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as خاتالىق:
                    كىرگۈزۈش_قىممىتى['parse_error'] = str(خاتالىق)
            خاتىرە_قۇر.append(كىرگۈزۈش_قىممىتى)
    ئۆلچەم = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': خاتىرە_قۇر,
          'file_count': len(خاتىرە_قۇر), 'ascii_filename_count': sum(كىرگۈزۈش_قىممىتى['ascii_filename'] for كىرگۈزۈش_قىممىتى in خاتىرە_قۇر),
          'python_files_with_ascii_declarations': sum(bool(كىرگۈزۈش_قىممىتى.get('ascii_python_declarations')) for كىرگۈزۈش_قىممىتى in خاتىرە_قۇر),
          'all_repository_identifiers_korean': False,
          'note': '표준 ئۇلا 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    نىشان_قىممىتى = كۆرسىتىش_يىلتىز/'build/verification/naming'; نىشان_قىممىتى.mkdir(parents=True, exist_ok=True)
    (نىشان_قىممىتى/'source-review.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2)+'\n')
    print('مەنبە', ئۆلچەم['file_count'], '개; ASCII ھۆججەت_نامى_تېكست', ئۆلچەم['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ھۆججەت', ئۆلچەم['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ئىجرا_قىل_2()
