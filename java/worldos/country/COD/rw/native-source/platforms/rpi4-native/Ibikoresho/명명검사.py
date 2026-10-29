#!/usr/bin/env python3
"""명명 kiripu·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ihuriro():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    ikibazo_agaciro = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Inzira in list((기준/'Ibikoresho').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if Inzira.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Inzira.read_text()); 나무들[Inzira] = 나무
        for icyinjizwa_agaciro in ast.walk(나무):
            if isinstance(icyinjizwa_agaciro, ast.FunctionDef):
                매개변수표.setdefault(icyinjizwa_agaciro.name, set()).update(인자.arg for 인자 in icyinjizwa_agaciro.args.args + icyinjizwa_agaciro.args.kwonlyargs)
                if icyinjizwa_agaciro.args.kwarg: 가변매개함수.add(icyinjizwa_agaciro.name)
            if isinstance(icyinjizwa_agaciro, ast.ClassDef):
                for FUNCTION_agaciro in icyinjizwa_agaciro.body:
                    if isinstance(FUNCTION_agaciro, ast.FunctionDef) and FUNCTION_agaciro.name == '__init__':
                        매개변수표.setdefault(icyinjizwa_agaciro.name, set()).update(인자.arg for 인자 in FUNCTION_agaciro.args.args + FUNCTION_agaciro.args.kwonlyargs)
            Izina = ''
            if isinstance(icyinjizwa_agaciro, (ast.FunctionDef, ast.ClassDef)): Izina = icyinjizwa_agaciro.name
            elif isinstance(icyinjizwa_agaciro, ast.Name) and isinstance(icyinjizwa_agaciro.ctx, ast.Store): Izina = icyinjizwa_agaciro.id
            elif isinstance(icyinjizwa_agaciro, ast.arg): Izina = icyinjizwa_agaciro.arg
            if Izina and Izina not in ikibazo_agaciro and all(ord(inyuguti_agaciro)<128 for inyuguti_agaciro in Izina):
                실패들.append('{}:{}: {}'.format(Inzira.relative_to(저장소), icyinjizwa_agaciro.lineno, Izina))
    for Inzira, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Izina = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Izina not in 매개변수표 or Izina in 가변매개함수 or not any(ord(inyuguti_agaciro)>127 for inyuguti_agaciro in Izina): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Izina]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Inzira.relative_to(저장소), 호출.lineno, Izina, 인자.arg))
    for umurongo in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Inzira_agaciro_icyinjizwa = umurongo.split('\t')
        if not (기준/현재).is_file(): 실패들.append('kwimura_agaciro Idosiye 없음: '+현재)
        if Inzira_agaciro_icyinjizwa == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 icyinjizwa_inota 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Inzira in sorted((기준.parents[1]/'example/java').glob('*.java')):
        Inkomoko = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Inzira.read_text())
        for Izina in re.findall(r'\b[^\W\d]\w*\b', Inkomoko, re.UNICODE):
            if Izina not in 예약어 and all(ord(inyuguti_agaciro)<128 for inyuguti_agaciro in Izina):
                실패들.append('{}: 예제의 영어 indanga_agaciro {}'.format(Inzira.name, Izina))
    for Izina in ('창', 'buto', 'Akarango', 'SMS_umwanya', '화면구성요소', 'icyabaye_umurongo_utegererezwaho', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Inkomoko = (기준/'한국어자바/Ikinyarwanda/자체'/(Izina+'.java')).read_text()
        Inkomoko = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Inkomoko)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Inkomoko):
            실패들.append(Izina+': Ikinyarwanda 직접 구현에 표준 ikintu_agaciro_2ed200e9 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Izina in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Izina in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Izina: '+Izina)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Izina in ('karawudi_Umuryango', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Izina+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makoro_agaciro 사용: '+Izina)
    자바파일수 = 0
    for 뿌리 in ('Inkomoko', 'ukoresha/자바', '한국어자바'):
        for Inzira in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            Inkomoko = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Inzira.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Inkomoko):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Inzira.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Inkomoko):
                실패들.append('{}: 공개 예외 선언'.format(Inzira.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Inzira in sorted((저장소/'os/Inkomoko').glob('*.java')):
        x86자바파일수 += 1
        Inkomoko = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Inzira.read_text())
        for Izina in re.findall(r'\b[^\W\d]\w*\b', Inkomoko, re.UNICODE):
            if Izina not in 예약어 | 표준자바이름 and all(ord(inyuguti_agaciro)<128 for inyuguti_agaciro in Izina):
                실패들.append('{}: 자체 영어 indanga_agaciro {}'.format(Inzira.relative_to(저장소), Izina))
    kubika_umurongo = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Ibikoresho/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(IKOSA) for IKOSA in 분석['IKOSA'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for icyinjizwa_agaciro in 분석['선언'].values():
            Izina = icyinjizwa_agaciro['Izina']; Inzira = Path(icyinjizwa_agaciro['Idosiye'])
            Inkomoko = Inzira.read_bytes()
            # Ikinyarwanda 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Inkomoko[icyinjizwa_agaciro['Ofuseti_agaciro']:icyinjizwa_agaciro['Ofuseti_agaciro']+len(Izina)] == Izina.encode() and Izina not in 공개규약:
                실패들.append('{}:{}: {}'.format(Inzira.relative_to(기준), icyinjizwa_agaciro['줄'], Izina))
        kubika_umurongo['c_semantic_checked'] = True
        kubika_umurongo['c_source_sha256'] = {str(Path(Idosiye).relative_to(기준)):hashi_dosiye for Idosiye,hashi_dosiye in 분석['원문해시'].items()}
    kubika_umurongo['passed'] = not 실패들; kubika_umurongo['failures'] = 실패들
    aho_ijya_agaciro = 기준/'build/verification/naming'; aho_ijya_agaciro.mkdir(parents=True, exist_ok=True)
    (aho_ijya_agaciro/'report.json').write_text(json.dumps(kubika_umurongo, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Ikinyarwanda 선언·Idosiye Inzira·호환 icyinjizwa_inota·통신 예제')

if __name__ == '__main__': ihuriro()
