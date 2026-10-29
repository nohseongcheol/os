#!/usr/bin/env python3
"""명명 ಕ್ಲಿಪ್·ವಿನಾಯಿತಿ·경로를 검사한다. --시언어는 libclang ದೃಢೀಕರಣ 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]
ಸಂಗ್ರಹಣೆ_ಮೂಲ = ಬಿಂಬಿಸು_ಮೂಲ.parents[1]

def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    실패들 = []
    ಕೆಲಸ_ಮೌಲ್ಯ = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    ಪ್ಯಾರಾಮೀಟರ್_ಕೋಷ್ಟಕ = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [ಸಂಗ್ರಹಣೆ_ಮೂಲ/'compiler/컴파일러.py', ಸಂಗ್ರಹಣೆ_ಮೂಲ/'compiler/기계어미리번역.py']
    for ಮಾರ್ಗ in list((ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು').glob('*.py')) + list((ಬಿಂಬಿಸು_ಮೂಲ/'예제').rglob('*.py')) + 공용번역기들:
        if ಮಾರ್ಗ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ಮಾರ್ಗ.read_text()); 나무들[ಮಾರ್ಗ] = 나무
        for ನಮೂದು_ಮೌಲ್ಯ in ast.walk(나무):
            if isinstance(ನಮೂದು_ಮೌಲ್ಯ, ast.FunctionDef):
                ಪ್ಯಾರಾಮೀಟರ್_ಕೋಷ್ಟಕ.setdefault(ನಮೂದು_ಮೌಲ್ಯ.name, set()).update(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.arg for ಪ್ಯಾರಾಮೀಟರ್_ವಾದ in ನಮೂದು_ಮೌಲ್ಯ.args.args + ನಮೂದು_ಮೌಲ್ಯ.args.kwonlyargs)
                if ನಮೂದು_ಮೌಲ್ಯ.args.kwarg: 가변매개함수.add(ನಮೂದು_ಮೌಲ್ಯ.name)
            if isinstance(ನಮೂದು_ಮೌಲ್ಯ, ast.ClassDef):
                for ಕಾರ್ಯ_ಮೌಲ್ಯ in ನಮೂದು_ಮೌಲ್ಯ.body:
                    if isinstance(ಕಾರ್ಯ_ಮೌಲ್ಯ, ast.FunctionDef) and ಕಾರ್ಯ_ಮೌಲ್ಯ.name == '__init__':
                        ಪ್ಯಾರಾಮೀಟರ್_ಕೋಷ್ಟಕ.setdefault(ನಮೂದು_ಮೌಲ್ಯ.name, set()).update(ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.arg for ಪ್ಯಾರಾಮೀಟರ್_ವಾದ in ಕಾರ್ಯ_ಮೌಲ್ಯ.args.args + ಕಾರ್ಯ_ಮೌಲ್ಯ.args.kwonlyargs)
            ಹೆಸರು = ''
            if isinstance(ನಮೂದು_ಮೌಲ್ಯ, (ast.FunctionDef, ast.ClassDef)): ಹೆಸರು = ನಮೂದು_ಮೌಲ್ಯ.name
            elif isinstance(ನಮೂದು_ಮೌಲ್ಯ, ast.Name) and isinstance(ನಮೂದು_ಮೌಲ್ಯ.ctx, ast.Store): ಹೆಸರು = ನಮೂದು_ಮೌಲ್ಯ.id
            elif isinstance(ನಮೂದು_ಮೌಲ್ಯ, ast.arg): ಹೆಸರು = ನಮೂದು_ಮೌಲ್ಯ.arg
            if ಹೆಸರು and ಹೆಸರು not in ಕೆಲಸ_ಮೌಲ್ಯ and all(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)<128 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಹೆಸರು):
                실패들.append('{}:{}: {}'.format(ಮಾರ್ಗ.relative_to(ಸಂಗ್ರಹಣೆ_ಮೂಲ), ನಮೂದು_ಮೌಲ್ಯ.lineno, ಹೆಸರು))
    for ಮಾರ್ಗ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ಹೆಸರು = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ಹೆಸರು not in ಪ್ಯಾರಾಮೀಟರ್_ಕೋಷ್ಟಕ or ಹೆಸರು in 가변매개함수 or not any(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)>127 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಹೆಸರು): continue
            for ಪ್ಯಾರಾಮೀಟರ್_ವಾದ in 호출.keywords:
                if ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.arg and ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.arg not in ಪ್ಯಾರಾಮೀಟರ್_ಕೋಷ್ಟಕ[ಹೆಸರು]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ಮಾರ್ಗ.relative_to(ಸಂಗ್ರಹಣೆ_ಮೂಲ), 호출.lineno, ಹೆಸರು, ಪ್ಯಾರಾಮೀಟರ್_ವಾದ.arg))
    for ಸಾಲು in (ಬಿಂಬಿಸು_ಮೂಲ/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು = ಸಾಲು.split('\t')
        if not (ಬಿಂಬಿಸು_ಮೂಲ/현재).is_file(): 실패들.append('ಸರಿಸು_ಮೌಲ್ಯ ಕಡತ 없음: '+현재)
        if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು == '호환진입점유지' and not (ಬಿಂಬಿಸು_ಮೂಲ/이전).is_file(): 실패들.append('호환 ನಮೂದು_ಬಿಂದು 없음: '+이전)
    예제 = (ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ಮಾರ್ಗ in sorted((ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'example/java').glob('*.java')):
        ಮೂಲ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ಮಾರ್ಗ.read_text())
        for ಹೆಸರು in re.findall(r'\b[^\W\d]\w*\b', ಮೂಲ, re.UNICODE):
            if ಹೆಸರು not in 예약어 and all(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)<128 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಹೆಸರು):
                실패들.append('{}: 예제의 영어 ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ {}'.format(ಮಾರ್ಗ.name, ಹೆಸರು))
    for ಹೆಸರು in ('창', 'ಬಟನ್', 'ಲೇಬಲ್', 'ಪಠ್ಯ_ಕ್ಷೇತ್ರ', '화면구성요소', 'ಸಂಗತಿ_ಸರದಿ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ಮೂಲ = (ಬಿಂಬಿಸು_ಮೂಲ/'한국어자바/ಕನ್ನಡ/자체'/(ಹೆಸರು+'.java')).read_text()
        ಮೂಲ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ಮೂಲ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ಮೂಲ):
            실패들.append(ಹೆಸರು+': ಕನ್ನಡ 직접 구현에 표준 ಆಬ್ಜೆಕ್ಟ್_ಮೌಲ್ಯ 래퍼가 남았습니다.')
    시언어예제 = (ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'example/c/네트워크예제.c').read_text()
    for ಹೆಸರು in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ಹೆಸರು in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ಹೆಸರು: '+ಹೆಸರು)
    파이썬예제 = (ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ವಿನಾಯಿತಿ 직접 사용')
    머리 = (ಬಿಂಬಿಸು_ಮೂಲ.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ಹೆಸರು in ('ಕ್ಲೌಡ್_ಕುಟುಂಬ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ಹೆಸರು+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ಮ್ಯಾಕ್ರೊ_ಮೌಲ್ಯ 사용: '+ಹೆಸರು)
    자바파일수 = 0
    for ಮೂಲ_ಮೌಲ್ಯ in ('ಮೂಲ', 'ಬಳಕೆದಾರ/자바', '한국어자바'):
        for ಮಾರ್ಗ in (ಬಿಂಬಿಸು_ಮೂಲ/ಮೂಲ_ಮೌಲ್ಯ).rglob('*.java'):
            자바파일수 += 1
            ಮೂಲ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ಮಾರ್ಗ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ಮೂಲ):
                실패들.append('{}: 한국어화되지 않은 ದೃಢೀಕರಣ {}'.format(ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ), 맞음[1]))
            if ಮೂಲ_ಮೌಲ್ಯ == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ಮೂಲ):
                실패들.append('{}: 공개 ವಿನಾಯಿತಿ ದೃಢೀಕರಣ'.format(ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ಮಾರ್ಗ in sorted((ಸಂಗ್ರಹಣೆ_ಮೂಲ/'os/ಮೂಲ').glob('*.java')):
        x86자바파일수 += 1
        ಮೂಲ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ಮಾರ್ಗ.read_text())
        for ಹೆಸರು in re.findall(r'\b[^\W\d]\w*\b', ಮೂಲ, re.UNICODE):
            if ಹೆಸರು not in 예약어 | 표준자바이름 and all(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ)<128 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಹೆಸರು):
                실패들.append('{}: 자체 영어 ಗುರುತಿಸುವಿಕೆ_ಮೌಲ್ಯ {}'.format(ಮಾರ್ಗ.relative_to(ಸಂಗ್ರಹಣೆ_ಮೂಲ), ಹೆಸರು))
    ಲಾಗ್_ದಾಖಲೆ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/시언어이름분석.py')])
        분석 = json.loads((ಬಿಂಬಿಸು_ಮೂಲ/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ದೋಷ) for ದೋಷ in 분석['ದೋಷ'])
        공개규약 = set(json.loads((ಬಿಂಬಿಸು_ಮೂಲ/'명명/규격이름.json').read_text()))
        for ನಮೂದು_ಮೌಲ್ಯ in 분석['ದೃಢೀಕರಣ'].values():
            ಹೆಸರು = ನಮೂದು_ಮೌಲ್ಯ['ಹೆಸರು']; ಮಾರ್ಗ = Path(ನಮೂದು_ಮೌಲ್ಯ['ಕಡತ'])
            ಮೂಲ = ಮಾರ್ಗ.read_bytes()
            # ಕನ್ನಡ 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ಮೂಲ[ನಮೂದು_ಮೌಲ್ಯ['ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ']:ನಮೂದು_ಮೌಲ್ಯ['ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ']+len(ಹೆಸರು)] == ಹೆಸರು.encode() and ಹೆಸರು not in 공개규약:
                실패들.append('{}:{}: {}'.format(ಮಾರ್ಗ.relative_to(ಬಿಂಬಿಸು_ಮೂಲ), ನಮೂದು_ಮೌಲ್ಯ['줄'], ಹೆಸರು))
        ಲಾಗ್_ದಾಖಲೆ['c_semantic_checked'] = True
        ಲಾಗ್_ದಾಖಲೆ['c_source_sha256'] = {str(Path(ಕಡತ).relative_to(ಬಿಂಬಿಸು_ಮೂಲ)):ಹ್ಯಾಶ್_ಫೈಲ್ for ಕಡತ,ಹ್ಯಾಶ್_ಫೈಲ್ in 분석['원문해시'].items()}
    ಲಾಗ್_ದಾಖಲೆ['passed'] = not 실패들; ಲಾಗ್_ದಾಖಲೆ['failures'] = 실패들
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/naming'; ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ.mkdir(parents=True, exist_ok=True)
    (ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ/'report.json').write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: ಕನ್ನಡ ದೃಢೀಕರಣ·ಕಡತ ಮಾರ್ಗ·호환 ನಮೂದು_ಬಿಂದು·통신 예제')

if __name__ == '__main__': ಚಲಾಯಿಸು_2()
