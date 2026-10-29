#!/usr/bin/env python3
"""명명 ntipanye·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Bido():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    ngō_valuu = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ụzọ_ozi in list((기준/'Ngwaọrụ').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if ụzọ_ozi.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ụzọ_ozi.read_text()); 나무들[ụzọ_ozi] = 나무
        for ndebà_valuu in ast.walk(나무):
            if isinstance(ndebà_valuu, ast.FunctionDef):
                매개변수표.setdefault(ndebà_valuu.name, set()).update(인자.arg for 인자 in ndebà_valuu.args.args + ndebà_valuu.args.kwonlyargs)
                if ndebà_valuu.args.kwarg: 가변매개함수.add(ndebà_valuu.name)
            if isinstance(ndebà_valuu, ast.ClassDef):
                for ọrụ_valuu in ndebà_valuu.body:
                    if isinstance(ọrụ_valuu, ast.FunctionDef) and ọrụ_valuu.name == '__init__':
                        매개변수표.setdefault(ndebà_valuu.name, set()).update(인자.arg for 인자 in ọrụ_valuu.args.args + ọrụ_valuu.args.kwonlyargs)
            Aha = ''
            if isinstance(ndebà_valuu, (ast.FunctionDef, ast.ClassDef)): Aha = ndebà_valuu.name
            elif isinstance(ndebà_valuu, ast.Name) and isinstance(ndebà_valuu.ctx, ast.Store): Aha = ndebà_valuu.id
            elif isinstance(ndebà_valuu, ast.arg): Aha = ndebà_valuu.arg
            if Aha and Aha not in ngō_valuu and all(ord(mkpụrụedemede_valuu)<128 for mkpụrụedemede_valuu in Aha):
                실패들.append('{}:{}: {}'.format(ụzọ_ozi.relative_to(저장소), ndebà_valuu.lineno, Aha))
    for ụzọ_ozi, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Aha = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Aha not in 매개변수표 or Aha in 가변매개함수 or not any(ord(mkpụrụedemede_valuu)>127 for mkpụrụedemede_valuu in Aha): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Aha]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ụzọ_ozi.relative_to(저장소), 호출.lineno, Aha, 인자.arg))
    for ahịrī in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ùsòrò_valuu_ndebà = ahịrī.split('\t')
        if not (기준/현재).is_file(): 실패들.append('gàa_valuu Faịlụ 없음: '+현재)
        if ùsòrò_valuu_ndebà == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ndebà_akara 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ụzọ_ozi in sorted((기준.parents[1]/'example/java').glob('*.java')):
        ebensìbịa = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ụzọ_ozi.read_text())
        for Aha in re.findall(r'\b[^\W\d]\w*\b', ebensìbịa, re.UNICODE):
            if Aha not in 예약어 and all(ord(mkpụrụedemede_valuu)<128 for mkpụrụedemede_valuu in Aha):
                실패들.append('{}: 예제의 영어 ihe_nkọwapụta_valuu {}'.format(ụzọ_ozi.name, Aha))
    for Aha in ('창', 'ọdụmbi', 'nnyeahà', 'SMS_fild', '화면구성요소', 'mmèrème_ọgbàrànchere', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ebensìbịa = (기준/'한국어자바/한국어/자체'/(Aha+'.java')).read_text()
        ebensìbịa = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ebensìbịa)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ebensìbịa):
            실패들.append(Aha+': 한국어 직접 구현에 표준 ihe_valuu 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Aha in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Aha in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Aha: '+Aha)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Aha in ('urukpu_Ezinụlọ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Aha+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 nkèokpookpo_valuu 사용: '+Aha)
    자바파일수 = 0
    for 뿌리 in ('ebensìbịa', 'òjìàrụ/자바', '한국어자바'):
        for ụzọ_ozi in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            ebensìbịa = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ụzọ_ozi.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ebensìbịa):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(ụzọ_ozi.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ebensìbịa):
                실패들.append('{}: 공개 예외 선언'.format(ụzọ_ozi.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ụzọ_ozi in sorted((저장소/'os/ebensìbịa').glob('*.java')):
        x86자바파일수 += 1
        ebensìbịa = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ụzọ_ozi.read_text())
        for Aha in re.findall(r'\b[^\W\d]\w*\b', ebensìbịa, re.UNICODE):
            if Aha not in 예약어 | 표준자바이름 and all(ord(mkpụrụedemede_valuu)<128 for mkpụrụedemede_valuu in Aha):
                실패들.append('{}: 자체 영어 ihe_nkọwapụta_valuu {}'.format(ụzọ_ozi.relative_to(저장소), Aha))
    ndekọ_NDEKỌ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Ngwaọrụ/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(mmejọ) for mmejọ in 분석['mmejọ'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ndebà_valuu in 분석['선언'].values():
            Aha = ndebà_valuu['Aha']; ụzọ_ozi = Path(ndebà_valuu['Faịlụ'])
            ebensìbịa = ụzọ_ozi.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ebensìbịa[ndebà_valuu['Nnokwata_valuu']:ndebà_valuu['Nnokwata_valuu']+len(Aha)] == Aha.encode() and Aha not in 공개규약:
                실패들.append('{}:{}: {}'.format(ụzọ_ozi.relative_to(기준), ndebà_valuu['줄'], Aha))
        ndekọ_NDEKỌ['c_semantic_checked'] = True
        ndekọ_NDEKỌ['c_source_sha256'] = {str(Path(Faịlụ).relative_to(기준)):di_ike_ọbọakwụkwọ for Faịlụ,di_ike_ọbọakwụkwọ in 분석['원문해시'].items()}
    ndekọ_NDEKỌ['passed'] = not 실패들; ndekọ_NDEKỌ['failures'] = 실패들
    ebemwèga_valuu = 기준/'build/verification/naming'; ebemwèga_valuu.mkdir(parents=True, exist_ok=True)
    (ebemwèga_valuu/'report.json').write_text(json.dumps(ndekọ_NDEKỌ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Faịlụ ụzọ_ozi·호환 ndebà_akara·통신 예제')

if __name__ == '__main__': Bido()
