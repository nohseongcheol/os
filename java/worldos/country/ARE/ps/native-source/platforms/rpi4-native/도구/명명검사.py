#!/usr/bin/env python3
"""명명 ټوټه·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ځغلول():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    کیس_ارزښت = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for يونلور in list((기준/'도구').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if يونلور.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(يونلور.read_text()); 나무들[يونلور] = 나무
        for ننوت_ارزښت in ast.walk(나무):
            if isinstance(ننوت_ارزښت, ast.FunctionDef):
                매개변수표.setdefault(ننوت_ارزښت.name, set()).update(인자.arg for 인자 in ننوت_ارزښت.args.args + ننوت_ارزښت.args.kwonlyargs)
                if ننوت_ارزښت.args.kwarg: 가변매개함수.add(ننوت_ارزښت.name)
            if isinstance(ننوت_ارزښت, ast.ClassDef):
                for 함수 in ننوت_ارزښت.body:
                    if isinstance(함수, ast.FunctionDef) and 함수.name == '__init__':
                        매개변수표.setdefault(ننوت_ارزښت.name, set()).update(인자.arg for 인자 in 함수.args.args + 함수.args.kwonlyargs)
            نوم = ''
            if isinstance(ننوت_ارزښت, (ast.FunctionDef, ast.ClassDef)): نوم = ننوت_ارزښت.name
            elif isinstance(ننوت_ارزښت, ast.Name) and isinstance(ننوت_ارزښت.ctx, ast.Store): نوم = ننوت_ارزښت.id
            elif isinstance(ننوت_ارزښت, ast.arg): نوم = ننوت_ارزښت.arg
            if نوم and نوم not in کیس_ارزښت and all(ord(لوښه_ارزښت)<128 for لوښه_ارزښت in نوم):
                실패들.append('{}:{}: {}'.format(يونلور.relative_to(저장소), ننوت_ارزښت.lineno, نوم))
    for يونلور, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            نوم = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if نوم not in 매개변수표 or نوم in 가변매개함수 or not any(ord(لوښه_ارزښت)>127 for لوښه_ارزښت in نوم): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[نوم]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(يونلور.relative_to(저장소), 호출.lineno, نوم, 인자.arg))
    for ليکه in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, 처리 = ليکه.split('\t')
        if not (기준/현재).is_file(): 실패들.append('이동 دوتنه 없음: '+현재)
        if 처리 == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ننوت_ټکى 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for يونلور in sorted((기준.parents[1]/'example/java').glob('*.java')):
        سرچينه = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', يونلور.read_text())
        for نوم in re.findall(r'\b[^\W\d]\w*\b', سرچينه, re.UNICODE):
            if نوم not in 예약어 and all(ord(لوښه_ارزښت)<128 for لوښه_ارزښت in نوم):
                실패들.append('{}: 예제의 영어 식별자 {}'.format(يونلور.name, نوم))
    for نوم in ('창', 'تڼۍ', 'نښکه', '입력칸', '화면구성요소', 'پېښه_ليکه', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        سرچينه = (기준/'한국어자바/한국어/자체'/(نوم+'.java')).read_text()
        سرچينه = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', سرچينه)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', سرچينه):
            실패들.append(نوم+': 한국어 직접 구현에 표준 객체 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for نوم in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if نوم in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 نوم: '+نوم)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for نوم in ('인터넷주소갈래', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+نوم+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 مېکرو_ارزښت 사용: '+نوم)
    자바파일수 = 0
    for 뿌리 in ('سرچينه', 'کارن/자바', '한국어자바'):
        for يونلور in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            سرچينه = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', يونلور.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', سرچينه):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(يونلور.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', سرچينه):
                실패들.append('{}: 공개 예외 선언'.format(يونلور.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for يونلور in sorted((저장소/'os/سرچينه').glob('*.java')):
        x86자바파일수 += 1
        سرچينه = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', يونلور.read_text())
        for نوم in re.findall(r'\b[^\W\d]\w*\b', سرچينه, re.UNICODE):
            if نوم not in 예약어 | 표준자바이름 and all(ord(لوښه_ارزښت)<128 for لوښه_ارزښت in نوم):
                실패들.append('{}: 자체 영어 식별자 {}'.format(يونلور.relative_to(저장소), نوم))
    خبرال_کیل = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'도구/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(تېروتنه) for تېروتنه in 분석['تېروتنه'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ننوت_ارزښت in 분석['선언'].values():
            نوم = ننوت_ارزښت['نوم']; يونلور = Path(ننوت_ارزښت['دوتنه'])
            سرچينه = يونلور.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if سرچينه[ننوت_ارزښت['변위']:ننوت_ارزښت['변위']+len(نوم)] == نوم.encode() and نوم not in 공개규약:
                실패들.append('{}:{}: {}'.format(يونلور.relative_to(기준), ننوت_ارزښت['줄'], نوم))
        خبرال_کیل['c_semantic_checked'] = True
        خبرال_کیل['c_source_sha256'] = {str(Path(دوتنه).relative_to(기준)):해시 for دوتنه,해시 in 분석['원문해시'].items()}
    خبرال_کیل['passed'] = not 실패들; خبرال_کیل['failures'] = 실패들
    موخه_ارزښت = 기준/'build/verification/naming'; موخه_ارزښت.mkdir(parents=True, exist_ok=True)
    (موخه_ارزښت/'report.json').write_text(json.dumps(خبرال_کیل, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·دوتنه يونلور·호환 ننوت_ټکى·통신 예제')

if __name__ == '__main__': ځغلول()
