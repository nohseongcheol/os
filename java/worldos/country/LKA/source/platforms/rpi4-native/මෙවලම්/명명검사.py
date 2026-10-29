#!/usr/bin/env python3
"""명명 පසුර·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def ක්_රියාත්මක_කරන්න_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    විස්තාරක = 해석기.parse_args()
    실패들 = []
    කාරණය_අගය = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for මාර්_ගය in list((기준/'මෙවලම්').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if මාර්_ගය.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(මාර්_ගය.read_text()); 나무들[මාර්_ගය] = 나무
        for පිවිසුම_අගය in ast.walk(나무):
            if isinstance(පිවිසුම_අගය, ast.FunctionDef):
                매개변수표.setdefault(පිවිසුම_අගය.name, set()).update(인자.arg for 인자 in පිවිසුම_අගය.args.args + පිවිසුම_අගය.args.kwonlyargs)
                if පිවිසුම_අගය.args.kwarg: 가변매개함수.add(පිවිසුම_අගය.name)
            if isinstance(පිවිසුම_අගය, ast.ClassDef):
                for ශ්_රිතය_අගය in පිවිසුම_අගය.body:
                    if isinstance(ශ්_රිතය_අගය, ast.FunctionDef) and ශ්_රිතය_අගය.name == '__init__':
                        매개변수표.setdefault(පිවිසුම_අගය.name, set()).update(인자.arg for 인자 in ශ්_රිතය_අගය.args.args + ශ්_රිතය_අගය.args.kwonlyargs)
            නම = ''
            if isinstance(පිවිසුම_අගය, (ast.FunctionDef, ast.ClassDef)): නම = පිවිසුම_අගය.name
            elif isinstance(පිවිසුම_අගය, ast.Name) and isinstance(පිවිසුම_අගය.ctx, ast.Store): නම = පිවිසුම_අගය.id
            elif isinstance(පිවිසුම_අගය, ast.arg): නම = පිවිසුම_අගය.arg
            if නම and නම not in කාරණය_අගය and all(ord(අනුලකුණ_අගය)<128 for අනුලකුණ_අගය in නම):
                실패들.append('{}:{}: {}'.format(මාර්_ගය.relative_to(저장소), පිවිසුම_අගය.lineno, නම))
    for මාර්_ගය, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            නම = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if නම not in 매개변수표 or නම in 가변매개함수 or not any(ord(අනුලකුණ_අගය)>127 for අනුලකුණ_අගය in නම): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[නම]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(මාර්_ගය.relative_to(저장소), 호출.lineno, නම, 인자.arg))
    for පේළිය in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, ක්_රියාවලිය_අගය_පිවිසුම = පේළිය.split('\t')
        if not (기준/현재).is_file(): 실패들.append('ගෙනයන්න_අගය ගොනු 없음: '+현재)
        if ක්_රියාවලිය_අගය_පිවිසුම == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 පිවිසුම_ලකුණ 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for මාර්_ගය in sorted((기준.parents[1]/'example/java').glob('*.java')):
        මූලය = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', මාර්_ගය.read_text())
        for නම in re.findall(r'\b[^\W\d]\w*\b', මූලය, re.UNICODE):
            if නම not in 예약어 and all(ord(අනුලකුණ_අගය)<128 for අනුලකුණ_අගය in නම):
                실패들.append('{}: 예제의 영어 හඳුන්වනය_අගය {}'.format(මාර්_ගය.name, නම))
    for නම in ('කවුළුව', 'බොත්තම', 'ලේබලය', 'පෙළ_ක්ෂේත්_රය', '화면구성요소', 'සිද්ධිය_පෙළගැස්ම', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        මූලය = (기준/'한국어자바/한국어/자체'/(නම+'.java')).read_text()
        මූලය = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', මූලය)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', මූලය):
            실패들.append(නම+': 한국어 직접 구현에 표준 වස්තුව_අගය 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for නම in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if නම in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 නම: '+නම)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for නම in ('වළාකුළු_පවුල', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+නම+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 නියෝග_එකලස_අගය 사용: '+නම)
    자바파일수 = 0
    for 뿌리 in ('මූලය', 'පරිශීලක/자바', '한국어자바'):
        for මාර්_ගය in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            මූලය = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', මාර්_ගය.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', මූලය):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(මාර්_ගය.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', මූලය):
                실패들.append('{}: 공개 예외 선언'.format(මාර්_ගය.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for මාර්_ගය in sorted((저장소/'os/මූලය').glob('*.java')):
        x86자바파일수 += 1
        මූලය = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', මාර්_ගය.read_text())
        for නම in re.findall(r'\b[^\W\d]\w*\b', මූලය, re.UNICODE):
            if නම not in 예약어 | 표준자바이름 and all(ord(අනුලකුණ_අගය)<128 for අනුලකුණ_අගය in නම):
                실패들.append('{}: 자체 영어 හඳුන්වනය_අගය {}'.format(මාර්_ගය.relative_to(저장소), නම))
    ලොගය_පේළිය = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if විස්තාරක.시언어:
        subprocess.check_call(['python3', str(기준/'මෙවලම්/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(දෝෂය) for දෝෂය in 분석['දෝෂය'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for පිවිසුම_අගය in 분석['선언'].values():
            නම = පිවිසුම_අගය['නම']; මාර්_ගය = Path(පිවිසුම_අගය['ගොනු'])
            මූලය = මාර්_ගය.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if මූලය[පිවිසුම_අගය['ඕෆ්සෙට්_අගය']:පිවිසුම_අගය['ඕෆ්සෙට්_අගය']+len(නම)] == නම.encode() and නම not in 공개규약:
                실패들.append('{}:{}: {}'.format(මාර්_ගය.relative_to(기준), පිවිසුම_අගය['줄'], නම))
        ලොගය_පේළිය['c_semantic_checked'] = True
        ලොගය_පේළිය['c_source_sha256'] = {str(Path(ගොනු).relative_to(기준)):හෑෂ්_ගොනුව for ගොනු,හෑෂ්_ගොනුව in 분석['원문해시'].items()}
    ලොගය_පේළිය['passed'] = not 실패들; ලොගය_පේළිය['failures'] = 실패들
    ගමනාන්තය_අගය = 기준/'build/verification/naming'; ගමනාන්තය_අගය.mkdir(parents=True, exist_ok=True)
    (ගමනාන්තය_අගය/'report.json').write_text(json.dumps(ලොගය_පේළිය, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·ගොනු මාර්_ගය·호환 පිවිසුම_ලකුණ·통신 예제')

if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()
