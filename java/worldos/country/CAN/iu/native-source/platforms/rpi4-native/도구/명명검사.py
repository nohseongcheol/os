#!/usr/bin/env python3
"""명명 Nakatigat·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
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
    pijatsaq_atuutilik = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for aqqut in list((기준/'도구').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if aqqut.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(aqqut.read_text()); 나무들[aqqut] = 나무
        for Iliniku_atuutilik in ast.walk(나무):
            if isinstance(Iliniku_atuutilik, ast.FunctionDef):
                매개변수표.setdefault(Iliniku_atuutilik.name, set()).update(인자.arg for 인자 in Iliniku_atuutilik.args.args + Iliniku_atuutilik.args.kwonlyargs)
                if Iliniku_atuutilik.args.kwarg: 가변매개함수.add(Iliniku_atuutilik.name)
            if isinstance(Iliniku_atuutilik, ast.ClassDef):
                for sugiakkannirut_atuutilik in Iliniku_atuutilik.body:
                    if isinstance(sugiakkannirut_atuutilik, ast.FunctionDef) and sugiakkannirut_atuutilik.name == '__init__':
                        매개변수표.setdefault(Iliniku_atuutilik.name, set()).update(인자.arg for 인자 in sugiakkannirut_atuutilik.args.args + sugiakkannirut_atuutilik.args.kwonlyargs)
            atiq = ''
            if isinstance(Iliniku_atuutilik, (ast.FunctionDef, ast.ClassDef)): atiq = Iliniku_atuutilik.name
            elif isinstance(Iliniku_atuutilik, ast.Name) and isinstance(Iliniku_atuutilik.ctx, ast.Store): atiq = Iliniku_atuutilik.id
            elif isinstance(Iliniku_atuutilik, ast.arg): atiq = Iliniku_atuutilik.arg
            if atiq and atiq not in pijatsaq_atuutilik and all(ord(immikkuuqtuq_atuutilik)<128 for immikkuuqtuq_atuutilik in atiq):
                실패들.append('{}:{}: {}'.format(aqqut.relative_to(저장소), Iliniku_atuutilik.lineno, atiq))
    for aqqut, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            atiq = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if atiq not in 매개변수표 or atiq in 가변매개함수 or not any(ord(immikkuuqtuq_atuutilik)>127 for immikkuuqtuq_atuutilik in atiq): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[atiq]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(aqqut.relative_to(저장소), 호출.lineno, atiq, 인자.arg))
    for titikutaak in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Pivallianiq_atuutilik_Iliniku = titikutaak.split('\t')
        if not (기준/현재).is_file(): 실패들.append('nuulli_atuutilik ini 없음: '+현재)
        if Pivallianiq_atuutilik_Iliniku == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 Iliniku_puinti 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for aqqut in sorted((기준.parents[1]/'example/java').glob('*.java')):
        pivviujuq = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', aqqut.read_text())
        for atiq in re.findall(r'\b[^\W\d]\w*\b', pivviujuq, re.UNICODE):
            if atiq not in 예약어 and all(ord(immikkuuqtuq_atuutilik)<128 for immikkuuqtuq_atuutilik in atiq):
                실패들.append('{}: 예제의 영어 식별자 {}'.format(aqqut.name, atiq))
    for atiq in ('창', 'tikkuagaq', 'nalunairli', 'titiqqaq_kisumuungavik', '화면구성요소', 'piniku_utaqqivik', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        pivviujuq = (기준/'한국어자바/한국어/자체'/(atiq+'.java')).read_text()
        pivviujuq = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', pivviujuq)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', pivviujuq):
            실패들.append(atiq+': 한국어 직접 구현에 표준 kisu_atuutilik 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for atiq in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if atiq in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 atiq: '+atiq)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for atiq in ('cloud_illumiuqatigiit', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+atiq+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 aulattijjutialaaq_atuutilik 사용: '+atiq)
    자바파일수 = 0
    for 뿌리 in ('pivviujuq', 'atuqtuq/자바', '한국어자바'):
        for aqqut in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            pivviujuq = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', aqqut.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', pivviujuq):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(aqqut.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', pivviujuq):
                실패들.append('{}: 공개 예외 선언'.format(aqqut.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for aqqut in sorted((저장소/'os/pivviujuq').glob('*.java')):
        x86자바파일수 += 1
        pivviujuq = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', aqqut.read_text())
        for atiq in re.findall(r'\b[^\W\d]\w*\b', pivviujuq, re.UNICODE):
            if atiq not in 예약어 | 표준자바이름 and all(ord(immikkuuqtuq_atuutilik)<128 for immikkuuqtuq_atuutilik in atiq):
                실패들.append('{}: 자체 영어 식별자 {}'.format(aqqut.relative_to(저장소), atiq))
    papattivik_sanimukutaak = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'도구/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(tammarniq) for tammarniq in 분석['tammarniq'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for Iliniku_atuutilik in 분석['선언'].values():
            atiq = Iliniku_atuutilik['atiq']; aqqut = Path(Iliniku_atuutilik['ini'])
            pivviujuq = aqqut.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if pivviujuq[Iliniku_atuutilik['변위']:Iliniku_atuutilik['변위']+len(atiq)] == atiq.encode() and atiq not in 공개규약:
                실패들.append('{}:{}: {}'.format(aqqut.relative_to(기준), Iliniku_atuutilik['줄'], atiq))
        papattivik_sanimukutaak['c_semantic_checked'] = True
        papattivik_sanimukutaak['c_source_sha256'] = {str(Path(ini).relative_to(기준)):해시 for ini,해시 in 분석['원문해시'].items()}
    papattivik_sanimukutaak['passed'] = not 실패들; papattivik_sanimukutaak['failures'] = 실패들
    namunngarvik_atuutilik = 기준/'build/verification/naming'; namunngarvik_atuutilik.mkdir(parents=True, exist_ok=True)
    (namunngarvik_atuutilik/'report.json').write_text(json.dumps(papattivik_sanimukutaak, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·ini aqqut·호환 Iliniku_puinti·통신 예제')

if __name__ == '__main__': 시작()
