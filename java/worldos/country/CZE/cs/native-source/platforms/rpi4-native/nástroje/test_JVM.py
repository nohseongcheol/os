#!/usr/bin/env python3
"""OpenJDK와 vlastní ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Provést_příkaz import akce_kořen


def Spustit_2():
    výstup = akce_kořen / 'build/verification/jvm'
    Třída_cesta = výstup / 'classes'; Třída_cesta.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = akce_kořen / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((akce_kořen / 'zkoušky/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Třída_cesta)] + [str(řetězec_data) for řetězec_data in 원문목록])
    seznam_testů = [('객체시험', ['Pozadí_HODNOTA', 'větev_HODNOTA', '계산가능']), ('예외시험', []), ('inkaso_test', []),
             ('가닥시험', ['čítač_HODNOTA', 'úkol_Akce', 'vlákno_HODNOTA']), ('한글시험', []), ('test_Sítě', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('ověřit_5fb2b747.test_sada', []), ('položka_kompatibilita_test', [])]
    ověření_Zpráva = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Název, 포함인수 in seznam_testů:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Třída_cesta) + ':' + str(자바꾸러미), Název], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(akce_kořen / 'nástroje/Provést_Soubor.py'), str(Třída_cesta / (Název.replace('.', '/') + '.class'))]
            if '.' in Název: 명령인수 += ['--class-name', Název]
            for zahrnout in 포함인수: 명령인수 += ['--include', str(Třída_cesta / (zahrnout + '.class'))]
            if Název == '한글소스': 명령인수[2] = str(akce_kořen / 'zkoušky/자바/한글소스.java')
            dokončeno_částka = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            skutečný_KV = dokončeno_částka.stdout.decode('utf-8').replace('\r\n', '\n')
            (výstup / (Název + '.log')).write_text(skutečný_KV, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", skutečný_KV, re.S)
            assert dokončeno_částka.returncode == 0 and 일치, (Název, skutečný_KV)
            VÝSLEDEK = next(řetězec_data for řetězec_data in 일치.groups() if řetězec_data is not None) + '\n'
            assert VÝSLEDEK == 예상결과, (Název, 예상결과, VÝSLEDEK)
            ověření_Zpráva['tests'].append({'name': Název, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Název, flush=True)
        # vlastní JVM에 직접 연결한 čeština vlákno_HODNOTA/진입점은 OpenJDK용 래퍼가 아니다.
        dokončeno_částka = subprocess.run(['python3', str(akce_kořen/'nástroje/Provést_Soubor.py'), str(Třída_cesta/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        VÝSLEDEK = dokončeno_částka.stdout.decode('utf-8').replace('\r\n', '\n')
        (výstup/'한국어가닥시험.log').write_text(VÝSLEDEK)
        assert dokončeno_částka.returncode == 0 and 'čeština 직접 vlákno_HODNOTA předat_HODNOTA\n' in VÝSLEDEK and '\nexit 0\n' in VÝSLEDEK, VÝSLEDEK
        ověření_Zpráva['direct_korean_thread_and_entry'] = True
        print('PASS: čeština 직접 vlákno_HODNOTA·Spustit·Spustit_2 vstupní_bod', flush=True)
        platný = (Třída_cesta / '객체시험.class').read_bytes()
        testovací_případ = [('판거부', platný[:6] + b'\x00\x35' + platný[8:], 'supported class versions'),
                 ('잘린클래스', platný[:24], 'truncated class file')]
        ověření_Zpráva['rejection_tests'] = []
        for Název, vytížení_data, povinnost_zvěřejnit_SMS in testovací_případ:
            test_data = výstup / (Název + '.class'); test_data.write_bytes(vytížení_data)
            dokončeno_částka = subprocess.run(['python3', str(akce_kořen / 'nástroje/Provést_Soubor.py'), str(test_data)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            text = dokončeno_částka.stdout.decode('utf-8').replace('\r\n', '\n')
            (výstup / (Název + '.log')).write_text(text, encoding='utf-8')
            assert dokončeno_částka.returncode == 1 and povinnost_zvěřejnit_SMS in text and 'exit 1\n' in text, (Název, text)
            ověření_Zpráva['rejection_tests'].append({'name': Název, 'passed': True})
            print('PASS (rejected):', Název, flush=True)
        ověření_Zpráva['passed'] = True
    finally:
        (výstup / 'report.json').write_text(json.dumps(ověření_Zpráva, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Spustit_2()
