#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ක්_රියාත්මක_කරන්න_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ලොගය_පේළිය = []
    for නාමාවලිය_අගය, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(නම for නම in 하위들 if නම not in 제외)
        for නම in sorted(파일들):
            මාර්_ගය = Path(නාමාවලිය_අගය)/නම
            if මාර්_ගය.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            දත්ත = මාර්_ගය.read_bytes()
            පිවිසුම_අගය = {'path': str(මාර්_ගය.relative_to(저장소)), 'sha256': hashlib.sha256(දත්ත).hexdigest(),
                  'ascii_filename': all(ord(අනුලකුණ_අගය)<128 for අනුලකුණ_අගය in මාර්_ගය.stem)}
            if මාර්_ගය.suffix == '.py':
                남은선언 = []
                try:
                    for මංසල_අගය in ast.walk(ast.parse(දත්ත.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(මංසල_අගය, (ast.FunctionDef, ast.ClassDef)): 낱말 = මංසල_අගය.name
                        elif isinstance(මංසල_අගය, ast.arg): 낱말 = මංසල_අගය.arg
                        elif isinstance(මංසල_අගය, ast.Name) and isinstance(මංසල_අගය.ctx, ast.Store): 낱말 = මංසල_අගය.id
                        if 낱말 and all(ord(අනුලකුණ_අගය)<128 for අනුලකුණ_අගය in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': මංසල_අගය.lineno})
                    පිවිසුම_අගය['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as දෝෂය:
                    පිවිසුම_අගය['parse_error'] = str(දෝෂය)
            ලොගය_පේළිය.append(පිවිසුම_අගය)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ලොගය_පේළිය,
          'file_count': len(ලොගය_පේළිය), 'ascii_filename_count': sum(පිවිසුම_අගය['ascii_filename'] for පිවිසුම_අගය in ලොගය_පේළිය),
          'python_files_with_ascii_declarations': sum(bool(පිවිසුම_අගය.get('ascii_python_declarations')) for පිවිසුම_අගය in ලොගය_පේළිය),
          'all_repository_identifiers_korean': False,
          'note': '표준 සම්බන්ද_වන්න 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ගමනාන්තය_අගය = 기준/'build/verification/naming'; ගමනාන්තය_අගය.mkdir(parents=True, exist_ok=True)
    (ගමනාන්තය_අගය/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('මූලය', 결과['file_count'], '개; ASCII ගොනුව_නම_පෙළ', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ගොනු', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()
