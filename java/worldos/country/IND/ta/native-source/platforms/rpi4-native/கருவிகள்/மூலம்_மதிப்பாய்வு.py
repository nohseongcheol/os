#!/usr/bin/env python3
"""தொகுபதிவகம்_மூலம் 전체의 자체 원문을 목록화한다. 외부/உருவாக்குக 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]
தொகுபதிவகம்_மூலம் = திட்டப்பணி_மூலம்.parents[1]

def செயல்படுத்துக():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    பதிவு_பதிவு = []
    for கோப்பகம்_மதிப்பு, 하위들, 파일들 in os.walk(str(தொகுபதிவகம்_மூலம்)):
        하위들[:] = sorted(பெயர் for பெயர் in 하위들 if பெயர் not in 제외)
        for பெயர் in sorted(파일들):
            பாதை_2 = Path(கோப்பகம்_மதிப்பு)/பெயர்
            if பாதை_2.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            தரவு = பாதை_2.read_bytes()
            உள்ளீடு_மதிப்பு = {'path': str(பாதை_2.relative_to(தொகுபதிவகம்_மூலம்)), 'sha256': hashlib.sha256(தரவு).hexdigest(),
                  'ascii_filename': all(ord(எழுத்துக்குறி_மதிப்பு)<128 for எழுத்துக்குறி_மதிப்பு in பாதை_2.stem)}
            if பாதை_2.suffix == '.py':
                남은선언 = []
                try:
                    for கணு_மதிப்பு in ast.walk(ast.parse(தரவு.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(கணு_மதிப்பு, (ast.FunctionDef, ast.ClassDef)): 낱말 = கணு_மதிப்பு.name
                        elif isinstance(கணு_மதிப்பு, ast.arg): 낱말 = கணு_மதிப்பு.arg
                        elif isinstance(கணு_மதிப்பு, ast.Name) and isinstance(கணு_மதிப்பு.ctx, ast.Store): 낱말 = கணு_மதிப்பு.id
                        if 낱말 and all(ord(எழுத்துக்குறி_மதிப்பு)<128 for எழுத்துக்குறி_மதிப்பு in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': கணு_மதிப்பு.lineno})
                    உள்ளீடு_மதிப்பு['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as பிழை:
                    உள்ளீடு_மதிப்பு['parse_error'] = str(பிழை)
            பதிவு_பதிவு.append(உள்ளீடு_மதிப்பு)
    அளவிடக்கூடியது = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': பதிவு_பதிவு,
          'file_count': len(பதிவு_பதிவு), 'ascii_filename_count': sum(உள்ளீடு_மதிப்பு['ascii_filename'] for உள்ளீடு_மதிப்பு in பதிவு_பதிவு),
          'python_files_with_ascii_declarations': sum(bool(உள்ளீடு_மதிப்பு.get('ascii_python_declarations')) for உள்ளீடு_மதிப்பு in பதிவு_பதிவு),
          'all_repository_identifiers_korean': False,
          'note': '표준 இணைக்க 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    இலக்கு_மதிப்பு = திட்டப்பணி_மூலம்/'build/verification/naming'; இலக்கு_மதிப்பு.mkdir(parents=True, exist_ok=True)
    (இலக்கு_மதிப்பு/'source-review.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2)+'\n')
    print('மூலக்_கோப்பு', அளவிடக்கூடியது['file_count'], '개; ASCII கோப்பு_பெயர்_உரை', அளவிடக்கூடியது['ascii_filename_count'],
          '개; 영어 선언이 남은 Python கோப்பின்_பெயர்', அளவிடக்கூடியது['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': செயல்படுத்துக()
