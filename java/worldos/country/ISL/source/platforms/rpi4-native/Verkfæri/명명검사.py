#!/usr/bin/env python3
"""명명 miðlaskrá·undantekning·경로를 검사한다. --시언어는 libclang skýrsla 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

verk_rót = Path(__file__).resolve().parents[1]
gagnageymsla_rót = verk_rót.parents[1]

def Keyra_2():
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('--시언어', action='store_true')
    Viðföng = þáttari_48ee4b1b.parse_args()
    실패들 = []
    samningsvirði = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    skrá_COUNT = 0
    færibreyta_tafla = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [gagnageymsla_rót/'compiler/컴파일러.py', gagnageymsla_rót/'compiler/기계어미리번역.py']
    for SLÓÐ in list((verk_rót/'Verkfæri').glob('*.py')) + list((verk_rót/'예제').rglob('*.py')) + 공용번역기들:
        if SLÓÐ.name.endswith(('이름반영.py', '이름분석.py')): continue
        skrá_COUNT += 1
        나무 = ast.parse(SLÓÐ.read_text()); 나무들[SLÓÐ] = 나무
        for færsla_VALUE in ast.walk(나무):
            if isinstance(færsla_VALUE, ast.FunctionDef):
                færibreyta_tafla.setdefault(færsla_VALUE.name, set()).update(færibreyta_frumbreyta.arg for færibreyta_frumbreyta in færsla_VALUE.args.args + færsla_VALUE.args.kwonlyargs)
                if færsla_VALUE.args.kwarg: 가변매개함수.add(færsla_VALUE.name)
            if isinstance(færsla_VALUE, ast.ClassDef):
                for fall_VALUE in færsla_VALUE.body:
                    if isinstance(fall_VALUE, ast.FunctionDef) and fall_VALUE.name == '__init__':
                        færibreyta_tafla.setdefault(færsla_VALUE.name, set()).update(færibreyta_frumbreyta.arg for færibreyta_frumbreyta in fall_VALUE.args.args + fall_VALUE.args.kwonlyargs)
            Heiti = ''
            if isinstance(færsla_VALUE, (ast.FunctionDef, ast.ClassDef)): Heiti = færsla_VALUE.name
            elif isinstance(færsla_VALUE, ast.Name) and isinstance(færsla_VALUE.ctx, ast.Store): Heiti = færsla_VALUE.id
            elif isinstance(færsla_VALUE, ast.arg): Heiti = færsla_VALUE.arg
            if Heiti and Heiti not in samningsvirði and all(ord(stafur_VALUE)<128 for stafur_VALUE in Heiti):
                실패들.append('{}:{}: {}'.format(SLÓÐ.relative_to(gagnageymsla_rót), færsla_VALUE.lineno, Heiti))
    for SLÓÐ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Heiti = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Heiti not in færibreyta_tafla or Heiti in 가변매개함수 or not any(ord(stafur_VALUE)>127 for stafur_VALUE in Heiti): continue
            for færibreyta_frumbreyta in 호출.keywords:
                if færibreyta_frumbreyta.arg and færibreyta_frumbreyta.arg not in færibreyta_tafla[Heiti]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(SLÓÐ.relative_to(gagnageymsla_rót), 호출.lineno, Heiti, færibreyta_frumbreyta.arg))
    for Lína in (verk_rót/'명명/skrá_heiti_vörpun.tsv').read_text().splitlines()[1:]:
        이전, 현재, Ferli_VALUE_færsla = Lína.split('\t')
        if not (verk_rót/현재).is_file(): 실패들.append('færa_VALUE Skrá 없음: '+현재)
        if Ferli_VALUE_færsla == '호환진입점유지' and not (verk_rót/이전).is_file(): 실패들.append('호환 færsla_P 없음: '+이전)
    예제 = (verk_rót.parents[1]/'example/java/Netdæmi.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for SLÓÐ in sorted((verk_rót.parents[1]/'example/java').glob('*.java')):
        Uppruni = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', SLÓÐ.read_text())
        for Heiti in re.findall(r'\b[^\W\d]\w*\b', Uppruni, re.UNICODE):
            if Heiti not in 예약어 and all(ord(stafur_VALUE)<128 for stafur_VALUE in Heiti):
                실패들.append('{}: 예제의 영어 auðkenni_VALUE {}'.format(SLÓÐ.name, Heiti))
    for Heiti in ('Gluggi', 'hnappur', 'Skýring', 'SMS_reitur', '화면구성요소', 'atvik_biðröð', 'starfskraftur', '실행할일', '동작받이', '동작알림', '작업'):
        Uppruni = (verk_rót/'한국어자바/Íslenska/eigin'/(Heiti+'.java')).read_text()
        Uppruni = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Uppruni)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Uppruni):
            실패들.append(Heiti+': Íslenska 직접 구현에 표준 hlutur_VALUE 래퍼가 남았습니다.')
    시언어예제 = (verk_rót.parents[1]/'example/c/Netdæmi.c').read_text()
    for Heiti in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Heiti in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Heiti: '+Heiti)
    파이썬예제 = (verk_rót.parents[1]/'example/python/Netdæmi.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 undantekning 직접 사용')
    머리 = (verk_rót.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Heiti in ('skýið_Fjölskylda', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'stofna_endastöð', '자료전문보내기'):
        if re.search(r'^#define\s+'+Heiti+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 fjölvi_VALUE 사용: '+Heiti)
    자바파일수 = 0
    for rót_VALUE in ('Uppruni', 'notandi/자바', '한국어자바'):
        for SLÓÐ in (verk_rót/rót_VALUE).rglob('*.java'):
            자바파일수 += 1
            Uppruni = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', SLÓÐ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Uppruni):
                실패들.append('{}: 한국어화되지 않은 skýrsla {}'.format(SLÓÐ.relative_to(verk_rót), 맞음[1]))
            if rót_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Uppruni):
                실패들.append('{}: 공개 undantekning skýrsla'.format(SLÓÐ.relative_to(verk_rót)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for SLÓÐ in sorted((gagnageymsla_rót/'os/Uppruni').glob('*.java')):
        x86자바파일수 += 1
        Uppruni = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', SLÓÐ.read_text())
        for Heiti in re.findall(r'\b[^\W\d]\w*\b', Uppruni, re.UNICODE):
            if Heiti not in 예약어 | 표준자바이름 and all(ord(stafur_VALUE)<128 for stafur_VALUE in Heiti):
                실패들.append('{}: eigin 영어 auðkenni_VALUE {}'.format(SLÓÐ.relative_to(gagnageymsla_rót), Heiti))
    LOG_lína = {'passed': False, 'python_files': skrá_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Viðföng.시언어:
        subprocess.check_call(['python3', str(verk_rót/'Verkfæri/시언어이름분석.py')])
        분석 = json.loads((verk_rót/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Villa) for Villa in 분석['Villa'])
        공개규약 = set(json.loads((verk_rót/'명명/규격이름.json').read_text()))
        for færsla_VALUE in 분석['skýrsla'].values():
            Heiti = færsla_VALUE['Heiti']; SLÓÐ = Path(færsla_VALUE['Skrá'])
            Uppruni = SLÓÐ.read_bytes()
            # Íslenska 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Uppruni[færsla_VALUE['OFFSET_VALUE']:færsla_VALUE['OFFSET_VALUE']+len(Heiti)] == Heiti.encode() and Heiti not in 공개규약:
                실패들.append('{}:{}: {}'.format(SLÓÐ.relative_to(verk_rót), færsla_VALUE['Lína'], Heiti))
        LOG_lína['c_semantic_checked'] = True
        LOG_lína['c_source_sha256'] = {str(Path(Skrá).relative_to(verk_rót)):tæting_skrá for Skrá,tæting_skrá in 분석['원문해시'].items()}
    LOG_lína['passed'] = not 실패들; LOG_lína['failures'] = 실패들
    endastaður_VALUE = verk_rót/'build/verification/naming'; endastaður_VALUE.mkdir(parents=True, exist_ok=True)
    (endastaður_VALUE/'report.json').write_text(json.dumps(LOG_lína, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Íslenska skýrsla·Skrá SLÓÐ·호환 færsla_P·통신 예제')

if __name__ == '__main__': Keyra_2()
