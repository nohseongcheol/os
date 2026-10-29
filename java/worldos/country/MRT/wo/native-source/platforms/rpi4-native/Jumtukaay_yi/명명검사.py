#!/usr/bin/env python3
"""명명 kilip·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def daw():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    ay_xëyma = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Yoonu_jëmale in list((기준/'Jumtukaay_yi').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if Yoonu_jëmale.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Yoonu_jëmale.read_text()); 나무들[Yoonu_jëmale] = 나무
        for dugal_xabaar_xëyma in ast.walk(나무):
            if isinstance(dugal_xabaar_xëyma, ast.FunctionDef):
                매개변수표.setdefault(dugal_xabaar_xëyma.name, set()).update(인자.arg for 인자 in dugal_xabaar_xëyma.args.args + dugal_xabaar_xëyma.args.kwonlyargs)
                if dugal_xabaar_xëyma.args.kwarg: 가변매개함수.add(dugal_xabaar_xëyma.name)
            if isinstance(dugal_xabaar_xëyma, ast.ClassDef):
                for liëey_xëyma in dugal_xabaar_xëyma.body:
                    if isinstance(liëey_xëyma, ast.FunctionDef) and liëey_xëyma.name == '__init__':
                        매개변수표.setdefault(dugal_xabaar_xëyma.name, set()).update(인자.arg for 인자 in liëey_xëyma.args.args + liëey_xëyma.args.kwonlyargs)
            tur_253d1510 = ''
            if isinstance(dugal_xabaar_xëyma, (ast.FunctionDef, ast.ClassDef)): tur_253d1510 = dugal_xabaar_xëyma.name
            elif isinstance(dugal_xabaar_xëyma, ast.Name) and isinstance(dugal_xabaar_xëyma.ctx, ast.Store): tur_253d1510 = dugal_xabaar_xëyma.id
            elif isinstance(dugal_xabaar_xëyma, ast.arg): tur_253d1510 = dugal_xabaar_xëyma.arg
            if tur_253d1510 and tur_253d1510 not in ay_xëyma and all(ord(Araf_xëyma)<128 for Araf_xëyma in tur_253d1510):
                실패들.append('{}:{}: {}'.format(Yoonu_jëmale.relative_to(저장소), dugal_xabaar_xëyma.lineno, tur_253d1510))
    for Yoonu_jëmale, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            tur_253d1510 = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if tur_253d1510 not in 매개변수표 or tur_253d1510 in 가변매개함수 or not any(ord(Araf_xëyma)>127 for Araf_xëyma in tur_253d1510): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[tur_253d1510]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Yoonu_jëmale.relative_to(저장소), 호출.lineno, tur_253d1510, 인자.arg))
    for buum in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, yokkute_xëyma_dugal_xabaar = buum.split('\t')
        if not (기준/현재).is_file(): 실패들.append('toxal_xëyma bara_denc 없음: '+현재)
        if yokkute_xëyma_dugal_xabaar == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 dugal_xabaar_Tomb 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Yoonu_jëmale in sorted((기준.parents[1]/'example/java').glob('*.java')):
        Cosaan = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Yoonu_jëmale.read_text())
        for tur_253d1510 in re.findall(r'\b[^\W\d]\w*\b', Cosaan, re.UNICODE):
            if tur_253d1510 not in 예약어 and all(ord(Araf_xëyma)<128 for Araf_xëyma in tur_253d1510):
                실패들.append('{}: 예제의 영어 raññeekaay_xëyma {}'.format(Yoonu_jëmale.name, tur_253d1510))
    for tur_253d1510 in ('창', 'butoñ', 'tur', 'SMS_barabu_denc_ab_joxe', '화면구성요소', 'xewxew_Topplante_xaarandi', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Cosaan = (기준/'한국어자바/한국어/자체'/(tur_253d1510+'.java')).read_text()
        Cosaan = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Cosaan)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Cosaan):
            실패들.append(tur_253d1510+': 한국어 직접 구현에 표준 yëf_xëyma 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for tur_253d1510 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if tur_253d1510 in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 tur_253d1510: '+tur_253d1510)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for tur_253d1510 in ('net_Njaboot', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+tur_253d1510+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 gaawtal_xëyma 사용: '+tur_253d1510)
    자바파일수 = 0
    for 뿌리 in ('Cosaan', 'kiy_jariñoo_internet/자바', '한국어자바'):
        for Yoonu_jëmale in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            Cosaan = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Yoonu_jëmale.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Cosaan):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Yoonu_jëmale.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Cosaan):
                실패들.append('{}: 공개 예외 선언'.format(Yoonu_jëmale.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Yoonu_jëmale in sorted((저장소/'os/Cosaan').glob('*.java')):
        x86자바파일수 += 1
        Cosaan = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Yoonu_jëmale.read_text())
        for tur_253d1510 in re.findall(r'\b[^\W\d]\w*\b', Cosaan, re.UNICODE):
            if tur_253d1510 not in 예약어 | 표준자바이름 and all(ord(Araf_xëyma)<128 for Araf_xëyma in tur_253d1510):
                실패들.append('{}: 자체 영어 raññeekaay_xëyma {}'.format(Yoonu_jëmale.relative_to(저장소), tur_253d1510))
    làq_Dënk = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Jumtukaay_yi/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(njumte) for njumte in 분석['njumte'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for dugal_xabaar_xëyma in 분석['선언'].values():
            tur_253d1510 = dugal_xabaar_xëyma['tur_253d1510']; Yoonu_jëmale = Path(dugal_xabaar_xëyma['bara_denc'])
            Cosaan = Yoonu_jëmale.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Cosaan[dugal_xabaar_xëyma['Randal_xëyma']:dugal_xabaar_xëyma['Randal_xëyma']+len(tur_253d1510)] == tur_253d1510.encode() and tur_253d1510 not in 공개규약:
                실패들.append('{}:{}: {}'.format(Yoonu_jëmale.relative_to(기준), dugal_xabaar_xëyma['줄'], tur_253d1510))
        làq_Dënk['c_semantic_checked'] = True
        làq_Dënk['c_source_sha256'] = {str(Path(bara_denc).relative_to(기준)):caabiy_teqale_bi_bara_denc for bara_denc,caabiy_teqale_bi_bara_denc in 분석['원문해시'].items()}
    làq_Dënk['passed'] = not 실패들; làq_Dënk['failures'] = 실패들
    jëmmukaay_xëyma = 기준/'build/verification/naming'; jëmmukaay_xëyma.mkdir(parents=True, exist_ok=True)
    (jëmmukaay_xëyma/'report.json').write_text(json.dumps(làq_Dënk, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·bara_denc Yoonu_jëmale·호환 dugal_xabaar_Tomb·통신 예제')

if __name__ == '__main__': daw()
