#!/usr/bin/env python3
"""명명 ਕਲਿਪ·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
저장소 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]

def ਚਲਾਓ_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    실패들 = []
    ਕੰਮ_ਕੀਮਤ = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ਮਾਰਗ in list((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ').glob('*.py')) + list((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'예제').rglob('*.py')) + 공용번역기들:
        if ਮਾਰਗ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ਮਾਰਗ.read_text()); 나무들[ਮਾਰਗ] = 나무
        for ਦਾਖਲਾ_ਕੀਮਤ in ast.walk(나무):
            if isinstance(ਦਾਖਲਾ_ਕੀਮਤ, ast.FunctionDef):
                매개변수표.setdefault(ਦਾਖਲਾ_ਕੀਮਤ.name, set()).update(인자.arg for 인자 in ਦਾਖਲਾ_ਕੀਮਤ.args.args + ਦਾਖਲਾ_ਕੀਮਤ.args.kwonlyargs)
                if ਦਾਖਲਾ_ਕੀਮਤ.args.kwarg: 가변매개함수.add(ਦਾਖਲਾ_ਕੀਮਤ.name)
            if isinstance(ਦਾਖਲਾ_ਕੀਮਤ, ast.ClassDef):
                for ਫੰਗਸ਼ਨ_ਕੀਮਤ in ਦਾਖਲਾ_ਕੀਮਤ.body:
                    if isinstance(ਫੰਗਸ਼ਨ_ਕੀਮਤ, ast.FunctionDef) and ਫੰਗਸ਼ਨ_ਕੀਮਤ.name == '__init__':
                        매개변수표.setdefault(ਦਾਖਲਾ_ਕੀਮਤ.name, set()).update(인자.arg for 인자 in ਫੰਗਸ਼ਨ_ਕੀਮਤ.args.args + ਫੰਗਸ਼ਨ_ਕੀਮਤ.args.kwonlyargs)
            ਨਾਂ = ''
            if isinstance(ਦਾਖਲਾ_ਕੀਮਤ, (ast.FunctionDef, ast.ClassDef)): ਨਾਂ = ਦਾਖਲਾ_ਕੀਮਤ.name
            elif isinstance(ਦਾਖਲਾ_ਕੀਮਤ, ast.Name) and isinstance(ਦਾਖਲਾ_ਕੀਮਤ.ctx, ast.Store): ਨਾਂ = ਦਾਖਲਾ_ਕੀਮਤ.id
            elif isinstance(ਦਾਖਲਾ_ਕੀਮਤ, ast.arg): ਨਾਂ = ਦਾਖਲਾ_ਕੀਮਤ.arg
            if ਨਾਂ and ਨਾਂ not in ਕੰਮ_ਕੀਮਤ and all(ord(ਵਰਣ_ਕੀਮਤ)<128 for ਵਰਣ_ਕੀਮਤ in ਨਾਂ):
                실패들.append('{}:{}: {}'.format(ਮਾਰਗ.relative_to(저장소), ਦਾਖਲਾ_ਕੀਮਤ.lineno, ਨਾਂ))
    for ਮਾਰਗ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ਨਾਂ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ਨਾਂ not in 매개변수표 or ਨਾਂ in 가변매개함수 or not any(ord(ਵਰਣ_ਕੀਮਤ)>127 for ਵਰਣ_ਕੀਮਤ in ਨਾਂ): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[ਨਾਂ]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ਮਾਰਗ.relative_to(저장소), 호출.lineno, ਨਾਂ, 인자.arg))
    for ਲਾਈਨ in (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ = ਲਾਈਨ.split('\t')
        if not (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/현재).is_file(): 실패들.append('ਖਿਸਕਾਉਣਾ_ਕੀਮਤ ਫਾਇਲ 없음: '+현재)
        if ਕਾਰਵਾਈ_ਕੀਮਤ_ਦਾਖਲਾ == '호환진입점유지' and not (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/이전).is_file(): 실패들.append('호환 ਦਾਖਲਾ_ਪੌਇੰਟ 없음: '+이전)
    예제 = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ਮਾਰਗ in sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'example/java').glob('*.java')):
        ਸਰੋਤ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ਮਾਰਗ.read_text())
        for ਨਾਂ in re.findall(r'\b[^\W\d]\w*\b', ਸਰੋਤ, re.UNICODE):
            if ਨਾਂ not in 예약어 and all(ord(ਵਰਣ_ਕੀਮਤ)<128 for ਵਰਣ_ਕੀਮਤ in ਨਾਂ):
                실패들.append('{}: 예제의 영어 ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ {}'.format(ਮਾਰਗ.name, ਨਾਂ))
    for ਨਾਂ in ('창', 'ਬਟਨ', 'ਲੇਬਲ', 'ਟੈਕਸਟ_ਖੇਤਰ', '화면구성요소', 'ਇਵੈਂਟ_ਕਤਾਰ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ਸਰੋਤ = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'한국어자바/ਪੰਜਾਬੀ/자체'/(ਨਾਂ+'.java')).read_text()
        ਸਰੋਤ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ਸਰੋਤ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ਸਰੋਤ):
            실패들.append(ਨਾਂ+': ਪੰਜਾਬੀ 직접 구현에 표준 ਔਬਜੈਕਟ_ਕੀਮਤ 래퍼가 남았습니다.')
    시언어예제 = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'example/c/네트워크예제.c').read_text()
    for ਨਾਂ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ਨਾਂ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ਨਾਂ: '+ਨਾਂ)
    파이썬예제 = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ਨਾਂ in ('ਬੱਦਲ_ਪਰਿਵਾਰ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ਨਾਂ+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ਮੈਕ੍ਰੋ_ਕੀਮਤ 사용: '+ਨਾਂ)
    자바파일수 = 0
    for ਰੂਟ_ਕੀਮਤ in ('ਸਰੋਤ', 'ਉਪਭੋਗਤਾ/자바', '한국어자바'):
        for ਮਾਰਗ in (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/ਰੂਟ_ਕੀਮਤ).rglob('*.java'):
            자바파일수 += 1
            ਸਰੋਤ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ਮਾਰਗ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ਸਰੋਤ):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ), 맞음[1]))
            if ਰੂਟ_ਕੀਮਤ == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ਸਰੋਤ):
                실패들.append('{}: 공개 예외 선언'.format(ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ਮਾਰਗ in sorted((저장소/'os/ਸਰੋਤ').glob('*.java')):
        x86자바파일수 += 1
        ਸਰੋਤ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ਮਾਰਗ.read_text())
        for ਨਾਂ in re.findall(r'\b[^\W\d]\w*\b', ਸਰੋਤ, re.UNICODE):
            if ਨਾਂ not in 예약어 | 표준자바이름 and all(ord(ਵਰਣ_ਕੀਮਤ)<128 for ਵਰਣ_ਕੀਮਤ in ਨਾਂ):
                실패들.append('{}: 자체 영어 ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ_ਕੀਮਤ {}'.format(ਮਾਰਗ.relative_to(저장소), ਨਾਂ))
    ਲੌਗ_ਕਤਾਰ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if ਆਰਗੂਮੈਂਟ.시언어:
        subprocess.check_call(['python3', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/시언어이름분석.py')])
        분석 = json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ਗਲਤੀ) for ਗਲਤੀ in 분석['ਗਲਤੀ'])
        공개규약 = set(json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'명명/규격이름.json').read_text()))
        for ਦਾਖਲਾ_ਕੀਮਤ in 분석['선언'].values():
            ਨਾਂ = ਦਾਖਲਾ_ਕੀਮਤ['ਨਾਂ']; ਮਾਰਗ = Path(ਦਾਖਲਾ_ਕੀਮਤ['ਫਾਇਲ'])
            ਸਰੋਤ = ਮਾਰਗ.read_bytes()
            # ਪੰਜਾਬੀ 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ਸਰੋਤ[ਦਾਖਲਾ_ਕੀਮਤ['ਔਫਸੈਟ_ਕੀਮਤ']:ਦਾਖਲਾ_ਕੀਮਤ['ਔਫਸੈਟ_ਕੀਮਤ']+len(ਨਾਂ)] == ਨਾਂ.encode() and ਨਾਂ not in 공개규약:
                실패들.append('{}:{}: {}'.format(ਮਾਰਗ.relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ), ਦਾਖਲਾ_ਕੀਮਤ['ਲਾਈਨ'], ਨਾਂ))
        ਲੌਗ_ਕਤਾਰ['c_semantic_checked'] = True
        ਲੌਗ_ਕਤਾਰ['c_source_sha256'] = {str(Path(ਫਾਇਲ).relative_to(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ)):ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ for ਫਾਇਲ,ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ in 분석['원문해시'].items()}
    ਲੌਗ_ਕਤਾਰ['passed'] = not 실패들; ਲੌਗ_ਕਤਾਰ['failures'] = 실패들
    ਮੰਜਿਲ_ਕੀਮਤ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/naming'; ਮੰਜਿਲ_ਕੀਮਤ.mkdir(parents=True, exist_ok=True)
    (ਮੰਜਿਲ_ਕੀਮਤ/'report.json').write_text(json.dumps(ਲੌਗ_ਕਤਾਰ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: ਪੰਜਾਬੀ 선언·ਫਾਇਲ ਮਾਰਗ·호환 ਦਾਖਲਾ_ਪੌਇੰਟ·통신 예제')

if __name__ == '__main__': ਚਲਾਓ_2()
