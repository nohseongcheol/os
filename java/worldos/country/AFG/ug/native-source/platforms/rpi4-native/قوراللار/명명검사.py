#!/usr/bin/env python3
"""명명 كەسمە·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]
저장소 = كۆرسىتىش_يىلتىز.parents[1]

def ئىجرا_قىل_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    실패들 = []
    خىزمەت_قىممىتى = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for يول in list((كۆرسىتىش_يىلتىز/'قوراللار').glob('*.py')) + list((كۆرسىتىش_يىلتىز/'예제').rglob('*.py')) + 공용번역기들:
        if يول.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(يول.read_text()); 나무들[يول] = 나무
        for كىرگۈزۈش_قىممىتى in ast.walk(나무):
            if isinstance(كىرگۈزۈش_قىممىتى, ast.FunctionDef):
                매개변수표.setdefault(كىرگۈزۈش_قىممىتى.name, set()).update(인자.arg for 인자 in كىرگۈزۈش_قىممىتى.args.args + كىرگۈزۈش_قىممىتى.args.kwonlyargs)
                if كىرگۈزۈش_قىممىتى.args.kwarg: 가변매개함수.add(كىرگۈزۈش_قىممىتى.name)
            if isinstance(كىرگۈزۈش_قىممىتى, ast.ClassDef):
                for فۇنكسىيە_قىممىتى in كىرگۈزۈش_قىممىتى.body:
                    if isinstance(فۇنكسىيە_قىممىتى, ast.FunctionDef) and فۇنكسىيە_قىممىتى.name == '__init__':
                        매개변수표.setdefault(كىرگۈزۈش_قىممىتى.name, set()).update(인자.arg for 인자 in فۇنكسىيە_قىممىتى.args.args + فۇنكسىيە_قىممىتى.args.kwonlyargs)
            ئاتى = ''
            if isinstance(كىرگۈزۈش_قىممىتى, (ast.FunctionDef, ast.ClassDef)): ئاتى = كىرگۈزۈش_قىممىتى.name
            elif isinstance(كىرگۈزۈش_قىممىتى, ast.Name) and isinstance(كىرگۈزۈش_قىممىتى.ctx, ast.Store): ئاتى = كىرگۈزۈش_قىممىتى.id
            elif isinstance(كىرگۈزۈش_قىممىتى, ast.arg): ئاتى = كىرگۈزۈش_قىممىتى.arg
            if ئاتى and ئاتى not in خىزمەت_قىممىتى and all(ord(ھەرپ_بەلگە_قىممىتى)<128 for ھەرپ_بەلگە_قىممىتى in ئاتى):
                실패들.append('{}:{}: {}'.format(يول.relative_to(저장소), كىرگۈزۈش_قىممىتى.lineno, ئاتى))
    for يول, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ئاتى = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ئاتى not in 매개변수표 or ئاتى in 가변매개함수 or not any(ord(ھەرپ_بەلگە_قىممىتى)>127 for ھەرپ_بەلگە_قىممىتى in ئاتى): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[ئاتى]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(يول.relative_to(저장소), 호출.lineno, ئاتى, 인자.arg))
    for قۇر in (كۆرسىتىش_يىلتىز/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, جەريان_قىممىتى_كىرگۈزۈش = قۇر.split('\t')
        if not (كۆرسىتىش_يىلتىز/현재).is_file(): 실패들.append('يۆتكىمەك_قىممىتى ھۆججەت 없음: '+현재)
        if جەريان_قىممىتى_كىرگۈزۈش == '호환진입점유지' and not (كۆرسىتىش_يىلتىز/이전).is_file(): 실패들.append('호환 كىرگۈزۈش_نوقتا 없음: '+이전)
    예제 = (كۆرسىتىش_يىلتىز.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for يول in sorted((كۆرسىتىش_يىلتىز.parents[1]/'example/java').glob('*.java')):
        مەنبە = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', يول.read_text())
        for ئاتى in re.findall(r'\b[^\W\d]\w*\b', مەنبە, re.UNICODE):
            if ئاتى not in 예약어 and all(ord(ھەرپ_بەلگە_قىممىتى)<128 for ھەرپ_بەلگە_قىممىتى in ئاتى):
                실패들.append('{}: 예제의 영어 پەرقلەندۈرگۈچ_قىممىتى {}'.format(يول.name, ئاتى))
    for ئاتى in ('كۆزنەك', 'كۇنۇپكا', 'ئەن', 'تېكىست_بۆلىكى', '화면구성요소', 'ھادىسە_تەرتىپ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        مەنبە = (كۆرسىتىش_يىلتىز/'한국어자바/한국어/자체'/(ئاتى+'.java')).read_text()
        مەنبە = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', مەنبە)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', مەنبە):
            실패들.append(ئاتى+': 한국어 직접 구현에 표준 ئوبيېكت_قىممىتى 래퍼가 남았습니다.')
    시언어예제 = (كۆرسىتىش_يىلتىز.parents[1]/'example/c/네트워크예제.c').read_text()
    for ئاتى in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ئاتى in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ئاتى: '+ئاتى)
    파이썬예제 = (كۆرسىتىش_يىلتىز.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (كۆرسىتىش_يىلتىز.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ئاتى in ('بۇلۇت_ئائىلە', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+ئاتى+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 بۇيرۇق_توپى_قىممىتى 사용: '+ئاتى)
    자바파일수 = 0
    for يىلتىز_قىممىتى in ('مەنبە', 'ئىشلەتكۈچى/자바', '한국어자바'):
        for يول in (كۆرسىتىش_يىلتىز/يىلتىز_قىممىتى).rglob('*.java'):
            자바파일수 += 1
            مەنبە = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', يول.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', مەنبە):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(يول.relative_to(كۆرسىتىش_يىلتىز), 맞음[1]))
            if يىلتىز_قىممىتى == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', مەنبە):
                실패들.append('{}: 공개 예외 선언'.format(يول.relative_to(كۆرسىتىش_يىلتىز)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for يول in sorted((저장소/'os/مەنبە').glob('*.java')):
        x86자바파일수 += 1
        مەنبە = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', يول.read_text())
        for ئاتى in re.findall(r'\b[^\W\d]\w*\b', مەنبە, re.UNICODE):
            if ئاتى not in 예약어 | 표준자바이름 and all(ord(ھەرپ_بەلگە_قىممىتى)<128 for ھەرپ_بەلگە_قىممىتى in ئاتى):
                실패들.append('{}: 자체 영어 پەرقلەندۈرگۈچ_قىممىتى {}'.format(يول.relative_to(저장소), ئاتى))
    خاتىرە_قۇر = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if ئۆزگەرگۈچىلەر.시언어:
        subprocess.check_call(['python3', str(كۆرسىتىش_يىلتىز/'قوراللار/시언어이름분석.py')])
        ئانالىز_قىلماق_قىممىتى = json.loads((كۆرسىتىش_يىلتىز/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(خاتالىق) for خاتالىق in ئانالىز_قىلماق_قىممىتى['خاتالىق'])
        공개규약 = set(json.loads((كۆرسىتىش_يىلتىز/'명명/규격이름.json').read_text()))
        for كىرگۈزۈش_قىممىتى in ئانالىز_قىلماق_قىممىتى['선언'].values():
            ئاتى = كىرگۈزۈش_قىممىتى['ئاتى']; يول = Path(كىرگۈزۈش_قىممىتى['ھۆججەت'])
            مەنبە = يول.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if مەنبە[كىرگۈزۈش_قىممىتى['ئاغما_قىممىتى']:كىرگۈزۈش_قىممىتى['ئاغما_قىممىتى']+len(ئاتى)] == ئاتى.encode() and ئاتى not in 공개규약:
                실패들.append('{}:{}: {}'.format(يول.relative_to(كۆرسىتىش_يىلتىز), كىرگۈزۈش_قىممىتى['قۇر'], ئاتى))
        خاتىرە_قۇر['c_semantic_checked'] = True
        خاتىرە_قۇر['c_source_sha256'] = {str(Path(ھۆججەت).relative_to(كۆرسىتىش_يىلتىز)):چاچما_ھۆججەت for ھۆججەت,چاچما_ھۆججەت in ئانالىز_قىلماق_قىممىتى['원문해시'].items()}
    خاتىرە_قۇر['passed'] = not 실패들; خاتىرە_قۇر['failures'] = 실패들
    نىشان_قىممىتى = كۆرسىتىش_يىلتىز/'build/verification/naming'; نىشان_قىممىتى.mkdir(parents=True, exist_ok=True)
    (نىشان_قىممىتى/'report.json').write_text(json.dumps(خاتىرە_قۇر, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·ھۆججەت يول·호환 كىرگۈزۈش_نوقتا·통신 예제')

if __name__ == '__main__': ئىجرا_قىل_2()
