#!/usr/bin/env python3
"""명명 հոլովակ·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

արձակել_արմատ = Path(__file__).resolve().parents[1]
저장소 = արձակել_արմատ.parents[1]

def Գործարկել():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    գործ_արժեք = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Ճանապարհ in list((արձակել_արմատ/'Գործիքներ').glob('*.py')) + list((արձակել_արմատ/'예제').rglob('*.py')) + 공용번역기들:
        if Ճանապարհ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Ճանապարհ.read_text()); 나무들[Ճանապարհ] = 나무
        for մուտքագրում_արժեք in ast.walk(나무):
            if isinstance(մուտքագրում_արժեք, ast.FunctionDef):
                매개변수표.setdefault(մուտքագրում_արժեք.name, set()).update(인자.arg for 인자 in մուտքագրում_արժեք.args.args + մուտքագրում_արժեք.args.kwonlyargs)
                if մուտքագրում_արժեք.args.kwarg: 가변매개함수.add(մուտքագրում_արժեք.name)
            if isinstance(մուտքագրում_արժեք, ast.ClassDef):
                for ՖՈՒՆԿՑԻԱ_արժեք in մուտքագրում_արժեք.body:
                    if isinstance(ՖՈՒՆԿՑԻԱ_արժեք, ast.FunctionDef) and ՖՈՒՆԿՑԻԱ_արժեք.name == '__init__':
                        매개변수표.setdefault(մուտքագրում_արժեք.name, set()).update(인자.arg for 인자 in ՖՈՒՆԿՑԻԱ_արժեք.args.args + ՖՈՒՆԿՑԻԱ_արժեք.args.kwonlyargs)
            Անուն = ''
            if isinstance(մուտքագրում_արժեք, (ast.FunctionDef, ast.ClassDef)): Անուն = մուտքագրում_արժեք.name
            elif isinstance(մուտքագրում_արժեք, ast.Name) and isinstance(մուտքագրում_արժեք.ctx, ast.Store): Անուն = մուտքագրում_արժեք.id
            elif isinstance(մուտքագրում_արժեք, ast.arg): Անուն = մուտքագրում_արժեք.arg
            if Անուն and Անուն not in գործ_արժեք and all(ord(գրանշան_արժեք)<128 for գրանշան_արժեք in Անուն):
                실패들.append('{}:{}: {}'.format(Ճանապարհ.relative_to(저장소), մուտքագրում_արժեք.lineno, Անուն))
    for Ճանապարհ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Անուն = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Անուն not in 매개변수표 or Անուն in 가변매개함수 or not any(ord(գրանշան_արժեք)>127 for գրանշան_արժեք in Անուն): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Անուն]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Ճանապարհ.relative_to(저장소), 호출.lineno, Անուն, 인자.arg))
    for կապ in (արձակել_արմատ/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Ընթացք_արժեք_մուտքագրում = կապ.split('\t')
        if not (արձակել_արմատ/현재).is_file(): 실패들.append('տեղափոխել_արժեք Ֆայլ 없음: '+현재)
        if Ընթացք_արժեք_մուտքագրում == '호환진입점유지' and not (արձակել_արմատ/이전).is_file(): 실패들.append('호환 մուտքագրում_կետ 없음: '+이전)
    예제 = (արձակել_արմատ.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Ճանապարհ in sorted((արձակել_արմատ.parents[1]/'example/java').glob('*.java')):
        ԱՂԲՅՈՒՐ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Ճանապարհ.read_text())
        for Անուն in re.findall(r'\b[^\W\d]\w*\b', ԱՂԲՅՈՒՐ, re.UNICODE):
            if Անուն not in 예약어 and all(ord(գրանշան_արժեք)<128 for գրանշան_արժեք in Անուն):
                실패들.append('{}: 예제의 영어 նույնացուցիչ_արժեք {}'.format(Ճանապարհ.name, Անուն))
    for Անուն in ('창', 'կոճակ', 'Պիտակ', 'գրվածքի_դաշտ', '화면구성요소', 'միջոցառում_հերթ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ԱՂԲՅՈՒՐ = (արձակել_արմատ/'한국어자바/한국어/자체'/(Անուն+'.java')).read_text()
        ԱՂԲՅՈՒՐ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ԱՂԲՅՈՒՐ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ԱՂԲՅՈՒՐ):
            실패들.append(Անուն+': 한국어 직접 구현에 표준 առարկա_արժեք 래퍼가 남았습니다.')
    시언어예제 = (արձակել_արմատ.parents[1]/'example/c/네트워크예제.c').read_text()
    for Անուն in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Անուն in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Անուն: '+Անուն)
    파이썬예제 = (արձակել_արմատ.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (արձակել_արմատ.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Անուն in ('ամպ_Ընտանիք', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Անուն+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 մակրո_արժեք 사용: '+Անուն)
    자바파일수 = 0
    for արմատ_արժեք in ('ԱՂԲՅՈՒՐ', 'օգտվող/자바', '한국어자바'):
        for Ճանապարհ in (արձակել_արմատ/արմատ_արժեք).rglob('*.java'):
            자바파일수 += 1
            ԱՂԲՅՈՒՐ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Ճանապարհ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ԱՂԲՅՈՒՐ):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Ճանապարհ.relative_to(արձակել_արմատ), 맞음[1]))
            if արմատ_արժեք == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ԱՂԲՅՈՒՐ):
                실패들.append('{}: 공개 예외 선언'.format(Ճանապարհ.relative_to(արձակել_արմատ)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Ճանապարհ in sorted((저장소/'os/ԱՂԲՅՈՒՐ').glob('*.java')):
        x86자바파일수 += 1
        ԱՂԲՅՈՒՐ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Ճանապարհ.read_text())
        for Անուն in re.findall(r'\b[^\W\d]\w*\b', ԱՂԲՅՈՒՐ, re.UNICODE):
            if Անուն not in 예약어 | 표준자바이름 and all(ord(գրանշան_արժեք)<128 for գրանշան_արժեք in Անուն):
                실패들.append('{}: 자체 영어 նույնացուցիչ_արժեք {}'.format(Ճանապարհ.relative_to(저장소), Անուն))
    մատյան_տող = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(արձակել_արմատ/'Գործիքներ/시언어이름분석.py')])
        분석 = json.loads((արձակել_արմատ/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Սխալ) for Սխալ in 분석['Սխալ'])
        공개규약 = set(json.loads((արձակել_արմատ/'명명/규격이름.json').read_text()))
        for մուտքագրում_արժեք in 분석['선언'].values():
            Անուն = մուտքագրում_արժեք['Անուն']; Ճանապարհ = Path(մուտքագրում_արժեք['Ֆայլ'])
            ԱՂԲՅՈՒՐ = Ճանապարհ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ԱՂԲՅՈՒՐ[մուտքագրում_արժեք['Տեղաշարժում_արժեք']:մուտքագրում_արժեք['Տեղաշարժում_արժեք']+len(Անուն)] == Անուն.encode() and Անուն not in 공개규약:
                실패들.append('{}:{}: {}'.format(Ճանապարհ.relative_to(արձակել_արմատ), մուտքագրում_արժեք['줄'], Անուն))
        մատյան_տող['c_semantic_checked'] = True
        մատյան_տող['c_source_sha256'] = {str(Path(Ֆայլ).relative_to(արձակել_արմատ)):պատահական_տվյալներ_նիշք for Ֆայլ,պատահական_տվյալներ_նիշք in 분석['원문해시'].items()}
    մատյան_տող['passed'] = not 실패들; մատյան_տող['failures'] = 실패들
    նպատակակետ_արժեք = արձակել_արմատ/'build/verification/naming'; նպատակակետ_արժեք.mkdir(parents=True, exist_ok=True)
    (նպատակակետ_արժեք/'report.json').write_text(json.dumps(մատյան_տող, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Ֆայլ Ճանապարհ·호환 մուտքագրում_կետ·통신 예제')

if __name__ == '__main__': Գործարկել()
