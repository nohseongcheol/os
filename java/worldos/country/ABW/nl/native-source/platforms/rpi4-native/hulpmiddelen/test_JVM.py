#!/usr/bin/env python3
"""OpenJDK와 Eigen ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Uitvoeren_opdracht import Taken_wortel


def starten():
    uitvoer = Taken_wortel / 'build/verification/jvm'
    les_pad = uitvoer / 'classes'; les_pad.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Taken_wortel / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Taken_wortel / 'tests/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(les_pad)] + [str(tekenreeks_gegevens) for tekenreeks_gegevens in 원문목록])
    test_Lijst = [('객체시험', ['Achtergrond_WAARDE', 'branch_WAARDE', '계산가능']), ('예외시험', []), ('incasso_test', []),
             ('가닥시험', ['teller_WAARDE', 'taak_Actie', 'thread_WAARDE']), ('한글시험', []), ('test_Netwerken', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('valideren.test_bundel', []), ('invoer_compatibiliteit_test', [])]
    validatie_Rapport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Naam, 포함인수 in test_Lijst:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(les_pad) + ':' + str(자바꾸러미), Naam], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Taken_wortel / 'hulpmiddelen/Uitvoeren_Bestand.py'), str(les_pad / (Naam.replace('.', '/') + '.class'))]
            if '.' in Naam: 명령인수 += ['--class-name', Naam]
            for bevatten in 포함인수: 명령인수 += ['--include', str(les_pad / (bevatten + '.class'))]
            if Naam == '한글소스': 명령인수[2] = str(Taken_wortel / 'tests/자바/한글소스.java')
            Voltooid_aantal = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            werkelijk_HR = Voltooid_aantal.stdout.decode('utf-8').replace('\r\n', '\n')
            (uitvoer / (Naam + '.log')).write_text(werkelijk_HR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", werkelijk_HR, re.S)
            assert Voltooid_aantal.returncode == 0 and 일치, (Naam, werkelijk_HR)
            resultaat = next(tekenreeks_gegevens for tekenreeks_gegevens in 일치.groups() if tekenreeks_gegevens is not None) + '\n'
            assert resultaat == 예상결과, (Naam, 예상결과, resultaat)
            validatie_Rapport['tests'].append({'name': Naam, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Naam, flush=True)
        # Eigen JVM에 직접 연결한 Nederlands thread_WAARDE/진입점은 OpenJDK용 래퍼가 아니다.
        Voltooid_aantal = subprocess.run(['python3', str(Taken_wortel/'hulpmiddelen/Uitvoeren_Bestand.py'), str(les_pad/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        resultaat = Voltooid_aantal.stdout.decode('utf-8').replace('\r\n', '\n')
        (uitvoer/'한국어가닥시험.log').write_text(resultaat)
        assert Voltooid_aantal.returncode == 0 and 'Nederlands 직접 thread_WAARDE doorgeven_WAARDE\n' in resultaat and '\nexit 0\n' in resultaat, resultaat
        validatie_Rapport['direct_korean_thread_and_entry'] = True
        print('PASS: Nederlands 직접 thread_WAARDE·Uitvoeren·starten beginpunt', flush=True)
        geldig = (les_pad / '객체시험.class').read_bytes()
        test_case = [('판거부', geldig[:6] + b'\x00\x35' + geldig[8:], 'supported class versions'),
                 ('잘린클래스', geldig[:24], 'truncated class file')]
        validatie_Rapport['rejection_tests'] = []
        for Naam, payload_gegevens, kennisgeving_sms in test_case:
            test_gegevens = uitvoer / (Naam + '.class'); test_gegevens.write_bytes(payload_gegevens)
            Voltooid_aantal = subprocess.run(['python3', str(Taken_wortel / 'hulpmiddelen/Uitvoeren_Bestand.py'), str(test_gegevens)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            tekst = Voltooid_aantal.stdout.decode('utf-8').replace('\r\n', '\n')
            (uitvoer / (Naam + '.log')).write_text(tekst, encoding='utf-8')
            assert Voltooid_aantal.returncode == 1 and kennisgeving_sms in tekst and 'exit 1\n' in tekst, (Naam, tekst)
            validatie_Rapport['rejection_tests'].append({'name': Naam, 'passed': True})
            print('PASS (rejected):', Naam, flush=True)
        validatie_Rapport['passed'] = True
    finally:
        (uitvoer / 'report.json').write_text(json.dumps(validatie_Rapport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    starten()
