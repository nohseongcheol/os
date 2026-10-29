#!/usr/bin/env python3
"""명명 clip·excepción·경로를 검사한다. --시언어는 libclang declaración 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_raíz = Path(__file__).resolve().parents[1]
repositorio_raíz = Project_raíz.parents[1]

def Executar_2():
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('--시언어', action='store_true')
    Argumentos = analizador_48ee4b1b.parse_args()
    실패들 = []
    caso_VALOR = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Ficheiro_CONTAR = 0
    parámetro_táboa = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repositorio_raíz/'compiler/컴파일러.py', repositorio_raíz/'compiler/기계어미리번역.py']
    for CAMIÑO in list((Project_raíz/'Ferramentas').glob('*.py')) + list((Project_raíz/'예제').rglob('*.py')) + 공용번역기들:
        if CAMIÑO.name.endswith(('이름반영.py', '이름분석.py')): continue
        Ficheiro_CONTAR += 1
        나무 = ast.parse(CAMIÑO.read_text()); 나무들[CAMIÑO] = 나무
        for introdución_VALOR in ast.walk(나무):
            if isinstance(introdución_VALOR, ast.FunctionDef):
                parámetro_táboa.setdefault(introdución_VALOR.name, set()).update(parámetro_argumento.arg for parámetro_argumento in introdución_VALOR.args.args + introdución_VALOR.args.kwonlyargs)
                if introdución_VALOR.args.kwarg: 가변매개함수.add(introdución_VALOR.name)
            if isinstance(introdución_VALOR, ast.ClassDef):
                for FUNCIÓN_VALOR in introdución_VALOR.body:
                    if isinstance(FUNCIÓN_VALOR, ast.FunctionDef) and FUNCIÓN_VALOR.name == '__init__':
                        parámetro_táboa.setdefault(introdución_VALOR.name, set()).update(parámetro_argumento.arg for parámetro_argumento in FUNCIÓN_VALOR.args.args + FUNCIÓN_VALOR.args.kwonlyargs)
            Nome = ''
            if isinstance(introdución_VALOR, (ast.FunctionDef, ast.ClassDef)): Nome = introdución_VALOR.name
            elif isinstance(introdución_VALOR, ast.Name) and isinstance(introdución_VALOR.ctx, ast.Store): Nome = introdución_VALOR.id
            elif isinstance(introdución_VALOR, ast.arg): Nome = introdución_VALOR.arg
            if Nome and Nome not in caso_VALOR and all(ord(carácter_VALOR)<128 for carácter_VALOR in Nome):
                실패들.append('{}:{}: {}'.format(CAMIÑO.relative_to(repositorio_raíz), introdución_VALOR.lineno, Nome))
    for CAMIÑO, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nome = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nome not in parámetro_táboa or Nome in 가변매개함수 or not any(ord(carácter_VALOR)>127 for carácter_VALOR in Nome): continue
            for parámetro_argumento in 호출.keywords:
                if parámetro_argumento.arg and parámetro_argumento.arg not in parámetro_táboa[Nome]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(CAMIÑO.relative_to(repositorio_raíz), 호출.lineno, Nome, parámetro_argumento.arg))
    for Liña in (Project_raíz/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, ao_corrente_elemento, Proceso_VALOR_introdución = Liña.split('\t')
        if not (Project_raíz/ao_corrente_elemento).is_file(): 실패들.append('mover_VALOR Ficheiro 없음: '+ao_corrente_elemento)
        if Proceso_VALOR_introdución == '호환진입점유지' and not (Project_raíz/이전).is_file(): 실패들.append('호환 introdución_p 없음: '+이전)
    예제 = (Project_raíz.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for CAMIÑO in sorted((Project_raíz.parents[1]/'example/java').glob('*.java')):
        FONTE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CAMIÑO.read_text())
        for Nome in re.findall(r'\b[^\W\d]\w*\b', FONTE, re.UNICODE):
            if Nome not in 예약어 and all(ord(carácter_VALOR)<128 for carácter_VALOR in Nome):
                실패들.append('{}: 예제의 영어 식별자 {}'.format(CAMIÑO.name, Nome))
    for Nome in ('Xanela', 'botón', 'Etiqueta', 'SMS_campo', '화면구성요소', 'evento_cola', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        FONTE = (Project_raíz/'한국어자바/Galego/자체'/(Nome+'.java')).read_text()
        FONTE = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', FONTE)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', FONTE):
            실패들.append(Nome+': Galego 직접 구현에 표준 obxecto_VALOR 래퍼가 남았습니다.')
    시언어예제 = (Project_raíz.parents[1]/'example/c/네트워크예제.c').read_text()
    for Nome in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nome in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nome: '+Nome)
    파이썬예제 = (Project_raíz.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 excepción 직접 사용')
    머리 = (Project_raíz.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nome in ('nube_Familia', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'crear_extremo', '자료전문보내기'):
        if re.search(r'^#define\s+'+Nome+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 macro_VALOR 사용: '+Nome)
    자바파일수 = 0
    for raíz_VALOR in ('FONTE', 'usuario/자바', '한국어자바'):
        for CAMIÑO in (Project_raíz/raíz_VALOR).rglob('*.java'):
            자바파일수 += 1
            FONTE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CAMIÑO.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', FONTE):
                실패들.append('{}: 한국어화되지 않은 declaración {}'.format(CAMIÑO.relative_to(Project_raíz), 맞음[1]))
            if raíz_VALOR == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', FONTE):
                실패들.append('{}: 공개 excepción declaración'.format(CAMIÑO.relative_to(Project_raíz)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for CAMIÑO in sorted((repositorio_raíz/'os/FONTE').glob('*.java')):
        x86자바파일수 += 1
        FONTE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CAMIÑO.read_text())
        for Nome in re.findall(r'\b[^\W\d]\w*\b', FONTE, re.UNICODE):
            if Nome not in 예약어 | 표준자바이름 and all(ord(carácter_VALOR)<128 for carácter_VALOR in Nome):
                실패들.append('{}: 자체 영어 식별자 {}'.format(CAMIÑO.relative_to(repositorio_raíz), Nome))
    LOG_fila = {'passed': False, 'python_files': Ficheiro_CONTAR, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumentos.시언어:
        subprocess.check_call(['python3', str(Project_raíz/'Ferramentas/시언어이름분석.py')])
        Análise_VALOR = json.loads((Project_raíz/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ERRO) for ERRO in Análise_VALOR['ERRO'])
        공개규약 = set(json.loads((Project_raíz/'명명/규격이름.json').read_text()))
        for introdución_VALOR in Análise_VALOR['declaración'].values():
            Nome = introdución_VALOR['Nome']; CAMIÑO = Path(introdución_VALOR['Ficheiro'])
            FONTE = CAMIÑO.read_bytes()
            # Galego 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if FONTE[introdución_VALOR['DESPRAZAMENTO_VALOR']:introdución_VALOR['DESPRAZAMENTO_VALOR']+len(Nome)] == Nome.encode() and Nome not in 공개규약:
                실패들.append('{}:{}: {}'.format(CAMIÑO.relative_to(Project_raíz), introdución_VALOR['Liña'], Nome))
        LOG_fila['c_semantic_checked'] = True
        LOG_fila['c_source_sha256'] = {str(Path(Ficheiro).relative_to(Project_raíz)):hash_Ficheiro for Ficheiro,hash_Ficheiro in Análise_VALOR['원문해시'].items()}
    LOG_fila['passed'] = not 실패들; LOG_fila['failures'] = 실패들
    destino_VALOR = Project_raíz/'build/verification/naming'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    (destino_VALOR/'report.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Galego declaración·Ficheiro CAMIÑO·호환 introdución_p·통신 예제')

if __name__ == '__main__': Executar_2()
