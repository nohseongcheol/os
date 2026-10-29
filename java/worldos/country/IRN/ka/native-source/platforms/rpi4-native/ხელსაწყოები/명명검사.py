#!/usr/bin/env python3
"""명명 კლიპი·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]
저장소 = პროეცირება_ფესვი.parents[1]

def გაშვება():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    დავალება_მნიშვნელობა = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for გეზი in list((პროეცირება_ფესვი/'ხელსაწყოები').glob('*.py')) + list((პროეცირება_ფესვი/'예제').rglob('*.py')) + 공용번역기들:
        if გეზი.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(გეზი.read_text()); 나무들[გეზი] = 나무
        for შენატანი_მნიშვნელობა in ast.walk(나무):
            if isinstance(შენატანი_მნიშვნელობა, ast.FunctionDef):
                매개변수표.setdefault(შენატანი_მნიშვნელობა.name, set()).update(인자.arg for 인자 in შენატანი_მნიშვნელობა.args.args + შენატანი_მნიშვნელობა.args.kwonlyargs)
                if შენატანი_მნიშვნელობა.args.kwarg: 가변매개함수.add(შენატანი_მნიშვნელობა.name)
            if isinstance(შენატანი_მნიშვნელობა, ast.ClassDef):
                for ფუნქცია_მნიშვნელობა in შენატანი_მნიშვნელობა.body:
                    if isinstance(ფუნქცია_მნიშვნელობა, ast.FunctionDef) and ფუნქცია_მნიშვნელობა.name == '__init__':
                        매개변수표.setdefault(შენატანი_მნიშვნელობა.name, set()).update(인자.arg for 인자 in ფუნქცია_მნიშვნელობა.args.args + ფუნქცია_მნიშვნელობა.args.kwonlyargs)
            სახელი = ''
            if isinstance(შენატანი_მნიშვნელობა, (ast.FunctionDef, ast.ClassDef)): სახელი = შენატანი_მნიშვნელობა.name
            elif isinstance(შენატანი_მნიშვნელობა, ast.Name) and isinstance(შენატანი_მნიშვნელობა.ctx, ast.Store): სახელი = შენატანი_მნიშვნელობა.id
            elif isinstance(შენატანი_მნიშვნელობა, ast.arg): სახელი = შენატანი_მნიშვნელობა.arg
            if სახელი and სახელი not in დავალება_მნიშვნელობა and all(ord(სიმბოლო_მნიშვნელობა_068c2631)<128 for სიმბოლო_მნიშვნელობა_068c2631 in სახელი):
                실패들.append('{}:{}: {}'.format(გეზი.relative_to(저장소), შენატანი_მნიშვნელობა.lineno, სახელი))
    for გეზი, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            სახელი = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if სახელი not in 매개변수표 or სახელი in 가변매개함수 or not any(ord(სიმბოლო_მნიშვნელობა_068c2631)>127 for სიმბოლო_მნიშვნელობა_068c2631 in სახელი): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[სახელი]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(გეზი.relative_to(저장소), 호출.lineno, სახელი, 인자.arg))
    for ხაზი in (პროეცირება_ფესვი/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, პროცესი_მნიშვნელობა_შენატანი = ხაზი.split('\t')
        if not (პროეცირება_ფესვი/현재).is_file(): 실패들.append('გადატანა_მნიშვნელობა ფაილი 없음: '+현재)
        if პროცესი_მნიშვნელობა_შენატანი == '호환진입점유지' and not (პროეცირება_ფესვი/이전).is_file(): 실패들.append('호환 შენატანი_პტ 없음: '+이전)
    예제 = (პროეცირება_ფესვი.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for გეზი in sorted((პროეცირება_ფესვი.parents[1]/'example/java').glob('*.java')):
        წყარო = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', გეზი.read_text())
        for სახელი in re.findall(r'\b[^\W\d]\w*\b', წყარო, re.UNICODE):
            if სახელი not in 예약어 and all(ord(სიმბოლო_მნიშვნელობა_068c2631)<128 for სიმბოლო_მნიშვნელობა_068c2631 in სახელი):
                실패들.append('{}: 예제의 영어 იდენტიფიკატორი_მნიშვნელობა {}'.format(გეზი.name, სახელი))
    for სახელი in ('창', 'ღილაკი', 'სათაური', 'ტექსტური_ველი', '화면구성요소', 'მოვლენა_რიგი', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        წყარო = (პროეცირება_ფესვი/'한국어자바/한국어/자체'/(სახელი+'.java')).read_text()
        წყარო = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', წყარო)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', წყარო):
            실패들.append(სახელი+': 한국어 직접 구현에 표준 ობიექტი_მნიშვნელობა 래퍼가 남았습니다.')
    시언어예제 = (პროეცირება_ფესვი.parents[1]/'example/c/네트워크예제.c').read_text()
    for სახელი in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if სახელი in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 სახელი: '+სახელი)
    파이썬예제 = (პროეცირება_ფესვი.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (პროეცირება_ფესვი.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for სახელი in ('ინტერნეტი_ოჯახი', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+სახელი+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 მაკრო_მნიშვნელობა 사용: '+სახელი)
    자바파일수 = 0
    for ფესვი_მნიშვნელობა in ('წყარო', 'მომხმარებელი/자바', '한국어자바'):
        for გეზი in (პროეცირება_ფესვი/ფესვი_მნიშვნელობა).rglob('*.java'):
            자바파일수 += 1
            წყარო = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', გეზი.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', წყარო):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(გეზი.relative_to(პროეცირება_ფესვი), 맞음[1]))
            if ფესვი_მნიშვნელობა == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', წყარო):
                실패들.append('{}: 공개 예외 선언'.format(გეზი.relative_to(პროეცირება_ფესვი)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for გეზი in sorted((저장소/'os/წყარო').glob('*.java')):
        x86자바파일수 += 1
        წყარო = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', გეზი.read_text())
        for სახელი in re.findall(r'\b[^\W\d]\w*\b', წყარო, re.UNICODE):
            if სახელი not in 예약어 | 표준자바이름 and all(ord(სიმბოლო_მნიშვნელობა_068c2631)<128 for სიმბოლო_მნიშვნელობა_068c2631 in სახელი):
                실패들.append('{}: 자체 영어 იდენტიფიკატორი_მნიშვნელობა {}'.format(გეზი.relative_to(저장소), სახელი))
    ჟურნალი_ჩაწერა = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(პროეცირება_ფესვი/'ხელსაწყოები/시언어이름분석.py')])
        분석 = json.loads((პროეცირება_ფესვი/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(შეცდომა) for შეცდომა in 분석['შეცდომა'])
        공개규약 = set(json.loads((პროეცირება_ფესვი/'명명/규격이름.json').read_text()))
        for შენატანი_მნიშვნელობა in 분석['선언'].values():
            სახელი = შენატანი_მნიშვნელობა['სახელი']; გეზი = Path(შენატანი_მნიშვნელობა['ფაილი'])
            წყარო = გეზი.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if წყარო[შენატანი_მნიშვნელობა['ოფსეტი_მნიშვნელობა']:შენატანი_მნიშვნელობა['ოფსეტი_მნიშვნელობა']+len(სახელი)] == სახელი.encode() and სახელი not in 공개규약:
                실패들.append('{}:{}: {}'.format(გეზი.relative_to(პროეცირება_ფესვი), შენატანი_მნიშვნელობა['줄'], სახელი))
        ჟურნალი_ჩაწერა['c_semantic_checked'] = True
        ჟურნალი_ჩაწერა['c_source_sha256'] = {str(Path(ფაილი).relative_to(პროეცირება_ფესვი)):ჰეში_ფაილი for ფაილი,ჰეში_ფაილი in 분석['원문해시'].items()}
    ჟურნალი_ჩაწერა['passed'] = not 실패들; ჟურნალი_ჩაწერა['failures'] = 실패들
    მიმართულება_მნიშვნელობა = პროეცირება_ფესვი/'build/verification/naming'; მიმართულება_მნიშვნელობა.mkdir(parents=True, exist_ok=True)
    (მიმართულება_მნიშვნელობა/'report.json').write_text(json.dumps(ჟურნალი_ჩაწერა, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·ფაილი გეზი·호환 შენატანი_პტ·통신 예제')

if __name__ == '__main__': გაშვება()
