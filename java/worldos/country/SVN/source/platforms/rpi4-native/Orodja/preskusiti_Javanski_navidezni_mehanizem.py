#!/usr/bin/env python3
"""OpenJDK와 lastno ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Izvedi_ukaz import pobuda_koren


def Zaženi():
    출력결과 = pobuda_koren / 'build/verification/jvm'
    Razred_pot = 출력결과 / 'classes'; Razred_pot.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = pobuda_koren / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((pobuda_koren / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Razred_pot)] + [str(niz_podatki) for niz_podatki in 원문목록])
    preskusiti_Seznam = [('객체시험', ['Ozadje_VALUE', 'veja_VALUE', '계산가능']), ('예외시험', []), ('Zbirka_preskusiti', []),
             ('가닥시험', ['števec_VALUE', 'opravek_akcija', 'nit_VALUE']), ('한글시험', []), ('preskusiti_Uporaba_omrežij', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('preveriti_veljavnost.preskusiti_sveženj', []), ('vnos_združljivost_preskusiti', [])]
    preverjanje_veljavnosti_prijavi = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Ime, 포함인수 in preskusiti_Seznam:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Razred_pot) + ':' + str(자바꾸러미), Ime], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(pobuda_koren / 'Orodja/Izvedi_Datoteka.py'), str(Razred_pot / (Ime.replace('.', '/') + '.class'))]
            if '.' in Ime: 명령인수 += ['--class-name', Ime]
            for vključevati in 포함인수: 명령인수 += ['--include', str(Razred_pot / (vključevati + '.class'))]
            if Ime == '한글소스': 명령인수[2] = str(pobuda_koren / '시험/자바/한글소스.java')
            Dokončano_znesek = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            dejanski_KR = Dokončano_znesek.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ime + '.log')).write_text(dejanski_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", dejanski_KR, re.S)
            assert Dokončano_znesek.returncode == 0 and 일치, (Ime, dejanski_KR)
            REZULTAT = next(niz_podatki for niz_podatki in 일치.groups() if niz_podatki is not None) + '\n'
            assert REZULTAT == 예상결과, (Ime, 예상결과, REZULTAT)
            preverjanje_veljavnosti_prijavi['tests'].append({'name': Ime, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Ime, flush=True)
        # lastno JVM에 직접 연결한 slovenščina nit_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Dokončano_znesek = subprocess.run(['python3', str(pobuda_koren/'Orodja/Izvedi_Datoteka.py'), str(Razred_pot/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        REZULTAT = Dokončano_znesek.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(REZULTAT)
        assert Dokončano_znesek.returncode == 0 and 'slovenščina 직접 nit_VALUE posredovati_VALUE\n' in REZULTAT and '\nexit 0\n' in REZULTAT, REZULTAT
        preverjanje_veljavnosti_prijavi['direct_korean_thread_and_entry'] = True
        print('PASS: slovenščina 직접 nit_VALUE·Izvedi·Zaženi vnos_p', flush=True)
        유효함 = (Razred_pot / '객체시험.class').read_bytes()
        preskusiti_spor = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        preverjanje_veljavnosti_prijavi['rejection_tests'] = []
        for Ime, koristna_vsebina_podatki, obvestilo_SMS in preskusiti_spor:
            preskusiti_podatki = 출력결과 / (Ime + '.class'); preskusiti_podatki.write_bytes(koristna_vsebina_podatki)
            Dokončano_znesek = subprocess.run(['python3', str(pobuda_koren / 'Orodja/Izvedi_Datoteka.py'), str(preskusiti_podatki)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Besedilo = Dokončano_znesek.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Ime + '.log')).write_text(Besedilo, encoding='utf-8')
            assert Dokončano_znesek.returncode == 1 and obvestilo_SMS in Besedilo and 'exit 1\n' in Besedilo, (Ime, Besedilo)
            preverjanje_veljavnosti_prijavi['rejection_tests'].append({'name': Ime, 'passed': True})
            print('PASS (rejected):', Ime, flush=True)
        preverjanje_veljavnosti_prijavi['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Zaženi()
