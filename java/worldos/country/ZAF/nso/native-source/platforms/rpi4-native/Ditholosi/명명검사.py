#!/usr/bin/env python3
"""명명 setsopolwa·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Diriša():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    taba_boleng = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Tsejana in list((기준/'Ditholosi').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if Tsejana.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Tsejana.read_text()); 나무들[Tsejana] = 나무
        for go_tsenya_tshedimošo_boleng in ast.walk(나무):
            if isinstance(go_tsenya_tshedimošo_boleng, ast.FunctionDef):
                매개변수표.setdefault(go_tsenya_tshedimošo_boleng.name, set()).update(인자.arg for 인자 in go_tsenya_tshedimošo_boleng.args.args + go_tsenya_tshedimošo_boleng.args.kwonlyargs)
                if go_tsenya_tshedimošo_boleng.args.kwarg: 가변매개함수.add(go_tsenya_tshedimošo_boleng.name)
            if isinstance(go_tsenya_tshedimošo_boleng, ast.ClassDef):
                for TIRO_boleng in go_tsenya_tshedimošo_boleng.body:
                    if isinstance(TIRO_boleng, ast.FunctionDef) and TIRO_boleng.name == '__init__':
                        매개변수표.setdefault(go_tsenya_tshedimošo_boleng.name, set()).update(인자.arg for 인자 in TIRO_boleng.args.args + TIRO_boleng.args.kwonlyargs)
            Leina = ''
            if isinstance(go_tsenya_tshedimošo_boleng, (ast.FunctionDef, ast.ClassDef)): Leina = go_tsenya_tshedimošo_boleng.name
            elif isinstance(go_tsenya_tshedimošo_boleng, ast.Name) and isinstance(go_tsenya_tshedimošo_boleng.ctx, ast.Store): Leina = go_tsenya_tshedimošo_boleng.id
            elif isinstance(go_tsenya_tshedimošo_boleng, ast.arg): Leina = go_tsenya_tshedimošo_boleng.arg
            if Leina and Leina not in taba_boleng and all(ord(tlhaka_boleng)<128 for tlhaka_boleng in Leina):
                실패들.append('{}:{}: {}'.format(Tsejana.relative_to(저장소), go_tsenya_tshedimošo_boleng.lineno, Leina))
    for Tsejana, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Leina = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Leina not in 매개변수표 or Leina in 가변매개함수 or not any(ord(tlhaka_boleng)>127 for tlhaka_boleng in Leina): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Leina]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Tsejana.relative_to(저장소), 호출.lineno, Leina, 인자.arg))
    for mothaladi in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, tiragalo_boleng_go_tsenya_tshedimošo = mothaladi.split('\t')
        if not (기준/현재).is_file(): 실패들.append('šuthiša_boleng Faele 없음: '+현재)
        if tiragalo_boleng_go_tsenya_tshedimošo == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 go_tsenya_tshedimošo_ntlha 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Tsejana in sorted((기준.parents[1]/'example/java').glob('*.java')):
        mohlodi = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Tsejana.read_text())
        for Leina in re.findall(r'\b[^\W\d]\w*\b', mohlodi, re.UNICODE):
            if Leina not in 예약어 and all(ord(tlhaka_boleng)<128 for tlhaka_boleng in Leina):
                실패들.append('{}: 예제의 영어 sešupi_boleng {}'.format(Tsejana.name, Leina))
    for Leina in ('창', 'konope', 'leibole', 'SMS_lefelwana', '화면구성요소', 'tiragalo_lenaneotetelo', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        mohlodi = (기준/'한국어자바/한국어/자체'/(Leina+'.java')).read_text()
        mohlodi = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', mohlodi)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', mohlodi):
            실패들.append(Leina+': 한국어 직접 구현에 표준 selo_boleng 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Leina in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Leina in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Leina: '+Leina)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Leina in ('Inthanete_Lapa', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Leina+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makhro_boleng 사용: '+Leina)
    자바파일수 = 0
    for 뿌리 in ('mohlodi', 'mošomiši/자바', '한국어자바'):
        for Tsejana in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            mohlodi = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Tsejana.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', mohlodi):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Tsejana.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', mohlodi):
                실패들.append('{}: 공개 예외 선언'.format(Tsejana.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Tsejana in sorted((저장소/'os/mohlodi').glob('*.java')):
        x86자바파일수 += 1
        mohlodi = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Tsejana.read_text())
        for Leina in re.findall(r'\b[^\W\d]\w*\b', mohlodi, re.UNICODE):
            if Leina not in 예약어 | 표준자바이름 and all(ord(tlhaka_boleng)<128 for tlhaka_boleng in Leina):
                실패들.append('{}: 자체 영어 sešupi_boleng {}'.format(Tsejana.relative_to(저장소), Leina))
    pego_rei = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Ditholosi/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Phošo) for Phošo in 분석['Phošo'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for go_tsenya_tshedimošo_boleng in 분석['선언'].values():
            Leina = go_tsenya_tshedimošo_boleng['Leina']; Tsejana = Path(go_tsenya_tshedimošo_boleng['Faele'])
            mohlodi = Tsejana.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if mohlodi[go_tsenya_tshedimošo_boleng['E_Šetšego_boleng']:go_tsenya_tshedimošo_boleng['E_Šetšego_boleng']+len(Leina)] == Leina.encode() and Leina not in 공개규약:
                실패들.append('{}:{}: {}'.format(Tsejana.relative_to(기준), go_tsenya_tshedimošo_boleng['줄'], Leina))
        pego_rei['c_semantic_checked'] = True
        pego_rei['c_source_sha256'] = {str(Path(Faele).relative_to(기준)):haše_faele for Faele,haše_faele in 분석['원문해시'].items()}
    pego_rei['passed'] = not 실패들; pego_rei['failures'] = 실패들
    boyo_boleng = 기준/'build/verification/naming'; boyo_boleng.mkdir(parents=True, exist_ok=True)
    (boyo_boleng/'report.json').write_text(json.dumps(pego_rei, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Faele Tsejana·호환 go_tsenya_tshedimošo_ntlha·통신 예제')

if __name__ == '__main__': Diriša()
