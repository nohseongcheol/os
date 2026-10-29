#!/usr/bin/env python3
"""OpenJDK와 vlastiti ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Izvrši_naredba import akcija_korijen


def Pokreni():
    출력결과 = akcija_korijen / 'build/verification/jvm'
    poduka_put = 출력결과 / 'classes'; poduka_put.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = akcija_korijen / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((akcija_korijen / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(poduka_put)] + [str(niz_podaci) for niz_podaci in 원문목록])
    시험목록 = [('객체시험', ['podloga_VALUE', 'grana_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['brojač_posjeta_VALUE', 'obaveza_akcija', 'nit_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('potvrditi.꾸러미시험', []), ('진입호환시험', [])]
    provjera_izvješće = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Ime, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(poduka_put) + ':' + str(자바꾸러미), Ime], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(akcija_korijen / 'Alati/Izvrši_Datoteka.py'), str(poduka_put / (Ime.replace('.', '/') + '.class'))]
            if '.' in Ime: 명령인수 += ['--class-name', Ime]
            for obuhvaćati in 포함인수: 명령인수 += ['--include', str(poduka_put / (obuhvaćati + '.class'))]
            if Ime == '한글소스': 명령인수[2] = str(akcija_korijen / '시험/자바/한글소스.java')
            Dovršeno_iznos = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            stvaran_KR = Dovršeno_iznos.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ime + '.log')).write_text(stvaran_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", stvaran_KR, re.S)
            assert Dovršeno_iznos.returncode == 0 and 일치, (Ime, stvaran_KR)
            REZULTAT = next(niz_podaci for niz_podaci in 일치.groups() if niz_podaci is not None) + '\n'
            assert REZULTAT == 예상결과, (Ime, 예상결과, REZULTAT)
            provjera_izvješće['tests'].append({'name': Ime, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Ime, flush=True)
        # vlastiti JVM에 직접 연결한 hrvatski nit_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Dovršeno_iznos = subprocess.run(['python3', str(akcija_korijen/'Alati/Izvrši_Datoteka.py'), str(poduka_put/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        REZULTAT = Dovršeno_iznos.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(REZULTAT)
        assert Dovršeno_iznos.returncode == 0 and 'hrvatski 직접 nit_VALUE proslijediti_VALUE\n' in REZULTAT and '\nexit 0\n' in REZULTAT, REZULTAT
        provjera_izvješće['direct_korean_thread_and_entry'] = True
        print('PASS: hrvatski 직접 nit_VALUE·Izvrši·Pokreni unos_p', flush=True)
        유효함 = (poduka_put / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        provjera_izvješće['rejection_tests'] = []
        for Ime, korisni_podaci_podaci, obavijest_SMS in 시험사례:
            시험자료 = 출력결과 / (Ime + '.class'); 시험자료.write_bytes(korisni_podaci_podaci)
            Dovršeno_iznos = subprocess.run(['python3', str(akcija_korijen / 'Alati/Izvrši_Datoteka.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekst = Dovršeno_iznos.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ime + '.log')).write_text(Tekst, encoding='utf-8')
            assert Dovršeno_iznos.returncode == 1 and obavijest_SMS in Tekst and 'exit 1\n' in Tekst, (Ime, Tekst)
            provjera_izvješće['rejection_tests'].append({'name': Ime, 'passed': True})
            print('PASS (rejected):', Ime, flush=True)
        provjera_izvješće['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(provjera_izvješće, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Pokreni()
