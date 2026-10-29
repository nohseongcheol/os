#!/usr/bin/env python3
"""명명 klip·istisna·경로를 검사한다. --시언어는 libclang bəyannamə 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_kök = Path(__file__).resolve().parents[1]
anbar_kök = Project_kök.parents[1]

def İcra_Et():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = parser_48ee4b1b.parse_args()
    실패들 = []
    müqavilə_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fayl_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [anbar_kök/'compiler/컴파일러.py', anbar_kök/'compiler/기계어미리번역.py']
    for Cığır in list((Project_kök/'Alətlər').glob('*.py')) + list((Project_kök/'예제').rglob('*.py')) + 공용번역기들:
        if Cığır.name.endswith(('이름반영.py', '이름분석.py')): continue
        fayl_COUNT += 1
        나무 = ast.parse(Cığır.read_text()); 나무들[Cığır] = 나무
        for daxiletmə_VALUE in ast.walk(나무):
            if isinstance(daxiletmə_VALUE, ast.FunctionDef):
                매개변수표.setdefault(daxiletmə_VALUE.name, set()).update(인자.arg for 인자 in daxiletmə_VALUE.args.args + daxiletmə_VALUE.args.kwonlyargs)
                if daxiletmə_VALUE.args.kwarg: 가변매개함수.add(daxiletmə_VALUE.name)
            if isinstance(daxiletmə_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in daxiletmə_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        매개변수표.setdefault(daxiletmə_VALUE.name, set()).update(인자.arg for 인자 in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Ad = ''
            if isinstance(daxiletmə_VALUE, (ast.FunctionDef, ast.ClassDef)): Ad = daxiletmə_VALUE.name
            elif isinstance(daxiletmə_VALUE, ast.Name) and isinstance(daxiletmə_VALUE.ctx, ast.Store): Ad = daxiletmə_VALUE.id
            elif isinstance(daxiletmə_VALUE, ast.arg): Ad = daxiletmə_VALUE.arg
            if Ad and Ad not in müqavilə_VALUE and all(ord(simvol_VALUE_068c2631)<128 for simvol_VALUE_068c2631 in Ad):
                실패들.append('{}:{}: {}'.format(Cığır.relative_to(anbar_kök), daxiletmə_VALUE.lineno, Ad))
    for Cığır, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ad = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ad not in 매개변수표 or Ad in 가변매개함수 or not any(ord(simvol_VALUE_068c2631)>127 for simvol_VALUE_068c2631 in Ad): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Ad]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Cığır.relative_to(anbar_kök), 호출.lineno, Ad, 인자.arg))
    for Giriş in (Project_kök/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proses_VALUE_daxiletmə = Giriş.split('\t')
        if not (Project_kök/현재).is_file(): 실패들.append('hərəkət_etdir_VALUE FAYL 없음: '+현재)
        if Proses_VALUE_daxiletmə == '호환진입점유지' and not (Project_kök/이전).is_file(): 실패들.append('호환 daxiletmə_p 없음: '+이전)
    예제 = (Project_kök.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Cığır in sorted((Project_kök.parents[1]/'example/java').glob('*.java')):
        QAYNAQ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cığır.read_text())
        for Ad in re.findall(r'\b[^\W\d]\w*\b', QAYNAQ, re.UNICODE):
            if Ad not in 예약어 and all(ord(simvol_VALUE_068c2631)<128 for simvol_VALUE_068c2631 in Ad):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(Cığır.name, Ad))
    for Ad in ('창', 'düymə', 'Etiket', 'SMS_sahə', '화면구성요소', 'hadisə_növbə', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        QAYNAQ = (Project_kök/'한국어자바/한국어/자체'/(Ad+'.java')).read_text()
        QAYNAQ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', QAYNAQ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', QAYNAQ):
            실패들.append(Ad+': 한국어 직접 구현에 표준 obyekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_kök.parents[1]/'example/c/네트워크예제.c').read_text()
    for Ad in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ad in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ad: '+Ad)
    파이썬예제 = (Project_kök.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 istisna 직접 사용')
    머리 = (Project_kök.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ad in ('bulud_Ailə', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Ad+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makros_VALUE 사용: '+Ad)
    자바파일수 = 0
    for kök_VALUE in ('QAYNAQ', 'istifadəçi/자바', '한국어자바'):
        for Cığır in (Project_kök/kök_VALUE).rglob('*.java'):
            자바파일수 += 1
            QAYNAQ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cığır.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', QAYNAQ):
                실패들.append('{}: 한국어화되지 않은 bəyannamə {}'.format(Cığır.relative_to(Project_kök), 맞음[1]))
            if kök_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', QAYNAQ):
                실패들.append('{}: 공개 istisna bəyannamə'.format(Cığır.relative_to(Project_kök)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Cığır in sorted((anbar_kök/'os/QAYNAQ').glob('*.java')):
        x86자바파일수 += 1
        QAYNAQ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cığır.read_text())
        for Ad in re.findall(r'\b[^\W\d]\w*\b', QAYNAQ, re.UNICODE):
            if Ad not in 예약어 | 표준자바이름 and all(ord(simvol_VALUE_068c2631)<128 for simvol_VALUE_068c2631 in Ad):
                실패들.append('{}: 자체 영어 identifikator_VALUE {}'.format(Cığır.relative_to(anbar_kök), Ad))
    LOG_yaz = {'passed': False, 'python_files': fayl_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(Project_kök/'Alətlər/시언어이름분석.py')])
        분석 = json.loads((Project_kök/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(XƏTA) for XƏTA in 분석['XƏTA'])
        공개규약 = set(json.loads((Project_kök/'명명/규격이름.json').read_text()))
        for daxiletmə_VALUE in 분석['bəyannamə'].values():
            Ad = daxiletmə_VALUE['Ad']; Cığır = Path(daxiletmə_VALUE['FAYL'])
            QAYNAQ = Cığır.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if QAYNAQ[daxiletmə_VALUE['OFFSET_VALUE']:daxiletmə_VALUE['OFFSET_VALUE']+len(Ad)] == Ad.encode() and Ad not in 공개규약:
                실패들.append('{}:{}: {}'.format(Cığır.relative_to(Project_kök), daxiletmə_VALUE['Giriş'], Ad))
        LOG_yaz['c_semantic_checked'] = True
        LOG_yaz['c_source_sha256'] = {str(Path(FAYL).relative_to(Project_kök)):heş_fayl for FAYL,heş_fayl in 분석['원문해시'].items()}
    LOG_yaz['passed'] = not 실패들; LOG_yaz['failures'] = 실패들
    təyinat_VALUE_a0fbc067 = Project_kök/'build/verification/naming'; təyinat_VALUE_a0fbc067.mkdir(parents=True, exist_ok=True)
    (təyinat_VALUE_a0fbc067/'report.json').write_text(json.dumps(LOG_yaz, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 bəyannamə·FAYL Cığır·호환 daxiletmə_p·통신 예제')

if __name__ == '__main__': İcra_Et()
