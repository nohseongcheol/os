#!/usr/bin/env python3
"""명명 تراشہ·استثنا·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]
저장소 = عکس_ڈالنا_روٹ.parents[1]

def چلائیں():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    دلائل = 해석기.parse_args()
    실패들 = []
    جاب_قدر = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    پیرا_میٹر_جدول = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for راستہ_2 in list((عکس_ڈالنا_روٹ/'ٹولز').glob('*.py')) + list((عکس_ڈالنا_روٹ/'예제').rglob('*.py')) + 공용번역기들:
        if راستہ_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(راستہ_2.read_text()); 나무들[راستہ_2] = 나무
        for اندراج_قدر in ast.walk(나무):
            if isinstance(اندراج_قدر, ast.FunctionDef):
                پیرا_میٹر_جدول.setdefault(اندراج_قدر.name, set()).update(پیرا_میٹر_دلائل.arg for پیرا_میٹر_دلائل in اندراج_قدر.args.args + اندراج_قدر.args.kwonlyargs)
                if اندراج_قدر.args.kwarg: 가변매개함수.add(اندراج_قدر.name)
            if isinstance(اندراج_قدر, ast.ClassDef):
                for فعل_قدر in اندراج_قدر.body:
                    if isinstance(فعل_قدر, ast.FunctionDef) and فعل_قدر.name == '__init__':
                        پیرا_میٹر_جدول.setdefault(اندراج_قدر.name, set()).update(پیرا_میٹر_دلائل.arg for پیرا_میٹر_دلائل in فعل_قدر.args.args + فعل_قدر.args.kwonlyargs)
            نام = ''
            if isinstance(اندراج_قدر, (ast.FunctionDef, ast.ClassDef)): نام = اندراج_قدر.name
            elif isinstance(اندراج_قدر, ast.Name) and isinstance(اندراج_قدر.ctx, ast.Store): نام = اندراج_قدر.id
            elif isinstance(اندراج_قدر, ast.arg): نام = اندراج_قدر.arg
            if نام and نام not in جاب_قدر and all(ord(کریکٹر_قدر)<128 for کریکٹر_قدر in نام):
                실패들.append('{}:{}: {}'.format(راستہ_2.relative_to(저장소), اندراج_قدر.lineno, نام))
    for راستہ_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            نام = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if نام not in پیرا_میٹر_جدول or نام in 가변매개함수 or not any(ord(کریکٹر_قدر)>127 for کریکٹر_قدر in نام): continue
            for پیرا_میٹر_دلائل in 호출.keywords:
                if پیرا_میٹر_دلائل.arg and پیرا_میٹر_دلائل.arg not in پیرا_میٹر_جدول[نام]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(راستہ_2.relative_to(저장소), 호출.lineno, نام, پیرا_میٹر_دلائل.arg))
    for اندراج_کی_سطر in (عکس_ڈالنا_روٹ/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, عمل_قدر_اندراج = اندراج_کی_سطر.split('\t')
        if not (عکس_ڈالنا_روٹ/현재).is_file(): 실패들.append('منتقل_کریں_قدر فائل_کا_نام 없음: '+현재)
        if عمل_قدر_اندراج == '호환진입점유지' and not (عکس_ڈالنا_روٹ/이전).is_file(): 실패들.append('호환 اندراج_نقطہ 없음: '+이전)
    예제 = (عکس_ڈالنا_روٹ.parents[1]/'example/java/نیٹورکمثال.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for راستہ_2 in sorted((عکس_ڈالنا_روٹ.parents[1]/'example/java').glob('*.java')):
        ماخذ_فائل = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', راستہ_2.read_text())
        for نام in re.findall(r'\b[^\W\d]\w*\b', ماخذ_فائل, re.UNICODE):
            if نام not in 예약어 and all(ord(کریکٹر_قدر)<128 for کریکٹر_قدر in نام):
                실패들.append('{}: 예제의 영어 شناخت_کنندہ_قدر {}'.format(راستہ_2.name, نام))
    for نام in ('ونڈو', 'بٹن', 'سرنامہ', 'متن_فیلڈ', '화면구성요소', 'ایونٹ_قطار', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ماخذ_فائل = (عکس_ڈالنا_روٹ/'한국어자바/اردو/اپنا'/(نام+'.java')).read_text()
        ماخذ_فائل = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ماخذ_فائل)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ماخذ_فائل):
            실패들.append(نام+': اردو 직접 구현에 표준 آبجیکٹ_قدر 래퍼가 남았습니다.')
    시언어예제 = (عکس_ڈالنا_روٹ.parents[1]/'example/c/نیٹورکمثال.c').read_text()
    for نام in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if نام in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 نام: '+نام)
    파이썬예제 = (عکس_ڈالنا_روٹ.parents[1]/'example/python/نیٹورکمثال.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 استثنا 직접 사용')
    머리 = (عکس_ڈالنا_روٹ.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for نام in ('بادل_خاندان', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+نام+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 میکرو_قدر 사용: '+نام)
    자바파일수 = 0
    for روٹ_قدر in ('ماخذ_فائل', 'صارف/자바', '한국어자바'):
        for راستہ_2 in (عکس_ڈالنا_روٹ/روٹ_قدر).rglob('*.java'):
            자바파일수 += 1
            ماخذ_فائل = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', راستہ_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ماخذ_فائل):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(راستہ_2.relative_to(عکس_ڈالنا_روٹ), 맞음[1]))
            if روٹ_قدر == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ماخذ_فائل):
                실패들.append('{}: 공개 استثنا 선언'.format(راستہ_2.relative_to(عکس_ڈالنا_روٹ)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for راستہ_2 in sorted((저장소/'os/ماخذ_فائل').glob('*.java')):
        x86자바파일수 += 1
        ماخذ_فائل = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', راستہ_2.read_text())
        for نام in re.findall(r'\b[^\W\d]\w*\b', ماخذ_فائل, re.UNICODE):
            if نام not in 예약어 | 표준자바이름 and all(ord(کریکٹر_قدر)<128 for کریکٹر_قدر in نام):
                실패들.append('{}: اپنا 영어 شناخت_کنندہ_قدر {}'.format(راستہ_2.relative_to(저장소), نام))
    لاگ_صف = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if دلائل.시언어:
        subprocess.check_call(['python3', str(عکس_ڈالنا_روٹ/'ٹولز/시언어이름분석.py')])
        분석 = json.loads((عکس_ڈالنا_روٹ/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(غلطی) for غلطی in 분석['غلطی'])
        공개규약 = set(json.loads((عکس_ڈالنا_روٹ/'명명/규격이름.json').read_text()))
        for اندراج_قدر in 분석['선언'].values():
            نام = اندراج_قدر['نام']; راستہ_2 = Path(اندراج_قدر['فائل_کا_نام'])
            ماخذ_فائل = راستہ_2.read_bytes()
            # اردو 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ماخذ_فائل[اندراج_قدر['آفسٹ_قدر']:اندراج_قدر['آفسٹ_قدر']+len(نام)] == نام.encode() and نام not in 공개규약:
                실패들.append('{}:{}: {}'.format(راستہ_2.relative_to(عکس_ڈالنا_روٹ), اندراج_قدر['اندراج_کی_سطر'], نام))
        لاگ_صف['c_semantic_checked'] = True
        لاگ_صف['c_source_sha256'] = {str(Path(فائل_کا_نام).relative_to(عکس_ڈالنا_روٹ)):ہيش_فائل for فائل_کا_نام,ہيش_فائل in 분석['원문해시'].items()}
    لاگ_صف['passed'] = not 실패들; لاگ_صف['failures'] = 실패들
    منزل_مقصود_قدر = عکس_ڈالنا_روٹ/'build/verification/naming'; منزل_مقصود_قدر.mkdir(parents=True, exist_ok=True)
    (منزل_مقصود_قدر/'report.json').write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: اردو 선언·فائل_کا_نام راستہ_2·호환 اندراج_نقطہ·통신 예제')

if __name__ == '__main__': چلائیں()
