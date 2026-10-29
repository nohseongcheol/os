#!/usr/bin/env python3
"""명명 snit·uitsondering·경로를 검사한다. --시언어는 libclang verklaring 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_wortel = Path(__file__).resolve().parents[1]
bewaarplek_wortel = Project_wortel.parents[1]

def Loop():
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = ontleder_48ee4b1b.parse_args()
    실패들 = []
    saak_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    lêer_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [bewaarplek_wortel/'compiler/컴파일러.py', bewaarplek_wortel/'compiler/기계어미리번역.py']
    for Pad in list((Project_wortel/'Nutsmiddels').glob('*.py')) + list((Project_wortel/'예제').rglob('*.py')) + 공용번역기들:
        if Pad.name.endswith(('이름반영.py', '이름분석.py')): continue
        lêer_COUNT += 1
        나무 = ast.parse(Pad.read_text()); 나무들[Pad] = 나무
        for inskrywing_VALUE in ast.walk(나무):
            if isinstance(inskrywing_VALUE, ast.FunctionDef):
                매개변수표.setdefault(inskrywing_VALUE.name, set()).update(인자.arg for 인자 in inskrywing_VALUE.args.args + inskrywing_VALUE.args.kwonlyargs)
                if inskrywing_VALUE.args.kwarg: 가변매개함수.add(inskrywing_VALUE.name)
            if isinstance(inskrywing_VALUE, ast.ClassDef):
                for funksie_VALUE in inskrywing_VALUE.body:
                    if isinstance(funksie_VALUE, ast.FunctionDef) and funksie_VALUE.name == '__init__':
                        매개변수표.setdefault(inskrywing_VALUE.name, set()).update(인자.arg for 인자 in funksie_VALUE.args.args + funksie_VALUE.args.kwonlyargs)
            Naam = ''
            if isinstance(inskrywing_VALUE, (ast.FunctionDef, ast.ClassDef)): Naam = inskrywing_VALUE.name
            elif isinstance(inskrywing_VALUE, ast.Name) and isinstance(inskrywing_VALUE.ctx, ast.Store): Naam = inskrywing_VALUE.id
            elif isinstance(inskrywing_VALUE, ast.arg): Naam = inskrywing_VALUE.arg
            if Naam and Naam not in saak_VALUE and all(ord(karakter_VALUE)<128 for karakter_VALUE in Naam):
                실패들.append('{}:{}: {}'.format(Pad.relative_to(bewaarplek_wortel), inskrywing_VALUE.lineno, Naam))
    for Pad, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Naam = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Naam not in 매개변수표 or Naam in 가변매개함수 or not any(ord(karakter_VALUE)>127 for karakter_VALUE in Naam): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Naam]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Pad.relative_to(bewaarplek_wortel), 호출.lineno, Naam, 인자.arg))
    for lyn in (Project_wortel/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proses_VALUE_inskrywing = lyn.split('\t')
        if not (Project_wortel/현재).is_file(): 실패들.append('skuif_VALUE Lêer 없음: '+현재)
        if Proses_VALUE_inskrywing == '호환진입점유지' and not (Project_wortel/이전).is_file(): 실패들.append('호환 inskrywing_p 없음: '+이전)
    예제 = (Project_wortel.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Pad in sorted((Project_wortel.parents[1]/'example/java').glob('*.java')):
        Bron = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Pad.read_text())
        for Naam in re.findall(r'\b[^\W\d]\w*\b', Bron, re.UNICODE):
            if Naam not in 예약어 and all(ord(karakter_VALUE)<128 for karakter_VALUE in Naam):
                실패들.append('{}: 예제의 영어 waarde_VALUE {}'.format(Pad.name, Naam))
    for Naam in ('창', 'knoppie', 'etiket', 'SMS_veld', '화면구성요소', 'gebeurtenis_tou', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Bron = (Project_wortel/'한국어자바/한국어/자체'/(Naam+'.java')).read_text()
        Bron = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Bron)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Bron):
            실패들.append(Naam+': 한국어 직접 구현에 표준 objek_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_wortel.parents[1]/'example/c/네트워크예제.c').read_text()
    for Naam in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Naam in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Naam: '+Naam)
    파이썬예제 = (Project_wortel.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 uitsondering 직접 사용')
    머리 = (Project_wortel.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Naam in ('wolk_Gesin', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Naam+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE 사용: '+Naam)
    자바파일수 = 0
    for wortel_VALUE in ('Bron', 'gebruiker/자바', '한국어자바'):
        for Pad in (Project_wortel/wortel_VALUE).rglob('*.java'):
            자바파일수 += 1
            Bron = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Pad.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Bron):
                실패들.append('{}: 한국어화되지 않은 verklaring {}'.format(Pad.relative_to(Project_wortel), 맞음[1]))
            if wortel_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Bron):
                실패들.append('{}: 공개 uitsondering verklaring'.format(Pad.relative_to(Project_wortel)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Pad in sorted((bewaarplek_wortel/'os/Bron').glob('*.java')):
        x86자바파일수 += 1
        Bron = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Pad.read_text())
        for Naam in re.findall(r'\b[^\W\d]\w*\b', Bron, re.UNICODE):
            if Naam not in 예약어 | 표준자바이름 and all(ord(karakter_VALUE)<128 for karakter_VALUE in Naam):
                실패들.append('{}: 자체 영어 waarde_VALUE {}'.format(Pad.relative_to(bewaarplek_wortel), Naam))
    LOG_ry = {'passed': False, 'python_files': lêer_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(Project_wortel/'Nutsmiddels/시언어이름분석.py')])
        분석 = json.loads((Project_wortel/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Fout) for Fout in 분석['Fout'])
        공개규약 = set(json.loads((Project_wortel/'명명/규격이름.json').read_text()))
        for inskrywing_VALUE in 분석['verklaring'].values():
            Naam = inskrywing_VALUE['Naam']; Pad = Path(inskrywing_VALUE['Lêer'])
            Bron = Pad.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Bron[inskrywing_VALUE['OFFSET_VALUE']:inskrywing_VALUE['OFFSET_VALUE']+len(Naam)] == Naam.encode() and Naam not in 공개규약:
                실패들.append('{}:{}: {}'.format(Pad.relative_to(Project_wortel), inskrywing_VALUE['줄'], Naam))
        LOG_ry['c_semantic_checked'] = True
        LOG_ry['c_source_sha256'] = {str(Path(Lêer).relative_to(Project_wortel)):huts_lêer for Lêer,huts_lêer in 분석['원문해시'].items()}
    LOG_ry['passed'] = not 실패들; LOG_ry['failures'] = 실패들
    bestemming_VALUE = Project_wortel/'build/verification/naming'; bestemming_VALUE.mkdir(parents=True, exist_ok=True)
    (bestemming_VALUE/'report.json').write_text(json.dumps(LOG_ry, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 verklaring·Lêer Pad·호환 inskrywing_p·통신 예제')

if __name__ == '__main__': Loop()
