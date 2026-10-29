#!/usr/bin/env python3
"""명명 gearrthóg·eisceacht·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

teilgean_fréamh = Path(__file__).resolve().parents[1]
저장소 = teilgean_fréamh.parents[1]

def Rith_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    Argóintí = 해석기.parse_args()
    실패들 = []
    cás_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    comhad_COUNT = 0
    paraiméadar_tábla = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for CONAIR in list((teilgean_fréamh/'Uirlisí').glob('*.py')) + list((teilgean_fréamh/'예제').rglob('*.py')) + 공용번역기들:
        if CONAIR.name.endswith(('이름반영.py', '이름분석.py')): continue
        comhad_COUNT += 1
        나무 = ast.parse(CONAIR.read_text()); 나무들[CONAIR] = 나무
        for iontráil_VALUE in ast.walk(나무):
            if isinstance(iontráil_VALUE, ast.FunctionDef):
                paraiméadar_tábla.setdefault(iontráil_VALUE.name, set()).update(paraiméadar_argóint.arg for paraiméadar_argóint in iontráil_VALUE.args.args + iontráil_VALUE.args.kwonlyargs)
                if iontráil_VALUE.args.kwarg: 가변매개함수.add(iontráil_VALUE.name)
            if isinstance(iontráil_VALUE, ast.ClassDef):
                for feidhm_VALUE in iontráil_VALUE.body:
                    if isinstance(feidhm_VALUE, ast.FunctionDef) and feidhm_VALUE.name == '__init__':
                        paraiméadar_tábla.setdefault(iontráil_VALUE.name, set()).update(paraiméadar_argóint.arg for paraiméadar_argóint in feidhm_VALUE.args.args + feidhm_VALUE.args.kwonlyargs)
            Ainm = ''
            if isinstance(iontráil_VALUE, (ast.FunctionDef, ast.ClassDef)): Ainm = iontráil_VALUE.name
            elif isinstance(iontráil_VALUE, ast.Name) and isinstance(iontráil_VALUE.ctx, ast.Store): Ainm = iontráil_VALUE.id
            elif isinstance(iontráil_VALUE, ast.arg): Ainm = iontráil_VALUE.arg
            if Ainm and Ainm not in cás_VALUE and all(ord(carachtar_VALUE)<128 for carachtar_VALUE in Ainm):
                실패들.append('{}:{}: {}'.format(CONAIR.relative_to(저장소), iontráil_VALUE.lineno, Ainm))
    for CONAIR, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ainm = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ainm not in paraiméadar_tábla or Ainm in 가변매개함수 or not any(ord(carachtar_VALUE)>127 for carachtar_VALUE in Ainm): continue
            for paraiméadar_argóint in 호출.keywords:
                if paraiméadar_argóint.arg and paraiméadar_argóint.arg not in paraiméadar_tábla[Ainm]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(CONAIR.relative_to(저장소), 호출.lineno, Ainm, paraiméadar_argóint.arg))
    for Líne in (teilgean_fréamh/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Próiseas_VALUE_iontráil = Líne.split('\t')
        if not (teilgean_fréamh/현재).is_file(): 실패들.append('bog_VALUE Comhad 없음: '+현재)
        if Próiseas_VALUE_iontráil == '호환진입점유지' and not (teilgean_fréamh/이전).is_file(): 실패들.append('호환 iontráil_pointe 없음: '+이전)
    예제 = (teilgean_fréamh.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for CONAIR in sorted((teilgean_fréamh.parents[1]/'example/java').glob('*.java')):
        FOINSE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CONAIR.read_text())
        for Ainm in re.findall(r'\b[^\W\d]\w*\b', FOINSE, re.UNICODE):
            if Ainm not in 예약어 and all(ord(carachtar_VALUE)<128 for carachtar_VALUE in Ainm):
                실패들.append('{}: 예제의 영어 aitheantóir_VALUE {}'.format(CONAIR.name, Ainm))
    for Ainm in ('창', 'cnaipe', 'Lipéad', 'réimse_téacs', '화면구성요소', 'ócáid_scuaine', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        FOINSE = (teilgean_fréamh/'한국어자바/Gaeilge/자체'/(Ainm+'.java')).read_text()
        FOINSE = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', FOINSE)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', FOINSE):
            실패들.append(Ainm+': Gaeilge 직접 구현에 표준 oibiacht_VALUE 래퍼가 남았습니다.')
    시언어예제 = (teilgean_fréamh.parents[1]/'example/c/네트워크예제.c').read_text()
    for Ainm in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ainm in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ainm: '+Ainm)
    파이썬예제 = (teilgean_fréamh.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 eisceacht 직접 사용')
    머리 = (teilgean_fréamh.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ainm in ('néal_Teaghlach', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Ainm+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 macra_VALUE 사용: '+Ainm)
    자바파일수 = 0
    for fréamh_VALUE in ('FOINSE', 'úsáideoir/자바', '한국어자바'):
        for CONAIR in (teilgean_fréamh/fréamh_VALUE).rglob('*.java'):
            자바파일수 += 1
            FOINSE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CONAIR.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', FOINSE):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(CONAIR.relative_to(teilgean_fréamh), 맞음[1]))
            if fréamh_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', FOINSE):
                실패들.append('{}: 공개 eisceacht 선언'.format(CONAIR.relative_to(teilgean_fréamh)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for CONAIR in sorted((저장소/'os/FOINSE').glob('*.java')):
        x86자바파일수 += 1
        FOINSE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CONAIR.read_text())
        for Ainm in re.findall(r'\b[^\W\d]\w*\b', FOINSE, re.UNICODE):
            if Ainm not in 예약어 | 표준자바이름 and all(ord(carachtar_VALUE)<128 for carachtar_VALUE in Ainm):
                실패들.append('{}: 자체 영어 aitheantóir_VALUE {}'.format(CONAIR.relative_to(저장소), Ainm))
    LOG_ró = {'passed': False, 'python_files': comhad_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argóintí.시언어:
        subprocess.check_call(['python3', str(teilgean_fréamh/'Uirlisí/시언어이름분석.py')])
        분석 = json.loads((teilgean_fréamh/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ERREÁID) for ERREÁID in 분석['ERREÁID'])
        공개규약 = set(json.loads((teilgean_fréamh/'명명/규격이름.json').read_text()))
        for iontráil_VALUE in 분석['선언'].values():
            Ainm = iontráil_VALUE['Ainm']; CONAIR = Path(iontráil_VALUE['Comhad'])
            FOINSE = CONAIR.read_bytes()
            # Gaeilge 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if FOINSE[iontráil_VALUE['OFFSET_VALUE']:iontráil_VALUE['OFFSET_VALUE']+len(Ainm)] == Ainm.encode() and Ainm not in 공개규약:
                실패들.append('{}:{}: {}'.format(CONAIR.relative_to(teilgean_fréamh), iontráil_VALUE['Líne'], Ainm))
        LOG_ró['c_semantic_checked'] = True
        LOG_ró['c_source_sha256'] = {str(Path(Comhad).relative_to(teilgean_fréamh)):hais_comhad for Comhad,hais_comhad in 분석['원문해시'].items()}
    LOG_ró['passed'] = not 실패들; LOG_ró['failures'] = 실패들
    sprioc_VALUE = teilgean_fréamh/'build/verification/naming'; sprioc_VALUE.mkdir(parents=True, exist_ok=True)
    (sprioc_VALUE/'report.json').write_text(json.dumps(LOG_ró, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Gaeilge 선언·Comhad CONAIR·호환 iontráil_pointe·통신 예제')

if __name__ == '__main__': Rith_2()
