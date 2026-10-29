#!/usr/bin/env python3
"""OpenJDK와 własny ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from Wykonaj_polecenie import Project_korzeń


def Uruchom_2():
    produkt_wyjściowy = Project_korzeń / 'build/verification/jvm'
    Klasa_ścieżka = produkt_wyjściowy / 'classes'; Klasa_ścieżka.mkdir(parents=True, exist_ok=True)
    자바꾸러미 = Project_korzeń / 'dist/jkoros-native-korean.jar'
    원문목록 = sorted((Project_korzeń / 'testy/자바').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(자바꾸러미), '-d', str(Klasa_ścieżka)] + [str(ciąg_dane) for ciąg_dane in 원문목록])
    lista_testów = [('객체시험', ['Tło_WARTOŚĆ', 'gałąź_WARTOŚĆ', '계산가능']), ('예외시험', []), ('Kolekcja_test', []),
             ('가닥시험', ['licznik_WARTOŚĆ', 'zadanie_akcja', 'wątek_WARTOŚĆ']), ('한글시험', []), ('test_Sieć', []), ('한국어통신시험', []), ('한국어예외시험', []), ('한글소스', []), ('경계시험', []), ('walidować.test_pakiet', []), ('wpis_zgodność_test', [])]
    walidacja_Raport = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(자바꾸러미.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Nazwa, 포함인수 in lista_testów:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 임시경로:
                예상결과 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(Klasa_ścieżka) + ':' + str(자바꾸러미), Nazwa], cwd=임시경로, timeout=15).decode('utf-8')
            명령인수 = ['python3', str(Project_korzeń / 'narzędzia/Wykonaj_Plik.py'), str(Klasa_ścieżka / (Nazwa.replace('.', '/') + '.class'))]
            if '.' in Nazwa: 명령인수 += ['--class-name', Nazwa]
            for 포함항목 in 포함인수: 명령인수 += ['--include', str(Klasa_ścieżka / (포함항목 + '.class'))]
            if Nazwa == '한글소스': 명령인수[2] = str(Project_korzeń / 'testy/자바/한글소스.java')
            Wykonane_ilość = subprocess.run(명령인수, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            rzeczywisty_KR = Wykonane_ilość.stdout.decode('utf-8').replace('\r\n', '\n')
            (produkt_wyjściowy / (Nazwa + '.log')).write_text(rzeczywisty_KR, encoding='utf-8')
            일치 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", rzeczywisty_KR, re.S)
            assert Wykonane_ilość.returncode == 0 and 일치, (Nazwa, rzeczywisty_KR)
            WYNIK = next(ciąg_dane for ciąg_dane in 일치.groups() if ciąg_dane is not None) + '\n'
            assert WYNIK == 예상결과, (Nazwa, 예상결과, WYNIK)
            walidacja_Raport['tests'].append({'name': Nazwa, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Nazwa, flush=True)
        # własny JVM에 직접 연결한 polski wątek_WARTOŚĆ/진입점은 OpenJDK용 래퍼가 아니다.
        Wykonane_ilość = subprocess.run(['python3', str(Project_korzeń/'narzędzia/Wykonaj_Plik.py'), str(Klasa_ścieżka/'한국어가닥시험.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        WYNIK = Wykonane_ilość.stdout.decode('utf-8').replace('\r\n', '\n')
        (produkt_wyjściowy/'한국어가닥시험.log').write_text(WYNIK)
        assert Wykonane_ilość.returncode == 0 and 'polski 직접 wątek_WARTOŚĆ przekazać_WARTOŚĆ\n' in WYNIK and '\nexit 0\n' in WYNIK, WYNIK
        walidacja_Raport['direct_korean_thread_and_entry'] = True
        print('PASS: polski 직접 wątek_WARTOŚĆ·Uruchom·Uruchom_2 punkt_wejścia', flush=True)
        prawidłowy = (Klasa_ścieżka / '객체시험.class').read_bytes()
        przypadek_testowy = [('판거부', prawidłowy[:6] + b'\x00\x35' + prawidłowy[8:], 'supported class versions'),
                 ('잘린클래스', prawidłowy[:24], 'truncated class file')]
        walidacja_Raport['rejection_tests'] = []
        for Nazwa, ładunek_dane, powiadomienie_SMS in przypadek_testowy:
            test_dane = produkt_wyjściowy / (Nazwa + '.class'); test_dane.write_bytes(ładunek_dane)
            Wykonane_ilość = subprocess.run(['python3', str(Project_korzeń / 'narzędzia/Wykonaj_Plik.py'), str(test_dane)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            tekst = Wykonane_ilość.stdout.decode('utf-8').replace('\r\n', '\n')
            (produkt_wyjściowy / (Nazwa + '.log')).write_text(tekst, encoding='utf-8')
            assert Wykonane_ilość.returncode == 1 and powiadomienie_SMS in tekst and 'exit 1\n' in tekst, (Nazwa, tekst)
            walidacja_Raport['rejection_tests'].append({'name': Nazwa, 'passed': True})
            print('PASS (rejected):', Nazwa, flush=True)
        walidacja_Raport['passed'] = True
    finally:
        (produkt_wyjściowy / 'report.json').write_text(json.dumps(walidacja_Raport, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Uruchom_2()
