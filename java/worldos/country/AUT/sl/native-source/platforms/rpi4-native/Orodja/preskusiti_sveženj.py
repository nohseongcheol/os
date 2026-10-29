#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 lastno 커널에서 검사한다."""
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
from 꾸러미중계 import sveženj_shramba, razširiti
from Izvedi_ukaz import pobuda_koren


def preskusiti_kolesce(Ime, 파일들, primer_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    podatki = io.BytesIO()
    with zipfile.ZipFile(podatki, 'w', zipfile.ZIP_DEFLATED) as sveženj:
        sveženj.writestr(Ime + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + primer_VALUE)
        sveženj.writestr(Ime + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Ime + '\nVersion: 1.0\n' + 의존성)
        for POT, vsebina_VALUE in 파일들.items():
            sveženj.writestr(POT, vsebina_VALUE)
    return podatki.getvalue()


def preveriti_gostiti():
    정상 = preskusiti_kolesce('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert razširiti('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for podatki in (
            preskusiti_kolesce('jkoros-fixture', {'../escape.py': ''}),
            preskusiti_kolesce('jkoros-fixture', {'/abs.py': ''}),
            preskusiti_kolesce('jkoros-fixture', {'big.py': 'x' * 16385}),
            preskusiti_kolesce('jkoros-fixture', {'mod.so': ''}),
            preskusiti_kolesce('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            preskusiti_kolesce('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            razširiti('jkoros_fixture-1.0-py3-none-any.whl', podatki, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel POT·Velikost·C pripona_VALUE·의존성 zavrniti_VALUE')


def prazen_številka_vrat():
    with socket.socket() as vtičnica_VALUE:
        vtičnica_VALUE.bind(('127.0.0.1', 0))
        return vtičnica_VALUE.getsockname()[1]


def Zaženi():
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    preveriti_gostiti()
    if Argumenti.host_only:
        return
    KR_pot = pobuda_koren/'build/verification/pip'
    KR_pot.mkdir(parents=True, exist_ok=True)
    Senzor_prostora_pot = KR_pot/'cache'
    Senzor_prostora_pot.mkdir(exist_ok=True)
    # dejanski_podatki PyPI 배포 Datoteka. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    sveženj_shramba(pobuda_koren/'build/pip-cache').Pripravi('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(pobuda_koren/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Senzor_prostora_pot/('micropython-bisect==3.3.3'+꼬리)))
    strojna_oprema_LOG = json.loads((Senzor_prostora_pot/'micropython-bisect==3.3.3.json').read_text())
    assert strojna_oprema_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Ime, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        podatki = preskusiti_kolesce(Ime, 파일들)
        (Senzor_prostora_pot/(Ime+'==1.0.archive')).write_bytes(podatki)
        (Senzor_prostora_pot/(Ime+'==1.0.json')).write_text(json.dumps({'name': Ime, 'version': '1.0',
            'filename': Ime.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(podatki).hexdigest()}))
    preveriti_veljavnost = {'passed': False, 'kernel_sha256': hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': strojna_oprema_LOG, 'checks': []}
    številka_vrat = prazen_številka_vrat()
    Opravilo = subprocess.Popen(['python3', str(pobuda_koren/'Orodja/Izvedi_ukaz.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(številka_vrat), '--pip-cache', str(Senzor_prostora_pot), '--ftp-port', str(prazen_številka_vrat())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    izbirnik_a916db4e = selectors.DefaultSelector()
    izbirnik_a916db4e.register(Opravilo.stdout, selectors.EVENT_READ)
    prepis = bytearray()
    def 기다리기(oddaja_VALUE_487749b8=b'jkoros-native> '):
        vsebina_VALUE = bytearray()
        끝 = time.monotonic()+120
        while oddaja_VALUE_487749b8 not in vsebina_VALUE:
            if time.monotonic() > 끝 or Opravilo.poll() is not None:
                raise AssertionError('게스트 odgovor 없음: '+vsebina_VALUE.decode('utf-8','replace'))
            for vnos_VALUE, _ in izbirnik_a916db4e.select(.1):
                조각 = vnos_VALUE.fileobj.read(4096)
                vsebina_VALUE.extend(조각)
                prepis.extend(조각)
        return vsebina_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def lupina(Ukaz, oddaja_VALUE_487749b8=b'jkoros-native> '):
        Opravilo.stdin.write(Ukaz.encode()+b'\n')
        Opravilo.stdin.flush()
        return 기다리기(oddaja_VALUE_487749b8)
    def Izvedi_ukaz(Ukaz, 예상, stanje_VALUE=0):
        vsebina_VALUE = lupina(Ukaz)
        assert 예상 in vsebina_VALUE and '\nexit '+str(stanje_VALUE)+'\n' in vsebina_VALUE, vsebina_VALUE
        preveriti_veljavnost['checks'].append(Ukaz)
        return vsebina_VALUE
    def Upload_Datoteke(Ime, podatki):
        lupina('load '+Ime, b'hex> ')
        for kazalec_mesta in range(0, len(podatki), 64):
            lupina(podatki[kazalec_mesta:kazalec_mesta+64].hex(), b'hex> ')
        assert 'LOADED' in lupina('.')
    try:
        기다리기()
        Izvedi_ukaz('pip --help', 'MicroPython vir_drevo 설치기')
        Upload_Datoteke('오류시험.py', (pobuda_koren/'시험/PYTHON/한국어오류시험.py').read_bytes())
        Izvedi_ukaz('python 오류시험.py', 'slovenščina Datoteka izjema 확인')
        Izvedi_ukaz('pip install micropython-bisect==3.3.3 --port '+str(številka_vrat), 'namesti_VALUE 완료: micropython-bisect 3.3.3')
        Izvedi_ukaz('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Izvedi_ukaz('python -m pip list', 'micropython-bisect 3.3.3')
        Izvedi_ukaz('pip install micropython-bisect==3.3.3 --port '+str(številka_vrat), '이미 설치됨:')
        Izvedi_ukaz('pip install jkoros-fixture==1.0 --port '+str(številka_vrat), 'namesti_VALUE 완료: jkoros-fixture')
        Izvedi_ukaz('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Izvedi_ukaz('pip install jkoros-syntax==1.0 --port '+str(številka_vrat), 'sveženj NAPAKA:', 1)
        Izvedi_ukaz('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 NAPAKA 보존")\'', '구문 NAPAKA 보존')
        Upload_Datoteke('공간시험.py', (pobuda_koren/'시험/PYTHON/sveženj_imenski_prostor_preskusiti.py').read_bytes())
        Izvedi_ukaz('python 공간시험.py '+str(številka_vrat), 'sveženj naslov_območje 부족 vrni_most 확인')
        Izvedi_ukaz('pip uninstall jkoros-fixture', 'odstraniti_vnos 완료: jkoros-fixture')
        Izvedi_ukaz('pip uninstall micropython-bisect', 'odstraniti_vnos 완료: micropython-bisect')
        Izvedi_ukaz('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("odstraniti_vnos 확인")\'', 'odstraniti_vnos 확인')
        preveriti_veljavnost['passed'] = True
        print('PASS: PyPI 실물 namesti_VALUE·import·Izvedi_ukaz, slovenščina izjema, 패키지 Imenik_VALUE, napaka_VALUE vrni_most, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Izhod_aplikacija 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Opravilo.stdin.write(b'\x01x')
            Opravilo.stdin.flush()
            Opravilo.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Opravilo.terminate()
            try:
                Opravilo.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Opravilo.kill()
                Opravilo.wait()
        if Opravilo.poll() is None:
            Opravilo.kill()
            Opravilo.wait()
        izbirnik_a916db4e.close()
        Opravilo.stdin.close()
        Opravilo.stdout.close()
        (KR_pot/'serial.log').write_bytes(prepis)
        (KR_pot/'report.json').write_text(json.dumps(preveriti_veljavnost, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Zaženi()
