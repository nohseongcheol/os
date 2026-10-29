#!/usr/bin/env python3
"""명명 ቅንጥብ·ልዩነት·경로를 검사한다. --시언어는 libclang እወጃ 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

አሳይ_ስር = Path(__file__).resolve().parents[1]
ማከማቻ_ስር = አሳይ_ስር.parents[1]

def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    실패들 = []
    ስራ_እሴት_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    ግቤት_ሰንጠረዥ = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [ማከማቻ_ስር/'compiler/컴파일러.py', ማከማቻ_ስር/'compiler/기계어미리번역.py']
    for መተላለፊያ in list((አሳይ_ስር/'መሳሪያዎች').glob('*.py')) + list((አሳይ_ስር/'예제').rglob('*.py')) + 공용번역기들:
        if መተላለፊያ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(መተላለፊያ.read_text()); 나무들[መተላለፊያ] = 나무
        for ምዝግብ_እሴት in ast.walk(나무):
            if isinstance(ምዝግብ_እሴት, ast.FunctionDef):
                ግቤት_ሰንጠረዥ.setdefault(ምዝግብ_እሴት.name, set()).update(ግቤት_ነጋሪ_እሴት.arg for ግቤት_ነጋሪ_እሴት in ምዝግብ_እሴት.args.args + ምዝግብ_እሴት.args.kwonlyargs)
                if ምዝግብ_እሴት.args.kwarg: 가변매개함수.add(ምዝግብ_እሴት.name)
            if isinstance(ምዝግብ_እሴት, ast.ClassDef):
                for ተግባር_እሴት in ምዝግብ_እሴት.body:
                    if isinstance(ተግባር_እሴት, ast.FunctionDef) and ተግባር_እሴት.name == '__init__':
                        ግቤት_ሰንጠረዥ.setdefault(ምዝግብ_እሴት.name, set()).update(ግቤት_ነጋሪ_እሴት.arg for ግቤት_ነጋሪ_እሴት in ተግባር_እሴት.args.args + ተግባር_እሴት.args.kwonlyargs)
            ስም = ''
            if isinstance(ምዝግብ_እሴት, (ast.FunctionDef, ast.ClassDef)): ስም = ምዝግብ_እሴት.name
            elif isinstance(ምዝግብ_እሴት, ast.Name) and isinstance(ምዝግብ_እሴት.ctx, ast.Store): ስም = ምዝግብ_እሴት.id
            elif isinstance(ምዝግብ_እሴት, ast.arg): ስም = ምዝግብ_እሴት.arg
            if ስም and ስም not in ስራ_እሴት_102996da and all(ord(ቁምፊ_እሴት)<128 for ቁምፊ_እሴት in ስም):
                실패들.append('{}:{}: {}'.format(መተላለፊያ.relative_to(ማከማቻ_ስር), ምዝግብ_እሴት.lineno, ስም))
    for መተላለፊያ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ስም = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ስም not in ግቤት_ሰንጠረዥ or ስም in 가변매개함수 or not any(ord(ቁምፊ_እሴት)>127 for ቁምፊ_እሴት in ስም): continue
            for ግቤት_ነጋሪ_እሴት in 호출.keywords:
                if ግቤት_ነጋሪ_እሴት.arg and ግቤት_ነጋሪ_እሴት.arg not in ግቤት_ሰንጠረዥ[ስም]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(መተላለፊያ.relative_to(ማከማቻ_ስር), 호출.lineno, ስም, ግቤት_ነጋሪ_እሴት.arg))
    for መስመር in (አሳይ_ስር/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ሂደት_እሴት_ምዝግብ = መስመር.split('\t')
        if not (አሳይ_ስር/현재).is_file(): 실패들.append('አንቀሳቅስ_እሴት ፋይል 없음: '+현재)
        if ሂደት_እሴት_ምዝግብ == '호환진입점유지' and not (አሳይ_ስር/이전).is_file(): 실패들.append('호환 ምዝግብ_ቦታ 없음: '+이전)
    예제 = (አሳይ_ስር.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for መተላለፊያ in sorted((አሳይ_ስር.parents[1]/'example/java').glob('*.java')):
        ምንጭ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', መተላለፊያ.read_text())
        for ስም in re.findall(r'\b[^\W\d]\w*\b', ምንጭ, re.UNICODE):
            if ስም not in 예약어 and all(ord(ቁምፊ_እሴት)<128 for ቁምፊ_እሴት in ስም):
                실패들.append('{}: 예제의 영어 መለያ_እሴት_5b7b8b77 {}'.format(መተላለፊያ.name, ስም))
    for ስም in ('창', 'አዝራር', 'ምልክት', 'ጽሁፍ_መስክ', '화면구성요소', 'ፍጻሜ_ሰልፍ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ምንጭ = (አሳይ_ስር/'한국어자바/አማርኛ/자체'/(ስም+'.java')).read_text()
        ምንጭ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ምንጭ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ምንጭ):
            실패들.append(ስም+': አማርኛ 직접 구현에 표준 ነገር_እሴት 래퍼가 남았습니다.')
    시언어예제 = (አሳይ_ስር.parents[1]/'example/c/네트워크예제.c').read_text()
    for ስም in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ስም in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ስም: '+ስም)
    파이썬예제 = (አሳይ_ስር.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ልዩነት 직접 사용')
    머리 = (አሳይ_ስር.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ስም in ('ክላውድ_ቤተሰብ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ስም+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 ማክሮ_እሴት 사용: '+ስም)
    자바파일수 = 0
    for ስር_እሴት in ('ምንጭ', 'ተጠቃሚ/자바', '한국어자바'):
        for መተላለፊያ in (አሳይ_ስር/ስር_እሴት).rglob('*.java'):
            자바파일수 += 1
            ምንጭ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', መተላለፊያ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ምንጭ):
                실패들.append('{}: 한국어화되지 않은 እወጃ {}'.format(መተላለፊያ.relative_to(አሳይ_ስር), 맞음[1]))
            if ስር_እሴት == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ምንጭ):
                실패들.append('{}: 공개 ልዩነት እወጃ'.format(መተላለፊያ.relative_to(አሳይ_ስር)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for መተላለፊያ in sorted((ማከማቻ_ስር/'os/ምንጭ').glob('*.java')):
        x86자바파일수 += 1
        ምንጭ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', መተላለፊያ.read_text())
        for ስም in re.findall(r'\b[^\W\d]\w*\b', ምንጭ, re.UNICODE):
            if ስም not in 예약어 | 표준자바이름 and all(ord(ቁምፊ_እሴት)<128 for ቁምፊ_እሴት in ስም):
                실패들.append('{}: 자체 영어 መለያ_እሴት_5b7b8b77 {}'.format(መተላለፊያ.relative_to(ማከማቻ_ስር), ስም))
    መዝግብ_ረድፍ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(አሳይ_ስር/'መሳሪያዎች/시언어이름분석.py')])
        분석 = json.loads((አሳይ_ስር/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ስህተት) for ስህተት in 분석['ስህተት'])
        공개규약 = set(json.loads((አሳይ_ስር/'명명/규격이름.json').read_text()))
        for ምዝግብ_እሴት in 분석['እወጃ'].values():
            ስም = ምዝግብ_እሴት['ስም']; መተላለፊያ = Path(ምዝግብ_እሴት['ፋይል'])
            ምንጭ = መተላለፊያ.read_bytes()
            # አማርኛ 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ምንጭ[ምዝግብ_እሴት['ዝንፍ_እሴት']:ምዝግብ_እሴት['ዝንፍ_እሴት']+len(ስም)] == ስም.encode() and ስም not in 공개규약:
                실패들.append('{}:{}: {}'.format(መተላለፊያ.relative_to(አሳይ_ስር), ምዝግብ_እሴት['줄'], ስም))
        መዝግብ_ረድፍ['c_semantic_checked'] = True
        መዝግብ_ረድፍ['c_source_sha256'] = {str(Path(ፋይል).relative_to(አሳይ_ስር)):ሃሽ_ፋይል for ፋይል,ሃሽ_ፋይል in 분석['원문해시'].items()}
    መዝግብ_ረድፍ['passed'] = not 실패들; መዝግብ_ረድፍ['failures'] = 실패들
    መድረሻ_እሴት = አሳይ_ስር/'build/verification/naming'; መድረሻ_እሴት.mkdir(parents=True, exist_ok=True)
    (መድረሻ_እሴት/'report.json').write_text(json.dumps(መዝግብ_ረድፍ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: አማርኛ እወጃ·ፋይል መተላለፊያ·호환 ምዝግብ_ቦታ·통신 예제')

if __name__ == '__main__': ማስኬጃ()
