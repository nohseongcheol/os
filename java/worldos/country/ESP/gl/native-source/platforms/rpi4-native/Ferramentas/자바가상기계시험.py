#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from executar_comando import Project_raíz


def Executar_2():
    출력결과 = Project_raíz / 'build/verification/jvm'
    Clase_camiño = 출력결과 / 'classes'; Clase_camiño.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_raíz / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_raíz / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Clase_camiño)] + [str(cadea_datos) for cadea_datos in 원문목록])
    시험목록 = [('객체시험', ['Fondo_VALOR', 'ramificación_VALOR', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['셈통', 'tarefa_acción', 'tema_VALOR']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validar.꾸러미시험', []), ('진입호환시험', [])]
    validación_informe = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_raíz / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nome, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Clase_camiño) + ':' + str(자바꾸러미), Nome], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_raíz / 'Ferramentas/executar_Ficheiro.py'), str(Clase_camiño / (Nome.replace('.', '/') + '.class'))]
            if '.' in Nome: 명령인수 += ['--class-name', Nome]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Clase_camiño / (포함항목 + '.class'))]
            if Nome == '한글소스': 명령인수[2] = str(Project_raíz / '시험/자바/한글소스.java')
            Completadas_cantidade = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            real_medida = Completadas_cantidade.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nome + '.log')).write_text(real_medida, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", real_medida, re.S)
            assert Completadas_cantidade.returncode == 0 and 일치, (Nome, real_medida)
            RESULTANTE = next(cadea_datos for cadea_datos in 일치.groups() if cadea_datos is not None) + '\n'
            assert RESULTANTE == 예상결과, (Nome, 예상결과, RESULTANTE)
            validación_informe['tests'].append({'name': Nome, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nome, flush=True)
        # 자체 JVM에 직접 연결한 Galego tema_VALOR/진입점은 OpenJDK용 래퍼가 아니다.
        Completadas_cantidade = subprocess.run(['python3', str(Project_raíz/'Ferramentas/executar_Ficheiro.py'), str(Clase_camiño/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        RESULTANTE = Completadas_cantidade.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(RESULTANTE)
        assert Completadas_cantidade.returncode == 0 and 'Galego 직접 tema_VALOR pass_VALOR\n' in RESULTANTE and '\nexit 0\n' in RESULTANTE, RESULTANTE
        validación_informe['direct_korean_thread_and_entry'] = True
        print('PASS: Galego 직접 tema_VALOR·Executar·Executar_2 introdución_p', flush=True)
        유효함 = (Clase_camiño / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validación_informe['rejection_tests'] = []
        for Nome, carga_datos_60367a51, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Nome + '.class'); 시험자료.write_bytes(carga_datos_60367a51)
            Completadas_cantidade = subprocess.run(['python3', str(Project_raíz / 'Ferramentas/executar_Ficheiro.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Texto = Completadas_cantidade.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nome + '.log')).write_text(Texto, encoding='utf-8')
            assert Completadas_cantidade.returncode == 1 and 알림문 in Texto and 'exit 1\n' in Texto, (Nome, Texto)
            validación_informe['rejection_tests'].append({'name': Nome, 'passed': True})
            print('PASS (rejected):', Nome, flush=True)
        validación_informe['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validación_informe, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Executar_2()
