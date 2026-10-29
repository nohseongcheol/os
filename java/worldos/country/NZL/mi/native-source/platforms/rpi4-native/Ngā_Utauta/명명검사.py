#!/usr/bin/env python3
"""명명 topenga·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

whakaatu_pūtake = Path(__file__).resolve().parents[1]
저장소 = whakaatu_pūtake.parents[1]

def whakahaere():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    kēhi_uara = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    kōnae_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ara in list((whakaatu_pūtake/'Ngā_Utauta').glob('*.py')) + list((whakaatu_pūtake/'예제').rglob('*.py')) + 공용번역기들:
        if ara.name.endswith(('이름반영.py', '이름분석.py')): continue
        kōnae_COUNT += 1
        나무 = ast.parse(ara.read_text()); 나무들[ara] = 나무
        for tāurunga_uara in ast.walk(나무):
            if isinstance(tāurunga_uara, ast.FunctionDef):
                매개변수표.setdefault(tāurunga_uara.name, set()).update(인자.arg for 인자 in tāurunga_uara.args.args + tāurunga_uara.args.kwonlyargs)
                if tāurunga_uara.args.kwarg: 가변매개함수.add(tāurunga_uara.name)
            if isinstance(tāurunga_uara, ast.ClassDef):
                for TAUMAHI_uara in tāurunga_uara.body:
                    if isinstance(TAUMAHI_uara, ast.FunctionDef) and TAUMAHI_uara.name == '__init__':
                        매개변수표.setdefault(tāurunga_uara.name, set()).update(인자.arg for 인자 in TAUMAHI_uara.args.args + TAUMAHI_uara.args.kwonlyargs)
            Ingoa = ''
            if isinstance(tāurunga_uara, (ast.FunctionDef, ast.ClassDef)): Ingoa = tāurunga_uara.name
            elif isinstance(tāurunga_uara, ast.Name) and isinstance(tāurunga_uara.ctx, ast.Store): Ingoa = tāurunga_uara.id
            elif isinstance(tāurunga_uara, ast.arg): Ingoa = tāurunga_uara.arg
            if Ingoa and Ingoa not in kēhi_uara and all(ord(pūāhua_uara)<128 for pūāhua_uara in Ingoa):
                실패들.append('{}:{}: {}'.format(ara.relative_to(저장소), tāurunga_uara.lineno, Ingoa))
    for ara, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ingoa = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ingoa not in 매개변수표 or Ingoa in 가변매개함수 or not any(ord(pūāhua_uara)>127 for pūāhua_uara in Ingoa): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Ingoa]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ara.relative_to(저장소), 호출.lineno, Ingoa, 인자.arg))
    for hononga in (whakaatu_pūtake/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Hātepe_uara_tāurunga = hononga.split('\t')
        if not (whakaatu_pūtake/현재).is_file(): 실패들.append('nuku_uara Kōnae 없음: '+현재)
        if Hātepe_uara_tāurunga == '호환진입점유지' and not (whakaatu_pūtake/이전).is_file(): 실패들.append('호환 tāurunga_ira 없음: '+이전)
    예제 = (whakaatu_pūtake.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ara in sorted((whakaatu_pūtake.parents[1]/'example/java').glob('*.java')):
        pūtake = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ara.read_text())
        for Ingoa in re.findall(r'\b[^\W\d]\w*\b', pūtake, re.UNICODE):
            if Ingoa not in 예약어 and all(ord(pūāhua_uara)<128 for pūāhua_uara in Ingoa):
                실패들.append('{}: 예제의 영어 pūtāutu_uara {}'.format(ara.name, Ingoa))
    for Ingoa in ('창', 'pātene', 'tapanga', 'āpure_kuputuhi', '화면구성요소', 'hui_tūtira', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        pūtake = (whakaatu_pūtake/'한국어자바/Reo_Māori/자체'/(Ingoa+'.java')).read_text()
        pūtake = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', pūtake)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', pūtake):
            실패들.append(Ingoa+': Reo_Māori 직접 구현에 표준 ahanoa_uara 래퍼가 남았습니다.')
    시언어예제 = (whakaatu_pūtake.parents[1]/'example/c/네트워크예제.c').read_text()
    for Ingoa in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ingoa in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ingoa: '+Ingoa)
    파이썬예제 = (whakaatu_pūtake.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (whakaatu_pūtake.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ingoa in ('kapua_Whānau', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Ingoa+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 tonotono_uara 사용: '+Ingoa)
    자바파일수 = 0
    for pūtake_uara in ('pūtake', 'kaiwhakamahi/자바', '한국어자바'):
        for ara in (whakaatu_pūtake/pūtake_uara).rglob('*.java'):
            자바파일수 += 1
            pūtake = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ara.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', pūtake):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(ara.relative_to(whakaatu_pūtake), 맞음[1]))
            if pūtake_uara == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', pūtake):
                실패들.append('{}: 공개 예외 선언'.format(ara.relative_to(whakaatu_pūtake)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ara in sorted((저장소/'os/pūtake').glob('*.java')):
        x86자바파일수 += 1
        pūtake = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ara.read_text())
        for Ingoa in re.findall(r'\b[^\W\d]\w*\b', pūtake, re.UNICODE):
            if Ingoa not in 예약어 | 표준자바이름 and all(ord(pūāhua_uara)<128 for pūāhua_uara in Ingoa):
                실패들.append('{}: 자체 영어 pūtāutu_uara {}'.format(ara.relative_to(저장소), Ingoa))
    LOG_RECORD = {'passed': False, 'python_files': kōnae_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(whakaatu_pūtake/'Ngā_Utauta/시언어이름분석.py')])
        분석 = json.loads((whakaatu_pūtake/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Pōhēhē) for Pōhēhē in 분석['Pōhēhē'])
        공개규약 = set(json.loads((whakaatu_pūtake/'명명/규격이름.json').read_text()))
        for tāurunga_uara in 분석['선언'].values():
            Ingoa = tāurunga_uara['Ingoa']; ara = Path(tāurunga_uara['Kōnae'])
            pūtake = ara.read_bytes()
            # Reo_Māori 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if pūtake[tāurunga_uara['OFFSET_uara']:tāurunga_uara['OFFSET_uara']+len(Ingoa)] == Ingoa.encode() and Ingoa not in 공개규약:
                실패들.append('{}:{}: {}'.format(ara.relative_to(whakaatu_pūtake), tāurunga_uara['줄'], Ingoa))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(Kōnae).relative_to(whakaatu_pūtake)):hash_kōnae for Kōnae,hash_kōnae in 분석['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    ūnga_uara = whakaatu_pūtake/'build/verification/naming'; ūnga_uara.mkdir(parents=True, exist_ok=True)
    (ūnga_uara/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Reo_Māori 선언·Kōnae ara·호환 tāurunga_ira·통신 예제')

if __name__ == '__main__': whakahaere()
