#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 wejście_WARTOŚĆ·RAM 되돌림을 własny 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from pakiet_Przekazywanie import pakiet_repozytorium, dekompresować
from Wykonaj_polecenie import Project_korzeń


def test_pokrętło(Nazwa, 파일들, wartość_kontraktu='Root-Is-Purelib: true\n', 의존성=''):
    dane = io.BytesIO()
    with zipfile.ZipFile(dane, 'w', zipfile.ZIP_DEFLATED) as pakiet:
        pakiet.writestr(Nazwa + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + wartość_kontraktu)
        pakiet.writestr(Nazwa + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nazwa + '\nVersion: 1.0\n' + 의존성)
        for ścieżka_2, treść_WARTOŚĆ_cb0f2404 in 파일들.items():
            pakiet.writestr(ścieżka_2, treść_WARTOŚĆ_cb0f2404)
    return dane.getvalue()


def czek_host():
    systemy_informacyjne_zwykła = test_pokrętło('jkoros-fixture', {'mod.py': 'WARTOŚĆ=42\n'})
    assert dekompresować('jkoros_fixture-1.0-py3-none-any.whl', systemy_informacyjne_zwykła, 'jkoros-fixture', '1.0') == {'mod.py': 'WARTOŚĆ=42\n'.encode()}
    for dane in (
            test_pokrętło('jkoros-fixture', {'../escape.py': ''}),
            test_pokrętło('jkoros-fixture', {'/abs.py': ''}),
            test_pokrętło('jkoros-fixture', {'big.py': 'x' * 16385}),
            test_pokrętło('jkoros-fixture', {'mod.so': ''}),
            test_pokrętło('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            test_pokrętło('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            dekompresować('jkoros_fixture-1.0-py3-none-any.whl', dane, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ścieżka_2·Rozmiar·C rozszerzenie_WARTOŚĆ·의존성 odrzucić_WARTOŚĆ')


def 빈접속번호():
    with socket.socket() as gniazdo_WARTOŚĆ:
        gniazdo_WARTOŚĆ.bind(('127.0.0.1', 0))
        return gniazdo_WARTOŚĆ.getsockname()[1]


def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    argumenty = parser_48ee4b1b.parse_args()
    czek_host()
    if argumenty.host_only:
        return
    KR_ścieżka = Project_korzeń/'build/verification/pip'
    KR_ścieżka.mkdir(parents=True, exist_ok=True)
    Pamięć_ścieżka = KR_ścieżka/'cache'
    Pamięć_ścieżka.mkdir(exist_ok=True)
    # rzeczywisty_dane PyPI dystrybucja_WARTOŚĆ nazwa_pliku. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    pakiet_repozytorium(Project_korzeń/'build/pip-cache').Przygotuj('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_korzeń/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Pamięć_ścieżka/('micropython-bisect==3.3.3'+꼬리)))
    sprzęt_LOG = json.loads((Pamięć_ścieżka/'micropython-bisect==3.3.3.json').read_text())
    assert sprzęt_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nazwa, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SEKUNDA_operand):\n return 가+SEKUNDA_operand\n'}),
            ('jkoros-space', {'space%d.py' % identyfikator: 'WARTOŚĆ=1\n' for identyfikator in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        dane = test_pokrętło(Nazwa, 파일들)
        (Pamięć_ścieżka/(Nazwa+'==1.0.archive')).write_bytes(dane)
        (Pamięć_ścieżka/(Nazwa+'==1.0.json')).write_text(json.dumps({'name': Nazwa, 'version': '1.0',
            'filename': Nazwa.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(dane).hexdigest()}))
    walidować = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': sprzęt_LOG, 'checks': []}
    numer_portu = 빈접속번호()
    Proces = subprocess.Popen(['python3', str(Project_korzeń/'narzędzia/Wykonaj_polecenie.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(numer_portu), '--pip-cache', str(Pamięć_ścieżka), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector()
    selektor_a916db4e.register(Proces.stdout, selectors.EVENT_READ)
    transkrypcja = bytearray()
    def 기다리기(program_WARTOŚĆ=b'jkoros-native> '):
        treść_WARTOŚĆ_cb0f2404 = bytearray()
        끝 = time.monotonic()+120
        while program_WARTOŚĆ not in treść_WARTOŚĆ_cb0f2404:
            if time.monotonic() > 끝 or Proces.poll() is not None:
                raise AssertionError('게스트 odpowiedź 없음: '+treść_WARTOŚĆ_cb0f2404.decode('utf-8','replace'))
            for wpis_WARTOŚĆ, _ in selektor_a916db4e.select(.1):
                fragment_WARTOŚĆ_652d4b53 = wpis_WARTOŚĆ.fileobj.read(4096)
                treść_WARTOŚĆ_cb0f2404.extend(fragment_WARTOŚĆ_652d4b53)
                transkrypcja.extend(fragment_WARTOŚĆ_652d4b53)
        return treść_WARTOŚĆ_cb0f2404.decode('utf-8', 'replace').replace('\r\n','\n')
    def powłoka(polecenie, program_WARTOŚĆ=b'jkoros-native> '):
        Proces.stdin.write(polecenie.encode()+b'\n')
        Proces.stdin.flush()
        return 기다리기(program_WARTOŚĆ)
    def Wykonaj_polecenie(polecenie, 예상, Stan_WARTOŚĆ=0):
        treść_WARTOŚĆ_cb0f2404 = powłoka(polecenie)
        assert 예상 in treść_WARTOŚĆ_cb0f2404 and '\nexit '+str(Stan_WARTOŚĆ)+'\n' in treść_WARTOŚĆ_cb0f2404, treść_WARTOŚĆ_cb0f2404
        walidować['checks'].append(polecenie)
        return treść_WARTOŚĆ_cb0f2404
    def Upload_Files(Nazwa, dane):
        powłoka('load '+Nazwa, b'hex> ')
        for indeks_pozycji in range(0, len(dane), 64):
            powłoka(dane[indeks_pozycji:indeks_pozycji+64].hex(), b'hex> ')
        assert 'LOADED' in powłoka('.')
    try:
        기다리기()
        Wykonaj_polecenie('pip --help', 'MicroPython źródło_drzewo 설치기')
        Upload_Files('오류시험.py', (Project_korzeń/'testy/PYTHON/한국어오류시험.py').read_bytes())
        Wykonaj_polecenie('python 오류시험.py', 'polski nazwa_pliku wyjątek 확인')
        Wykonaj_polecenie('pip install micropython-bisect==3.3.3 --port '+str(numer_portu), 'instalować_WARTOŚĆ 완료: micropython-bisect 3.3.3')
        Wykonaj_polecenie('python -c \'from bisect import insort as 순서대로넣기; WARTOŚĆ=[1,5]; 순서대로넣기(WARTOŚĆ,3); print(WARTOŚĆ)\'', '[1, 3, 5]')
        Wykonaj_polecenie('python -m pip list', 'micropython-bisect 3.3.3')
        Wykonaj_polecenie('pip install micropython-bisect==3.3.3 --port '+str(numer_portu), '이미 설치됨:')
        Wykonaj_polecenie('pip install jkoros-fixture==1.0 --port '+str(numer_portu), 'instalować_WARTOŚĆ 완료: jkoros-fixture')
        Wykonaj_polecenie('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Wykonaj_polecenie('pip install jkoros-syntax==1.0 --port '+str(numer_portu), 'pakiet błąd:', 1)
        Wykonaj_polecenie('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 błąd 보존")\'', '구문 błąd 보존')
        Upload_Files('공간시험.py', (Project_korzeń/'testy/PYTHON/pakiet_obszar_nazw_test.py').read_bytes())
        Wykonaj_polecenie('python 공간시험.py '+str(numer_portu), 'pakiet ADRES_region 부족 Zwrot_mostek 확인')
        Wykonaj_polecenie('pip uninstall jkoros-fixture', 'usuń_wpis 완료: jkoros-fixture')
        Wykonaj_polecenie('pip uninstall micropython-bisect', 'usuń_wpis 완료: micropython-bisect')
        Wykonaj_polecenie('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("usuń_wpis 확인")\'', 'usuń_wpis 확인')
        walidować['passed'] = True
        print('PASS: PyPI 실물 instalować_WARTOŚĆ·import·Wykonaj_polecenie, polski wyjątek, 패키지 Katalog_WARTOŚĆ, awaria_WARTOŚĆ Zwrot_mostek, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 wyjść_program 키로 QEMU를 끝내면 실행기의 Przekazywanie_WARTOŚĆ 문맥도 정리된다.
            Proces.stdin.write(b'\x01x')
            Proces.stdin.flush()
            Proces.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proces.terminate()
            try:
                Proces.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proces.kill()
                Proces.wait()
        if Proces.poll() is None:
            Proces.kill()
            Proces.wait()
        selektor_a916db4e.close()
        Proces.stdin.close()
        Proces.stdout.close()
        (KR_ścieżka/'serial.log').write_bytes(transkrypcja)
        (KR_ścieżka/'report.json').write_text(json.dumps(walidować, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Uruchom_2()
