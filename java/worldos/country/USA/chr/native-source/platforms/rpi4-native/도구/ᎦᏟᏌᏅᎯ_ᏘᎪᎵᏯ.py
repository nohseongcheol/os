#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ᎠᎢᏎᏍᏗ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = []
    for ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(ᏚᏙᎥᎢ for ᏚᏙᎥᎢ in 하위들 if ᏚᏙᎥᎢ not in 제외)
        for ᏚᏙᎥᎢ in sorted(파일들):
            ᎠᏍᏓᏩᏛᏍᏗ = Path(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)/ᏚᏙᎥᎢ
            if ᎠᏍᏓᏩᏛᏍᏗ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ᎦᏟᏌᏅᎯ = ᎠᏍᏓᏩᏛᏍᏗ.read_bytes()
            Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = {'path': str(ᎠᏍᏓᏩᏛᏍᏗ.relative_to(저장소)), 'sha256': hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest(),
                  'ascii_filename': all(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)<128 for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in ᎠᏍᏓᏩᏛᏍᏗ.stem)}
            if ᎠᏍᏓᏩᏛᏍᏗ.suffix == '.py':
                남은선언 = []
                try:
                    for ᏃᏗ_ᏧᎬᏩᎶᏗᏯ in ast.walk(ast.parse(ᎦᏟᏌᏅᎯ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ᏃᏗ_ᏧᎬᏩᎶᏗᏯ, (ast.FunctionDef, ast.ClassDef)): 낱말 = ᏃᏗ_ᏧᎬᏩᎶᏗᏯ.name
                        elif isinstance(ᏃᏗ_ᏧᎬᏩᎶᏗᏯ, ast.arg): 낱말 = ᏃᏗ_ᏧᎬᏩᎶᏗᏯ.arg
                        elif isinstance(ᏃᏗ_ᏧᎬᏩᎶᏗᏯ, ast.Name) and isinstance(ᏃᏗ_ᏧᎬᏩᎶᏗᏯ.ctx, ast.Store): 낱말 = ᏃᏗ_ᏧᎬᏩᎶᏗᏯ.id
                        if 낱말 and all(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)<128 for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ᏃᏗ_ᏧᎬᏩᎶᏗᏯ.lineno})
                    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ᎦᎵᏓᏍᏔᏅ:
                    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['parse_error'] = str(ᎦᎵᏓᏍᏔᏅ)
            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.append(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ,
          'file_count': len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ), 'ascii_filename_count': sum(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['ascii_filename'] for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ),
          'python_files_with_ascii_declarations': sum(bool(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.get('ascii_python_declarations')) for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ),
          'all_repository_identifiers_korean': False,
          'note': '표준 ᎫᏓᎳ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 기준/'build/verification/naming'; ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.mkdir(parents=True, exist_ok=True)
    (ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ᎦᏟᏌᏅᎯ_0201f362', 결과['file_count'], '개; ASCII ᎠᏍᏆᏂᎪᏙᏗ_ᏚᏙᎥᎢ_ᎠᎪᎵᏰᏗ', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ᎠᏍᏆᏂᎪᏙᏗ', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ᎠᎢᏎᏍᏗ()
