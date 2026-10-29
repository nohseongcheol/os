#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Izvrši_komanda import radnja_koren


def koristiti():
    출력결과 = radnja_koren / 'build/verification/jvm'
    Razred_putanja = 출력결과 / 'classes'; Razred_putanja.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = radnja_koren / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((radnja_koren / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Razred_putanja)] + [str(niska_podaci) for niska_podaci in 원문목록])
    시험목록 = [('객체시험', ['poster_VALUE', 'grana_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['brojač_VALUE', 'obaveza_radnja', 'nit_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('potvrditi.꾸러미시험', []), ('진입호환시험', [])]
    provera_valjanosti_izveštaj = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((radnja_koren / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for ime, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Razred_putanja) + ':' + str(자바꾸러미), ime], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(radnja_koren / 'Alatke/Izvrši_Datoteka.py'), str(Razred_putanja / (ime.replace('.', '/') + '.class'))]
            if '.' in ime: 명령인수 += ['--class-name', ime]
            for uključiti in 포함인수: 명령인수 += ['--include', str(Razred_putanja / (uključiti + '.class'))]
            if ime == '한글소스': 명령인수[2] = str(radnja_koren / '시험/자바/한글소스.java')
            Dovršeno_iznos = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            stvarni_KR = Dovršeno_iznos.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ime + '.log')).write_text(stvarni_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", stvarni_KR, re.S)
            assert Dovršeno_iznos.returncode == 0 and 일치, (ime, stvarni_KR)
            KR = next(niska_podaci for niska_podaci in 일치.groups() if niska_podaci is not None) + '\n'
            assert KR == 예상결과, (ime, 예상결과, KR)
            provera_valjanosti_izveštaj['tests'].append({'name': ime, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', ime, flush=True)
        # 자체 JVM에 직접 연결한 한국어 nit_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Dovršeno_iznos = subprocess.run(['python3', str(radnja_koren/'Alatke/Izvrši_Datoteka.py'), str(Razred_putanja/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        KR = Dovršeno_iznos.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(KR)
        assert Dovršeno_iznos.returncode == 0 and '한국어 직접 nit_VALUE prebaciti_VALUE\n' in KR and '\nexit 0\n' in KR, KR
        provera_valjanosti_izveštaj['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 nit_VALUE·Izvrši_obaveza·koristiti stavka_p', flush=True)
        유효함 = (Razred_putanja / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        provera_valjanosti_izveštaj['rejection_tests'] = []
        for ime, korisni_podaci_podaci, obaveštavanje_SMS in 시험사례:
            시험자료 = 출력결과 / (ime + '.class'); 시험자료.write_bytes(korisni_podaci_podaci)
            Dovršeno_iznos = subprocess.run(['python3', str(radnja_koren / 'Alatke/Izvrši_Datoteka.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            SMS = Dovršeno_iznos.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (ime + '.log')).write_text(SMS, encoding='utf-8')
            assert Dovršeno_iznos.returncode == 1 and obaveštavanje_SMS in SMS and 'exit 1\n' in SMS, (ime, SMS)
            provera_valjanosti_izveštaj['rejection_tests'].append({'name': ime, 'passed': True})
            print('PASS (rejected):', ime, flush=True)
        provera_valjanosti_izveštaj['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(provera_valjanosti_izveštaj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    koristiti()
