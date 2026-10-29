#!/usr/bin/env python3
"""명명 klip·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Bitir():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    ýumuş_baha_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Ýol in list((기준/'Gurallar').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if Ýol.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Ýol.read_text()); 나무들[Ýol] = 나무
        for girizmeklik_baha in ast.walk(나무):
            if isinstance(girizmeklik_baha, ast.FunctionDef):
                매개변수표.setdefault(girizmeklik_baha.name, set()).update(인자.arg for 인자 in girizmeklik_baha.args.args + girizmeklik_baha.args.kwonlyargs)
                if girizmeklik_baha.args.kwarg: 가변매개함수.add(girizmeklik_baha.name)
            if isinstance(girizmeklik_baha, ast.ClassDef):
                for FUNCTION_baha in girizmeklik_baha.body:
                    if isinstance(FUNCTION_baha, ast.FunctionDef) and FUNCTION_baha.name == '__init__':
                        매개변수표.setdefault(girizmeklik_baha.name, set()).update(인자.arg for 인자 in FUNCTION_baha.args.args + FUNCTION_baha.args.kwonlyargs)
            Ad = ''
            if isinstance(girizmeklik_baha, (ast.FunctionDef, ast.ClassDef)): Ad = girizmeklik_baha.name
            elif isinstance(girizmeklik_baha, ast.Name) and isinstance(girizmeklik_baha.ctx, ast.Store): Ad = girizmeklik_baha.id
            elif isinstance(girizmeklik_baha, ast.arg): Ad = girizmeklik_baha.arg
            if Ad and Ad not in ýumuş_baha_102996da and all(ord(nyşan_baha_068c2631)<128 for nyşan_baha_068c2631 in Ad):
                실패들.append('{}:{}: {}'.format(Ýol.relative_to(저장소), girizmeklik_baha.lineno, Ad))
    for Ýol, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ad = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ad not in 매개변수표 or Ad in 가변매개함수 or not any(ord(nyşan_baha_068c2631)>127 for nyşan_baha_068c2631 in Ad): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Ad]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Ýol.relative_to(저장소), 호출.lineno, Ad, 인자.arg))
    for setir in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proses_baha_girizmeklik = setir.split('\t')
        if not (기준/현재).is_file(): 실패들.append('ýerini_üýtget_baha Faýl 없음: '+현재)
        if Proses_baha_girizmeklik == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 girizmeklik_utuk 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Ýol in sorted((기준.parents[1]/'example/java').glob('*.java')):
        Çeşme = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Ýol.read_text())
        for Ad in re.findall(r'\b[^\W\d]\w*\b', Çeşme, re.UNICODE):
            if Ad not in 예약어 and all(ord(nyşan_baha_068c2631)<128 for nyşan_baha_068c2631 in Ad):
                실패들.append('{}: 예제의 영어 tanaýjy_baha {}'.format(Ýol.name, Ad))
    for Ad in ('창', 'düwme', 'belgi', 'tekst_meýdançasy', '화면구성요소', 'waka_nobat', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Çeşme = (기준/'한국어자바/한국어/자체'/(Ad+'.java')).read_text()
        Çeşme = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Çeşme)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Çeşme):
            실패들.append(Ad+': 한국어 직접 구현에 표준 obýekt_baha 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Ad in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ad in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ad: '+Ad)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ad in ('bulut_Maşgala', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Ad+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makros_baha 사용: '+Ad)
    자바파일수 = 0
    for 뿌리 in ('Çeşme', 'ulanyjy/자바', '한국어자바'):
        for Ýol in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            Çeşme = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Ýol.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Çeşme):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Ýol.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Çeşme):
                실패들.append('{}: 공개 예외 선언'.format(Ýol.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Ýol in sorted((저장소/'os/Çeşme').glob('*.java')):
        x86자바파일수 += 1
        Çeşme = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Ýol.read_text())
        for Ad in re.findall(r'\b[^\W\d]\w*\b', Çeşme, re.UNICODE):
            if Ad not in 예약어 | 표준자바이름 and all(ord(nyşan_baha_068c2631)<128 for nyşan_baha_068c2631 in Ad):
                실패들.append('{}: 자체 영어 tanaýjy_baha {}'.format(Ýol.relative_to(저장소), Ad))
    hasaba_alyş_setir = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Gurallar/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Hata) for Hata in 분석['Hata'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for girizmeklik_baha in 분석['선언'].values():
            Ad = girizmeklik_baha['Ad']; Ýol = Path(girizmeklik_baha['Faýl'])
            Çeşme = Ýol.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Çeşme[girizmeklik_baha['Süýşüriş_baha']:girizmeklik_baha['Süýşüriş_baha']+len(Ad)] == Ad.encode() and Ad not in 공개규약:
                실패들.append('{}:{}: {}'.format(Ýol.relative_to(기준), girizmeklik_baha['줄'], Ad))
        hasaba_alyş_setir['c_semantic_checked'] = True
        hasaba_alyş_setir['c_source_sha256'] = {str(Path(Faýl).relative_to(기준)):heş_kody_faýl for Faýl,heş_kody_faýl in 분석['원문해시'].items()}
    hasaba_alyş_setir['passed'] = not 실패들; hasaba_alyş_setir['failures'] = 실패들
    barylmaly_ýer_baha = 기준/'build/verification/naming'; barylmaly_ýer_baha.mkdir(parents=True, exist_ok=True)
    (barylmaly_ýer_baha/'report.json').write_text(json.dumps(hasaba_alyş_setir, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Faýl Ýol·호환 girizmeklik_utuk·통신 예제')

if __name__ == '__main__': Bitir()
