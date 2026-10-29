#!/usr/bin/env python3
"""저장소 전체의 ကိုယ်ပိုင် 원문을 목록화한다. ပြင်ပတန်ဖိုး/ထုတ်လုပ် 코드는 ရေတွက်မှု 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]
저장소 = စီမံကိန်းအမြစ်.parents[1]

def လုပ်ဆောင်():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = []
    for ဖိုင်တွဲတန်ဖိုး, 하위들, ဖိုင်အချက်များ in os.walk(str(저장소)):
        하위들[:] = sorted(အမည် for အမည် in 하위들 if အမည် not in 제외)
        for အမည် in sorted(ဖိုင်အချက်များ):
            လမ်း = Path(ဖိုင်တွဲတန်ဖိုး)/အမည်
            if လမ်း.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ဒေတာ = လမ်း.read_bytes()
            အချက်တန်ဖိုး = {'path': str(လမ်း.relative_to(저장소)), 'sha256': hashlib.sha256(ဒေတာ).hexdigest(),
                  'ascii_filename': all(ord(အက္ခရာတန်ဖိုး)<128 for အက္ခရာတန်ဖိုး in လမ်း.stem)}
            if လမ်း.suffix == '.py':
                ကျန်ရှိကြေညာချက်များ = []
                try:
                    for ဆုံမှတ်တန်ဖိုး in ast.walk(ast.parse(ဒေတာ.decode('utf-8-sig'))):
                        ဝေါဟာရ = ''
                        if isinstance(ဆုံမှတ်တန်ဖိုး, (ast.FunctionDef, ast.ClassDef)): ဝေါဟာရ = ဆုံမှတ်တန်ဖိုး.name
                        elif isinstance(ဆုံမှတ်တန်ဖိုး, ast.arg): ဝေါဟာရ = ဆုံမှတ်တန်ဖိုး.arg
                        elif isinstance(ဆုံမှတ်တန်ဖိုး, ast.Name) and isinstance(ဆုံမှတ်တန်ဖိုး.ctx, ast.Store): ဝေါဟာရ = ဆုံမှတ်တန်ဖိုး.id
                        if ဝေါဟာရ and all(ord(အက္ခရာတန်ဖိုး)<128 for အက္ခရာတန်ဖိုး in ဝေါဟာရ) and ဝေါဟာရ != '_' and not ဝေါဟာရ.startswith('__'):
                            ကျန်ရှိကြေညာချက်များ.append({'name': ဝေါဟာရ, 'line': ဆုံမှတ်တန်ဖိုး.lineno})
                    အချက်တန်ဖိုး['ascii_python_declarations'] = ကျန်ရှိကြေညာချက်များ
                except (SyntaxError, UnicodeError) as အမှား:
                    အချက်တန်ဖိုး['parse_error'] = str(အမှား)
            မှတ်တမ်းမှတ်တမ်းတစ်ခု.append(အချက်တန်ဖိုး)
    ရလဒ် = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': မှတ်တမ်းမှတ်တမ်းတစ်ခု,
          'file_count': len(မှတ်တမ်းမှတ်တမ်းတစ်ခု), 'ascii_filename_count': sum(အချက်တန်ဖိုး['ascii_filename'] for အချက်တန်ဖိုး in မှတ်တမ်းမှတ်တမ်းတစ်ခု),
          'python_files_with_ascii_declarations': sum(bool(အချက်တန်ဖိုး.get('ascii_python_declarations')) for အချက်တန်ဖိုး in မှတ်တမ်းမှတ်တမ်းတစ်ခု),
          'all_repository_identifiers_korean': False,
          'note': '표준 ချိတ်ဆက် 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ဦးတည်ရာတန်ဖိုး = စီမံကိန်းအမြစ်/'build/verification/naming'; ဦးတည်ရာတန်ဖိုး.mkdir(parents=True, exist_ok=True)
    (ဦးတည်ရာတန်ဖိုး/'source-review.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2)+'\n')
    print('မူရင်းကုဒ်', ရလဒ်['file_count'], '개; ASCII ဖိုင်အမည်စာသား', ရလဒ်['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ဖိုင်', ရလဒ်['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': လုပ်ဆောင်()
