#!/usr/bin/env python3
"""명명 تراشه·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def هلائڻ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    حالت_قدر_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for راههه in list((기준/'اوزار').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if راههه.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(راههه.read_text()); 나무들[راههه] = 나무
        for داخلا_قدر in ast.walk(나무):
            if isinstance(داخلا_قدر, ast.FunctionDef):
                매개변수표.setdefault(داخلا_قدر.name, set()).update(인자.arg for 인자 in داخلا_قدر.args.args + داخلا_قدر.args.kwonlyargs)
                if داخلا_قدر.args.kwarg: 가변매개함수.add(داخلا_قدر.name)
            if isinstance(داخلا_قدر, ast.ClassDef):
                for فعل_قدر in داخلا_قدر.body:
                    if isinstance(فعل_قدر, ast.FunctionDef) and فعل_قدر.name == '__init__':
                        매개변수표.setdefault(داخلا_قدر.name, set()).update(인자.arg for 인자 in فعل_قدر.args.args + فعل_قدر.args.kwonlyargs)
            نالو = ''
            if isinstance(داخلا_قدر, (ast.FunctionDef, ast.ClassDef)): نالو = داخلا_قدر.name
            elif isinstance(داخلا_قدر, ast.Name) and isinstance(داخلا_قدر.ctx, ast.Store): نالو = داخلا_قدر.id
            elif isinstance(داخلا_قدر, ast.arg): نالو = داخلا_قدر.arg
            if نالو and نالو not in حالت_قدر_102996da and all(ord(ڪريڪٽر_قدر)<128 for ڪريڪٽر_قدر in نالو):
                실패들.append('{}:{}: {}'.format(راههه.relative_to(저장소), داخلا_قدر.lineno, نالو))
    for راههه, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            نالو = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if نالو not in 매개변수표 or نالو in 가변매개함수 or not any(ord(ڪريڪٽر_قدر)>127 for ڪريڪٽر_قدر in نالو): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[نالو]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(راههه.relative_to(저장소), 호출.lineno, نالو, 인자.arg))
    for لڪير in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, عمل_قدر_داخلا = لڪير.split('\t')
        if not (기준/현재).is_file(): 실패들.append('وڌايو_قدر فائل 없음: '+현재)
        if عمل_قدر_داخلا == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 داخلا_هنڌ 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for راههه in sorted((기준.parents[1]/'example/java').glob('*.java')):
        ماخذ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', راههه.read_text())
        for نالو in re.findall(r'\b[^\W\d]\w*\b', ماخذ, re.UNICODE):
            if نالو not in 예약어 and all(ord(ڪريڪٽر_قدر)<128 for ڪريڪٽر_قدر in نالو):
                실패들.append('{}: 예제의 영어 سڃاڻپ_ڪندڙ_قدر {}'.format(راههه.name, نالو))
    for نالو in ('창', 'بٽن', 'پرچي', 'متن_فيلڊ', '화면구성요소', 'واقعو_قطار', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ماخذ = (기준/'한국어자바/한국어/자체'/(نالو+'.java')).read_text()
        ماخذ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ماخذ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ماخذ):
            실패들.append(نالو+': 한국어 직접 구현에 표준 عنصر_قدر_2ed200e9 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for نالو in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if نالو in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 نالو: '+نالو)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for نالو in ('ڪلائوڊ_خاندان', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+نالو+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ميڪرو_قدر 사용: '+نالو)
    자바파일수 = 0
    for 뿌리 in ('ماخذ', 'صارف/자바', '한국어자바'):
        for راههه in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            ماخذ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', راههه.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ماخذ):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(راههه.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ماخذ):
                실패들.append('{}: 공개 예외 선언'.format(راههه.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for راههه in sorted((저장소/'os/ماخذ').glob('*.java')):
        x86자바파일수 += 1
        ماخذ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', راههه.read_text())
        for نالو in re.findall(r'\b[^\W\d]\w*\b', ماخذ, re.UNICODE):
            if نالو not in 예약어 | 표준자바이름 and all(ord(ڪريڪٽر_قدر)<128 for ڪريڪٽر_قدر in نالو):
                실패들.append('{}: 자체 영어 سڃاڻپ_ڪندڙ_قدر {}'.format(راههه.relative_to(저장소), نالو))
    لاگ_صف = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'اوزار/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(نقص) for نقص in 분석['نقص'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for داخلا_قدر in 분석['선언'].values():
            نالو = داخلا_قدر['نالو']; راههه = Path(داخلا_قدر['فائل'])
            ماخذ = راههه.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ماخذ[داخلا_قدر['آف_سيٽ_قدر']:داخلا_قدر['آف_سيٽ_قدر']+len(نالو)] == نالو.encode() and نالو not in 공개규약:
                실패들.append('{}:{}: {}'.format(راههه.relative_to(기준), داخلا_قدر['줄'], نالو))
        لاگ_صف['c_semantic_checked'] = True
        لاگ_صف['c_source_sha256'] = {str(Path(فائل).relative_to(기준)):هيش_فائل for فائل,هيش_فائل in 분석['원문해시'].items()}
    لاگ_صف['passed'] = not 실패들; لاگ_صف['failures'] = 실패들
    منزل_مقصود_قدر = 기준/'build/verification/naming'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    (منزل_مقصود_قدر/'report.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·فائل راههه·호환 داخلا_هنڌ·통신 예제')

if __name__ == '__main__': هلائڻ()
