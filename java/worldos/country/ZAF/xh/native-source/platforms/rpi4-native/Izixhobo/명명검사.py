#!/usr/bin/env python3
"""명명 ikliphu·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Phumeza():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    isiganeko_ixabiso = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for INDLELA in list((기준/'Izixhobo').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if INDLELA.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(INDLELA.read_text()); 나무들[INDLELA] = 나무
        for ufako_nkcukacha_ixabiso in ast.walk(나무):
            if isinstance(ufako_nkcukacha_ixabiso, ast.FunctionDef):
                매개변수표.setdefault(ufako_nkcukacha_ixabiso.name, set()).update(인자.arg for 인자 in ufako_nkcukacha_ixabiso.args.args + ufako_nkcukacha_ixabiso.args.kwonlyargs)
                if ufako_nkcukacha_ixabiso.args.kwarg: 가변매개함수.add(ufako_nkcukacha_ixabiso.name)
            if isinstance(ufako_nkcukacha_ixabiso, ast.ClassDef):
                for INKQUBO_ixabiso in ufako_nkcukacha_ixabiso.body:
                    if isinstance(INKQUBO_ixabiso, ast.FunctionDef) and INKQUBO_ixabiso.name == '__init__':
                        매개변수표.setdefault(ufako_nkcukacha_ixabiso.name, set()).update(인자.arg for 인자 in INKQUBO_ixabiso.args.args + INKQUBO_ixabiso.args.kwonlyargs)
            Igama = ''
            if isinstance(ufako_nkcukacha_ixabiso, (ast.FunctionDef, ast.ClassDef)): Igama = ufako_nkcukacha_ixabiso.name
            elif isinstance(ufako_nkcukacha_ixabiso, ast.Name) and isinstance(ufako_nkcukacha_ixabiso.ctx, ast.Store): Igama = ufako_nkcukacha_ixabiso.id
            elif isinstance(ufako_nkcukacha_ixabiso, ast.arg): Igama = ufako_nkcukacha_ixabiso.arg
            if Igama and Igama not in isiganeko_ixabiso and all(ord(ikharakhtha_ixabiso)<128 for ikharakhtha_ixabiso in Igama):
                실패들.append('{}:{}: {}'.format(INDLELA.relative_to(저장소), ufako_nkcukacha_ixabiso.lineno, Igama))
    for INDLELA, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Igama = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Igama not in 매개변수표 or Igama in 가변매개함수 or not any(ord(ikharakhtha_ixabiso)>127 for ikharakhtha_ixabiso in Igama): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Igama]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(INDLELA.relative_to(저장소), 호출.lineno, Igama, 인자.arg))
    for umgca in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Inkqubo_ixabiso_ufako_nkcukacha = umgca.split('\t')
        if not (기준/현재).is_file(): 실패들.append('fudusa_ixabiso iFayili 없음: '+현재)
        if Inkqubo_ixabiso_ufako_nkcukacha == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ufako_nkcukacha_inqaku 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for INDLELA in sorted((기준.parents[1]/'example/java').glob('*.java')):
        UMTHOMBO = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', INDLELA.read_text())
        for Igama in re.findall(r'\b[^\W\d]\w*\b', UMTHOMBO, re.UNICODE):
            if Igama not in 예약어 and all(ord(ikharakhtha_ixabiso)<128 for ikharakhtha_ixabiso in Igama):
                실패들.append('{}: 예제의 영어 isalathisi_ixabiso {}'.format(INDLELA.name, Igama))
    for Igama in ('창', 'iqhosha', 'Ilebhile', 'I_SMS_ifildi', '화면구성요소', 'umcimbi_ityhu', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        UMTHOMBO = (기준/'한국어자바/isiXhosa/자체'/(Igama+'.java')).read_text()
        UMTHOMBO = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', UMTHOMBO)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', UMTHOMBO):
            실패들.append(Igama+': isiXhosa 직접 구현에 표준 into_ixabiso 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Igama in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Igama in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Igama: '+Igama)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Igama in ('ilifu_Usapho', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Igama+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 imakhro_ixabiso 사용: '+Igama)
    자바파일수 = 0
    for 뿌리 in ('UMTHOMBO', 'umsebenzisi/자바', '한국어자바'):
        for INDLELA in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            UMTHOMBO = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', INDLELA.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', UMTHOMBO):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(INDLELA.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', UMTHOMBO):
                실패들.append('{}: 공개 예외 선언'.format(INDLELA.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for INDLELA in sorted((저장소/'os/UMTHOMBO').glob('*.java')):
        x86자바파일수 += 1
        UMTHOMBO = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', INDLELA.read_text())
        for Igama in re.findall(r'\b[^\W\d]\w*\b', UMTHOMBO, re.UNICODE):
            if Igama not in 예약어 | 표준자바이름 and all(ord(ikharakhtha_ixabiso)<128 for ikharakhtha_ixabiso in Igama):
                실패들.append('{}: 자체 영어 isalathisi_ixabiso {}'.format(INDLELA.relative_to(저장소), Igama))
    ilog_umqolo = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Izixhobo/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Impazamo) for Impazamo in 분석['Impazamo'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ufako_nkcukacha_ixabiso in 분석['선언'].values():
            Igama = ufako_nkcukacha_ixabiso['Igama']; INDLELA = Path(ufako_nkcukacha_ixabiso['iFayili'])
            UMTHOMBO = INDLELA.read_bytes()
            # isiXhosa 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if UMTHOMBO[ufako_nkcukacha_ixabiso['Ukulinganisa_ixabiso']:ufako_nkcukacha_ixabiso['Ukulinganisa_ixabiso']+len(Igama)] == Igama.encode() and Igama not in 공개규약:
                실패들.append('{}:{}: {}'.format(INDLELA.relative_to(기준), ufako_nkcukacha_ixabiso['줄'], Igama))
        ilog_umqolo['c_semantic_checked'] = True
        ilog_umqolo['c_source_sha256'] = {str(Path(iFayili).relative_to(기준)):i_hash_ifayile for iFayili,i_hash_ifayile in 분석['원문해시'].items()}
    ilog_umqolo['passed'] = not 실패들; ilog_umqolo['failures'] = 실패들
    indawo_ekuyiwa_kuyo_ixabiso = 기준/'build/verification/naming'; indawo_ekuyiwa_kuyo_ixabiso.mkdir(parents=True, exist_ok=True)
    (indawo_ekuyiwa_kuyo_ixabiso/'report.json').write_text(json.dumps(ilog_umqolo, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: isiXhosa 선언·iFayili INDLELA·호환 ufako_nkcukacha_inqaku·통신 예제')

if __name__ == '__main__': Phumeza()
