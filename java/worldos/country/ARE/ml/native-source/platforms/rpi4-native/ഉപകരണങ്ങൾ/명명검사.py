#!/usr/bin/env python3
"""명명 ക്ലിപ്പ്·ഒഴിവാക്കൽ·경로를 검사한다. --시언어는 libclang പ്രസ്താവം 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]
കലവറ_വർഗ്ഗമൂലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]

def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    실패들 = []
    കേസ്_മൂല്യം = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    പാരാമീറ്റര്_పట్టిక = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [കലവറ_വർഗ്ഗമൂലം/'compiler/컴파일러.py', കലവറ_വർഗ്ഗമൂലം/'compiler/기계어미리번역.py']
    for വഴി in list((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ').glob('*.py')) + list((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'예제').rglob('*.py')) + 공용번역기들:
        if വഴി.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(വഴി.read_text()); 나무들[വഴി] = 나무
        for എന്_ട്രി_മൂല്യം in ast.walk(나무):
            if isinstance(എന്_ട്രി_മൂല്യം, ast.FunctionDef):
                പാരാമീറ്റര്_పట్టిక.setdefault(എന്_ട്രി_മൂല്യം.name, set()).update(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.arg for പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് in എന്_ട്രി_മൂല്യം.args.args + എന്_ട്രി_മൂല്യം.args.kwonlyargs)
                if എന്_ട്രി_മൂല്യം.args.kwarg: 가변매개함수.add(എന്_ട്രി_മൂല്യം.name)
            if isinstance(എന്_ട്രി_മൂല്യം, ast.ClassDef):
                for കാര്യപ്രവര്_ത്തനം_മൂല്യം in എന്_ട്രി_മൂല്യം.body:
                    if isinstance(കാര്യപ്രവര്_ത്തനം_മൂല്യം, ast.FunctionDef) and കാര്യപ്രവര്_ത്തനം_മൂല്യം.name == '__init__':
                        പാരാമീറ്റര്_పట్టిక.setdefault(എന്_ട്രി_മൂല്യം.name, set()).update(പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.arg for പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് in കാര്യപ്രവര്_ത്തനം_മൂല്യം.args.args + കാര്യപ്രവര്_ത്തനം_മൂല്യം.args.kwonlyargs)
            പേരു് = ''
            if isinstance(എന്_ട്രി_മൂല്യം, (ast.FunctionDef, ast.ClassDef)): പേരു് = എന്_ട്രി_മൂല്യം.name
            elif isinstance(എന്_ട്രി_മൂല്യം, ast.Name) and isinstance(എന്_ട്രി_മൂല്യം.ctx, ast.Store): പേരു് = എന്_ട്രി_മൂല്യം.id
            elif isinstance(എന്_ട്രി_മൂല്യം, ast.arg): പേരു് = എന്_ട്രി_മൂല്യം.arg
            if പേരു് and പേരു് not in കേസ്_മൂല്യം and all(ord(പ്രതീകം_മൂല്യം)<128 for പ്രതീകം_മൂല്യം in പേരു്):
                실패들.append('{}:{}: {}'.format(വഴി.relative_to(കലവറ_വർഗ്ഗമൂലം), എന്_ട്രി_മൂല്യം.lineno, പേരു്))
    for വഴി, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            പേരു് = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if പേരു് not in പാരാമീറ്റര്_పట్టిక or പേരു് in 가변매개함수 or not any(ord(പ്രതീകം_മൂല്യം)>127 for പ്രതീകം_മൂല്യം in പേരു്): continue
            for പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ് in 호출.keywords:
                if പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.arg and പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.arg not in പാരാമീറ്റര്_పట్టిక[പേരു്]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(വഴി.relative_to(കലവറ_വർഗ്ഗമൂലം), 호출.lineno, പേരു്, പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.arg))
    for ലൈൻ in (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, പ്രോസസ്_മൂല്യം_എന്_ട്രി = ലൈൻ.split('\t')
        if not (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/현재).is_file(): 실패들.append('നീക്കുക_മൂല്യം ഫയല് 없음: '+현재)
        if പ്രോസസ്_മൂല്യം_എന്_ട്രി == '호환진입점유지' and not (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/이전).is_file(): 실패들.append('호환 എന്_ട്രി_പോയിന്_റ് 없음: '+이전)
    예제 = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for വഴി in sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]/'example/java').glob('*.java')):
        ഉറവിടം = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', വഴി.read_text())
        for പേരു് in re.findall(r'\b[^\W\d]\w*\b', ഉറവിടം, re.UNICODE):
            if പേരു് not in 예약어 and all(ord(പ്രതീകം_മൂല്യം)<128 for പ്രതീകം_മൂല്യം in പേരു്):
                실패들.append('{}: 예제의 영어 ఐడెంటిఫయర్_മൂല്യം {}'.format(വഴി.name, പേരു്))
    for പേരു് in ('창', 'ബട്ടണ്', 'ലേബല്', 'പാഠ_മണ്ഡലം', '화면구성요소', 'ഇവന്റ്_ക്യൂ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ഉറവിടം = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'한국어자바/한국어/자체'/(പേരു്+'.java')).read_text()
        ഉറവിടം = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ഉറവിടം)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ഉറവിടം):
            실패들.append(പേരു്+': 한국어 직접 구현에 표준 ഓബ്ജക്റ്റ്_മൂല്യം 래퍼가 남았습니다.')
    시언어예제 = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]/'example/c/네트워크예제.c').read_text()
    for പേരു് in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if പേരു് in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 പേരു്: '+പേരു്)
    파이썬예제 = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ഒഴിവാക്കൽ 직접 사용')
    머리 = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for പേരു് in ('ക്ലൌഡ്_കുടുംബം', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'സൃഷ്_ടിക്കുക_അവസാനബിന്ദു', '자료전문보내기'):
        if re.search(r'^#define\s+'+പേരു്+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 മാക്രോ_മൂല്യം 사용: '+പേരു്)
    자바파일수 = 0
    for വർഗ്ഗമൂലം_മൂല്യം in ('ഉറവിടം', 'ഉപയോക്താവ്/자바', '한국어자바'):
        for വഴി in (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/വർഗ്ഗമൂലം_മൂല്യം).rglob('*.java'):
            자바파일수 += 1
            ഉറവിടം = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', വഴി.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ഉറവിടം):
                실패들.append('{}: 한국어화되지 않은 പ്രസ്താവം {}'.format(വഴി.relative_to(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം), 맞음[1]))
            if വർഗ്ഗമൂലം_മൂല്യം == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ഉറവിടം):
                실패들.append('{}: 공개 ഒഴിവാക്കൽ പ്രസ്താവം'.format(വഴി.relative_to(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for വഴി in sorted((കലവറ_വർഗ്ഗമൂലം/'os/ഉറവിടം').glob('*.java')):
        x86자바파일수 += 1
        ഉറവിടം = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', വഴി.read_text())
        for പേരു് in re.findall(r'\b[^\W\d]\w*\b', ഉറവിടം, re.UNICODE):
            if പേരു് not in 예약어 | 표준자바이름 and all(ord(പ്രതീകം_മൂല്യം)<128 for പ്രതീകം_മൂല്യം in പേരു്):
                실패들.append('{}: 자체 영어 ఐడెంటిఫయర్_മൂല്യം {}'.format(വഴി.relative_to(കലവറ_വർഗ്ഗമൂലം), പേരു്))
    ലോഗ്_രേഖ = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/시언어이름분석.py')])
        분석 = json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(പിശക്) for പിശക് in 분석['പിശക്'])
        공개규약 = set(json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'명명/규격이름.json').read_text()))
        for എന്_ട്രി_മൂല്യം in 분석['പ്രസ്താവം'].values():
            പേരു് = എന്_ട്രി_മൂല്യം['പേരു്']; വഴി = Path(എന്_ട്രി_മൂല്യം['ഫയല്'])
            ഉറവിടം = വഴി.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ഉറവിടം[എന്_ട്രി_മൂല്യം['ഓഫ്_സെറ്റ്_മൂല്യം']:എന്_ട്രി_മൂല്യം['ഓഫ്_സെറ്റ്_മൂല്യം']+len(പേരു്)] == പേരു്.encode() and പേരു് not in 공개규약:
                실패들.append('{}:{}: {}'.format(വഴി.relative_to(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം), എന്_ട്രി_മൂല്യം['줄'], പേരു്))
        ലോഗ്_രേഖ['c_semantic_checked'] = True
        ലോഗ്_രേഖ['c_source_sha256'] = {str(Path(ഫയല്).relative_to(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം)):ഹാഷ്_ഫയല് for ഫയല്,ഹാഷ്_ഫയല് in 분석['원문해시'].items()}
    ലോഗ്_രേഖ['passed'] = not 실패들; ലോഗ്_രേഖ['failures'] = 실패들
    ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/naming'; ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.mkdir(parents=True, exist_ok=True)
    (ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം/'report.json').write_text(json.dumps(ലോഗ്_രേഖ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 പ്രസ്താവം·ഫയല് വഴി·호환 എന്_ട്രി_പോയിന്_റ്·통신 예제')

if __name__ == '__main__': നടപ്പിലാക്കുക()
