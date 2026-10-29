#!/usr/bin/env python3
"""명명 clip·excepció·경로를 검사한다. --시언어는 libclang declaració 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_rel = Path(__file__).resolve().parents[1]
dipòsit_rel = Project_rel.parents[1]

def Executa_2():
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = analitzador_48ee4b1b.parse_args()
    실패들 = []
    cas_VALOR = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    arxiu_COMPT = 0
    paràmetre_taula = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [dipòsit_rel/'compiler/컴파일러.py', dipòsit_rel/'compiler/기계어미리번역.py']
    for Camí in list((Project_rel/'Eines').glob('*.py')) + list((Project_rel/'예제').rglob('*.py')) + 공용번역기들:
        if Camí.name.endswith(('이름반영.py', '이름분석.py')): continue
        arxiu_COMPT += 1
        나무 = ast.parse(Camí.read_text()); 나무들[Camí] = 나무
        for introducció_VALOR in ast.walk(나무):
            if isinstance(introducció_VALOR, ast.FunctionDef):
                paràmetre_taula.setdefault(introducció_VALOR.name, set()).update(paràmetre_arg.arg for paràmetre_arg in introducció_VALOR.args.args + introducció_VALOR.args.kwonlyargs)
                if introducció_VALOR.args.kwarg: 가변매개함수.add(introducció_VALOR.name)
            if isinstance(introducció_VALOR, ast.ClassDef):
                for FUNCIÓ_VALOR in introducció_VALOR.body:
                    if isinstance(FUNCIÓ_VALOR, ast.FunctionDef) and FUNCIÓ_VALOR.name == '__init__':
                        paràmetre_taula.setdefault(introducció_VALOR.name, set()).update(paràmetre_arg.arg for paràmetre_arg in FUNCIÓ_VALOR.args.args + FUNCIÓ_VALOR.args.kwonlyargs)
            Nom = ''
            if isinstance(introducció_VALOR, (ast.FunctionDef, ast.ClassDef)): Nom = introducció_VALOR.name
            elif isinstance(introducció_VALOR, ast.Name) and isinstance(introducció_VALOR.ctx, ast.Store): Nom = introducció_VALOR.id
            elif isinstance(introducció_VALOR, ast.arg): Nom = introducció_VALOR.arg
            if Nom and Nom not in cas_VALOR and all(ord(caràcter_VALOR)<128 for caràcter_VALOR in Nom):
                실패들.append('{}:{}: {}'.format(Camí.relative_to(dipòsit_rel), introducció_VALOR.lineno, Nom))
    for Camí, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nom = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nom not in paràmetre_taula or Nom in 가변매개함수 or not any(ord(caràcter_VALOR)>127 for caràcter_VALOR in Nom): continue
            for paràmetre_arg in 호출.keywords:
                if paràmetre_arg.arg and paràmetre_arg.arg not in paràmetre_taula[Nom]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Camí.relative_to(dipòsit_rel), 호출.lineno, Nom, paràmetre_arg.arg))
    for línia in (Project_rel/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Procés_VALOR_introducció = línia.split('\t')
        if not (Project_rel/현재).is_file(): 실패들.append('moure_VALOR Fitxer 없음: '+현재)
        if Procés_VALOR_introducció == '호환진입점유지' and not (Project_rel/이전).is_file(): 실패들.append('호환 introducció_p 없음: '+이전)
    예제 = (Project_rel.parents[1]/'example/java/ExempleXarxa.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Camí in sorted((Project_rel.parents[1]/'example/java').glob('*.java')):
        FONT = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Camí.read_text())
        for Nom in re.findall(r'\b[^\W\d]\w*\b', FONT, re.UNICODE):
            if Nom not in 예약어 and all(ord(caràcter_VALOR)<128 for caràcter_VALOR in Nom):
                실패들.append('{}: 예제의 영어 identificador_VALOR {}'.format(Camí.name, Nom))
    for Nom in ('Finestra', 'Botó', 'Etiqueta', 'SMS_camp', '화면구성요소', 'incidència_cua', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        FONT = (Project_rel/'한국어자바/Català/propi'/(Nom+'.java')).read_text()
        FONT = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', FONT)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', FONT):
            실패들.append(Nom+': Català 직접 구현에 표준 objecte_VALOR 래퍼가 남았습니다.')
    시언어예제 = (Project_rel.parents[1]/'example/c/ExempleXarxa.c').read_text()
    for Nom in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nom in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nom: '+Nom)
    파이썬예제 = (Project_rel.parents[1]/'example/python/ExempleXarxa.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 excepció 직접 ús_VALOR')
    머리 = (Project_rel.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nom in ('núvol_Família', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'Crear_extrem', '자료전문보내기'):
        if re.search(r'^#define\s+'+Nom+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 macro_VALOR ús_VALOR: '+Nom)
    자바파일수 = 0
    for rel_VALOR in ('FONT', 'usuari/자바', '한국어자바'):
        for Camí in (Project_rel/rel_VALOR).rglob('*.java'):
            자바파일수 += 1
            FONT = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Camí.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', FONT):
                실패들.append('{}: 한국어화되지 않은 declaració {}'.format(Camí.relative_to(Project_rel), 맞음[1]))
            if rel_VALOR == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', FONT):
                실패들.append('{}: 공개 excepció declaració'.format(Camí.relative_to(Project_rel)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Camí in sorted((dipòsit_rel/'os/FONT').glob('*.java')):
        x86자바파일수 += 1
        FONT = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Camí.read_text())
        for Nom in re.findall(r'\b[^\W\d]\w*\b', FONT, re.UNICODE):
            if Nom not in 예약어 | 표준자바이름 and all(ord(caràcter_VALOR)<128 for caràcter_VALOR in Nom):
                실패들.append('{}: propi 영어 identificador_VALOR {}'.format(Camí.relative_to(dipòsit_rel), Nom))
    LOG_fila = {'passed': False, 'python_files': arxiu_COMPT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(Project_rel/'Eines/시언어이름분석.py')])
        Anàlisi_VALOR = json.loads((Project_rel/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(s_ha_produït_un_error) for s_ha_produït_un_error in Anàlisi_VALOR['s_ha_produït_un_error'])
        공개규약 = set(json.loads((Project_rel/'명명/규격이름.json').read_text()))
        for introducció_VALOR in Anàlisi_VALOR['declaració'].values():
            Nom = introducció_VALOR['Nom']; Camí = Path(introducció_VALOR['Fitxer'])
            FONT = Camí.read_bytes()
            # Català 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if FONT[introducció_VALOR['DESPLAÇAMENT_VALOR']:introducció_VALOR['DESPLAÇAMENT_VALOR']+len(Nom)] == Nom.encode() and Nom not in 공개규약:
                실패들.append('{}:{}: {}'.format(Camí.relative_to(Project_rel), introducció_VALOR['línia'], Nom))
        LOG_fila['c_semantic_checked'] = True
        LOG_fila['c_source_sha256'] = {str(Path(Fitxer).relative_to(Project_rel)):hash_arxiu for Fitxer,hash_arxiu in Anàlisi_VALOR['원문해시'].items()}
    LOG_fila['passed'] = not 실패들; LOG_fila['failures'] = 실패들
    destinació_VALOR = Project_rel/'build/verification/naming'; destinació_VALOR.mkdir(parents=True, exist_ok=True)
    (destinació_VALOR/'report.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Català declaració·Fitxer Camí·호환 introducció_p·통신 예제')

if __name__ == '__main__': Executa_2()
