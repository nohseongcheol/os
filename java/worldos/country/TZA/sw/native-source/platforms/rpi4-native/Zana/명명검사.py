#!/usr/bin/env python3
"""명명 dondoo·vighairi·경로를 검사한다. --시언어는 libclang tamko 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def endesha():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    실패들 = []
    Kazi_thamani = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    parameta_jedwali = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for njia in list((기준/'Zana').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if njia.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(njia.read_text()); 나무들[njia] = 나무
        for ingizo_thamani in ast.walk(나무):
            if isinstance(ingizo_thamani, ast.FunctionDef):
                parameta_jedwali.setdefault(ingizo_thamani.name, set()).update(parameta_hoja.arg for parameta_hoja in ingizo_thamani.args.args + ingizo_thamani.args.kwonlyargs)
                if ingizo_thamani.args.kwarg: 가변매개함수.add(ingizo_thamani.name)
            if isinstance(ingizo_thamani, ast.ClassDef):
                for KITENDAKAZI_thamani in ingizo_thamani.body:
                    if isinstance(KITENDAKAZI_thamani, ast.FunctionDef) and KITENDAKAZI_thamani.name == '__init__':
                        parameta_jedwali.setdefault(ingizo_thamani.name, set()).update(parameta_hoja.arg for parameta_hoja in KITENDAKAZI_thamani.args.args + KITENDAKAZI_thamani.args.kwonlyargs)
            Jina = ''
            if isinstance(ingizo_thamani, (ast.FunctionDef, ast.ClassDef)): Jina = ingizo_thamani.name
            elif isinstance(ingizo_thamani, ast.Name) and isinstance(ingizo_thamani.ctx, ast.Store): Jina = ingizo_thamani.id
            elif isinstance(ingizo_thamani, ast.arg): Jina = ingizo_thamani.arg
            if Jina and Jina not in Kazi_thamani and all(ord(kibambo_thamani)<128 for kibambo_thamani in Jina):
                실패들.append('{}:{}: {}'.format(njia.relative_to(저장소), ingizo_thamani.lineno, Jina))
    for njia, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Jina = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Jina not in parameta_jedwali or Jina in 가변매개함수 or not any(ord(kibambo_thamani)>127 for kibambo_thamani in Jina): continue
            for parameta_hoja in 호출.keywords:
                if parameta_hoja.arg and parameta_hoja.arg not in parameta_jedwali[Jina]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(njia.relative_to(저장소), 호출.lineno, Jina, parameta_hoja.arg))
    for laini in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Mchakato_thamani_ingizo = laini.split('\t')
        if not (기준/현재).is_file(): 실패들.append('hamisha_thamani faili 없음: '+현재)
        if Mchakato_thamani_ingizo == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 ingizo_pointi 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for njia in sorted((기준.parents[1]/'example/java').glob('*.java')):
        chanzo = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', njia.read_text())
        for Jina in re.findall(r'\b[^\W\d]\w*\b', chanzo, re.UNICODE):
            if Jina not in 예약어 and all(ord(kibambo_thamani)<128 for kibambo_thamani in Jina):
                실패들.append('{}: 예제의 영어 kitambulishi_thamani {}'.format(njia.name, Jina))
    for Jina in ('창', 'kitufe', 'lebo', 'SMS_uga', '화면구성요소', 'tukio_foleni', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        chanzo = (기준/'한국어자바/한국어/자체'/(Jina+'.java')).read_text()
        chanzo = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', chanzo)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', chanzo):
            실패들.append(Jina+': 한국어 직접 구현에 표준 kipengee_thamani 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Jina in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Jina in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Jina: '+Jina)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 vighairi 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Jina in ('wingu_Familia', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Jina+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_thamani 사용: '+Jina)
    자바파일수 = 0
    for 뿌리 in ('chanzo', 'mtumiaji/자바', '한국어자바'):
        for njia in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            chanzo = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', njia.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', chanzo):
                실패들.append('{}: 한국어화되지 않은 tamko {}'.format(njia.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', chanzo):
                실패들.append('{}: 공개 vighairi tamko'.format(njia.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for njia in sorted((저장소/'os/chanzo').glob('*.java')):
        x86자바파일수 += 1
        chanzo = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', njia.read_text())
        for Jina in re.findall(r'\b[^\W\d]\w*\b', chanzo, re.UNICODE):
            if Jina not in 예약어 | 표준자바이름 and all(ord(kibambo_thamani)<128 for kibambo_thamani in Jina):
                실패들.append('{}: 자체 영어 kitambulishi_thamani {}'.format(njia.relative_to(저장소), Jina))
    batli_REKODI = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Zana/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(kosa) for kosa in 분석['kosa'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for ingizo_thamani in 분석['tamko'].values():
            Jina = ingizo_thamani['Jina']; njia = Path(ingizo_thamani['faili'])
            chanzo = njia.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if chanzo[ingizo_thamani['Chipua_thamani']:ingizo_thamani['Chipua_thamani']+len(Jina)] == Jina.encode() and Jina not in 공개규약:
                실패들.append('{}:{}: {}'.format(njia.relative_to(기준), ingizo_thamani['줄'], Jina))
        batli_REKODI['c_semantic_checked'] = True
        batli_REKODI['c_source_sha256'] = {str(Path(faili).relative_to(기준)):kali_faili for faili,kali_faili in 분석['원문해시'].items()}
    batli_REKODI['passed'] = not 실패들; batli_REKODI['failures'] = 실패들
    fikio_thamani = 기준/'build/verification/naming'; fikio_thamani.mkdir(parents=True, exist_ok=True)
    (fikio_thamani/'report.json').write_text(json.dumps(batli_REKODI, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 tamko·faili njia·호환 ingizo_pointi·통신 예제')

if __name__ == '__main__': endesha()
