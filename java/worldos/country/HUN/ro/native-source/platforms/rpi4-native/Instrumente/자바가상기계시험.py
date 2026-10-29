#!/usr/bin/env python3
"""OpenJDK와 propriu ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from executa_comandă import Project_rădăcină


def Pornește():
    출력결과 = Project_rădăcină / 'build/verification/jvm'
    Clasă_cale = 출력결과 / 'classes'; Clasă_cale.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_rădăcină / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_rădăcină / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Clasă_cale)] + [str(șir_date) for șir_date in 원문목록])
    시험목록 = [('객체시험', ['tapet_VALUE', 'ramură_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['contor_VALUE', 'sarcină_Acțiune', 'fir_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('valida.꾸러미시험', []), ('진입호환시험', [])]
    validare_raport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nume, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Clasă_cale) + ':' + str(자바꾸러미), Nume], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_rădăcină / 'Instrumente/executa_Fișier.py'), str(Clasă_cale / (Nume.replace('.', '/') + '.class'))]
            if '.' in Nume: 명령인수 += ['--class-name', Nume]
            for include in 포함인수: 명령인수 += ['--include', str(Clasă_cale / (include + '.class'))]
            if Nume == '한글소스': 명령인수[2] = str(Project_rădăcină / '시험/자바/한글소스.java')
            Finalizate_sumă = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            real_KR = Finalizate_sumă.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nume + '.log')).write_text(real_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", real_KR, re.S)
            assert Finalizate_sumă.returncode == 0 and 일치, (Nume, real_KR)
            KR = next(șir_date for șir_date in 일치.groups() if șir_date is not None) + '\n'
            assert KR == 예상결과, (Nume, 예상결과, KR)
            validare_raport['tests'].append({'name': Nume, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nume, flush=True)
        # propriu JVM에 직접 연결한 Română fir_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Finalizate_sumă = subprocess.run(['python3', str(Project_rădăcină/'Instrumente/executa_Fișier.py'), str(Clasă_cale/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        KR = Finalizate_sumă.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(KR)
        assert Finalizate_sumă.returncode == 0 and 'Română 직접 fir_VALUE transfera_VALUE\n' in KR and '\nexit 0\n' in KR, KR
        validare_raport['direct_korean_thread_and_entry'] = True
        print('PASS: Română 직접 fir_VALUE·Execută·Pornește intrare_p', flush=True)
        유효함 = (Clasă_cale / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        validare_raport['rejection_tests'] = []
        for Nume, sarcină_date, înștiințare_SMS in 시험사례:
            시험자료 = 출력결과 / (Nume + '.class'); 시험자료.write_bytes(sarcină_date)
            Finalizate_sumă = subprocess.run(['python3', str(Project_rădăcină / 'Instrumente/executa_Fișier.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = Finalizate_sumă.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Nume + '.log')).write_text(SMS, encoding='utf-8')
            assert Finalizate_sumă.returncode == 1 and înștiințare_SMS in SMS and 'exit 1\n' in SMS, (Nume, SMS)
            validare_raport['rejection_tests'].append({'name': Nume, 'passed': True})
            print('PASS (rejected):', Nume, flush=True)
        validare_raport['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(validare_raport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Pornește()
