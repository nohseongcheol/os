#!/usr/bin/env python3
"""명명 ક્લિપ·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]
저장소 = પ્રોજેક્ટ_રૂટ.parents[1]

def ચલાવો_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    દલીલો = 해석기.parse_args()
    실패들 = []
    કામ_મૂલ્ય = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    પેરામીટર_કોષ્ટક = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for પથ in list((પ્રોજેક્ટ_રૂટ/'ઉપકરણો').glob('*.py')) + list((પ્રોજેક્ટ_રૂટ/'예제').rglob('*.py')) + 공용번역기들:
        if પથ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(પથ.read_text()); 나무들[પથ] = 나무
        for પ્રવેશ_મૂલ્ય in ast.walk(나무):
            if isinstance(પ્રવેશ_મૂલ્ય, ast.FunctionDef):
                પેરામીટર_કોષ્ટક.setdefault(પ્રવેશ_મૂલ્ય.name, set()).update(પેરામીટર_દલીલ.arg for પેરામીટર_દલીલ in પ્રવેશ_મૂલ્ય.args.args + પ્રવેશ_મૂલ્ય.args.kwonlyargs)
                if પ્રવેશ_મૂલ્ય.args.kwarg: 가변매개함수.add(પ્રવેશ_મૂલ્ય.name)
            if isinstance(પ્રવેશ_મૂલ્ય, ast.ClassDef):
                for ફંક્શંસ_મૂલ્ય in પ્રવેશ_મૂલ્ય.body:
                    if isinstance(ફંક્શંસ_મૂલ્ય, ast.FunctionDef) and ફંક્શંસ_મૂલ્ય.name == '__init__':
                        પેરામીટર_કોષ્ટક.setdefault(પ્રવેશ_મૂલ્ય.name, set()).update(પેરામીટર_દલીલ.arg for પેરામીટર_દલીલ in ફંક્શંસ_મૂલ્ય.args.args + ફંક્શંસ_મૂલ્ય.args.kwonlyargs)
            નામ = ''
            if isinstance(પ્રવેશ_મૂલ્ય, (ast.FunctionDef, ast.ClassDef)): નામ = પ્રવેશ_મૂલ્ય.name
            elif isinstance(પ્રવેશ_મૂલ્ય, ast.Name) and isinstance(પ્રવેશ_મૂલ્ય.ctx, ast.Store): નામ = પ્રવેશ_મૂલ્ય.id
            elif isinstance(પ્રવેશ_મૂલ્ય, ast.arg): નામ = પ્રવેશ_મૂલ્ય.arg
            if નામ and નામ not in કામ_મૂલ્ય and all(ord(વર્ણ_મૂલ્ય)<128 for વર્ણ_મૂલ્ય in નામ):
                실패들.append('{}:{}: {}'.format(પથ.relative_to(저장소), પ્રવેશ_મૂલ્ય.lineno, નામ))
    for પથ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            નામ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if નામ not in પેરામીટર_કોષ્ટક or નામ in 가변매개함수 or not any(ord(વર્ણ_મૂલ્ય)>127 for વર્ણ_મૂલ્ય in નામ): continue
            for પેરામીટર_દલીલ in 호출.keywords:
                if પેરામીટર_દલીલ.arg and પેરામીટર_દલીલ.arg not in પેરામીટર_કોષ્ટક[નામ]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(પથ.relative_to(저장소), 호출.lineno, નામ, પેરામીટર_દલીલ.arg))
    for લાઇન in (પ્રોજેક્ટ_રૂટ/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, પ્રક્રિયા_મૂલ્ય_પ્રવેશ = લાઇન.split('\t')
        if not (પ્રોજેક્ટ_રૂટ/현재).is_file(): 실패들.append('ખસેડવું_મૂલ્ય ફાઈલ 없음: '+현재)
        if પ્રક્રિયા_મૂલ્ય_પ્રવેશ == '호환진입점유지' and not (પ્રોજેક્ટ_રૂટ/이전).is_file(): 실패들.append('호환 પ્રવેશ_બિંદુ 없음: '+이전)
    예제 = (પ્રોજેક્ટ_રૂટ.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for પથ in sorted((પ્રોજેક્ટ_રૂટ.parents[1]/'example/java').glob('*.java')):
        સ્રોત = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', પથ.read_text())
        for નામ in re.findall(r'\b[^\W\d]\w*\b', સ્રોત, re.UNICODE):
            if નામ not in 예약어 and all(ord(વર્ણ_મૂલ્ય)<128 for વર્ણ_મૂલ્ય in નામ):
                실패들.append('{}: 예제의 영어 ઓળખકર્તા_મૂલ્ય {}'.format(પથ.name, નામ))
    for નામ in ('창', 'બટન', 'લેબલ', 'ટેક્સ્ટ_ફીલ્ડ', '화면구성요소', 'ઇવેંટ_કતાર', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        સ્રોત = (પ્રોજેક્ટ_રૂટ/'한국어자바/ગુજરાતી/자체'/(નામ+'.java')).read_text()
        સ્રોત = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', સ્રોત)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', સ્રોત):
            실패들.append(નામ+': ગુજરાતી 직접 구현에 표준 ઑબ્જેક્ટ_મૂલ્ય 래퍼가 남았습니다.')
    시언어예제 = (પ્રોજેક્ટ_રૂટ.parents[1]/'example/c/네트워크예제.c').read_text()
    for નામ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if નામ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 નામ: '+નામ)
    파이썬예제 = (પ્રોજેક્ટ_રૂટ.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (પ્રોજેક્ટ_રૂટ.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for નામ in ('ક્લાઉડ_કુટુંબ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+નામ+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 મૅક્રો_મૂલ્ય 사용: '+નામ)
    자바파일수 = 0
    for રૂટ_મૂલ્ય in ('સ્રોત', 'ઉપયોગકર્તા/자바', '한국어자바'):
        for પથ in (પ્રોજેક્ટ_રૂટ/રૂટ_મૂલ્ય).rglob('*.java'):
            자바파일수 += 1
            સ્રોત = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', પથ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', સ્રોત):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(પથ.relative_to(પ્રોજેક્ટ_રૂટ), 맞음[1]))
            if રૂટ_મૂલ્ય == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', સ્રોત):
                실패들.append('{}: 공개 예외 선언'.format(પથ.relative_to(પ્રોજેક્ટ_રૂટ)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for પથ in sorted((저장소/'os/સ્રોત').glob('*.java')):
        x86자바파일수 += 1
        સ્રોત = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', પથ.read_text())
        for નામ in re.findall(r'\b[^\W\d]\w*\b', સ્રોત, re.UNICODE):
            if નામ not in 예약어 | 표준자바이름 and all(ord(વર્ણ_મૂલ્ય)<128 for વર્ણ_મૂલ્ય in નામ):
                실패들.append('{}: 자체 영어 ઓળખકર્તા_મૂલ્ય {}'.format(પથ.relative_to(저장소), નામ))
    લૉગ_પંક્તિ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if દલીલો.시언어:
        subprocess.check_call(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/시언어이름분석.py')])
        분석 = json.loads((પ્રોજેક્ટ_રૂટ/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ભૂલ) for ભૂલ in 분석['ભૂલ'])
        공개규약 = set(json.loads((પ્રોજેક્ટ_રૂટ/'명명/규격이름.json').read_text()))
        for પ્રવેશ_મૂલ્ય in 분석['선언'].values():
            નામ = પ્રવેશ_મૂલ્ય['નામ']; પથ = Path(પ્રવેશ_મૂલ્ય['ફાઈલ'])
            સ્રોત = પથ.read_bytes()
            # ગુજરાતી 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if સ્રોત[પ્રવેશ_મૂલ્ય['ઑફસેટ_મૂલ્ય']:પ્રવેશ_મૂલ્ય['ઑફસેટ_મૂલ્ય']+len(નામ)] == નામ.encode() and નામ not in 공개규약:
                실패들.append('{}:{}: {}'.format(પથ.relative_to(પ્રોજેક્ટ_રૂટ), પ્રવેશ_મૂલ્ય['줄'], નામ))
        લૉગ_પંક્તિ['c_semantic_checked'] = True
        લૉગ_પંક્તિ['c_source_sha256'] = {str(Path(ફાઈલ).relative_to(પ્રોજેક્ટ_રૂટ)):હૅશ_ફાઇલ for ફાઈલ,હૅશ_ફાઇલ in 분석['원문해시'].items()}
    લૉગ_પંક્તિ['passed'] = not 실패들; લૉગ_પંક્તિ['failures'] = 실패들
    ગંતવ્ય_મૂલ્ય = પ્રોજેક્ટ_રૂટ/'build/verification/naming'; ગંતવ્ય_મૂલ્ય.mkdir(parents=True, exist_ok=True)
    (ગંતવ્ય_મૂલ્ય/'report.json').write_text(json.dumps(લૉગ_પંક્તિ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: ગુજરાતી 선언·ફાઈલ પથ·호환 પ્રવેશ_બિંદુ·통신 예제')

if __name__ == '__main__': ચલાવો_2()
