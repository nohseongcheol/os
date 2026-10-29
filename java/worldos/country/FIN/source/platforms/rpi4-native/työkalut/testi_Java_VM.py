#!/usr/bin/env python3
"""OpenJDK와 oma ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Suorita_komento import aloite_juuri


def Suorita_2():
    tulos = aloite_juuri / 'build/verification/jvm'
    Luokka_polku = tulos / 'classes'; Luokka_polku.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = aloite_juuri / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((aloite_juuri / 'testit/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Luokka_polku)] + [str(merkkijono_data) for merkkijono_data in 원문목록])
    testi_luettelo = [('객체시험', ['Tausta_ARVO', 'haara_ARVO', '계산가능']), ('예외시험', []), ('perintä_testi', []),
             ('가닥시험', ['laskuri_ARVO', 'tehtävä_toimi', 'säie_ARVO']), ('한글시험', []), ('testi_Verkot', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('vahvista.testi_nippu', []), ('merkintä_yhteensopivuus_testi', [])]
    vahvistus_raportti = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nimi, 포함인수 in testi_luettelo:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Luokka_polku) + ':' + str(자바꾸러미), Nimi], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(aloite_juuri / 'työkalut/Suorita_Tiedosto.py'), str(Luokka_polku / (Nimi.replace('.', '/') + '.class'))]
            if '.' in Nimi: 명령인수 += ['--class-name', Nimi]
            for sisältää in 포함인수: 명령인수 += ['--include', str(Luokka_polku / (sisältää + '.class'))]
            if Nimi == '한글소스': 명령인수[2] = str(aloite_juuri / 'testit/자바/한글소스.java')
            valmis_määrä = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            todellinen_KR = valmis_määrä.stdout.decode('utf-8').replace('\r\n', '\n')
            (tulos / (Nimi + '.log')).write_text(todellinen_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", todellinen_KR, re.S)
            assert valmis_määrä.returncode == 0 and 일치, (Nimi, todellinen_KR)
            TULOS = next(merkkijono_data for merkkijono_data in 일치.groups() if merkkijono_data is not None) + '\n'
            assert TULOS == 예상결과, (Nimi, 예상결과, TULOS)
            vahvistus_raportti['tests'].append({'name': Nimi, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nimi, flush=True)
        # oma JVM에 직접 연결한 suomi säie_ARVO/진입점은 OpenJDK용 래퍼가 아니다.
        valmis_määrä = subprocess.run(['python3', str(aloite_juuri/'työkalut/Suorita_Tiedosto.py'), str(Luokka_polku/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        TULOS = valmis_määrä.stdout.decode('utf-8').replace('\r\n', '\n')
        (tulos/'한국어가닥시험.log').write_text(TULOS)
        assert valmis_määrä.returncode == 0 and 'suomi 직접 säie_ARVO välittää_ARVO\n' in TULOS and '\nexit 0\n' in TULOS, TULOS
        vahvistus_raportti['direct_korean_thread_and_entry'] = True
        print('PASS: suomi 직접 säie_ARVO·Suorita·Suorita_2 aloituskohta', flush=True)
        kelvollinen = (Luokka_polku / '객체시험.class').read_bytes()
        testi_työ = [('판거부', kelvollinen[:6] + b'\x00\x35' + kelvollinen[8:], 'supported class versions'),
                 ('잘린클래스', kelvollinen[:24], 'truncated class file')]
        vahvistus_raportti['rejection_tests'] = []
        for Nimi, tiedot_data, 알림문 in testi_työ:
            testi_data = tulos / (Nimi + '.class'); testi_data.write_bytes(tiedot_data)
            valmis_määrä = subprocess.run(['python3', str(aloite_juuri / 'työkalut/Suorita_Tiedosto.py'), str(testi_data)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            teksti = valmis_määrä.stdout.decode('utf-8').replace('\r\n', '\n')
            (tulos / (Nimi + '.log')).write_text(teksti, encoding='utf-8')
            assert valmis_määrä.returncode == 1 and 알림문 in teksti and 'exit 1\n' in teksti, (Nimi, teksti)
            vahvistus_raportti['rejection_tests'].append({'name': Nimi, 'passed': True})
            print('PASS (rejected):', Nimi, flush=True)
        vahvistus_raportti['passed'] = True
    finally:
        (tulos / 'report.json').write_text(json.dumps(vahvistus_raportti, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Suorita_2()
