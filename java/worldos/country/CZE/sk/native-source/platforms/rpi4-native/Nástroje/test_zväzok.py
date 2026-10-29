#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 vstup_VALUE·RAM 되돌림을 vlastné 커널에서 검사한다."""
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
from 꾸러미중계 import zväzok_odkladací_priestor, 압축풀기
from Vykonať_príkaz import akcia_koreň


def test_koliesko(Názov, 파일들, prípad_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    údaje = io.BytesIO()
    with zipfile.ZipFile(údaje, 'w', zipfile.ZIP_DEFLATED) as zväzok:
        zväzok.writestr(Názov + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + prípad_VALUE)
        zväzok.writestr(Názov + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Názov + '\nVersion: 1.0\n' + 의존성)
        for Cesta, obsah_VALUE in 파일들.items():
            zväzok.writestr(Cesta, obsah_VALUE)
    return údaje.getvalue()


def skontrolovať_hostiteľ():
    정상 = test_koliesko('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for údaje in (
            test_koliesko('jkoros-fixture', {'../escape.py': ''}),
            test_koliesko('jkoros-fixture', {'/abs.py': ''}),
            test_koliesko('jkoros-fixture', {'big.py': 'x' * 16385}),
            test_koliesko('jkoros-fixture', {'mod.so': ''}),
            test_koliesko('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            test_koliesko('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', údaje, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Cesta·Veľkosť·C prípona_VALUE·의존성 odmietnuť_VALUE')


def prázdny_číslo_portu():
    with socket.socket() as soket_VALUE:
        soket_VALUE.bind(('127.0.0.1', 0))
        return soket_VALUE.getsockname()[1]


def Spustiť_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    skontrolovať_hostiteľ()
    if Argumenty.host_only:
        return
    KR_cesta = akcia_koreň/'build/verification/pip'
    KR_cesta.mkdir(parents=True, exist_ok=True)
    Úložisko_cesta = KR_cesta/'cache'
    Úložisko_cesta.mkdir(exist_ok=True)
    # skutočný_údaje PyPI 배포 Súbor. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    zväzok_odkladací_priestor(akcia_koreň/'build/pip-cache').Pripraviť('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(akcia_koreň/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Úložisko_cesta/('micropython-bisect==3.3.3'+꼬리)))
    hardvér_LOG = json.loads((Úložisko_cesta/'micropython-bisect==3.3.3.json').read_text())
    assert hardvér_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Názov, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        údaje = test_koliesko(Názov, 파일들)
        (Úložisko_cesta/(Názov+'==1.0.archive')).write_bytes(údaje)
        (Úložisko_cesta/(Názov+'==1.0.json')).write_text(json.dumps({'name': Názov, 'version': '1.0',
            'filename': Názov.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(údaje).hexdigest()}))
    overiť_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardvér_LOG, 'checks': []}
    číslo_portu = prázdny_číslo_portu()
    Proces = subprocess.Popen(['python3', str(akcia_koreň/'Nástroje/Vykonať_príkaz.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(číslo_portu), '--pip-cache', str(Úložisko_cesta), '--ftp-port', str(prázdny_číslo_portu())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector()
    selektor_a916db4e.register(Proces.stdout, selectors.EVENT_READ)
    prepis = bytearray()
    def 기다리기(zobraziť_VALUE_487749b8=b'jkoros-native> '):
        obsah_VALUE = bytearray()
        끝 = time.monotonic()+120
        while zobraziť_VALUE_487749b8 not in obsah_VALUE:
            if time.monotonic() > 끝 or Proces.poll() is not None:
                raise AssertionError('게스트 odozva 없음: '+obsah_VALUE.decode('utf-8','replace'))
            for položka_VALUE, _ in selektor_a916db4e.select(.1):
                조각 = položka_VALUE.fileobj.read(4096)
                obsah_VALUE.extend(조각)
                prepis.extend(조각)
        return obsah_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def 셸(Príkaz, zobraziť_VALUE_487749b8=b'jkoros-native> '):
        Proces.stdin.write(Príkaz.encode()+b'\n')
        Proces.stdin.flush()
        return 기다리기(zobraziť_VALUE_487749b8)
    def Vykonať_príkaz(Príkaz, 예상, Stav_VALUE=0):
        obsah_VALUE = 셸(Príkaz)
        assert 예상 in obsah_VALUE and '\nexit '+str(Stav_VALUE)+'\n' in obsah_VALUE, obsah_VALUE
        overiť_5fb2b747['checks'].append(Príkaz)
        return obsah_VALUE
    def nahrať_Súbory(Názov, údaje):
        셸('load '+Názov, b'hex> ')
        for pozičný_index in range(0, len(údaje), 64):
            셸(údaje[pozičný_index:pozičný_index+64].hex(), b'hex> ')
        assert 'LOADED' in 셸('.')
    try:
        기다리기()
        Vykonať_príkaz('pip --help', 'MicroPython zdroj_strom 설치기')
        nahrať_Súbory('오류시험.py', (akcia_koreň/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Vykonať_príkaz('python 오류시험.py', 'Slovenský Súbor výnimka overiť')
        Vykonať_príkaz('pip install micropython-bisect==3.3.3 --port '+str(číslo_portu), 'inštalovať_VALUE 완료: micropython-bisect 3.3.3')
        Vykonať_príkaz('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Vykonať_príkaz('python -m pip list', 'micropython-bisect 3.3.3')
        Vykonať_príkaz('pip install micropython-bisect==3.3.3 --port '+str(číslo_portu), '이미 설치됨:')
        Vykonať_príkaz('pip install jkoros-fixture==1.0 --port '+str(číslo_portu), 'inštalovať_VALUE 완료: jkoros-fixture')
        Vykonať_príkaz('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Vykonať_príkaz('pip install jkoros-syntax==1.0 --port '+str(číslo_portu), 'zväzok chyba:', 1)
        Vykonať_príkaz('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 chyba 보존")\'', '구문 chyba 보존')
        nahrať_Súbory('공간시험.py', (akcia_koreň/'시험/PYTHON/zväzok_priestor_názvov_test.py').read_bytes())
        Vykonať_príkaz('python 공간시험.py '+str(číslo_portu), 'zväzok adresa_oblasť 부족 vrátiť_most overiť')
        Vykonať_príkaz('pip uninstall jkoros-fixture', 'odobrať_položka 완료: jkoros-fixture')
        Vykonať_príkaz('pip uninstall micropython-bisect', 'odobrať_položka 완료: micropython-bisect')
        Vykonať_príkaz('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("odobrať_položka overiť")\'', 'odobrať_položka overiť')
        overiť_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 inštalovať_VALUE·import·Vykonať_príkaz, Slovenský výnimka, 패키지 Adresár_VALUE, zlyhanie_VALUE vrátiť_most, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Skončiť_program 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        (KR_cesta/'serial.log').write_bytes(prepis)
        (KR_cesta/'report.json').write_text(json.dumps(overiť_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Spustiť_2()
