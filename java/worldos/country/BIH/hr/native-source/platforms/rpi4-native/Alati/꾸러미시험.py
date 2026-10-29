#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 vlastiti 커널에서 검사한다."""
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
from 꾸러미중계 import komplet_spremište, dekomprimirati
from Izvrši_naredba import akcija_korijen


def 시험휠(Ime, 파일들, slučaj_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    podaci = io.BytesIO()
    with zipfile.ZipFile(podaci, 'w', zipfile.ZIP_DEFLATED) as komplet:
        komplet.writestr(Ime + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + slučaj_VALUE)
        komplet.writestr(Ime + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ime + '\nVersion: 1.0\n' + 의존성)
        for PUTANJA, Sadržaj_VALUE in 파일들.items():
            komplet.writestr(PUTANJA, Sadržaj_VALUE)
    return podaci.getvalue()


def 호스트검사():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert dekomprimirati('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for podaci in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            dekomprimirati('jkoros_fixture-1.0-py3-none-any.whl', podaci, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel PUTANJA·Veličina·C nastavak_VALUE·의존성 odbiti_VALUE')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Pokreni():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumenti = analizator_48ee4b1b.parse_args()
    호스트검사()
    if Argumenti.host_only:
        return
    KR_put = akcija_korijen/'build/verification/pip'
    KR_put.mkdir(parents=True, exist_ok=True)
    Pohrana_put = KR_put/'cache'
    Pohrana_put.mkdir(exist_ok=True)
    # stvaran_podaci PyPI 배포 Datoteka. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    komplet_spremište(akcija_korijen/'build/pip-cache').Pripremi('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(akcija_korijen/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Pohrana_put/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Pohrana_put/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ime, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        podaci = 시험휠(Ime, 파일들)
        (Pohrana_put/(Ime+'==1.0.archive')).write_bytes(podaci)
        (Pohrana_put/(Ime+'==1.0.json')).write_text(json.dumps({'name': Ime, 'version': '1.0',
            'filename': Ime.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(podaci).hexdigest()}))
    potvrditi = {'passed': False, 'kernel_sha256': hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    broj_priključka = 빈접속번호()
    Proces = subprocess.Popen(['python3', str(akcija_korijen/'Alati/Izvrši_naredba.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(broj_priključka), '--pip-cache', str(Pohrana_put), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    odabirač_a916db4e = selectors.DefaultSelector()
    odabirač_a916db4e.register(Proces.stdout, selectors.EVENT_READ)
    transkript = bytearray()
    def 기다리기(emisija_VALUE=b'jkoros-native> '):
        Sadržaj_VALUE = bytearray()
        끝 = time.monotonic()+120
        while emisija_VALUE not in Sadržaj_VALUE:
            if time.monotonic() > 끝 or Proces.poll() is not None:
                raise AssertionError('게스트 odgovor 없음: '+Sadržaj_VALUE.decode('utf-8','replace'))
            for unos_VALUE, _ in odabirač_a916db4e.select(.1):
                fragment_VALUE = unos_VALUE.fileobj.read(4096)
                Sadržaj_VALUE.extend(fragment_VALUE)
                transkript.extend(fragment_VALUE)
        return Sadržaj_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def ljuska(Naredba, emisija_VALUE=b'jkoros-native> '):
        Proces.stdin.write(Naredba.encode()+b'\n')
        Proces.stdin.flush()
        return 기다리기(emisija_VALUE)
    def Izvrši_naredba(Naredba, 예상, Stanje_VALUE=0):
        Sadržaj_VALUE = ljuska(Naredba)
        assert 예상 in Sadržaj_VALUE and '\nexit '+str(Stanje_VALUE)+'\n' in Sadržaj_VALUE, Sadržaj_VALUE
        potvrditi['checks'].append(Naredba)
        return Sadržaj_VALUE
    def Prijenos_Datoteke(Ime, podaci):
        ljuska('load '+Ime, b'hex> ')
        for indeks_položaja in range(0, len(podaci), 64):
            ljuska(podaci[indeks_položaja:indeks_položaja+64].hex(), b'hex> ')
        assert 'LOADED' in ljuska('.')
    try:
        기다리기()
        Izvrši_naredba('pip --help', 'MicroPython izvor_stablo 설치기')
        Prijenos_Datoteke('오류시험.py', (akcija_korijen/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Izvrši_naredba('python 오류시험.py', 'hrvatski Datoteka iznimka provjeriti')
        Izvrši_naredba('pip install micropython-bisect==3.3.3 --port '+str(broj_priključka), 'instaliraj_VALUE 완료: micropython-bisect 3.3.3')
        Izvrši_naredba('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Izvrši_naredba('python -m pip list', 'micropython-bisect 3.3.3')
        Izvrši_naredba('pip install micropython-bisect==3.3.3 --port '+str(broj_priključka), '이미 설치됨:')
        Izvrši_naredba('pip install jkoros-fixture==1.0 --port '+str(broj_priključka), 'instaliraj_VALUE 완료: jkoros-fixture')
        Izvrši_naredba('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Izvrši_naredba('pip install jkoros-syntax==1.0 --port '+str(broj_priključka), 'komplet GREŠKA:', 1)
        Izvrši_naredba('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 GREŠKA 보존")\'', '구문 GREŠKA 보존')
        Prijenos_Datoteke('공간시험.py', (akcija_korijen/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Izvrši_naredba('python 공간시험.py '+str(broj_priključka), 'komplet adresa_regije 부족 vratiti_most provjeriti')
        Izvrši_naredba('pip uninstall jkoros-fixture', 'ukloniti_unos 완료: jkoros-fixture')
        Izvrši_naredba('pip uninstall micropython-bisect', 'ukloniti_unos 완료: micropython-bisect')
        Izvrši_naredba('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ukloniti_unos provjeriti")\'', 'ukloniti_unos provjeriti')
        potvrditi['passed'] = True
        print('PASS: PyPI 실물 instaliraj_VALUE·import·Izvrši_naredba, hrvatski iznimka, 패키지 imenik_VALUE, kvar_VALUE vratiti_most, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Izlaz_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        odabirač_a916db4e.close()
        Proces.stdin.close()
        Proces.stdout.close()
        (KR_put/'serial.log').write_bytes(transkript)
        (KR_put/'report.json').write_text(json.dumps(potvrditi, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Pokreni()
