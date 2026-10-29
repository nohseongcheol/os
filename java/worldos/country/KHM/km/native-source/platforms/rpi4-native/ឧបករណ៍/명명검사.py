#!/usr/bin/env python3
"""명명 មេឌៀខ្លីៗ·ការលើកលែង·경로를 검사한다. --시언어는 libclang ការប្រកាស 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]
ឃ្លាំង_ផ្ទុក_ឬស = បញ្ចាំង_ឬស.parents[1]

def រត់():
    មុខងារ_ញែក_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    មុខងារ_ញែក_48ee4b1b.add_argument('--시언어', action='store_true')
    អាគុយម៉ង់ = មុខងារ_ញែក_48ee4b1b.parse_args()
    실패들 = []
    ករណី_តំលៃ = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    ប៉ារ៉ាម៉ែត្រ_តារាង = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [ឃ្លាំង_ផ្ទុក_ឬស/'compiler/컴파일러.py', ឃ្លាំង_ផ្ទុក_ឬស/'compiler/기계어미리번역.py']
    for ផ្លូវ in list((បញ្ចាំង_ឬស/'ឧបករណ៍').glob('*.py')) + list((បញ្ចាំង_ឬស/'예제').rglob('*.py')) + 공용번역기들:
        if ផ្លូវ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ផ្លូវ.read_text()); 나무들[ផ្លូវ] = 나무
        for ការបញ្ចូល_តំលៃ in ast.walk(나무):
            if isinstance(ការបញ្ចូល_តំលៃ, ast.FunctionDef):
                ប៉ារ៉ាម៉ែត្រ_តារាង.setdefault(ការបញ្ចូល_តំលៃ.name, set()).update(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.arg for ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ in ការបញ្ចូល_តំលៃ.args.args + ការបញ្ចូល_តំលៃ.args.kwonlyargs)
                if ការបញ្ចូល_តំលៃ.args.kwarg: 가변매개함수.add(ការបញ្ចូល_តំលៃ.name)
            if isinstance(ការបញ្ចូល_តំលៃ, ast.ClassDef):
                for អនុគមន៍_តំលៃ in ការបញ្ចូល_តំលៃ.body:
                    if isinstance(អនុគមន៍_តំលៃ, ast.FunctionDef) and អនុគមន៍_តំលៃ.name == '__init__':
                        ប៉ារ៉ាម៉ែត្រ_តារាង.setdefault(ការបញ្ចូល_តំលៃ.name, set()).update(ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.arg for ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ in អនុគមន៍_តំលៃ.args.args + អនុគមន៍_តំលៃ.args.kwonlyargs)
            ឈ្មោះ = ''
            if isinstance(ការបញ្ចូល_តំលៃ, (ast.FunctionDef, ast.ClassDef)): ឈ្មោះ = ការបញ្ចូល_តំលៃ.name
            elif isinstance(ការបញ្ចូល_តំលៃ, ast.Name) and isinstance(ការបញ្ចូល_តំលៃ.ctx, ast.Store): ឈ្មោះ = ការបញ្ចូល_តំលៃ.id
            elif isinstance(ការបញ្ចូល_តំលៃ, ast.arg): ឈ្មោះ = ការបញ្ចូល_តំលៃ.arg
            if ឈ្មោះ and ឈ្មោះ not in ករណី_តំលៃ and all(ord(តួអក្សរ_តំលៃ)<128 for តួអក្សរ_តំលៃ in ឈ្មោះ):
                실패들.append('{}:{}: {}'.format(ផ្លូវ.relative_to(ឃ្លាំង_ផ្ទុក_ឬស), ការបញ្ចូល_តំលៃ.lineno, ឈ្មោះ))
    for ផ្លូវ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ឈ្មោះ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ឈ្មោះ not in ប៉ារ៉ាម៉ែត្រ_តារាង or ឈ្មោះ in 가변매개함수 or not any(ord(តួអក្សរ_តំលៃ)>127 for តួអក្សរ_តំលៃ in ឈ្មោះ): continue
            for ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់ in 호출.keywords:
                if ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.arg and ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.arg not in ប៉ារ៉ាម៉ែត្រ_តារាង[ឈ្មោះ]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ផ្លូវ.relative_to(ឃ្លាំង_ផ្ទុក_ឬស), 호출.lineno, ឈ្មោះ, ប៉ារ៉ាម៉ែត្រ_អាគុយម៉ង់.arg))
    for បន្ទាត់ in (បញ្ចាំង_ឬស/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ដំណើរការ_តំលៃ_ការបញ្ចូល = បន្ទាត់.split('\t')
        if not (បញ្ចាំង_ឬស/현재).is_file(): 실패들.append('ផ្លាស់ទី_តំលៃ ឯកសារ 없음: '+현재)
        if ដំណើរការ_តំលៃ_ការបញ្ចូល == '호환진입점유지' and not (បញ្ចាំង_ឬស/이전).is_file(): 실패들.append('호환 ការបញ្ចូល_ចំនុច 없음: '+이전)
    예제 = (បញ្ចាំង_ឬស.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ផ្លូវ in sorted((បញ្ចាំង_ឬស.parents[1]/'example/java').glob('*.java')):
        ប្រភព = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ផ្លូវ.read_text())
        for ឈ្មោះ in re.findall(r'\b[^\W\d]\w*\b', ប្រភព, re.UNICODE):
            if ឈ្មោះ not in 예약어 and all(ord(តួអក្សរ_តំលៃ)<128 for តួអក្សរ_តំលៃ in ឈ្មោះ):
                실패들.append('{}: 예제의 영어 អង្គសម្គាល់_តំលៃ {}'.format(ផ្លូវ.name, ឈ្មោះ))
    for ឈ្មោះ in ('창', 'ប៊ូតុង', 'ស្លាក', 'អត្ថបទ_កន្លែង_បញ្ចូល', '화면구성요소', 'ព្រឹត្តិការណ៍_ជួរ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ប្រភព = (បញ្ចាំង_ឬស/'한국어자바/한국어/자체'/(ឈ្មោះ+'.java')).read_text()
        ប្រភព = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ប្រភព)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ប្រភព):
            실패들.append(ឈ្មោះ+': 한국어 직접 구현에 표준 វត្ថុ_តំលៃ 래퍼가 남았습니다.')
    시언어예제 = (បញ្ចាំង_ឬស.parents[1]/'example/c/네트워크예제.c').read_text()
    for ឈ្មោះ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ឈ្មោះ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ឈ្មោះ: '+ឈ្មោះ)
    파이썬예제 = (បញ្ចាំង_ឬស.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ការលើកលែង 직접 사용')
    머리 = (បញ្ចាំង_ឬស.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ឈ្មោះ in ('អ៊ីនធឺណិត_គ្រួសារ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ឈ្មោះ+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ម៉ាក្រូ_តំលៃ 사용: '+ឈ្មោះ)
    자바파일수 = 0
    for ឬស_តំលៃ in ('ប្រភព', 'អ្នកប្រើ/자바', '한국어자바'):
        for ផ្លូវ in (បញ្ចាំង_ឬស/ឬស_តំលៃ).rglob('*.java'):
            자바파일수 += 1
            ប្រភព = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ផ្លូវ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ប្រភព):
                실패들.append('{}: 한국어화되지 않은 ការប្រកាស {}'.format(ផ្លូវ.relative_to(បញ្ចាំង_ឬស), 맞음[1]))
            if ឬស_តំលៃ == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ប្រភព):
                실패들.append('{}: 공개 ការលើកលែង ការប្រកាស'.format(ផ្លូវ.relative_to(បញ្ចាំង_ឬស)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ផ្លូវ in sorted((ឃ្លាំង_ផ្ទុក_ឬស/'os/ប្រភព').glob('*.java')):
        x86자바파일수 += 1
        ប្រភព = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ផ្លូវ.read_text())
        for ឈ្មោះ in re.findall(r'\b[^\W\d]\w*\b', ប្រភព, re.UNICODE):
            if ឈ្មោះ not in 예약어 | 표준자바이름 and all(ord(តួអក្សរ_តំលៃ)<128 for តួអក្សរ_តំលៃ in ឈ្មោះ):
                실패들.append('{}: 자체 영어 អង្គសម្គាល់_តំលៃ {}'.format(ផ្លូវ.relative_to(ឃ្លាំង_ផ្ទុក_ឬស), ឈ្មោះ))
    កំណត់_ហេតុ_ថត = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if អាគុយម៉ង់.시언어:
        subprocess.check_call(['python3', str(បញ្ចាំង_ឬស/'ឧបករណ៍/시언어이름분석.py')])
        분석 = json.loads((បញ្ចាំង_ឬស/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(កំហុស) for កំហុស in 분석['កំហុស'])
        공개규약 = set(json.loads((បញ្ចាំង_ឬស/'명명/규격이름.json').read_text()))
        for ការបញ្ចូល_តំលៃ in 분석['ការប្រកាស'].values():
            ឈ្មោះ = ការបញ្ចូល_តំលៃ['ឈ្មោះ']; ផ្លូវ = Path(ការបញ្ចូល_តំលៃ['ឯកសារ'])
            ប្រភព = ផ្លូវ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ប្រភព[ការបញ្ចូល_តំលៃ['ការបែង_ភាគ_តំលៃ']:ការបញ្ចូល_តំលៃ['ការបែង_ភាគ_តំលៃ']+len(ឈ្មោះ)] == ឈ្មោះ.encode() and ឈ្មោះ not in 공개규약:
                실패들.append('{}:{}: {}'.format(ផ្លូវ.relative_to(បញ្ចាំង_ឬស), ការបញ្ចូល_តំលៃ['បន្ទាត់'], ឈ្មោះ))
        កំណត់_ហេតុ_ថត['c_semantic_checked'] = True
        កំណត់_ហេតុ_ថត['c_source_sha256'] = {str(Path(ឯកសារ).relative_to(បញ្ចាំង_ឬស)):ហាស_ឯកសារ for ឯកសារ,ហាស_ឯកសារ in 분석['원문해시'].items()}
    កំណត់_ហេតុ_ថត['passed'] = not 실패들; កំណត់_ហេតុ_ថត['failures'] = 실패들
    ទិសដៅ_តំលៃ = បញ្ចាំង_ឬស/'build/verification/naming'; ទិសដៅ_តំលៃ.mkdir(parents=True, exist_ok=True)
    (ទិសដៅ_តំលៃ/'report.json').write_text(json.dumps(កំណត់_ហេតុ_ថត, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 ការប្រកាស·ឯកសារ ផ្លូវ·호환 ការបញ្ចូល_ចំនុច·통신 예제')

if __name__ == '__main__': រត់()
