#!/usr/bin/env python3
"""명명 külipü_ayaakuaapijana·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    achikii_ajutuu = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for wopu_a_ttaaleemüin in list((기준/'도구').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if wopu_a_ttaaleemüin.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(wopu_a_ttaaleemüin.read_text()); 나무들[wopu_a_ttaaleemüin] = 나무
        for ekeroliaa_ajutuu in ast.walk(나무):
            if isinstance(ekeroliaa_ajutuu, ast.FunctionDef):
                매개변수표.setdefault(ekeroliaa_ajutuu.name, set()).update(인자.arg for 인자 in ekeroliaa_ajutuu.args.args + ekeroliaa_ajutuu.args.kwonlyargs)
                if ekeroliaa_ajutuu.args.kwarg: 가변매개함수.add(ekeroliaa_ajutuu.name)
            if isinstance(ekeroliaa_ajutuu, ast.ClassDef):
                for 함수 in ekeroliaa_ajutuu.body:
                    if isinstance(함수, ast.FunctionDef) and 함수.name == '__init__':
                        매개변수표.setdefault(ekeroliaa_ajutuu.name, set()).update(인자.arg for 인자 in 함수.args.args + 함수.args.kwonlyargs)
            이름 = ''
            if isinstance(ekeroliaa_ajutuu, (ast.FunctionDef, ast.ClassDef)): 이름 = ekeroliaa_ajutuu.name
            elif isinstance(ekeroliaa_ajutuu, ast.Name) and isinstance(ekeroliaa_ajutuu.ctx, ast.Store): 이름 = ekeroliaa_ajutuu.id
            elif isinstance(ekeroliaa_ajutuu, ast.arg): 이름 = ekeroliaa_ajutuu.arg
            if 이름 and 이름 not in achikii_ajutuu and all(ord(jeerü_ajutuu)<128 for jeerü_ajutuu in 이름):
                실패들.append('{}:{}: {}'.format(wopu_a_ttaaleemüin.relative_to(저장소), ekeroliaa_ajutuu.lineno, 이름))
    for wopu_a_ttaaleemüin, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            이름 = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if 이름 not in 매개변수표 or 이름 in 가변매개함수 or not any(ord(jeerü_ajutuu)>127 for jeerü_ajutuu in 이름): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[이름]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(wopu_a_ttaaleemüin.relative_to(저장소), 호출.lineno, 이름, 인자.arg))
    for liinia in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, 처리 = liinia.split('\t')
        if not (기준/현재).is_file(): 실패들.append('이동 anaajaalaa 없음: '+현재)
        if 처리 == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ekeroliaa_o_uchikanain 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for wopu_a_ttaaleemüin in sorted((기준.parents[1]/'example/java').glob('*.java')):
        eejeejetülein = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', wopu_a_ttaaleemüin.read_text())
        for 이름 in re.findall(r'\b[^\W\d]\w*\b', eejeejetülein, re.UNICODE):
            if 이름 not in 예약어 and all(ord(jeerü_ajutuu)<128 for jeerü_ajutuu in 이름):
                실패들.append('{}: 예제의 영어 식별자 {}'.format(wopu_a_ttaaleemüin.name, 이름))
    for 이름 in ('창', 'ajüttülee', 'akanüliajaa', '입력칸', '화면구성요소', 'kasachiki_a_atapajüsüirua', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        eejeejetülein = (기준/'한국어자바/한국어/자체'/(이름+'.java')).read_text()
        eejeejetülein = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', eejeejetülein)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', eejeejetülein):
            실패들.append(이름+': 한국어 직접 구현에 표준 객체 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for 이름 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if 이름 in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 이름: '+이름)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for 이름 in ('인터넷주소갈래', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+이름+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 maaküra_ajutuu 사용: '+이름)
    자바파일수 = 0
    for 뿌리 in ('eejeejetülein', 'ka_yataayakalü/자바', '한국어자바'):
        for wopu_a_ttaaleemüin in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            eejeejetülein = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', wopu_a_ttaaleemüin.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', eejeejetülein):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(wopu_a_ttaaleemüin.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', eejeejetülein):
                실패들.append('{}: 공개 예외 선언'.format(wopu_a_ttaaleemüin.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for wopu_a_ttaaleemüin in sorted((저장소/'os/eejeejetülein').glob('*.java')):
        x86자바파일수 += 1
        eejeejetülein = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', wopu_a_ttaaleemüin.read_text())
        for 이름 in re.findall(r'\b[^\W\d]\w*\b', eejeejetülein, re.UNICODE):
            if 이름 not in 예약어 | 표준자바이름 and all(ord(jeerü_ajutuu)<128 for jeerü_ajutuu in 이름):
                실패들.append('{}: 자체 영어 식별자 {}'.format(wopu_a_ttaaleemüin.relative_to(저장소), 이름))
    aa_innachikimaajatü_aparatsee = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'도구/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ajachitia) for ajachitia in 분석['ajachitia'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ekeroliaa_ajutuu in 분석['선언'].values():
            이름 = ekeroliaa_ajutuu['이름']; wopu_a_ttaaleemüin = Path(ekeroliaa_ajutuu['anaajaalaa'])
            eejeejetülein = wopu_a_ttaaleemüin.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if eejeejetülein[ekeroliaa_ajutuu['변위']:ekeroliaa_ajutuu['변위']+len(이름)] == 이름.encode() and 이름 not in 공개규약:
                실패들.append('{}:{}: {}'.format(wopu_a_ttaaleemüin.relative_to(기준), ekeroliaa_ajutuu['줄'], 이름))
        aa_innachikimaajatü_aparatsee['c_semantic_checked'] = True
        aa_innachikimaajatü_aparatsee['c_source_sha256'] = {str(Path(anaajaalaa).relative_to(기준)):해시 for anaajaalaa,해시 in 분석['원문해시'].items()}
    aa_innachikimaajatü_aparatsee['passed'] = not 실패들; aa_innachikimaajatü_aparatsee['failures'] = 실패들
    jalamüinjatü_ajutuu = 기준/'build/verification/naming'; jalamüinjatü_ajutuu.mkdir(parents=True, exist_ok=True)
    (jalamüinjatü_ajutuu/'report.json').write_text(json.dumps(aa_innachikimaajatü_aparatsee, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·anaajaalaa wopu_a_ttaaleemüin·호환 ekeroliaa_o_uchikanain·통신 예제')

if __name__ == '__main__': 시작()
