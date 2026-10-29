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
from 꾸러미중계 import 꾸러미저장소, 압축풀기
from Izvrši_komanda import projicirati_koijen


def 시험휠(Naziv, 파일들, slučaj_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    podaci = io.BytesIO()
    with zipfile.ZipFile(podaci, 'w', zipfile.ZIP_DEFLATED) as paket:
        paket.writestr(Naziv + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + slučaj_VALUE)
        paket.writestr(Naziv + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Naziv + '\nVersion: 1.0\n' + 의존성)
        for Putanja, Sadržaj_VALUE in 파일들.items():
            paket.writestr(Putanja, Sadržaj_VALUE)
    return podaci.getvalue()


def ček_organizator():
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
    print('PASS: wheel Putanja·Veličina·C ekstenzija_VALUE·의존성 odbiti_VALUE')


def prazno_broj_priključka():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Pokreni():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    Argumenti = 해석기.parse_args()
    ček_organizator()
    if Argumenti.host_only:
        return
    mjera_put = projicirati_koijen/'build/verification/pip'
    mjera_put.mkdir(parents=True, exist_ok=True)
    Pohrana_put = mjera_put/'cache'
    Pohrana_put.mkdir(exist_ok=True)
    # stvaran_podaci PyPI 배포 Fajl. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(projicirati_koijen/'build/pip-cache').Pripremiti('micropython-bisect==3.3.3')
    for rep_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(projicirati_koijen/'build/pip-cache'/('micropython-bisect==3.3.3'+rep_VALUE)), str(Pohrana_put/('micropython-bisect==3.3.3'+rep_VALUE)))
    hardver_LOG = json.loads((Pohrana_put/'micropython-bisect==3.3.3.json').read_text())
    assert hardver_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Naziv, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        podaci = 시험휠(Naziv, 파일들)
        (Pohrana_put/(Naziv+'==1.0.archive')).write_bytes(podaci)
        (Pohrana_put/(Naziv+'==1.0.json')).write_text(json.dumps({'name': Naziv, 'version': '1.0',
            'filename': Naziv.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(podaci).hexdigest()}))
    ovjeriti = {'passed': False, 'kernel_sha256': hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardver_LOG, 'checks': []}
    broj_priključka = prazno_broj_priključka()
    proces = subprocess.Popen(['python3', str(projicirati_koijen/'Alati/Izvrši_komanda.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(broj_priključka), '--pip-cache', str(Pohrana_put), '--ftp-port', str(prazno_broj_priključka())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    birač_a916db4e = selectors.DefaultSelector()
    birač_a916db4e.register(proces.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(program_VALUE=b'jkoros-native> '):
        Sadržaj_VALUE = bytearray()
        끝 = time.monotonic()+120
        while program_VALUE not in Sadržaj_VALUE:
            if time.monotonic() > 끝 or proces.poll() is not None:
                raise AssertionError('게스트 odgovoriti 없음: '+Sadržaj_VALUE.decode('utf-8','replace'))
            for unos_VALUE, _ in birač_a916db4e.select(.1):
                조각 = unos_VALUE.fileobj.read(4096)
                Sadržaj_VALUE.extend(조각)
                대화기록.extend(조각)
        return Sadržaj_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def ljuska(Naredba, program_VALUE=b'jkoros-native> '):
        proces.stdin.write(Naredba.encode()+b'\n')
        proces.stdin.flush()
        return 기다리기(program_VALUE)
    def Izvrši_komanda(Naredba, 예상, stanje_VALUE=0):
        Sadržaj_VALUE = ljuska(Naredba)
        assert 예상 in Sadržaj_VALUE and '\nexit '+str(stanje_VALUE)+'\n' in Sadržaj_VALUE, Sadržaj_VALUE
        ovjeriti['checks'].append(Naredba)
        return Sadržaj_VALUE
    def Upload_Fajlovi(Naziv, podaci):
        ljuska('load '+Naziv, b'hex> ')
        for položaj_INDEX in range(0, len(podaci), 64):
            ljuska(podaci[položaj_INDEX:položaj_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in ljuska('.')
    try:
        기다리기()
        Izvrši_komanda('pip --help', 'MicroPython izvor_stablo 설치기')
        Upload_Fajlovi('오류시험.py', (projicirati_koijen/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Izvrši_komanda('python 오류시험.py', '한국어 Fajl izuzetak potvrditi')
        Izvrši_komanda('pip install micropython-bisect==3.3.3 --port '+str(broj_priključka), 'instalirati_VALUE 완료: micropython-bisect 3.3.3')
        Izvrši_komanda('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Izvrši_komanda('python -m pip list', 'micropython-bisect 3.3.3')
        Izvrši_komanda('pip install micropython-bisect==3.3.3 --port '+str(broj_priključka), '이미 설치됨:')
        Izvrši_komanda('pip install jkoros-fixture==1.0 --port '+str(broj_priključka), 'instalirati_VALUE 완료: jkoros-fixture')
        Izvrši_komanda('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Izvrši_komanda('pip install jkoros-syntax==1.0 --port '+str(broj_priključka), 'paket GRESKA:', 1)
        Izvrši_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 GRESKA 보존")\'', '구문 GRESKA 보존')
        Upload_Fajlovi('공간시험.py', (projicirati_koijen/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        Izvrši_komanda('python 공간시험.py '+str(broj_priključka), 'paket 공간 부족 vratiti_most potvrditi')
        Izvrši_komanda('pip uninstall jkoros-fixture', 'ukloniti_unos 완료: jkoros-fixture')
        Izvrši_komanda('pip uninstall micropython-bisect', 'ukloniti_unos 완료: micropython-bisect')
        Izvrši_komanda('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ukloniti_unos potvrditi")\'', 'ukloniti_unos potvrditi')
        ovjeriti['passed'] = True
        print('PASS: PyPI 실물 instalirati_VALUE·import·Izvrši_komanda, 한국어 izuzetak, 패키지 Direktorij_VALUE, neuspjeh_VALUE vratiti_most, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 izaći_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            proces.stdin.write(b'\x01x')
            proces.stdin.flush()
            proces.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            proces.terminate()
            try:
                proces.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proces.kill()
                proces.wait()
        if proces.poll() is None:
            proces.kill()
            proces.wait()
        birač_a916db4e.close()
        proces.stdin.close()
        proces.stdout.close()
        (mjera_put/'serial.log').write_bytes(대화기록)
        (mjera_put/'report.json').write_text(json.dumps(ovjeriti, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Pokreni()
