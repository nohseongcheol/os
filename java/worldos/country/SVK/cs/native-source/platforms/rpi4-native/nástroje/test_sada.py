#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 vstup_HODNOTA·RAM 되돌림을 vlastní 커널에서 검사한다."""
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
from sada_Přenos import sada_úložiště, dekomprimovat
from Provést_příkaz import akce_kořen


def test_kolečko(Název, 파일들, hodnota_smlouvy='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as sada:
        sada.writestr(Název + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + hodnota_smlouvy)
        sada.writestr(Název + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Název + '\nVersion: 1.0\n' + 의존성)
        for cesta_2, Obsah_HODNOTA in 파일들.items():
            sada.writestr(cesta_2, Obsah_HODNOTA)
    return data.getvalue()


def šek_hostit():
    informační_systémy_normální = test_kolečko('jkoros-fixture', {'mod.py': 'HODNOTA=42\n'})
    assert dekomprimovat('jkoros_fixture-1.0-py3-none-any.whl', informační_systémy_normální, 'jkoros-fixture', '1.0') == {'mod.py': 'HODNOTA=42\n'.encode()}
    for data in (
            test_kolečko('jkoros-fixture', {'../escape.py': ''}),
            test_kolečko('jkoros-fixture', {'/abs.py': ''}),
            test_kolečko('jkoros-fixture', {'big.py': 'x' * 16385}),
            test_kolečko('jkoros-fixture', {'mod.so': ''}),
            test_kolečko('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            test_kolečko('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            dekomprimovat('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel cesta_2·Velikost·C přípona_HODNOTA·의존성 odmítnout_HODNOTA')


def 빈접속번호():
    with socket.socket() as soket_HODNOTA:
        soket_HODNOTA.bind(('127.0.0.1', 0))
        return soket_HODNOTA.getsockname()[1]


def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--host-only', action='store_true')
    argumenty = analyzátor_48ee4b1b.parse_args()
    šek_hostit()
    if argumenty.host_only:
        return
    KV_cesta = akce_kořen/'build/verification/pip'
    KV_cesta.mkdir(parents=True, exist_ok=True)
    Storage_cesta = KV_cesta/'cache'
    Storage_cesta.mkdir(exist_ok=True)
    # skutečný_data PyPI distribuce_HODNOTA název_souboru. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    sada_úložiště(akce_kořen/'build/pip-cache').Připravit('micropython-bisect==3.3.3')
    for chvost_HODNOTA in ('.archive', '.json'):
        shutil.copyfile(str(akce_kořen/'build/pip-cache'/('micropython-bisect==3.3.3'+chvost_HODNOTA)), str(Storage_cesta/('micropython-bisect==3.3.3'+chvost_HODNOTA)))
    hardware_LOGZ = json.loads((Storage_cesta/'micropython-bisect==3.3.3.json').read_text())
    assert hardware_LOGZ['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Název, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SEKUNDA_operand):\n return 가+SEKUNDA_operand\n'}),
            ('jkoros-space', {'space%d.py' % číslo: 'HODNOTA=1\n' for číslo in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = test_kolečko(Název, 파일들)
        (Storage_cesta/(Název+'==1.0.archive')).write_bytes(data)
        (Storage_cesta/(Název+'==1.0.json')).write_text(json.dumps({'name': Název, 'version': '1.0',
            'filename': Název.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    ověřit_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardware_LOGZ, 'checks': []}
    číslo_portu = 빈접속번호()
    Proces = subprocess.Popen(['python3', str(akce_kořen/'nástroje/Provést_příkaz.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(číslo_portu), '--pip-cache', str(Storage_cesta), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector()
    selektor_a916db4e.register(Proces.stdout, selectors.EVENT_READ)
    přepis = bytearray()
    def 기다리기(zobrazit_HODNOTA=b'jkoros-native> '):
        Obsah_HODNOTA = bytearray()
        끝 = time.monotonic()+120
        while zobrazit_HODNOTA not in Obsah_HODNOTA:
            if time.monotonic() > 끝 or Proces.poll() is not None:
                raise AssertionError('게스트 odezva 없음: '+Obsah_HODNOTA.decode('utf-8','replace'))
            for položka_HODNOTA, _ in selektor_a916db4e.select(.1):
                조각 = položka_HODNOTA.fileobj.read(4096)
                Obsah_HODNOTA.extend(조각)
                přepis.extend(조각)
        return Obsah_HODNOTA.decode('utf-8', 'replace').replace('\r\n','\n')
    def prostředí(příkaz, zobrazit_HODNOTA=b'jkoros-native> '):
        Proces.stdin.write(příkaz.encode()+b'\n')
        Proces.stdin.flush()
        return 기다리기(zobrazit_HODNOTA)
    def Provést_příkaz(příkaz, 예상, Stav_HODNOTA=0):
        Obsah_HODNOTA = prostředí(příkaz)
        assert 예상 in Obsah_HODNOTA and '\nexit '+str(Stav_HODNOTA)+'\n' in Obsah_HODNOTA, Obsah_HODNOTA
        ověřit_5fb2b747['checks'].append(příkaz)
        return Obsah_HODNOTA
    def Upload_Files(Název, data):
        prostředí('load '+Název, b'hex> ')
        for poziční_index in range(0, len(data), 64):
            prostředí(data[poziční_index:poziční_index+64].hex(), b'hex> ')
        assert 'LOADED' in prostředí('.')
    try:
        기다리기()
        Provést_příkaz('pip --help', 'MicroPython zdroj_strom 설치기')
        Upload_Files('오류시험.py', (akce_kořen/'zkoušky/PYTHON/한국어오류시험.py').read_bytes())
        Provést_příkaz('python 오류시험.py', 'čeština název_souboru výjimka ověřit')
        Provést_příkaz('pip install micropython-bisect==3.3.3 --port '+str(číslo_portu), 'instalovat_HODNOTA 완료: micropython-bisect 3.3.3')
        Provést_příkaz('python -c \'from bisect import insort as 순서대로넣기; HODNOTA=[1,5]; 순서대로넣기(HODNOTA,3); print(HODNOTA)\'', '[1, 3, 5]')
        Provést_příkaz('python -m pip list', 'micropython-bisect 3.3.3')
        Provést_příkaz('pip install micropython-bisect==3.3.3 --port '+str(číslo_portu), '이미 설치됨:')
        Provést_příkaz('pip install jkoros-fixture==1.0 --port '+str(číslo_portu), 'instalovat_HODNOTA 완료: jkoros-fixture')
        Provést_příkaz('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Provést_příkaz('pip install jkoros-syntax==1.0 --port '+str(číslo_portu), 'sada chyba:', 1)
        Provést_příkaz('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 chyba 보존")\'', '구문 chyba 보존')
        Upload_Files('공간시험.py', (akce_kořen/'zkoušky/PYTHON/sada_kořen_test.py').read_bytes())
        Provést_příkaz('python 공간시험.py '+str(číslo_portu), 'sada ODKAZ_oblast 부족 Vratka_most ověřit')
        Provést_příkaz('pip uninstall jkoros-fixture', 'odebrat_položka 완료: jkoros-fixture')
        Provést_příkaz('pip uninstall micropython-bisect', 'odebrat_položka 완료: micropython-bisect')
        Provést_příkaz('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("odebrat_položka ověřit")\'', 'odebrat_položka ověřit')
        ověřit_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 instalovat_HODNOTA·import·Provést_příkaz, čeština výjimka, 패키지 Adresář_HODNOTA, selhání_HODNOTA Vratka_most, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Konec_program 키로 QEMU를 끝내면 실행기의 Přenos_HODNOTA 문맥도 정리된다.
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
        (KV_cesta/'serial.log').write_bytes(přepis)
        (KV_cesta/'report.json').write_text(json.dumps(ověřit_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Spustit_2()
