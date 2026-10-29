#!/usr/bin/env python3
"""명명 klipp·unntak·경로를 검사한다. --시언어는 libclang erklæring 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

spegle_rot = Path(__file__).resolve().parents[1]
저장소 = spegle_rot.parents[1]

def Køyr_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    Argument = 해석기.parse_args()
    실패들 = []
    sak_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fil_COUNT = 0
    parameter_tabell = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for STIGE in list((spegle_rot/'Verktøy').glob('*.py')) + list((spegle_rot/'예제').rglob('*.py')) + 공용번역기들:
        if STIGE.name.endswith(('이름반영.py', '이름분석.py')): continue
        fil_COUNT += 1
        나무 = ast.parse(STIGE.read_text()); 나무들[STIGE] = 나무
        for oppføring_VALUE in ast.walk(나무):
            if isinstance(oppføring_VALUE, ast.FunctionDef):
                parameter_tabell.setdefault(oppføring_VALUE.name, set()).update(parameter_argument.arg for parameter_argument in oppføring_VALUE.args.args + oppføring_VALUE.args.kwonlyargs)
                if oppføring_VALUE.args.kwarg: 가변매개함수.add(oppføring_VALUE.name)
            if isinstance(oppføring_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in oppføring_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parameter_tabell.setdefault(oppføring_VALUE.name, set()).update(parameter_argument.arg for parameter_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Namn = ''
            if isinstance(oppføring_VALUE, (ast.FunctionDef, ast.ClassDef)): Namn = oppføring_VALUE.name
            elif isinstance(oppføring_VALUE, ast.Name) and isinstance(oppføring_VALUE.ctx, ast.Store): Namn = oppføring_VALUE.id
            elif isinstance(oppføring_VALUE, ast.arg): Namn = oppføring_VALUE.arg
            if Namn and Namn not in sak_VALUE and all(ord(teikn_VALUE)<128 for teikn_VALUE in Namn):
                실패들.append('{}:{}: {}'.format(STIGE.relative_to(저장소), oppføring_VALUE.lineno, Namn))
    for STIGE, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Namn = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Namn not in parameter_tabell or Namn in 가변매개함수 or not any(ord(teikn_VALUE)>127 for teikn_VALUE in Namn): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabell[Namn]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(STIGE.relative_to(저장소), 호출.lineno, Namn, parameter_argument.arg))
    for linje in (spegle_rot/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, betalt_vare, Prosess_VALUE_oppføring = linje.split('\t')
        if not (spegle_rot/betalt_vare).is_file(): 실패들.append('flytte_VALUE Fil 없음: '+betalt_vare)
        if Prosess_VALUE_oppføring == '호환진입점유지' and not (spegle_rot/이전).is_file(): 실패들.append('호환 oppføring_p 없음: '+이전)
    예제 = (spegle_rot.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for STIGE in sorted((spegle_rot.parents[1]/'example/java').glob('*.java')):
        KJELDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', STIGE.read_text())
        for Namn in re.findall(r'\b[^\W\d]\w*\b', KJELDE, re.UNICODE):
            if Namn not in 예약어 and all(ord(teikn_VALUE)<128 for teikn_VALUE in Namn):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(STIGE.name, Namn))
    for Namn in ('창', 'knapp', 'Etikett', 'SMS_felt', '화면구성요소', 'hending_kø', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        KJELDE = (spegle_rot/'한국어자바/한국어/자체'/(Namn+'.java')).read_text()
        KJELDE = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', KJELDE)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', KJELDE):
            실패들.append(Namn+': 한국어 직접 구현에 표준 objekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (spegle_rot.parents[1]/'example/c/네트워크예제.c').read_text()
    for Namn in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Namn in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Namn: '+Namn)
    파이썬예제 = (spegle_rot.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 unntak 직접 사용')
    머리 = (spegle_rot.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Namn in ('sky_Familie', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'Opprett_endepunkt', '자료전문보내기'):
        if re.search(r'^#define\s+'+Namn+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE 사용: '+Namn)
    자바파일수 = 0
    for rot_VALUE in ('KJELDE', 'brukar/자바', '한국어자바'):
        for STIGE in (spegle_rot/rot_VALUE).rglob('*.java'):
            자바파일수 += 1
            KJELDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', STIGE.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', KJELDE):
                실패들.append('{}: 한국어화되지 않은 erklæring {}'.format(STIGE.relative_to(spegle_rot), 맞음[1]))
            if rot_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', KJELDE):
                실패들.append('{}: 공개 unntak erklæring'.format(STIGE.relative_to(spegle_rot)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for STIGE in sorted((저장소/'os/KJELDE').glob('*.java')):
        x86자바파일수 += 1
        KJELDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', STIGE.read_text())
        for Namn in re.findall(r'\b[^\W\d]\w*\b', KJELDE, re.UNICODE):
            if Namn not in 예약어 | 표준자바이름 and all(ord(teikn_VALUE)<128 for teikn_VALUE in Namn):
                실패들.append('{}: 자체 영어 identifikator_VALUE {}'.format(STIGE.relative_to(저장소), Namn))
    LOG_rad = {'passed': False, 'python_files': fil_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argument.시언어:
        subprocess.check_call(['python3', str(spegle_rot/'Verktøy/시언어이름분석.py')])
        분석 = json.loads((spegle_rot/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(FEIL) for FEIL in 분석['FEIL'])
        공개규약 = set(json.loads((spegle_rot/'명명/규격이름.json').read_text()))
        for oppføring_VALUE in 분석['erklæring'].values():
            Namn = oppføring_VALUE['Namn']; STIGE = Path(oppføring_VALUE['Fil'])
            KJELDE = STIGE.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if KJELDE[oppføring_VALUE['OFFSET_VALUE']:oppføring_VALUE['OFFSET_VALUE']+len(Namn)] == Namn.encode() and Namn not in 공개규약:
                실패들.append('{}:{}: {}'.format(STIGE.relative_to(spegle_rot), oppføring_VALUE['linje'], Namn))
        LOG_rad['c_semantic_checked'] = True
        LOG_rad['c_source_sha256'] = {str(Path(Fil).relative_to(spegle_rot)):hash_fil for Fil,hash_fil in 분석['원문해시'].items()}
    LOG_rad['passed'] = not 실패들; LOG_rad['failures'] = 실패들
    mål_VALUE = spegle_rot/'build/verification/naming'; mål_VALUE.mkdir(parents=True, exist_ok=True)
    (mål_VALUE/'report.json').write_text(json.dumps(LOG_rad, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 erklæring·Fil STIGE·호환 oppføring_p·통신 예제')

if __name__ == '__main__': Køyr_2()
