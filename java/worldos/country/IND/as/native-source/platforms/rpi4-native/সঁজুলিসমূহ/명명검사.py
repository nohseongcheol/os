#!/usr/bin/env python3
"""명명 ক্লিপ·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def সঞ্চালন():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    কেছ_মান = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for পথ in list((기준/'সঁজুলিসমূহ').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if পথ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(পথ.read_text()); 나무들[পথ] = 나무
        for প্রবিষ্ট_মান in ast.walk(나무):
            if isinstance(প্রবিষ্ট_মান, ast.FunctionDef):
                매개변수표.setdefault(প্রবিষ্ট_মান.name, set()).update(인자.arg for 인자 in প্রবিষ্ট_মান.args.args + প্রবিষ্ট_মান.args.kwonlyargs)
                if প্রবিষ্ট_মান.args.kwarg: 가변매개함수.add(প্রবিষ্ট_মান.name)
            if isinstance(প্রবিষ্ট_মান, ast.ClassDef):
                for ফাংছন_মান in প্রবিষ্ট_মান.body:
                    if isinstance(ফাংছন_মান, ast.FunctionDef) and ফাংছন_মান.name == '__init__':
                        매개변수표.setdefault(প্রবিষ্ট_মান.name, set()).update(인자.arg for 인자 in ফাংছন_মান.args.args + ফাংছন_মান.args.kwonlyargs)
            নাম = ''
            if isinstance(প্রবিষ্ট_মান, (ast.FunctionDef, ast.ClassDef)): নাম = প্রবিষ্ট_মান.name
            elif isinstance(প্রবিষ্ট_মান, ast.Name) and isinstance(প্রবিষ্ট_মান.ctx, ast.Store): নাম = প্রবিষ্ট_মান.id
            elif isinstance(প্রবিষ্ট_মান, ast.arg): নাম = প্রবিষ্ট_মান.arg
            if নাম and নাম not in কেছ_মান and all(ord(বৰ্ণ_মান)<128 for বৰ্ণ_মান in নাম):
                실패들.append('{}:{}: {}'.format(পথ.relative_to(저장소), প্রবিষ্ট_মান.lineno, নাম))
    for পথ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            নাম = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if নাম not in 매개변수표 or নাম in 가변매개함수 or not any(ord(বৰ্ণ_মান)>127 for বৰ্ণ_মান in নাম): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[নাম]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(পথ.relative_to(저장소), 호출.lineno, নাম, 인자.arg))
    for লাইন in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, প্ৰক্ৰিয়া_মান_প্রবিষ্ট = লাইন.split('\t')
        if not (기준/현재).is_file(): 실패들.append('লৈ_যাওক_মান নথিপত্ৰ 없음: '+현재)
        if প্ৰক্ৰিয়া_মান_প্রবিষ্ট == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 প্রবিষ্ট_পইণ্ট 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for পথ in sorted((기준.parents[1]/'example/java').glob('*.java')):
        উৎস = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', পথ.read_text())
        for নাম in re.findall(r'\b[^\W\d]\w*\b', উৎস, re.UNICODE):
            if নাম not in 예약어 and all(ord(বৰ্ণ_মান)<128 for বৰ্ণ_মান in নাম):
                실패들.append('{}: 예제의 영어 চিনাক্তকাৰী_মান {}'.format(পথ.name, নাম))
    for নাম in ('창', 'বুটাম', 'লেবেল', 'পাঠৰ_ক্ষেত্ৰ', '화면구성요소', 'ইভেণ্ট_লানি', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        উৎস = (기준/'한국어자바/한국어/자체'/(নাম+'.java')).read_text()
        উৎস = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', উৎস)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', উৎস):
            실패들.append(নাম+': 한국어 직접 구현에 표준 অবজেক্ট_মান 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for নাম in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if নাম in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 নাম: '+নাম)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for নাম in ('ক্লাউড_পৰিয়াল', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+নাম+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 মেক্ৰ_মান 사용: '+নাম)
    자바파일수 = 0
    for ৰুট_মান in ('উৎস', 'ব্যৱহাৰকৰ্তা/자바', '한국어자바'):
        for পথ in (기준/ৰুট_মান).rglob('*.java'):
            자바파일수 += 1
            উৎস = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', পথ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', উৎস):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(পথ.relative_to(기준), 맞음[1]))
            if ৰুট_মান == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', উৎস):
                실패들.append('{}: 공개 예외 선언'.format(পথ.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for পথ in sorted((저장소/'os/উৎস').glob('*.java')):
        x86자바파일수 += 1
        উৎস = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', পথ.read_text())
        for নাম in re.findall(r'\b[^\W\d]\w*\b', উৎস, re.UNICODE):
            if নাম not in 예약어 | 표준자바이름 and all(ord(বৰ্ণ_মান)<128 for বৰ্ণ_মান in নাম):
                실패들.append('{}: 자체 영어 চিনাক্তকাৰী_মান {}'.format(পথ.relative_to(저장소), নাম))
    লগ_শাৰী = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'সঁজুলিসমূহ/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ত্ৰুটি) for ত্ৰুটি in 분석['ত্ৰুটি'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for প্রবিষ্ট_মান in 분석['선언'].values():
            নাম = প্রবিষ্ট_মান['নাম']; পথ = Path(প্রবিষ্ট_মান['নথিপত্ৰ'])
            উৎস = পথ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if উৎস[প্রবিষ্ট_মান['অফছেট_মান']:প্রবিষ্ট_মান['অফছেট_মান']+len(নাম)] == নাম.encode() and নাম not in 공개규약:
                실패들.append('{}:{}: {}'.format(পথ.relative_to(기준), প্রবিষ্ট_মান['줄'], নাম))
        লগ_শাৰী['c_semantic_checked'] = True
        লগ_শাৰী['c_source_sha256'] = {str(Path(নথিপত্ৰ).relative_to(기준)):হেচ_ফাইল for নথিপত্ৰ,হেচ_ফাইল in 분석['원문해시'].items()}
    লগ_শাৰী['passed'] = not 실패들; লগ_শাৰী['failures'] = 실패들
    গন্তব্য_স্থান_মান = 기준/'build/verification/naming'; গন্তব্য_স্থান_মান.mkdir(parents=True, exist_ok=True)
    (গন্তব্য_স্থান_মান/'report.json').write_text(json.dumps(লগ_শাৰী, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·নথিপত্ৰ পথ·호환 প্রবিষ্ট_পইণ্ট·통신 예제')

if __name__ == '__main__': সঞ্চালন()
