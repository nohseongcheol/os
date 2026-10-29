#!/usr/bin/env python3
"""명명 క్లిప్·మినహాయింపు·경로를 검사한다. --시언어는 libclang ప్రకటన 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
రిపోజిటరీ_మూలం = ప్రొజెక్ట్_మూలం.parents[1]

def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = పార్సర్_48ee4b1b.parse_args()
    실패들 = []
    పని_మూల్యం_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    పారామీటర్_పట్టిక = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [రిపోజిటరీ_మూలం/'compiler/컴파일러.py', రిపోజిటరీ_మూలం/'compiler/기계어미리번역.py']
    for పాత్ in list((ప్రొజెక్ట్_మూలం/'ఉపకరణాలు').glob('*.py')) + list((ప్రొజెక్ట్_మూలం/'예제').rglob('*.py')) + 공용번역기들:
        if పాత్.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(పాత్.read_text()); 나무들[పాత్] = 나무
        for ప్రవేశం_మూల్యం in ast.walk(나무):
            if isinstance(ప్రవేశం_మూల్యం, ast.FunctionDef):
                పారామీటర్_పట్టిక.setdefault(ప్రవేశం_మూల్యం.name, set()).update(పారామీటర్_కారకం.arg for పారామీటర్_కారకం in ప్రవేశం_మూల్యం.args.args + ప్రవేశం_మూల్యం.args.kwonlyargs)
                if ప్రవేశం_మూల్యం.args.kwarg: 가변매개함수.add(ప్రవేశం_మూల్యం.name)
            if isinstance(ప్రవేశం_మూల్యం, ast.ClassDef):
                for కార్యం_మూల్యం in ప్రవేశం_మూల్యం.body:
                    if isinstance(కార్యం_మూల్యం, ast.FunctionDef) and కార్యం_మూల్యం.name == '__init__':
                        పారామీటర్_పట్టిక.setdefault(ప్రవేశం_మూల్యం.name, set()).update(పారామీటర్_కారకం.arg for పారామీటర్_కారకం in కార్యం_మూల్యం.args.args + కార్యం_మూల్యం.args.kwonlyargs)
            పేరు = ''
            if isinstance(ప్రవేశం_మూల్యం, (ast.FunctionDef, ast.ClassDef)): పేరు = ప్రవేశం_మూల్యం.name
            elif isinstance(ప్రవేశం_మూల్యం, ast.Name) and isinstance(ప్రవేశం_మూల్యం.ctx, ast.Store): పేరు = ప్రవేశం_మూల్యం.id
            elif isinstance(ప్రవేశం_మూల్యం, ast.arg): పేరు = ప్రవేశం_మూల్యం.arg
            if పేరు and పేరు not in పని_మూల్యం_102996da and all(ord(అక్షరం_మూల్యం)<128 for అక్షరం_మూల్యం in పేరు):
                실패들.append('{}:{}: {}'.format(పాత్.relative_to(రిపోజిటరీ_మూలం), ప్రవేశం_మూల్యం.lineno, పేరు))
    for పాత్, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            పేరు = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if పేరు not in పారామీటర్_పట్టిక or పేరు in 가변매개함수 or not any(ord(అక్షరం_మూల్యం)>127 for అక్షరం_మూల్యం in పేరు): continue
            for పారామీటర్_కారకం in 호출.keywords:
                if పారామీటర్_కారకం.arg and పారామీటర్_కారకం.arg not in పారామీటర్_పట్టిక[పేరు]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(పాత్.relative_to(రిపోజిటరీ_మూలం), 호출.lineno, పేరు, పారామీటర్_కారకం.arg))
    for పంక్తి in (ప్రొజెక్ట్_మూలం/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, విధానం_మూల్యం_ప్రవేశం = పంక్తి.split('\t')
        if not (ప్రొజెక్ట్_మూలం/현재).is_file(): 실패들.append('తరలించు_మూల్యం దస్త్రం 없음: '+현재)
        if విధానం_మూల్యం_ప్రవేశం == '호환진입점유지' and not (ప్రొజెక్ట్_మూలం/이전).is_file(): 실패들.append('호환 ప్రవేశం_పాయింట్ 없음: '+이전)
    예제 = (ప్రొజెక్ట్_మూలం.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for పాత్ in sorted((ప్రొజెక్ట్_మూలం.parents[1]/'example/java').glob('*.java')):
        వనరు = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', పాత్.read_text())
        for పేరు in re.findall(r'\b[^\W\d]\w*\b', వనరు, re.UNICODE):
            if పేరు not in 예약어 and all(ord(అక్షరం_మూల్యం)<128 for అక్షరం_మూల్యం in పేరు):
                실패들.append('{}: 예제의 영어 ఐడెంటిఫయర్_మూల్యం {}'.format(పాత్.name, పేరు))
    for పేరు in ('విండో', 'బటన్', 'లేబుల్', 'పాఠం_ఫీల్డ్', '화면구성요소', 'ఈవెంట్_నిరీక్షణ_క్రమం', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        వనరు = (ప్రొజెక్ట్_మూలం/'한국어자바/한국어/자체'/(పేరు+'.java')).read_text()
        వనరు = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', వనరు)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', వనరు):
            실패들.append(పేరు+': 한국어 직접 구현에 표준 అంశం_మూల్యం 래퍼가 남았습니다.')
    시언어예제 = (ప్రొజెక్ట్_మూలం.parents[1]/'example/c/네트워크예제.c').read_text()
    for పేరు in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if పేరు in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 పేరు: '+పేరు)
    파이썬예제 = (ప్రొజెక్ట్_మూలం.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 మినహాయింపు 직접 사용')
    머리 = (ప్రొజెక్ట్_మూలం.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for పేరు in ('మేఘం_కుటుంబం', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+పేరు+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 మ్యాక్రో_మూల్యం 사용: '+పేరు)
    자바파일수 = 0
    for మూలం_మూల్యం in ('వనరు', 'వినియోగదారు/자바', '한국어자바'):
        for పాత్ in (ప్రొజెక్ట్_మూలం/మూలం_మూల్యం).rglob('*.java'):
            자바파일수 += 1
            వనరు = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', పాత్.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', వనరు):
                실패들.append('{}: 한국어화되지 않은 ప్రకటన {}'.format(పాత్.relative_to(ప్రొజెక్ట్_మూలం), 맞음[1]))
            if మూలం_మూల్యం == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', వనరు):
                실패들.append('{}: 공개 మినహాయింపు ప్రకటన'.format(పాత్.relative_to(ప్రొజెక్ట్_మూలం)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for పాత్ in sorted((రిపోజిటరీ_మూలం/'os/వనరు').glob('*.java')):
        x86자바파일수 += 1
        వనరు = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', పాత్.read_text())
        for పేరు in re.findall(r'\b[^\W\d]\w*\b', వనరు, re.UNICODE):
            if పేరు not in 예약어 | 표준자바이름 and all(ord(అక్షరం_మూల్యం)<128 for అక్షరం_మూల్యం in పేరు):
                실패들.append('{}: 자체 영어 ఐడెంటిఫయర్_మూల్యం {}'.format(పాత్.relative_to(రిపోజిటరీ_మూలం), పేరు))
    లాగ్_వరుస = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/시언어이름분석.py')])
        분석 = json.loads((ప్రొజెక్ట్_మూలం/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(దోషం) for దోషం in 분석['దోషం'])
        공개규약 = set(json.loads((ప్రొజెక్ట్_మూలం/'명명/규격이름.json').read_text()))
        for ప్రవేశం_మూల్యం in 분석['ప్రకటన'].values():
            పేరు = ప్రవేశం_మూల్యం['పేరు']; పాత్ = Path(ప్రవేశం_మూల్యం['దస్త్రం'])
            వనరు = పాత్.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if వనరు[ప్రవేశం_మూల్యం['ఆఫ్_సెట్_మూల్యం']:ప్రవేశం_మూల్యం['ఆఫ్_సెట్_మూల్యం']+len(పేరు)] == పేరు.encode() and పేరు not in 공개규약:
                실패들.append('{}:{}: {}'.format(పాత్.relative_to(ప్రొజెక్ట్_మూలం), ప్రవేశం_మూల్యం['줄'], పేరు))
        లాగ్_వరుస['c_semantic_checked'] = True
        లాగ్_వరుస['c_source_sha256'] = {str(Path(దస్త్రం).relative_to(ప్రొజెక్ట్_మూలం)):హాష్_ఫైలు for దస్త్రం,హాష్_ఫైలు in 분석['원문해시'].items()}
    లాగ్_వరుస['passed'] = not 실패들; లాగ్_వరుస['failures'] = 실패들
    గమ్యం_మూల్యం = ప్రొజెక్ట్_మూలం/'build/verification/naming'; గమ్యం_మూల్యం.mkdir(parents=True, exist_ok=True)
    (గమ్యం_మూల్యం/'report.json').write_text(json.dumps(లాగ్_వరుస, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 ప్రకటన·దస్త్రం పాత్·호환 ప్రవేశం_పాయింట్·통신 예제')

if __name__ == '__main__': నడుపుము()
