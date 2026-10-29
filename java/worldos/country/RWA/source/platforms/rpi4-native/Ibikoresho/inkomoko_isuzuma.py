#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ihuriro():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    kubika_umurongo = []
    for ububiko_agaciro_e5561a2b, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Izina for Izina in 하위들 if Izina not in 제외)
        for Izina in sorted(파일들):
            Inzira = Path(ububiko_agaciro_e5561a2b)/Izina
            if Inzira.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            amakurushingiro = Inzira.read_bytes()
            icyinjizwa_agaciro = {'path': str(Inzira.relative_to(저장소)), 'sha256': hashlib.sha256(amakurushingiro).hexdigest(),
                  'ascii_filename': all(ord(inyuguti_agaciro)<128 for inyuguti_agaciro in Inzira.stem)}
            if Inzira.suffix == '.py':
                남은선언 = []
                try:
                    for ipfundo_agaciro in ast.walk(ast.parse(amakurushingiro.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ipfundo_agaciro, (ast.FunctionDef, ast.ClassDef)): 낱말 = ipfundo_agaciro.name
                        elif isinstance(ipfundo_agaciro, ast.arg): 낱말 = ipfundo_agaciro.arg
                        elif isinstance(ipfundo_agaciro, ast.Name) and isinstance(ipfundo_agaciro.ctx, ast.Store): 낱말 = ipfundo_agaciro.id
                        if 낱말 and all(ord(inyuguti_agaciro)<128 for inyuguti_agaciro in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ipfundo_agaciro.lineno})
                    icyinjizwa_agaciro['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as IKOSA:
                    icyinjizwa_agaciro['parse_error'] = str(IKOSA)
            kubika_umurongo.append(icyinjizwa_agaciro)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': kubika_umurongo,
          'file_count': len(kubika_umurongo), 'ascii_filename_count': sum(icyinjizwa_agaciro['ascii_filename'] for icyinjizwa_agaciro in kubika_umurongo),
          'python_files_with_ascii_declarations': sum(bool(icyinjizwa_agaciro.get('ascii_python_declarations')) for icyinjizwa_agaciro in kubika_umurongo),
          'all_repository_identifiers_korean': False,
          'note': '표준 Guhuza 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    aho_ijya_agaciro = 기준/'build/verification/naming'; aho_ijya_agaciro.mkdir(parents=True, exist_ok=True)
    (aho_ijya_agaciro/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('Inkomoko', 결과['file_count'], '개; ASCII dosiye_izina_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Idosiye', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ihuriro()
