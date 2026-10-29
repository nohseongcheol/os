#!/usr/bin/env python3
"""OpenJDK와 자체 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Izvrši_komanda import projicirati_koijen


def Pokreni():
    출력결과 = projicirati_koijen / 'build/verification/jvm'
    klasa_put = 출력결과 / 'classes'; klasa_put.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = projicirati_koijen / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((projicirati_koijen / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(klasa_put)] + [str(string_podaci) for string_podaci in 원문목록])
    시험목록 = [('객체시험', ['poster_VALUE', 'ogranak_VALUE', '계산가능']), ('예외시험', []), ('모음시험', []),
             ('가닥시험', ['brojač_VALUE', 'zadatak_radnja', 'nit_VALUE']), ('한글시험', []), ('통신시험', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ovjeriti.꾸러미시험', []), ('진입호환시험', [])]
    provjera_izvještaj = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Naziv, 포함인수 in 시험목록:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klasa_put) + ':' + str(자바꾸러미), Naziv], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(projicirati_koijen / 'Alati/Izvrši_fajl.py'), str(klasa_put / (Naziv.replace('.', '/') + '.class'))]
            if '.' in Naziv: 명령인수 += ['--class-name', Naziv]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(klasa_put / (포함항목 + '.class'))]
            if Naziv == '한글소스': 명령인수[2] = str(projicirati_koijen / '시험/자바/한글소스.java')
            완료량 = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            stvaran_mjera = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Naziv + '.log')).write_text(stvaran_mjera, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", stvaran_mjera, re.S)
            assert 완료량.returncode == 0 and 일치, (Naziv, stvaran_mjera)
            mjera = next(string_podaci for string_podaci in 일치.groups() if string_podaci is not None) + '\n'
            assert mjera == 예상결과, (Naziv, 예상결과, mjera)
            provjera_izvještaj['tests'].append({'name': Naziv, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Naziv, flush=True)
        # 자체 JVM에 직접 연결한 한국어 nit_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        완료량 = subprocess.run(['python3', str(projicirati_koijen/'Alati/Izvrši_fajl.py'), str(klasa_put/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        mjera = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(mjera)
        assert 완료량.returncode == 0 and '한국어 직접 nit_VALUE proslijediti_VALUE\n' in mjera and '\nexit 0\n' in mjera, mjera
        provjera_izvještaj['direct_korean_thread_and_entry'] = True
        print('PASS: 한국어 직접 nit_VALUE·Izvrši·Pokreni unos_p', flush=True)
        유효함 = (klasa_put / '객체시험.class').read_bytes()
        시험사례 = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        provjera_izvještaj['rejection_tests'] = []
        for Naziv, korisni_sadržaj_podaci, 알림문 in 시험사례:
            시험자료 = 출력결과 / (Naziv + '.class'); 시험자료.write_bytes(korisni_sadržaj_podaci)
            완료량 = subprocess.run(['python3', str(projicirati_koijen / 'Alati/Izvrši_fajl.py'), str(시험자료)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Tekst = 완료량.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Naziv + '.log')).write_text(Tekst, encoding='utf-8')
            assert 완료량.returncode == 1 and 알림문 in Tekst and 'exit 1\n' in Tekst, (Naziv, Tekst)
            provjera_izvještaj['rejection_tests'].append({'name': Naziv, 'passed': True})
            print('PASS (rejected):', Naziv, flush=True)
        provjera_izvještaj['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(provjera_izvještaj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Pokreni()
