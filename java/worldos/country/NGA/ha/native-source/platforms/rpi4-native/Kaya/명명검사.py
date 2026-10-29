#!/usr/bin/env python3
"""명명 darfi·banbanchi·경로를 검사한다. --시언어는 libclang bayyanarwa 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Tafiyar_da():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    실패들 = []
    Kes_Daraja = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    maaunin_tebur = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Hanyar_shiga in list((기준/'Kaya').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if Hanyar_shiga.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Hanyar_shiga.read_text()); 나무들[Hanyar_shiga] = 나무
        for Mashigar_bayanai_Daraja in ast.walk(나무):
            if isinstance(Mashigar_bayanai_Daraja, ast.FunctionDef):
                maaunin_tebur.setdefault(Mashigar_bayanai_Daraja.name, set()).update(maaunin_Tubalin_aiki.arg for maaunin_Tubalin_aiki in Mashigar_bayanai_Daraja.args.args + Mashigar_bayanai_Daraja.args.kwonlyargs)
                if Mashigar_bayanai_Daraja.args.kwarg: 가변매개함수.add(Mashigar_bayanai_Daraja.name)
            if isinstance(Mashigar_bayanai_Daraja, ast.ClassDef):
                for AIKI_Daraja in Mashigar_bayanai_Daraja.body:
                    if isinstance(AIKI_Daraja, ast.FunctionDef) and AIKI_Daraja.name == '__init__':
                        maaunin_tebur.setdefault(Mashigar_bayanai_Daraja.name, set()).update(maaunin_Tubalin_aiki.arg for maaunin_Tubalin_aiki in AIKI_Daraja.args.args + AIKI_Daraja.args.kwonlyargs)
            Suna = ''
            if isinstance(Mashigar_bayanai_Daraja, (ast.FunctionDef, ast.ClassDef)): Suna = Mashigar_bayanai_Daraja.name
            elif isinstance(Mashigar_bayanai_Daraja, ast.Name) and isinstance(Mashigar_bayanai_Daraja.ctx, ast.Store): Suna = Mashigar_bayanai_Daraja.id
            elif isinstance(Mashigar_bayanai_Daraja, ast.arg): Suna = Mashigar_bayanai_Daraja.arg
            if Suna and Suna not in Kes_Daraja and all(ord(Harafi_Daraja)<128 for Harafi_Daraja in Suna):
                실패들.append('{}:{}: {}'.format(Hanyar_shiga.relative_to(저장소), Mashigar_bayanai_Daraja.lineno, Suna))
    for Hanyar_shiga, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Suna = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Suna not in maaunin_tebur or Suna in 가변매개함수 or not any(ord(Harafi_Daraja)>127 for Harafi_Daraja in Suna): continue
            for maaunin_Tubalin_aiki in 호출.keywords:
                if maaunin_Tubalin_aiki.arg and maaunin_Tubalin_aiki.arg not in maaunin_tebur[Suna]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Hanyar_shiga.relative_to(저장소), 호출.lineno, Suna, maaunin_Tubalin_aiki.arg))
    for Layi in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, haryar_aikin_na_ura_Daraja_Mashigar_bayanai = Layi.split('\t')
        if not (기준/현재).is_file(): 실패들.append('Matsar_da_Daraja Fayil 없음: '+현재)
        if haryar_aikin_na_ura_Daraja_Mashigar_bayanai == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 Mashigar_bayanai_maki 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Hanyar_shiga in sorted((기준.parents[1]/'example/java').glob('*.java')):
        tushe = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Hanyar_shiga.read_text())
        for Suna in re.findall(r'\b[^\W\d]\w*\b', tushe, re.UNICODE):
            if Suna not in 예약어 and all(ord(Harafi_Daraja)<128 for Harafi_Daraja in Suna):
                실패들.append('{}: 예제의 영어 mai_ganewa_Daraja {}'.format(Hanyar_shiga.name, Suna))
    for Suna in ('창', 'maɓali', 'alama', 'SMS_Fili', '화면구성요소', 'Faruwa_Jerin_ayyukan_da_za_a_yi', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        tushe = (기준/'한국어자바/한국어/자체'/(Suna+'.java')).read_text()
        tushe = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', tushe)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', tushe):
            실패들.append(Suna+': 한국어 직접 구현에 표준 abu_Daraja 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Suna in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Suna in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Suna: '+Suna)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 banbanchi 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Suna in ('Intanet_Iyali', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Suna+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 Makullin_gargadi_Daraja 사용: '+Suna)
    자바파일수 = 0
    for 뿌리 in ('tushe', 'Mai_anfani_da_kwamfuta/자바', '한국어자바'):
        for Hanyar_shiga in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            tushe = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Hanyar_shiga.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', tushe):
                실패들.append('{}: 한국어화되지 않은 bayyanarwa {}'.format(Hanyar_shiga.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', tushe):
                실패들.append('{}: 공개 banbanchi bayyanarwa'.format(Hanyar_shiga.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Hanyar_shiga in sorted((저장소/'os/tushe').glob('*.java')):
        x86자바파일수 += 1
        tushe = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Hanyar_shiga.read_text())
        for Suna in re.findall(r'\b[^\W\d]\w*\b', tushe, re.UNICODE):
            if Suna not in 예약어 | 표준자바이름 and all(ord(Harafi_Daraja)<128 for Harafi_Daraja in Suna):
                실패들.append('{}: 자체 영어 mai_ganewa_Daraja {}'.format(Hanyar_shiga.relative_to(저장소), Suna))
    logu_naɗa = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Kaya/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Kuskure) for Kuskure in 분석['Kuskure'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for Mashigar_bayanai_Daraja in 분석['bayyanarwa'].values():
            Suna = Mashigar_bayanai_Daraja['Suna']; Hanyar_shiga = Path(Mashigar_bayanai_Daraja['Fayil'])
            tushe = Hanyar_shiga.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if tushe[Mashigar_bayanai_Daraja['Sassautawa_Daraja']:Mashigar_bayanai_Daraja['Sassautawa_Daraja']+len(Suna)] == Suna.encode() and Suna not in 공개규약:
                실패들.append('{}:{}: {}'.format(Hanyar_shiga.relative_to(기준), Mashigar_bayanai_Daraja['줄'], Suna))
        logu_naɗa['c_semantic_checked'] = True
        logu_naɗa['c_source_sha256'] = {str(Path(Fayil).relative_to(기준)):hash_Fayil for Fayil,hash_Fayil in 분석['원문해시'].items()}
    logu_naɗa['passed'] = not 실패들; logu_naɗa['failures'] = 실패들
    Zangon_ƙarshe_Daraja = 기준/'build/verification/naming'; Zangon_ƙarshe_Daraja.mkdir(parents=True, exist_ok=True)
    (Zangon_ƙarshe_Daraja/'report.json').write_text(json.dumps(logu_naɗa, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 bayyanarwa·Fayil Hanyar_shiga·호환 Mashigar_bayanai_maki·통신 예제')

if __name__ == '__main__': Tafiyar_da()
