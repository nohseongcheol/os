#!/usr/bin/env python3
"""명명 клип·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def порча():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    кор_қимат = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for масир in list((기준/'Абзорҳо').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if масир.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(масир.read_text()); 나무들[масир] = 나무
        for ворида_қимат in ast.walk(나무):
            if isinstance(ворида_қимат, ast.FunctionDef):
                매개변수표.setdefault(ворида_қимат.name, set()).update(인자.arg for 인자 in ворида_қимат.args.args + ворида_қимат.args.kwonlyargs)
                if ворида_қимат.args.kwarg: 가변매개함수.add(ворида_қимат.name)
            if isinstance(ворида_қимат, ast.ClassDef):
                for функсия_қимат in ворида_қимат.body:
                    if isinstance(функсия_қимат, ast.FunctionDef) and функсия_қимат.name == '__init__':
                        매개변수표.setdefault(ворида_қимат.name, set()).update(인자.arg for 인자 in функсия_қимат.args.args + функсия_қимат.args.kwonlyargs)
            Ном = ''
            if isinstance(ворида_қимат, (ast.FunctionDef, ast.ClassDef)): Ном = ворида_қимат.name
            elif isinstance(ворида_қимат, ast.Name) and isinstance(ворида_қимат.ctx, ast.Store): Ном = ворида_қимат.id
            elif isinstance(ворида_қимат, ast.arg): Ном = ворида_қимат.arg
            if Ном and Ном not in кор_қимат and all(ord(аломат_қимат_068c2631)<128 for аломат_қимат_068c2631 in Ном):
                실패들.append('{}:{}: {}'.format(масир.relative_to(저장소), ворида_қимат.lineno, Ном))
    for масир, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ном = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ном not in 매개변수표 or Ном in 가변매개함수 or not any(ord(аломат_қимат_068c2631)>127 for аломат_қимат_068c2631 in Ном): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Ном]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(масир.relative_to(저장소), 호출.lineno, Ном, 인자.arg))
    for хат in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Раванд_қимат_ворида = хат.split('\t')
        if not (기준/현재).is_file(): 실패들.append('интиқол_додан_қимат Файл 없음: '+현재)
        if Раванд_қимат_ворида == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ворида_нуқта 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for масир in sorted((기준.parents[1]/'example/java').glob('*.java')):
        манбаъ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', масир.read_text())
        for Ном in re.findall(r'\b[^\W\d]\w*\b', манбаъ, re.UNICODE):
            if Ном not in 예약어 and all(ord(аломат_қимат_068c2631)<128 for аломат_қимат_068c2631 in Ном):
                실패들.append('{}: 예제의 영어 идентификатор_қимат {}'.format(масир.name, Ном))
    for Ном in ('창', 'тугма', 'барчасп', 'Матн_майдон', '화면구성요소', 'рӯйдод_навбат', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        манбаъ = (기준/'한국어자바/한국어/자체'/(Ном+'.java')).read_text()
        манбаъ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', манбаъ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', манбаъ):
            실패들.append(Ном+': 한국어 직접 구현에 표준 объект_қимат 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Ном in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ном in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ном: '+Ном)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ном in ('абр_Оила', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Ном+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макро_қимат 사용: '+Ном)
    자바파일수 = 0
    for 뿌리 in ('манбаъ', 'корбар/자바', '한국어자바'):
        for масир in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            манбаъ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', масир.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', манбаъ):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(масир.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', манбаъ):
                실패들.append('{}: 공개 예외 선언'.format(масир.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for масир in sorted((저장소/'os/манбаъ').glob('*.java')):
        x86자바파일수 += 1
        манбаъ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', масир.read_text())
        for Ном in re.findall(r'\b[^\W\d]\w*\b', манбаъ, re.UNICODE):
            if Ном not in 예약어 | 표준자바이름 and all(ord(аломат_қимат_068c2631)<128 for аломат_қимат_068c2631 in Ном):
                실패들.append('{}: 자체 영어 идентификатор_қимат {}'.format(масир.relative_to(저장소), Ном))
    сабт_кардан_сабт = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Абзорҳо/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Хато) for Хато in 분석['Хато'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ворида_қимат in 분석['선언'].values():
            Ном = ворида_қимат['Ном']; масир = Path(ворида_қимат['Файл'])
            манбаъ = масир.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if манбаъ[ворида_қимат['Интиқолшавӣ_қимат']:ворида_қимат['Интиқолшавӣ_қимат']+len(Ном)] == Ном.encode() and Ном not in 공개규약:
                실패들.append('{}:{}: {}'.format(масир.relative_to(기준), ворида_қимат['줄'], Ном))
        сабт_кардан_сабт['c_semantic_checked'] = True
        сабт_кардан_сабт['c_source_sha256'] = {str(Path(Файл).relative_to(기준)):ҳэш_файл for Файл,ҳэш_файл in 분석['원문해시'].items()}
    сабт_кардан_сабт['passed'] = not 실패들; сабт_кардан_сабт['failures'] = 실패들
    ҷои_таъинот_қимат = 기준/'build/verification/naming'; ҷои_таъинот_қимат.mkdir(parents=True, exist_ok=True)
    (ҷои_таъинот_қимат/'report.json').write_text(json.dumps(сабт_кардан_сабт, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Файл масир·호환 ворида_нуқта·통신 예제')

if __name__ == '__main__': порча()
