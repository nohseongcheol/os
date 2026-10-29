#!/usr/bin/env python3
"""명명 کلیپ·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ڕادان():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    ئەرک_نرخ = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for گوزەر in list((기준/'ئامرازەکان').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if گوزەر.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(گوزەر.read_text()); 나무들[گوزەر] = 나무
        for تێنووسین_نرخ in ast.walk(나무):
            if isinstance(تێنووسین_نرخ, ast.FunctionDef):
                매개변수표.setdefault(تێنووسین_نرخ.name, set()).update(인자.arg for 인자 in تێنووسین_نرخ.args.args + تێنووسین_نرخ.args.kwonlyargs)
                if تێنووسین_نرخ.args.kwarg: 가변매개함수.add(تێنووسین_نرخ.name)
            if isinstance(تێنووسین_نرخ, ast.ClassDef):
                for کردار_نرخ in تێنووسین_نرخ.body:
                    if isinstance(کردار_نرخ, ast.FunctionDef) and کردار_نرخ.name == '__init__':
                        매개변수표.setdefault(تێنووسین_نرخ.name, set()).update(인자.arg for 인자 in کردار_نرخ.args.args + کردار_نرخ.args.kwonlyargs)
            ناو = ''
            if isinstance(تێنووسین_نرخ, (ast.FunctionDef, ast.ClassDef)): ناو = تێنووسین_نرخ.name
            elif isinstance(تێنووسین_نرخ, ast.Name) and isinstance(تێنووسین_نرخ.ctx, ast.Store): ناو = تێنووسین_نرخ.id
            elif isinstance(تێنووسین_نرخ, ast.arg): ناو = تێنووسین_نرخ.arg
            if ناو and ناو not in ئەرک_نرخ and all(ord(نووسە_نرخ)<128 for نووسە_نرخ in ناو):
                실패들.append('{}:{}: {}'.format(گوزەر.relative_to(저장소), تێنووسین_نرخ.lineno, ناو))
    for گوزەر, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ناو = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ناو not in 매개변수표 or ناو in 가변매개함수 or not any(ord(نووسە_نرخ)>127 for نووسە_نرخ in ناو): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[ناو]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(گوزەر.relative_to(저장소), 호출.lineno, ناو, 인자.arg))
    for دێڕ in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, پرۆسە_نرخ_تێنووسین = دێڕ.split('\t')
        if not (기준/현재).is_file(): 실패들.append('گواستنەوە_نرخ فایل 없음: '+현재)
        if پرۆسە_نرخ_تێنووسین == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 تێنووسین_خاڵ 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for گوزەر in sorted((기준.parents[1]/'example/java').glob('*.java')):
        ژێدەر = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', گوزەر.read_text())
        for ناو in re.findall(r'\b[^\W\d]\w*\b', ژێدەر, re.UNICODE):
            if ناو not in 예약어 and all(ord(نووسە_نرخ)<128 for نووسە_نرخ in ناو):
                실패들.append('{}: 예제의 영어 ناسێنەر_نرخ {}'.format(گوزەر.name, ناو))
    for ناو in ('창', 'دوگمه', 'نیشانە', 'دەق_خانە', '화면구성요소', 'پێشهات_ڕیز', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ژێدەر = (기준/'한국어자바/한국어/자체'/(ناو+'.java')).read_text()
        ژێدەر = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ژێدەر)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ژێدەر):
            실패들.append(ناو+': 한국어 직접 구현에 표준 شت_نرخ 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for ناو in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ناو in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ناو: '+ناو)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ناو in ('هەور_خێزان', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ناو+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ماکرۆ_نرخ 사용: '+ناو)
    자바파일수 = 0
    for 뿌리 in ('ژێدەر', 'بەکارهێنەر/자바', '한국어자바'):
        for گوزەر in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            ژێدەر = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', گوزەر.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ژێدەر):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(گوزەر.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ژێدەر):
                실패들.append('{}: 공개 예외 선언'.format(گوزەر.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for گوزەر in sorted((저장소/'os/ژێدەر').glob('*.java')):
        x86자바파일수 += 1
        ژێدەر = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', گوزەر.read_text())
        for ناو in re.findall(r'\b[^\W\d]\w*\b', ژێدەر, re.UNICODE):
            if ناو not in 예약어 | 표준자바이름 and all(ord(نووسە_نرخ)<128 for نووسە_نرخ in ناو):
                실패들.append('{}: 자체 영어 ناسێنەر_نرخ {}'.format(گوزەر.relative_to(저장소), ناو))
    تۆمار_ڕزن = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'ئامرازەکان/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(هەڵە) for هەڵە in 분석['هەڵە'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for تێنووسین_نرخ in 분석['선언'].values():
            ناو = تێنووسین_نرخ['ناو']; گوزەر = Path(تێنووسین_نرخ['فایل'])
            ژێدەر = گوزەر.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ژێدەر[تێنووسین_نرخ['ئۆفسێت_نرخ']:تێنووسین_نرخ['ئۆفسێت_نرخ']+len(ناو)] == ناو.encode() and ناو not in 공개규약:
                실패들.append('{}:{}: {}'.format(گوزەر.relative_to(기준), تێنووسین_نرخ['줄'], ناو))
        تۆمار_ڕزن['c_semantic_checked'] = True
        تۆمار_ڕزن['c_source_sha256'] = {str(Path(فایل).relative_to(기준)):دەرەنجام_فایل for فایل,دەرەنجام_فایل in 분석['원문해시'].items()}
    تۆمار_ڕزن['passed'] = not 실패들; تۆمار_ڕزن['failures'] = 실패들
    جێمەبەست_نرخ = 기준/'build/verification/naming'; جێمەبەست_نرخ.mkdir(parents=True, exist_ok=True)
    (جێمەبەست_نرخ/'report.json').write_text(json.dumps(تۆمار_ڕزن, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·فایل گوزەر·호환 تێنووسین_خاڵ·통신 예제')

if __name__ == '__main__': ڕادان()
