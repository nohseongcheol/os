#!/usr/bin/env python3
"""OpenJDK와 propi ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Executa_ordre import Project_rel


def Executa_2():
    출력결과 = Project_rel / 'build/verification/jvm'
    Classe_camí = 출력결과 / 'classes'; Classe_camí.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_rel / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_rel / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Classe_camí)] + [str(cadena_dades) for cadena_dades in 원문목록])
    시험목록 = [('객체시험', ['Fons_VALOR', 'branca_VALOR', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['셈통', 'tasca_acció', 'fil_VALOR']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('validar.꾸러미시험', []), ('진입호환시험', [])]
    validació_informe = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nom, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Classe_camí) + ':' + str(자바꾸러미), Nom], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_rel / 'Eines/Executa_arxiu.py'), str(Classe_camí / (Nom.replace('.', '/') + '.class'))]
            if '.' in Nom: 명령인수 += ['--class-name', Nom]
            for incloure in 포함인수: 명령인수 += ['--include', str(Classe_camí / (incloure + '.class'))]
            if Nom == '한글소스': 명령인수[2] = str(Project_rel / '시험/자바/한글소스.java')
            Completades_quantitat = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            real_mesura = Completades_quantitat.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nom + '.log')).write_text(real_mesura, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", real_mesura, re.S)
            assert Completades_quantitat.returncode == 0 and 일치, (Nom, real_mesura)
            RESULTAT = next(cadena_dades for cadena_dades in 일치.groups() if cadena_dades is not None) + '\n'
            assert RESULTAT == 예상결과, (Nom, 예상결과, RESULTAT)
            validació_informe['tests'].append({'name': Nom, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nom, flush=True)
        # propi JVM에 직접 연결한 Català fil_VALOR/진입점은 OpenJDK용 래퍼가 아니다.
        Completades_quantitat = subprocess.run(['python3', str(Project_rel/'Eines/Executa_arxiu.py'), str(Classe_camí/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        RESULTAT = Completades_quantitat.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(RESULTAT)
        assert Completades_quantitat.returncode == 0 and 'Català 직접 fil_VALOR transmetre_VALOR\n' in RESULTAT and '\nexit 0\n' in RESULTAT, RESULTAT
        validació_informe['direct_korean_thread_and_entry'] = True
        print('PASS: Català 직접 fil_VALOR·Executa·Executa_2 introducció_p', flush=True)
        유효함 = (Classe_camí / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validació_informe['rejection_tests'] = []
        for Nom, càrrega_dades, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Nom + '.class'); 시험자료.write_bytes(càrrega_dades)
            Completades_quantitat = subprocess.run(['python3', str(Project_rel / 'Eines/Executa_arxiu.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = Completades_quantitat.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nom + '.log')).write_text(SMS, encoding='utf-8')
            assert Completades_quantitat.returncode == 1 and 알림문 in SMS and 'exit 1\n' in SMS, (Nom, SMS)
            validació_informe['rejection_tests'].append({'name': Nom, 'passed': True})
            print('PASS (rejected):', Nom, flush=True)
        validació_informe['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validació_informe, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Executa_2()
