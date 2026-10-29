#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 syöte_ARVO·RAM 되돌림을 oma 커널에서 검사한다."""
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
from 꾸러미중계 import nippu_säilö, purkaa_794097ae
from Suorita_komento import aloite_juuri


def testi_valintakiekko(Nimi, 파일들, sopimuksen_arvo='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as nippu:
        nippu.writestr(Nimi + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + sopimuksen_arvo)
        nippu.writestr(Nimi + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nimi + '\nVersion: 1.0\n' + 의존성)
        for polku_2, Sisältö_ARVO in 파일들.items():
            nippu.writestr(polku_2, Sisältö_ARVO)
    return data.getvalue()


def sekki_isäntä():
    tietojärjestelmät_normaali = testi_valintakiekko('jkoros-fixture', {'mod.py': 'ARVO=42\n'})
    assert purkaa_794097ae('jkoros_fixture-1.0-py3-none-any.whl', tietojärjestelmät_normaali, 'jkoros-fixture', '1.0') == {'mod.py': 'ARVO=42\n'.encode()}
    for data in (
            testi_valintakiekko('jkoros-fixture', {'../escape.py': ''}),
            testi_valintakiekko('jkoros-fixture', {'/abs.py': ''}),
            testi_valintakiekko('jkoros-fixture', {'big.py': 'x' * 16385}),
            testi_valintakiekko('jkoros-fixture', {'mod.so': ''}),
            testi_valintakiekko('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            testi_valintakiekko('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            purkaa_794097ae('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel polku_2·Koko·C tarkenne_ARVO·의존성 hylkää_ARVO_e3ecc00b')


def 빈접속번호():
    with socket.socket() as vastake_ARVO:
        vastake_ARVO.bind(('127.0.0.1', 0))
        return vastake_ARVO.getsockname()[1]


def Suorita_2():
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('--host-only', action='store_true')
    argumentit = jäsennin_48ee4b1b.parse_args()
    sekki_isäntä()
    if argumentit.host_only:
        return
    KR_polku = aloite_juuri/'build/verification/pip'
    KR_polku.mkdir(parents=True, exist_ok=True)
    Tallennus_polku = KR_polku/'cache'
    Tallennus_polku.mkdir(exist_ok=True)
    # todellinen_data PyPI jakelu_ARVO tiedoston_nimi. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    nippu_säilö(aloite_juuri/'build/pip-cache').Valmistele('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(aloite_juuri/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Tallennus_polku/('micropython-bisect==3.3.3'+꼬리)))
    laitteisto_LOG = json.loads((Tallennus_polku/'micropython-bisect==3.3.3.json').read_text())
    assert laitteisto_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nimi, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SEKUNNIT_operandi):\n return 가+SEKUNNIT_operandi\n'}),
            ('jkoros-space', {'space%d.py' % numero: 'ARVO=1\n' for numero in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = testi_valintakiekko(Nimi, 파일들)
        (Tallennus_polku/(Nimi+'==1.0.archive')).write_bytes(data)
        (Tallennus_polku/(Nimi+'==1.0.json')).write_text(json.dumps({'name': Nimi, 'version': '1.0',
            'filename': Nimi.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    vahvista = {'passed': False, 'kernel_sha256': hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': laitteisto_LOG, 'checks': []}
    portin_numero = 빈접속번호()
    Prosessi = subprocess.Popen(['python3', str(aloite_juuri/'työkalut/Suorita_komento.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(portin_numero), '--pip-cache', str(Tallennus_polku), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    valitsin_a916db4e = selectors.DefaultSelector()
    valitsin_a916db4e.register(Prosessi.stdout, selectors.EVENT_READ)
    transkriptio = bytearray()
    def 기다리기(näyttää_ARVO=b'jkoros-native> '):
        Sisältö_ARVO = bytearray()
        끝 = time.monotonic()+120
        while näyttää_ARVO not in Sisältö_ARVO:
            if time.monotonic() > 끝 or Prosessi.poll() is not None:
                raise AssertionError('게스트 palaute 없음: '+Sisältö_ARVO.decode('utf-8','replace'))
            for merkintä_ARVO_962f286b, _ in valitsin_a916db4e.select(.1):
                조각 = merkintä_ARVO_962f286b.fileobj.read(4096)
                Sisältö_ARVO.extend(조각)
                transkriptio.extend(조각)
        return Sisältö_ARVO.decode('utf-8', 'replace').replace('\r\n','\n')
    def liittymä(komento, näyttää_ARVO=b'jkoros-native> '):
        Prosessi.stdin.write(komento.encode()+b'\n')
        Prosessi.stdin.flush()
        return 기다리기(näyttää_ARVO)
    def Suorita_komento(komento, 예상, Tila_ARVO=0):
        Sisältö_ARVO = liittymä(komento)
        assert 예상 in Sisältö_ARVO and '\nexit '+str(Tila_ARVO)+'\n' in Sisältö_ARVO, Sisältö_ARVO
        vahvista['checks'].append(komento)
        return Sisältö_ARVO
    def Upload_Files(Nimi, data):
        liittymä('load '+Nimi, b'hex> ')
        for sijainti in range(0, len(data), 64):
            liittymä(data[sijainti:sijainti+64].hex(), b'hex> ')
        assert 'LOADED' in liittymä('.')
    try:
        기다리기()
        Suorita_komento('pip --help', 'MicroPython lähde_puu 설치기')
        Upload_Files('오류시험.py', (aloite_juuri/'testit/PYTHON/한국어오류시험.py').read_bytes())
        Suorita_komento('python 오류시험.py', 'suomi tiedoston_nimi poikkeus tarkistaa')
        Suorita_komento('pip install micropython-bisect==3.3.3 --port '+str(portin_numero), 'asentaa_ARVO 완료: micropython-bisect 3.3.3')
        Suorita_komento('python -c \'from bisect import insort as 순서대로넣기; ARVO=[1,5]; 순서대로넣기(ARVO,3); print(ARVO)\'', '[1, 3, 5]')
        Suorita_komento('python -m pip list', 'micropython-bisect 3.3.3')
        Suorita_komento('pip install micropython-bisect==3.3.3 --port '+str(portin_numero), '이미 설치됨:')
        Suorita_komento('pip install jkoros-fixture==1.0 --port '+str(portin_numero), 'asentaa_ARVO 완료: jkoros-fixture')
        Suorita_komento('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Suorita_komento('pip install jkoros-syntax==1.0 --port '+str(portin_numero), 'nippu VIRHE:', 1)
        Suorita_komento('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 VIRHE 보존")\'', '구문 VIRHE 보존')
        Upload_Files('공간시험.py', (aloite_juuri/'testit/PYTHON/nippu_nimitila_testi.py').read_bytes())
        Suorita_komento('python 공간시험.py '+str(portin_numero), 'nippu OSOITE_alue 부족 palauttaa_silta tarkistaa')
        Suorita_komento('pip uninstall jkoros-fixture', 'poistaa_merkintä 완료: jkoros-fixture')
        Suorita_komento('pip uninstall micropython-bisect', 'poistaa_merkintä 완료: micropython-bisect')
        Suorita_komento('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("poistaa_merkintä tarkistaa")\'', 'poistaa_merkintä tarkistaa')
        vahvista['passed'] = True
        print('PASS: PyPI 실물 asentaa_ARVO·import·Suorita_komento, suomi poikkeus, 패키지 Directory_ARVO, virhe_ARVO palauttaa_silta, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Lopeta_ohjelma 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Prosessi.stdin.write(b'\x01x')
            Prosessi.stdin.flush()
            Prosessi.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Prosessi.terminate()
            try:
                Prosessi.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Prosessi.kill()
                Prosessi.wait()
        if Prosessi.poll() is None:
            Prosessi.kill()
            Prosessi.wait()
        valitsin_a916db4e.close()
        Prosessi.stdin.close()
        Prosessi.stdout.close()
        (KR_polku/'serial.log').write_bytes(transkriptio)
        (KR_polku/'report.json').write_text(json.dumps(vahvista, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Suorita_2()
