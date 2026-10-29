#!/usr/bin/env python3
"""명명 범위·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Bimeşîne():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    규약 = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for RÊ in list((기준/'도구').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if RÊ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(RÊ.read_text()); 나무들[RÊ] = 나무
        for 항목 in ast.walk(나무):
            if isinstance(항목, ast.FunctionDef):
                매개변수표.setdefault(항목.name, set()).update(인자.arg for 인자 in 항목.args.args + 항목.args.kwonlyargs)
                if 항목.args.kwarg: 가변매개함수.add(항목.name)
            if isinstance(항목, ast.ClassDef):
                for 함수 in 항목.body:
                    if isinstance(함수, ast.FunctionDef) and 함수.name == '__init__':
                        매개변수표.setdefault(항목.name, set()).update(인자.arg for 인자 in 함수.args.args + 함수.args.kwonlyargs)
            Nav = ''
            if isinstance(항목, (ast.FunctionDef, ast.ClassDef)): Nav = 항목.name
            elif isinstance(항목, ast.Name) and isinstance(항목.ctx, ast.Store): Nav = 항목.id
            elif isinstance(항목, ast.arg): Nav = 항목.arg
            if Nav and Nav not in 규약 and all(ord(글자)<128 for 글자 in Nav):
                실패들.append('{}:{}: {}'.format(RÊ.relative_to(저장소), 항목.lineno, Nav))
    for RÊ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nav = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nav not in 매개변수표 or Nav in 가변매개함수 or not any(ord(글자)>127 for 글자 in Nav): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Nav]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(RÊ.relative_to(저장소), 호출.lineno, Nav, 인자.arg))
    for 줄 in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, 처리 = 줄.split('\t')
        if not (기준/현재).is_file(): 실패들.append('이동 Pel 없음: '+현재)
        if 처리 == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 진입점 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for RÊ in sorted((기준.parents[1]/'example/java').glob('*.java')):
        ÇAVKANÎ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', RÊ.read_text())
        for Nav in re.findall(r'\b[^\W\d]\w*\b', ÇAVKANÎ, re.UNICODE):
            if Nav not in 예약어 and all(ord(글자)<128 for 글자 in Nav):
                실패들.append('{}: 예제의 영어 식별자 {}'.format(RÊ.name, Nav))
    for Nav in ('창', '단추', '글표지', '입력칸', '화면구성요소', '화면일정', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ÇAVKANÎ = (기준/'한국어자바/한국어/자체'/(Nav+'.java')).read_text()
        ÇAVKANÎ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ÇAVKANÎ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ÇAVKANÎ):
            실패들.append(Nav+': 한국어 직접 구현에 표준 객체 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Nav in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nav in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nav: '+Nav)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nav in ('인터넷주소갈래', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Nav+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 매크로 사용: '+Nav)
    자바파일수 = 0
    for 뿌리 in ('ÇAVKANÎ', '사용자/자바', '한국어자바'):
        for RÊ in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            ÇAVKANÎ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', RÊ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ÇAVKANÎ):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(RÊ.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ÇAVKANÎ):
                실패들.append('{}: 공개 예외 선언'.format(RÊ.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for RÊ in sorted((저장소/'os/ÇAVKANÎ').glob('*.java')):
        x86자바파일수 += 1
        ÇAVKANÎ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', RÊ.read_text())
        for Nav in re.findall(r'\b[^\W\d]\w*\b', ÇAVKANÎ, re.UNICODE):
            if Nav not in 예약어 | 표준자바이름 and all(ord(글자)<128 for 글자 in Nav):
                실패들.append('{}: 자체 영어 식별자 {}'.format(RÊ.relative_to(저장소), Nav))
    기록 = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'도구/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Çewtî) for Çewtî in 분석['Çewtî'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for 항목 in 분석['선언'].values():
            Nav = 항목['Nav']; RÊ = Path(항목['Pel'])
            ÇAVKANÎ = RÊ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ÇAVKANÎ[항목['변위']:항목['변위']+len(Nav)] == Nav.encode() and Nav not in 공개규약:
                실패들.append('{}:{}: {}'.format(RÊ.relative_to(기준), 항목['줄'], Nav))
        기록['c_semantic_checked'] = True
        기록['c_source_sha256'] = {str(Path(Pel).relative_to(기준)):해시 for Pel,해시 in 분석['원문해시'].items()}
    기록['passed'] = not 실패들; 기록['failures'] = 실패들
    목적 = 기준/'build/verification/naming'; 목적.mkdir(parents=True, exist_ok=True)
    (목적/'report.json').write_text(json.dumps(기록, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Pel RÊ·호환 진입점·통신 예제')

if __name__ == '__main__': Bimeşîne()
