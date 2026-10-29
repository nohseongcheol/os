#!/usr/bin/env python3
"""OpenJDK와 vlastné ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Vykonať_príkaz import akcia_koreň


def Spustiť_2():
    출력결과 = akcia_koreň / 'build/verification/jvm'
    lekcia_cesta = 출력결과 / 'classes'; lekcia_cesta.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = akcia_koreň / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((akcia_koreň / '시험/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(lekcia_cesta)] + [str(reťazec_údaje) for reťazec_údaje in 원문목록])
    test_Zoznam = [('객체시험', ['tapeta_VALUE', 'vetva_VALUE', '계산가능']), ('예외시험', []), ('Kolekcia_test', []),
             ('가닥시험', ['počítadlo_VALUE', 'úloha_Akcia', 'vlákno_VALUE']), ('한글시험', []), ('test_Siete', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('overiť_5fb2b747.test_zväzok', []), ('položka_kompatibilita_test', [])]
    overenie_správa = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((akcia_koreň / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Názov, 포함인수 in test_Zoznam:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(lekcia_cesta) + ':' + str(자바꾸러미), Názov], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(akcia_koreň / 'Nástroje/Vykonať_Súbor.py'), str(lekcia_cesta / (Názov.replace('.', '/') + '.class'))]
            if '.' in Názov: 명령인수 += ['--class-name', Názov]
            for zahrnúť in 포함인수: 명령인수 += ['--include', str(lekcia_cesta / (zahrnúť + '.class'))]
            if Názov == '한글소스': 명령인수[2] = str(akcia_koreň / '시험/자바/한글소스.java')
            Dokončené_úlohy_suma = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            skutočný_KR = Dokončené_úlohy_suma.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Názov + '.log')).write_text(skutočný_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", skutočný_KR, re.S)
            assert Dokončené_úlohy_suma.returncode == 0 and 일치, (Názov, skutočný_KR)
            KR = next(reťazec_údaje for reťazec_údaje in 일치.groups() if reťazec_údaje is not None) + '\n'
            assert KR == 예상결과, (Názov, 예상결과, KR)
            overenie_správa['tests'].append({'name': Názov, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Názov, flush=True)
        # vlastné JVM에 직접 연결한 Slovenský vlákno_VALUE/진입점은 OpenJDK용 래퍼가 아니다.
        Dokončené_úlohy_suma = subprocess.run(['python3', str(akcia_koreň/'Nástroje/Vykonať_Súbor.py'), str(lekcia_cesta/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        KR = Dokončené_úlohy_suma.stdout.decode('utf-8').replace('\r\n', '\n')
        (출력결과/'한국어가닥시험.log').write_text(KR)
        assert Dokončené_úlohy_suma.returncode == 0 and 'Slovenský 직접 vlákno_VALUE odovzdať_VALUE\n' in KR and '\nexit 0\n' in KR, KR
        overenie_správa['direct_korean_thread_and_entry'] = True
        print('PASS: Slovenský 직접 vlákno_VALUE·Spustiť·Spustiť_2 položka_bod', flush=True)
        유효함 = (lekcia_cesta / '객체시험.class').read_bytes()
        test_prípad = [('판거부', 유효함[:6] + b'\x00\x35' + 유효함[8:], 'supported class versions'),
                 ('잘린클래스', 유효함[:24], 'truncated class file')]
        overenie_správa['rejection_tests'] = []
        for Názov, údajová_časť_údaje, upozornenie_SMS in test_prípad:
            test_údaje = 출력결과 / (Názov + '.class'); test_údaje.write_bytes(údajová_časť_údaje)
            Dokončené_úlohy_suma = subprocess.run(['python3', str(akcia_koreň / 'Nástroje/Vykonať_Súbor.py'), str(test_údaje)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Spracovanie_textu = Dokončené_úlohy_suma.stdout.decode('utf-8').replace('\r\n', '\n')
            (출력결과 / (Názov + '.log')).write_text(Spracovanie_textu, encoding='utf-8')
            assert Dokončené_úlohy_suma.returncode == 1 and upozornenie_SMS in Spracovanie_textu and 'exit 1\n' in Spracovanie_textu, (Názov, Spracovanie_textu)
            overenie_správa['rejection_tests'].append({'name': Názov, 'passed': True})
            print('PASS (rejected):', Názov, flush=True)
        overenie_správa['passed'] = True
    finally:
        (출력결과 / 'report.json').write_text(json.dumps(overenie_správa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Spustiť_2()
