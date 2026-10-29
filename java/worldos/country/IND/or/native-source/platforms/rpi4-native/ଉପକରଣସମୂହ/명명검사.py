#!/usr/bin/env python3
"""명명 କ୍ଲିପ୍·ବ୍ୟତିକ୍ରମ·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
저장소 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]

def ଚଳାନ୍ତୁ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    କର୍ମ_ମୂଲ୍ୟ = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    ପାରାମିଟର୍_ସାରଣୀ = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ପଥ in list((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ').glob('*.py')) + list((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'예제').rglob('*.py')) + 공용번역기들:
        if ପଥ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ପଥ.read_text()); 나무들[ପଥ] = 나무
        for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ast.walk(나무):
            if isinstance(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, ast.FunctionDef):
                ପାରାମିଟର୍_ସାରଣୀ.setdefault(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name, set()).update(ପାରାମିଟର୍_ଯୁକ୍ତି.arg for ପାରାମିଟର୍_ଯୁକ୍ତି in ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.args.args + ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.args.kwonlyargs)
                if ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.args.kwarg: 가변매개함수.add(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name)
            if isinstance(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, ast.ClassDef):
                for Excel_ଟେବଲ୍_ମୂଲ୍ୟ in ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.body:
                    if isinstance(Excel_ଟେବଲ୍_ମୂଲ୍ୟ, ast.FunctionDef) and Excel_ଟେବଲ୍_ମୂଲ୍ୟ.name == '__init__':
                        ପାରାମିଟର୍_ସାରଣୀ.setdefault(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name, set()).update(ପାରାମିଟର୍_ଯୁକ୍ତି.arg for ପାରାମିଟର୍_ଯୁକ୍ତି in Excel_ଟେବଲ୍_ମୂଲ୍ୟ.args.args + Excel_ଟେବଲ୍_ମୂଲ୍ୟ.args.kwonlyargs)
            ନାମ = ''
            if isinstance(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, (ast.FunctionDef, ast.ClassDef)): ନାମ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name
            elif isinstance(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, ast.Name) and isinstance(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.ctx, ast.Store): ନାମ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.id
            elif isinstance(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ, ast.arg): ନାମ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.arg
            if ନାମ and ନାମ not in କର୍ମ_ମୂଲ୍ୟ and all(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)<128 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ନାମ):
                실패들.append('{}:{}: {}'.format(ପଥ.relative_to(저장소), ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.lineno, ନାମ))
    for ପଥ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ନାମ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ନାମ not in ପାରାମିଟର୍_ସାରଣୀ or ନାମ in 가변매개함수 or not any(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)>127 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ନାମ): continue
            for ପାରାମିଟର୍_ଯୁକ୍ତି in 호출.keywords:
                if ପାରାମିଟର୍_ଯୁକ୍ତି.arg and ପାରାମିଟର୍_ଯୁକ୍ତି.arg not in ପାରାମିଟର୍_ସାରଣୀ[ନାମ]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ପଥ.relative_to(저장소), 호출.lineno, ନାମ, ପାରାମିଟର୍_ଯୁକ୍ତି.arg))
    for ରେଖା in (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି = ରେଖା.split('\t')
        if not (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/현재).is_file(): 실패들.append('ଘୁଞ୍ଚାଇବା_ମୂଲ୍ୟ ଫାଇଲ 없음: '+현재)
        if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି == '호환진입점유지' and not (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/이전).is_file(): 실패들.append('호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍ 없음: '+이전)
    예제 = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ପଥ in sorted((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'example/java').glob('*.java')):
        ଉତ୍ସ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ପଥ.read_text())
        for ନାମ in re.findall(r'\b[^\W\d]\w*\b', ଉତ୍ସ, re.UNICODE):
            if ନାମ not in 예약어 and all(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)<128 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ନାମ):
                실패들.append('{}: 예제의 영어 ପରିଚାୟକ_ମୂଲ୍ୟ {}'.format(ପଥ.name, ନାମ))
    for ନାମ in ('창', 'ବଟନ୍', 'ସୂଚକ', 'ପାଠ୍ୟ_କ୍ଷେତ୍ର', '화면구성요소', 'ଘଟଣା_ପ୍ରତିଧାଡ଼ି', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ଉତ୍ସ = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'한국어자바/한국어/자체'/(ନାମ+'.java')).read_text()
        ଉତ୍ସ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ଉତ୍ସ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ଉତ୍ସ):
            실패들.append(ନାମ+': 한국어 직접 구현에 표준 ଅବଜେକ୍ଟ_ମୂଲ୍ୟ 래퍼가 남았습니다.')
    시언어예제 = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'example/c/네트워크예제.c').read_text()
    for ନାମ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ନାମ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ନାମ: '+ନାମ)
    파이썬예제 = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ବ୍ୟତିକ୍ରମ 직접 사용')
    머리 = (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ନାମ in ('କ୍ଲାଉଡ୍_ପରିବାର', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ନାମ+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ମାକ୍ରୋ_ମୂଲ୍ୟ 사용: '+ନାମ)
    자바파일수 = 0
    for ରୁଟ୍_ମୂଲ୍ୟ in ('ଉତ୍ସ', 'ଉପଭୋକ୍ତା/자바', '한국어자바'):
        for ପଥ in (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/ରୁଟ୍_ମୂଲ୍ୟ).rglob('*.java'):
            자바파일수 += 1
            ଉତ୍ସ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ପଥ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ଉତ୍ସ):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍), 맞음[1]))
            if ରୁଟ୍_ମୂଲ୍ୟ == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ଉତ୍ସ):
                실패들.append('{}: 공개 ବ୍ୟତିକ୍ରମ 선언'.format(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ପଥ in sorted((저장소/'os/ଉତ୍ସ').glob('*.java')):
        x86자바파일수 += 1
        ଉତ୍ସ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ପଥ.read_text())
        for ନାମ in re.findall(r'\b[^\W\d]\w*\b', ଉତ୍ସ, re.UNICODE):
            if ନାମ not in 예약어 | 표준자바이름 and all(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)<128 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ନାମ):
                실패들.append('{}: 자체 영어 ପରିଚାୟକ_ମୂଲ୍ୟ {}'.format(ପଥ.relative_to(저장소), ନାମ))
    ଲଗ୍_ଧାଡ଼ି = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/시언어이름분석.py')])
        분석 = json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ତ୍ରୁଟି) for ତ୍ରୁଟି in 분석['ତ୍ରୁଟି'])
        공개규약 = set(json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'명명/규격이름.json').read_text()))
        for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 분석['선언'].values():
            ନାମ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['ନାମ']; ପଥ = Path(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['ଫାଇଲ'])
            ଉତ୍ସ = ପଥ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ଉତ୍ସ[ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ']:ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ']+len(ନାମ)] == ନାମ.encode() and ନାମ not in 공개규약:
                실패들.append('{}:{}: {}'.format(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍), ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['줄'], ନାମ))
        ଲଗ୍_ଧାଡ଼ି['c_semantic_checked'] = True
        ଲଗ୍_ଧାଡ଼ି['c_source_sha256'] = {str(Path(ଫାଇଲ).relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍)):ହାସ୍_ଫାଇଲ୍ for ଫାଇଲ,ହାସ୍_ଫାଇଲ୍ in 분석['원문해시'].items()}
    ଲଗ୍_ଧାଡ଼ି['passed'] = not 실패들; ଲଗ୍_ଧାଡ଼ି['failures'] = 실패들
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/naming'; ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.mkdir(parents=True, exist_ok=True)
    (ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'report.json').write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·ଫାଇଲ ପଥ·호환 ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍·통신 예제')

if __name__ == '__main__': ଚଳାନ୍ତୁ()
