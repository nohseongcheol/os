#!/usr/bin/env python3
"""명명 ক্লিপ·ব্যতিক্রম·경로를 검사한다. --시언어는 libclang ঘোষণা 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
সংগ্রহস্থলের_মূল = প্রকল্প_মূল.parents[1]

def চালনা():
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('--시언어', action='store_true')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    실패들 = []
    কাজ_মান = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    প্যারামিটার_সারণি = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [সংগ্রহস্থলের_মূল/'compiler/컴파일러.py', সংগ্রহস্থলের_মূল/'compiler/기계어미리번역.py']
    for পথ_2 in list((প্রকল্প_মূল/'সরঞ্জামগুলি').glob('*.py')) + list((প্রকল্প_মূল/'예제').rglob('*.py')) + 공용번역기들:
        if পথ_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(পথ_2.read_text()); 나무들[পথ_2] = 나무
        for ভুক্তি_মান in ast.walk(나무):
            if isinstance(ভুক্তি_মান, ast.FunctionDef):
                প্যারামিটার_সারণি.setdefault(ভুক্তি_মান.name, set()).update(প্যারামিটার_যুক্তি.arg for প্যারামিটার_যুক্তি in ভুক্তি_মান.args.args + ভুক্তি_মান.args.kwonlyargs)
                if ভুক্তি_মান.args.kwarg: 가변매개함수.add(ভুক্তি_মান.name)
            if isinstance(ভুক্তি_মান, ast.ClassDef):
                for ফাংশন_মান in ভুক্তি_মান.body:
                    if isinstance(ফাংশন_মান, ast.FunctionDef) and ফাংশন_মান.name == '__init__':
                        প্যারামিটার_সারণি.setdefault(ভুক্তি_মান.name, set()).update(প্যারামিটার_যুক্তি.arg for প্যারামিটার_যুক্তি in ফাংশন_মান.args.args + ফাংশন_মান.args.kwonlyargs)
            নাম = ''
            if isinstance(ভুক্তি_মান, (ast.FunctionDef, ast.ClassDef)): নাম = ভুক্তি_মান.name
            elif isinstance(ভুক্তি_মান, ast.Name) and isinstance(ভুক্তি_মান.ctx, ast.Store): নাম = ভুক্তি_মান.id
            elif isinstance(ভুক্তি_মান, ast.arg): নাম = ভুক্তি_মান.arg
            if নাম and নাম not in কাজ_মান and all(ord(অক্ষর_মান)<128 for অক্ষর_মান in নাম):
                실패들.append('{}:{}: {}'.format(পথ_2.relative_to(সংগ্রহস্থলের_মূল), ভুক্তি_মান.lineno, নাম))
    for পথ_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            নাম = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if নাম not in প্যারামিটার_সারণি or নাম in 가변매개함수 or not any(ord(অক্ষর_মান)>127 for অক্ষর_মান in নাম): continue
            for প্যারামিটার_যুক্তি in 호출.keywords:
                if প্যারামিটার_যুক্তি.arg and প্যারামিটার_যুক্তি.arg not in প্যারামিটার_সারণি[নাম]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(পথ_2.relative_to(সংগ্রহস্থলের_মূল), 호출.lineno, নাম, প্যারামিটার_যুক্তি.arg))
    for নিবেশের_পঙ্_ক্তি in (প্রকল্প_মূল/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, প্রসেসর_মান_ভুক্তি = নিবেশের_পঙ্_ক্তি.split('\t')
        if not (প্রকল্প_মূল/현재).is_file(): 실패들.append('অপসারণ_করা_মান নথির_নাম 없음: '+현재)
        if প্রসেসর_মান_ভুক্তি == '호환진입점유지' and not (প্রকল্প_মূল/이전).is_file(): 실패들.append('호환 ভুক্তি_বিন্দু 없음: '+이전)
    예제 = (প্রকল্প_মূল.parents[1]/'example/java/নেটওয়ার্ক.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for পথ_2 in sorted((প্রকল্প_মূল.parents[1]/'example/java').glob('*.java')):
        উৎস_নথি = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', পথ_2.read_text())
        for নাম in re.findall(r'\b[^\W\d]\w*\b', উৎস_নথি, re.UNICODE):
            if নাম not in 예약어 and all(ord(অক্ষর_মান)<128 for অক্ষর_মান in নাম):
                실패들.append('{}: 예제의 영어 সনাক্তকারী_মান {}'.format(পথ_2.name, নাম))
    for নাম in ('창', 'বোতাম', 'লেবেল', 'পাঠ্য_ক্ষেত্র', '화면구성요소', 'ঘটনা_সারিবদ্ধ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        উৎস_নথি = (প্রকল্প_মূল/'한국어자바/বাংলা/নিজ'/(নাম+'.java')).read_text()
        উৎস_নথি = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', উৎস_নথি)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', উৎস_নথি):
            실패들.append(নাম+': বাংলা 직접 구현에 표준 বস্তু_মান 래퍼가 남았습니다.')
    시언어예제 = (প্রকল্প_মূল.parents[1]/'example/c/নেটওয়ার্ক.c').read_text()
    for নাম in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if নাম in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 নাম: '+নাম)
    파이썬예제 = (প্রকল্প_মূল.parents[1]/'example/python/নেটওয়ার্ক.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ব্যতিক্রম 직접 사용')
    머리 = (প্রকল্প_মূল.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for নাম in ('ক্লাউড_পরিবার', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+নাম+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ম্যাক্রো_মান 사용: '+নাম)
    자바파일수 = 0
    for মূল_মান in ('উৎস_নথি', 'ব্যবহারকারী/자바', '한국어자바'):
        for পথ_2 in (প্রকল্প_মূল/মূল_মান).rglob('*.java'):
            자바파일수 += 1
            উৎস_নথি = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', পথ_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', উৎস_নথি):
                실패들.append('{}: 한국어화되지 않은 ঘোষণা {}'.format(পথ_2.relative_to(প্রকল্প_মূল), 맞음[1]))
            if মূল_মান == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', উৎস_নথি):
                실패들.append('{}: 공개 ব্যতিক্রম ঘোষণা'.format(পথ_2.relative_to(প্রকল্প_মূল)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for পথ_2 in sorted((সংগ্রহস্থলের_মূল/'os/উৎস_নথি').glob('*.java')):
        x86자바파일수 += 1
        উৎস_নথি = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', পথ_2.read_text())
        for নাম in re.findall(r'\b[^\W\d]\w*\b', উৎস_নথি, re.UNICODE):
            if নাম not in 예약어 | 표준자바이름 and all(ord(অক্ষর_মান)<128 for অক্ষর_মান in নাম):
                실패들.append('{}: নিজ 영어 সনাক্তকারী_মান {}'.format(পথ_2.relative_to(সংগ্রহস্থলের_মূল), নাম))
    লগ_সারি = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if আর্গুমেন্ট_তালিকা.시언어:
        subprocess.check_call(['python3', str(প্রকল্প_মূল/'সরঞ্জামগুলি/시언어이름분석.py')])
        분석 = json.loads((প্রকল্প_মূল/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ত্রুটি) for ত্রুটি in 분석['ত্রুটি'])
        공개규약 = set(json.loads((প্রকল্প_মূল/'명명/규격이름.json').read_text()))
        for ভুক্তি_মান in 분석['ঘোষণা'].values():
            নাম = ভুক্তি_মান['নাম']; পথ_2 = Path(ভুক্তি_মান['নথির_নাম'])
            উৎস_নথি = পথ_2.read_bytes()
            # বাংলা 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if উৎস_নথি[ভুক্তি_মান['অফসেট_মান']:ভুক্তি_মান['অফসেট_মান']+len(নাম)] == নাম.encode() and নাম not in 공개규약:
                실패들.append('{}:{}: {}'.format(পথ_2.relative_to(প্রকল্প_মূল), ভুক্তি_মান['নিবেশের_পঙ্_ক্তি'], নাম))
        লগ_সারি['c_semantic_checked'] = True
        লগ_সারি['c_source_sha256'] = {str(Path(নথির_নাম).relative_to(প্রকল্প_মূল)):হ্যাশ_ফাইল for নথির_নাম,হ্যাশ_ফাইল in 분석['원문해시'].items()}
    লগ_সারি['passed'] = not 실패들; লগ_সারি['failures'] = 실패들
    গন্তব্য_মান = প্রকল্প_মূল/'build/verification/naming'; গন্তব্য_মান.mkdir(parents=True, exist_ok=True)
    (গন্তব্য_মান/'report.json').write_text(json.dumps(লগ_সারি, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: বাংলা ঘোষণা·নথির_নাম পথ_2·호환 ভুক্তি_বিন্দু·통신 예제')

if __name__ == '__main__': চালনা()
