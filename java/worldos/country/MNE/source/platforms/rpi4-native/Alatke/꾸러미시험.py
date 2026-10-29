#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 자체 커널에서 검사한다."""
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
from 꾸러미중계 import komplet_depo, 압축풀기
from Izvrši_komanda import radnja_koren


def 시험휠(ime, 파일들, ugovor_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    podaci = io.BytesIO()
    with zipfile.ZipFile(podaci, 'w', zipfile.ZIP_DEFLATED) as komplet:
        komplet.writestr(ime + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ugovor_VALUE)
        komplet.writestr(ime + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ime + '\nVersion: 1.0\n' + 의존성)
        for putanja, Sadržaj_VALUE in 파일들.items():
            komplet.writestr(putanja, Sadržaj_VALUE)
    return podaci.getvalue()


def proveriti_host():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for podaci in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', podaci, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel putanja·promeniti_veličinu·C ekstenzija_VALUE·의존성 odbaciti_VALUE_e3ecc00b')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def koristiti():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = analizator_48ee4b1b.parse_args()
    proveriti_host()
    if 인수.host_only:
        return
    KR_putanja = radnja_koren/'build/verification/pip'
    KR_putanja.mkdir(parents=True, exist_ok=True)
    Skladište_putanja = KR_putanja/'cache'
    Skladište_putanja.mkdir(exist_ok=True)
    # stvarni_podaci PyPI 배포 Datoteka. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    komplet_depo(radnja_koren/'build/pip-cache').Pripremi('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(radnja_koren/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Skladište_putanja/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Skladište_putanja/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ime, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        podaci = 시험휠(ime, 파일들)
        (Skladište_putanja/(ime+'==1.0.archive')).write_bytes(podaci)
        (Skladište_putanja/(ime+'==1.0.json')).write_text(json.dumps({'name': ime, 'version': '1.0',
            'filename': ime.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(podaci).hexdigest()}))
    potvrditi = {'passed': False, 'kernel_sha256': hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    broj_porta = 빈접속번호()
    Proces = subprocess.Popen(['python3', str(radnja_koren/'Alatke/Izvrši_komanda.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(broj_porta), '--pip-cache', str(Skladište_putanja), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač_a916db4e = selectors.DefaultSelector()
    birač_a916db4e.register(Proces.stdout, selectors.EVENT_READ)
    transkript = bytearray()
    def 기다리기(emisija_VALUE=b'jkoros-native> '):
        Sadržaj_VALUE = bytearray()
        끝 = time.monotonic()+120
        while emisija_VALUE not in Sadržaj_VALUE:
            if time.monotonic() > 끝 or Proces.poll() is not None:
                raise AssertionError('게스트 odgovor 없음: '+Sadržaj_VALUE.decode('utf-8','replace'))
            for stavka_VALUE, _ in birač_a916db4e.select(.1):
                조각 = stavka_VALUE.fileobj.read(4096)
                Sadržaj_VALUE.extend(조각)
                transkript.extend(조각)
        return Sadržaj_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def ljuska(komanda, emisija_VALUE=b'jkoros-native> '):
        Proces.stdin.write(komanda.encode()+b'\n')
        Proces.stdin.flush()
        return 기다리기(emisija_VALUE)
    def Izvrši_komanda(komanda, 예상, Status_VALUE=0):
        Sadržaj_VALUE = ljuska(komanda)
        assert 예상 in Sadržaj_VALUE and '\nexit '+str(Status_VALUE)+'\n' in Sadržaj_VALUE, Sadržaj_VALUE
        potvrditi['checks'].append(komanda)
        return Sadržaj_VALUE
    def Otprema_Datoteke(ime, podaci):
        ljuska('load '+ime, b'hex> ')
        for indeks_pozicije in range(0, len(podaci), 64):
            ljuska(podaci[indeks_pozicije:indeks_pozicije+64].hex(), b'hex> ')
        assert 'LOADED' in ljuska('.')
    try:
        기다리기()
        Izvrši_komanda('pip --help', 'MicroPython izvor_stablo 설치기')
        Otprema_Datoteke('오류시험.py', (radnja_koren/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Izvrši_komanda('python 오류시험.py', '한국어 Datoteka izuzetak verifikovati')
        Izvrši_komanda('pip install micropython-bisect==3.3.3 --port '+str(broj_porta), 'instaliraj_VALUE 완료: micropython-bisect 3.3.3')
        Izvrši_komanda('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Izvrši_komanda('python -m pip list', 'micropython-bisect 3.3.3')
        Izvrši_komanda('pip install micropython-bisect==3.3.3 --port '+str(broj_porta), '이미 설치됨:')
        Izvrši_komanda('pip install jkoros-fixture==1.0 --port '+str(broj_porta), 'instaliraj_VALUE 완료: jkoros-fixture')
        Izvrši_komanda('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Izvrši_komanda('pip install jkoros-syntax==1.0 --port '+str(broj_porta), 'komplet greška:', 1)
        Izvrši_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 greška 보존")\'', '구문 greška 보존')
        Otprema_Datoteke('공간시험.py', (radnja_koren/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Izvrši_komanda('python 공간시험.py '+str(broj_porta), 'komplet adresa_oblast 부족 vratiti_most verifikovati')
        Izvrši_komanda('pip uninstall jkoros-fixture', 'ukloniti_stavka 완료: jkoros-fixture')
        Izvrši_komanda('pip uninstall micropython-bisect', 'ukloniti_stavka 완료: micropython-bisect')
        Izvrši_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ukloniti_stavka verifikovati")\'', 'ukloniti_stavka verifikovati')
        potvrditi['passed'] = True
        print('PASS: PyPI 실물 instaliraj_VALUE·import·Izvrši_komanda, 한국어 izuzetak, 패키지 Imenik_VALUE, otkazivanje_VALUE vratiti_most, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Izađi_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        birač_a916db4e.close()
        Proces.stdin.close()
        Proces.stdout.close()
        (KR_putanja/'serial.log').write_bytes(transkript)
        (KR_putanja/'report.json').write_text(json.dumps(potvrditi, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    koristiti()
