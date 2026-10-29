#!/usr/bin/env python3
"""명명 cliop·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

tilg_freumh = Path(__file__).resolve().parents[1]
저장소 = tilg_freumh.parents[1]

def ruith():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    cùis_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    faidhle_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Slighe in list((tilg_freumh/'innealan').glob('*.py')) + list((tilg_freumh/'예제').rglob('*.py')) + 공용번역기들:
        if Slighe.name.endswith(('이름반영.py', '이름분석.py')): continue
        faidhle_COUNT += 1
        나무 = ast.parse(Slighe.read_text()); 나무들[Slighe] = 나무
        for cur_a_steach_VALUE in ast.walk(나무):
            if isinstance(cur_a_steach_VALUE, ast.FunctionDef):
                매개변수표.setdefault(cur_a_steach_VALUE.name, set()).update(인자.arg for 인자 in cur_a_steach_VALUE.args.args + cur_a_steach_VALUE.args.kwonlyargs)
                if cur_a_steach_VALUE.args.kwarg: 가변매개함수.add(cur_a_steach_VALUE.name)
            if isinstance(cur_a_steach_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in cur_a_steach_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        매개변수표.setdefault(cur_a_steach_VALUE.name, set()).update(인자.arg for 인자 in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Ainm = ''
            if isinstance(cur_a_steach_VALUE, (ast.FunctionDef, ast.ClassDef)): Ainm = cur_a_steach_VALUE.name
            elif isinstance(cur_a_steach_VALUE, ast.Name) and isinstance(cur_a_steach_VALUE.ctx, ast.Store): Ainm = cur_a_steach_VALUE.id
            elif isinstance(cur_a_steach_VALUE, ast.arg): Ainm = cur_a_steach_VALUE.arg
            if Ainm and Ainm not in cùis_VALUE and all(ord(caractar_VALUE)<128 for caractar_VALUE in Ainm):
                실패들.append('{}:{}: {}'.format(Slighe.relative_to(저장소), cur_a_steach_VALUE.lineno, Ainm))
    for Slighe, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ainm = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ainm not in 매개변수표 or Ainm in 가변매개함수 or not any(ord(caractar_VALUE)>127 for caractar_VALUE in Ainm): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Ainm]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Slighe.relative_to(저장소), 호출.lineno, Ainm, 인자.arg))
    for loidhne in (tilg_freumh/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Pròiseas_VALUE_cur_a_steach = loidhne.split('\t')
        if not (tilg_freumh/현재).is_file(): 실패들.append('gluais_VALUE faidhle 없음: '+현재)
        if Pròiseas_VALUE_cur_a_steach == '호환진입점유지' and not (tilg_freumh/이전).is_file(): 실패들.append('호환 cur_a_steach_puing 없음: '+이전)
    예제 = (tilg_freumh.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Slighe in sorted((tilg_freumh.parents[1]/'example/java').glob('*.java')):
        tùs = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Slighe.read_text())
        for Ainm in re.findall(r'\b[^\W\d]\w*\b', tùs, re.UNICODE):
            if Ainm not in 예약어 and all(ord(caractar_VALUE)<128 for caractar_VALUE in Ainm):
                실패들.append('{}: 예제의 영어 aithnichear_VALUE {}'.format(Slighe.name, Ainm))
    for Ainm in ('창', 'putan', 'bileag', 'raon_teacsa', '화면구성요소', 'tachartas_ciutha', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        tùs = (tilg_freumh/'한국어자바/한국어/자체'/(Ainm+'.java')).read_text()
        tùs = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', tùs)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', tùs):
            실패들.append(Ainm+': 한국어 직접 구현에 표준 nì_VALUE 래퍼가 남았습니다.')
    시언어예제 = (tilg_freumh.parents[1]/'example/c/네트워크예제.c').read_text()
    for Ainm in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ainm in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ainm: '+Ainm)
    파이썬예제 = (tilg_freumh.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (tilg_freumh.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ainm in ('neul_teaghlach', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Ainm+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 macro_VALUE 사용: '+Ainm)
    자바파일수 = 0
    for freumh_VALUE in ('tùs', 'cleachdaiche/자바', '한국어자바'):
        for Slighe in (tilg_freumh/freumh_VALUE).rglob('*.java'):
            자바파일수 += 1
            tùs = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Slighe.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', tùs):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Slighe.relative_to(tilg_freumh), 맞음[1]))
            if freumh_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', tùs):
                실패들.append('{}: 공개 예외 선언'.format(Slighe.relative_to(tilg_freumh)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Slighe in sorted((저장소/'os/tùs').glob('*.java')):
        x86자바파일수 += 1
        tùs = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Slighe.read_text())
        for Ainm in re.findall(r'\b[^\W\d]\w*\b', tùs, re.UNICODE):
            if Ainm not in 예약어 | 표준자바이름 and all(ord(caractar_VALUE)<128 for caractar_VALUE in Ainm):
                실패들.append('{}: 자체 영어 aithnichear_VALUE {}'.format(Slighe.relative_to(저장소), Ainm))
    LOG_ràgh = {'passed': False, 'python_files': faidhle_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(tilg_freumh/'innealan/시언어이름분석.py')])
        분석 = json.loads((tilg_freumh/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Mearachd) for Mearachd in 분석['Mearachd'])
        공개규약 = set(json.loads((tilg_freumh/'명명/규격이름.json').read_text()))
        for cur_a_steach_VALUE in 분석['선언'].values():
            Ainm = cur_a_steach_VALUE['Ainm']; Slighe = Path(cur_a_steach_VALUE['faidhle'])
            tùs = Slighe.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if tùs[cur_a_steach_VALUE['OFFSET_VALUE']:cur_a_steach_VALUE['OFFSET_VALUE']+len(Ainm)] == Ainm.encode() and Ainm not in 공개규약:
                실패들.append('{}:{}: {}'.format(Slighe.relative_to(tilg_freumh), cur_a_steach_VALUE['줄'], Ainm))
        LOG_ràgh['c_semantic_checked'] = True
        LOG_ràgh['c_source_sha256'] = {str(Path(faidhle).relative_to(tilg_freumh)):hais_faidhle for faidhle,hais_faidhle in 분석['원문해시'].items()}
    LOG_ràgh['passed'] = not 실패들; LOG_ràgh['failures'] = 실패들
    ceann_uidhe_VALUE = tilg_freumh/'build/verification/naming'; ceann_uidhe_VALUE.mkdir(parents=True, exist_ok=True)
    (ceann_uidhe_VALUE/'report.json').write_text(json.dumps(LOG_ràgh, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·faidhle Slighe·호환 cur_a_steach_puing·통신 예제')

if __name__ == '__main__': ruith()
