#!/usr/bin/env python3
"""명명 ní_ṣókí·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Rọ́ọ̀nù():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    iṣẹ́_iye = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ọ̀nà in list((기준/'Àwọn_irinṣẹ́').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if ọ̀nà.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ọ̀nà.read_text()); 나무들[ọ̀nà] = 나무
        for ìgbéwọlé_iye in ast.walk(나무):
            if isinstance(ìgbéwọlé_iye, ast.FunctionDef):
                매개변수표.setdefault(ìgbéwọlé_iye.name, set()).update(인자.arg for 인자 in ìgbéwọlé_iye.args.args + ìgbéwọlé_iye.args.kwonlyargs)
                if ìgbéwọlé_iye.args.kwarg: 가변매개함수.add(ìgbéwọlé_iye.name)
            if isinstance(ìgbéwọlé_iye, ast.ClassDef):
                for ÀKÀNṢEFỌMÚLÀ_iye in ìgbéwọlé_iye.body:
                    if isinstance(ÀKÀNṢEFỌMÚLÀ_iye, ast.FunctionDef) and ÀKÀNṢEFỌMÚLÀ_iye.name == '__init__':
                        매개변수표.setdefault(ìgbéwọlé_iye.name, set()).update(인자.arg for 인자 in ÀKÀNṢEFỌMÚLÀ_iye.args.args + ÀKÀNṢEFỌMÚLÀ_iye.args.kwonlyargs)
            Orúkọ = ''
            if isinstance(ìgbéwọlé_iye, (ast.FunctionDef, ast.ClassDef)): Orúkọ = ìgbéwọlé_iye.name
            elif isinstance(ìgbéwọlé_iye, ast.Name) and isinstance(ìgbéwọlé_iye.ctx, ast.Store): Orúkọ = ìgbéwọlé_iye.id
            elif isinstance(ìgbéwọlé_iye, ast.arg): Orúkọ = ìgbéwọlé_iye.arg
            if Orúkọ and Orúkọ not in iṣẹ́_iye and all(ord(ẹyọ_ọ̀rọ̀_iye)<128 for ẹyọ_ọ̀rọ̀_iye in Orúkọ):
                실패들.append('{}:{}: {}'.format(ọ̀nà.relative_to(저장소), ìgbéwọlé_iye.lineno, Orúkọ))
    for ọ̀nà, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Orúkọ = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Orúkọ not in 매개변수표 or Orúkọ in 가변매개함수 or not any(ord(ẹyọ_ọ̀rọ̀_iye)>127 for ẹyọ_ọ̀rọ̀_iye in Orúkọ): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Orúkọ]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ọ̀nà.relative_to(저장소), 호출.lineno, Orúkọ, 인자.arg))
    for ìlà in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Ìlànà_iye_ìgbéwọlé = ìlà.split('\t')
        if not (기준/현재).is_file(): 실패들.append('gbé_iye Fáìlì 없음: '+현재)
        if Ìlànà_iye_ìgbéwọlé == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ìgbéwọlé_kókó 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ọ̀nà in sorted((기준.parents[1]/'example/java').glob('*.java')):
        orísun = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ọ̀nà.read_text())
        for Orúkọ in re.findall(r'\b[^\W\d]\w*\b', orísun, re.UNICODE):
            if Orúkọ not in 예약어 and all(ord(ẹyọ_ọ̀rọ̀_iye)<128 for ẹyọ_ọ̀rọ̀_iye in Orúkọ):
                실패들.append('{}: 예제의 영어 Àfidámọ̀_iye {}'.format(ọ̀nà.name, Orúkọ))
    for Orúkọ in ('창', 'bọ́tìnnì', 'àkọlé', 'SMS_àayè_wúnrẹ̀n', '화면구성요소', 'ìgbéṣẹ̀_ìtòléra', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        orísun = (기준/'한국어자바/한국어/자체'/(Orúkọ+'.java')).read_text()
        orísun = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', orísun)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', orísun):
            실패들.append(Orúkọ+': 한국어 직접 구현에 표준 nǹkan_iye 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Orúkọ in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Orúkọ in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Orúkọ: '+Orúkọ)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Orúkọ in ('Íntánẹ́ẹ̀tì_Ẹbí', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Orúkọ+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 àtòpọ̀_bọ́tìnnì_ẹ̀bùrú_iye 사용: '+Orúkọ)
    자바파일수 = 0
    for 뿌리 in ('orísun', 'aṣàmúlò/자바', '한국어자바'):
        for ọ̀nà in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            orísun = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ọ̀nà.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', orísun):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(ọ̀nà.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', orísun):
                실패들.append('{}: 공개 예외 선언'.format(ọ̀nà.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ọ̀nà in sorted((저장소/'os/orísun').glob('*.java')):
        x86자바파일수 += 1
        orísun = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ọ̀nà.read_text())
        for Orúkọ in re.findall(r'\b[^\W\d]\w*\b', orísun, re.UNICODE):
            if Orúkọ not in 예약어 | 표준자바이름 and all(ord(ẹyọ_ọ̀rọ̀_iye)<128 for ẹyọ_ọ̀rọ̀_iye in Orúkọ):
                실패들.append('{}: 자체 영어 Àfidámọ̀_iye {}'.format(ọ̀nà.relative_to(저장소), Orúkọ))
    àkọsílẹ̀_ìṣe_ìlà_ìbú = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Àwọn_irinṣẹ́/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(àṣìṣe) for àṣìṣe in 분석['àṣìṣe'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ìgbéwọlé_iye in 분석['선언'].values():
            Orúkọ = ìgbéwọlé_iye['Orúkọ']; ọ̀nà = Path(ìgbéwọlé_iye['Fáìlì'])
            orísun = ọ̀nà.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if orísun[ìgbéwọlé_iye['Ìtayọ_iye']:ìgbéwọlé_iye['Ìtayọ_iye']+len(Orúkọ)] == Orúkọ.encode() and Orúkọ not in 공개규약:
                실패들.append('{}:{}: {}'.format(ọ̀nà.relative_to(기준), ìgbéwọlé_iye['줄'], Orúkọ))
        àkọsílẹ̀_ìṣe_ìlà_ìbú['c_semantic_checked'] = True
        àkọsílẹ̀_ìṣe_ìlà_ìbú['c_source_sha256'] = {str(Path(Fáìlì).relative_to(기준)):burú_fáìlì for Fáìlì,burú_fáìlì in 분석['원문해시'].items()}
    àkọsílẹ̀_ìṣe_ìlà_ìbú['passed'] = not 실패들; àkọsílẹ̀_ìṣe_ìlà_ìbú['failures'] = 실패들
    èbúté_iye = 기준/'build/verification/naming'; èbúté_iye.mkdir(parents=True, exist_ok=True)
    (èbúté_iye/'report.json').write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Fáìlì ọ̀nà·호환 ìgbéwọlé_kókó·통신 예제')

if __name__ == '__main__': Rọ́ọ̀nù()
