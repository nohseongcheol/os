#!/usr/bin/env python3
"""명명 klipp·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

pprojetta_għerq = Path(__file__).resolve().parents[1]
저장소 = pprojetta_għerq.parents[1]

def serje():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    każ_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fajl_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for mogħdija in list((pprojetta_għerq/'Għodod').glob('*.py')) + list((pprojetta_għerq/'예제').rglob('*.py')) + 공용번역기들:
        if mogħdija.name.endswith(('이름반영.py', '이름분석.py')): continue
        fajl_COUNT += 1
        나무 = ast.parse(mogħdija.read_text()); 나무들[mogħdija] = 나무
        for entrata_VALUE in ast.walk(나무):
            if isinstance(entrata_VALUE, ast.FunctionDef):
                매개변수표.setdefault(entrata_VALUE.name, set()).update(인자.arg for 인자 in entrata_VALUE.args.args + entrata_VALUE.args.kwonlyargs)
                if entrata_VALUE.args.kwarg: 가변매개함수.add(entrata_VALUE.name)
            if isinstance(entrata_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in entrata_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        매개변수표.setdefault(entrata_VALUE.name, set()).update(인자.arg for 인자 in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            isem = ''
            if isinstance(entrata_VALUE, (ast.FunctionDef, ast.ClassDef)): isem = entrata_VALUE.name
            elif isinstance(entrata_VALUE, ast.Name) and isinstance(entrata_VALUE.ctx, ast.Store): isem = entrata_VALUE.id
            elif isinstance(entrata_VALUE, ast.arg): isem = entrata_VALUE.arg
            if isem and isem not in każ_VALUE and all(ord(karattru_VALUE)<128 for karattru_VALUE in isem):
                실패들.append('{}:{}: {}'.format(mogħdija.relative_to(저장소), entrata_VALUE.lineno, isem))
    for mogħdija, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            isem = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if isem not in 매개변수표 or isem in 가변매개함수 or not any(ord(karattru_VALUE)>127 for karattru_VALUE in isem): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[isem]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(mogħdija.relative_to(저장소), 호출.lineno, isem, 인자.arg))
    for linja in (pprojetta_għerq/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proċess_VALUE_entrata = linja.split('\t')
        if not (pprojetta_għerq/현재).is_file(): 실패들.append('mexxi_VALUE fajl 없음: '+현재)
        if Proċess_VALUE_entrata == '호환진입점유지' and not (pprojetta_għerq/이전).is_file(): 실패들.append('호환 entrata_punt 없음: '+이전)
    예제 = (pprojetta_għerq.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for mogħdija in sorted((pprojetta_għerq.parents[1]/'example/java').glob('*.java')):
        sors = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', mogħdija.read_text())
        for isem in re.findall(r'\b[^\W\d]\w*\b', sors, re.UNICODE):
            if isem not in 예약어 and all(ord(karattru_VALUE)<128 for karattru_VALUE in isem):
                실패들.append('{}: 예제의 영어 identifikatur_VALUE {}'.format(mogħdija.name, isem))
    for isem in ('창', 'buttuna', 'tikketta', 'qasam_ta_test', '화면구성요소', 'avveniment_kju', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        sors = (pprojetta_għerq/'한국어자바/Malti/자체'/(isem+'.java')).read_text()
        sors = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', sors)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', sors):
            실패들.append(isem+': Malti 직접 구현에 표준 oġġett_VALUE 래퍼가 남았습니다.')
    시언어예제 = (pprojetta_għerq.parents[1]/'example/c/네트워크예제.c').read_text()
    for isem in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if isem in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 isem: '+isem)
    파이썬예제 = (pprojetta_għerq.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (pprojetta_għerq.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for isem in ('cloud_Familja', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+isem+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE 사용: '+isem)
    자바파일수 = 0
    for għerq_VALUE in ('sors', 'utent/자바', '한국어자바'):
        for mogħdija in (pprojetta_għerq/għerq_VALUE).rglob('*.java'):
            자바파일수 += 1
            sors = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', mogħdija.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', sors):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(mogħdija.relative_to(pprojetta_għerq), 맞음[1]))
            if għerq_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', sors):
                실패들.append('{}: 공개 예외 선언'.format(mogħdija.relative_to(pprojetta_għerq)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for mogħdija in sorted((저장소/'os/sors').glob('*.java')):
        x86자바파일수 += 1
        sors = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', mogħdija.read_text())
        for isem in re.findall(r'\b[^\W\d]\w*\b', sors, re.UNICODE):
            if isem not in 예약어 | 표준자바이름 and all(ord(karattru_VALUE)<128 for karattru_VALUE in isem):
                실패들.append('{}: 자체 영어 identifikatur_VALUE {}'.format(mogħdija.relative_to(저장소), isem))
    LOG_RECORD = {'passed': False, 'python_files': fajl_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(pprojetta_għerq/'Għodod/시언어이름분석.py')])
        분석 = json.loads((pprojetta_għerq/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(żball) for żball in 분석['żball'])
        공개규약 = set(json.loads((pprojetta_għerq/'명명/규격이름.json').read_text()))
        for entrata_VALUE in 분석['선언'].values():
            isem = entrata_VALUE['isem']; mogħdija = Path(entrata_VALUE['fajl'])
            sors = mogħdija.read_bytes()
            # Malti 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if sors[entrata_VALUE['OFFSET_VALUE']:entrata_VALUE['OFFSET_VALUE']+len(isem)] == isem.encode() and isem not in 공개규약:
                실패들.append('{}:{}: {}'.format(mogħdija.relative_to(pprojetta_għerq), entrata_VALUE['줄'], isem))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(fajl).relative_to(pprojetta_għerq)):hash_fajl for fajl,hash_fajl in 분석['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    destinazzjoni_VALUE = pprojetta_għerq/'build/verification/naming'; destinazzjoni_VALUE.mkdir(parents=True, exist_ok=True)
    (destinazzjoni_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Malti 선언·fajl mogħdija·호환 entrata_punt·통신 예제')

if __name__ == '__main__': serje()
