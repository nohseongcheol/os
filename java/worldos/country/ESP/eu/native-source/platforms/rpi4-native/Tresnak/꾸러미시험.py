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
from 꾸러미중계 import multzo_biltegi, 압축풀기
from exekutatu_komando import Project_erro


def 시험휠(Izena, 파일들, kasu_balio='Root-Is-Purelib: true\n', 의존성=''):
    datuak = io.BytesIO()
    with zipfile.ZipFile(datuak, 'w', zipfile.ZIP_DEFLATED) as multzo:
        multzo.writestr(Izena + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + kasu_balio)
        multzo.writestr(Izena + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Izena + '\nVersion: 1.0\n' + 의존성)
        for Bide_izena, eduki_balio in 파일들.items():
            multzo.writestr(Bide_izena, eduki_balio)
    return datuak.getvalue()


def txeke_Ostalari():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'balio=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'balio=42\n'.encode()}
    for datuak in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', datuak, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Bide_izena·Tamaina·C luzapen_balio·의존성 baztertu_balio')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Exekutatu_2():
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('--host-only', action='store_true')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    txeke_Ostalari()
    if Argumentuak.host_only:
        return
    neurria_bide_izen = Project_erro/'build/verification/pip'
    neurria_bide_izen.mkdir(parents=True, exist_ok=True)
    biltegi_bide_izen_02e62bb7 = neurria_bide_izen/'cache'
    biltegi_bide_izen_02e62bb7.mkdir(exist_ok=True)
    # benetako_datuak PyPI 배포 Fitxategia. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    multzo_biltegi(Project_erro/'build/pip-cache').준비('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(Project_erro/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(biltegi_bide_izen_02e62bb7/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((biltegi_bide_izen_02e62bb7/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Izena, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'balio=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        datuak = 시험휠(Izena, 파일들)
        (biltegi_bide_izen_02e62bb7/(Izena+'==1.0.archive')).write_bytes(datuak)
        (biltegi_bide_izen_02e62bb7/(Izena+'==1.0.json')).write_text(json.dumps({'name': Izena, 'version': '1.0',
            'filename': Izena.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(datuak).hexdigest()}))
    baliozkotu = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    ataka_zenbaki = 빈접속번호()
    Prozesua = subprocess.Popen(['python3', str(Project_erro/'Tresnak/exekutatu_komando.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(ataka_zenbaki), '--pip-cache', str(biltegi_bide_izen_02e62bb7), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(Prozesua.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(erakutsi_balio=b'jkoros-native> '):
        eduki_balio = bytearray()
        끝 = time.monotonic()+120
        while erakutsi_balio not in eduki_balio:
            if time.monotonic() > 끝 or Prozesua.poll() is not None:
                raise AssertionError('게스트 erantzun 없음: '+eduki_balio.decode('utf-8','replace'))
            for sarrera_balio, _ in 선택기.select(.1):
                조각 = sarrera_balio.fileobj.read(4096)
                eduki_balio.extend(조각)
                대화기록.extend(조각)
        return eduki_balio.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(Komandoa, erakutsi_balio=b'jkoros-native> '):
        Prozesua.stdin.write(Komandoa.encode()+b'\n')
        Prozesua.stdin.flush()
        return 기다리기(erakutsi_balio)
    def exekutatu_komando(Komandoa, 예상, Egoera_balio=0):
        eduki_balio = shell(Komandoa)
        assert 예상 in eduki_balio and '\nexit '+str(Egoera_balio)+'\n' in eduki_balio, eduki_balio
        baliozkotu['checks'].append(Komandoa)
        return eduki_balio
    def Upload_Fitxategiak(Izena, datuak):
        shell('load '+Izena, b'hex> ')
        for kargu_INDIZE in range(0, len(datuak), 64):
            shell(datuak[kargu_INDIZE:kargu_INDIZE+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        exekutatu_komando('pip --help', 'MicroPython iturburu_zuhaitz 설치기')
        Upload_Fitxategiak('오류시험.py', (Project_erro/'시험/PYTHON/한국어오류시험.py').read_bytes())
        exekutatu_komando('python 오류시험.py', 'Euskara Fitxategia salbuespen egiaztatu')
        exekutatu_komando('pip install micropython-bisect==3.3.3 --port '+str(ataka_zenbaki), 'instalatu_balio 완료: micropython-bisect 3.3.3')
        exekutatu_komando('python -c \'from bisect import insort as 순서대로넣기; balio=[1,5]; 순서대로넣기(balio,3); print(balio)\'', '[1, 3, 5]')
        exekutatu_komando('python -m pip list', 'micropython-bisect 3.3.3')
        exekutatu_komando('pip install micropython-bisect==3.3.3 --port '+str(ataka_zenbaki), '이미 설치됨:')
        exekutatu_komando('pip install jkoros-fixture==1.0 --port '+str(ataka_zenbaki), 'instalatu_balio 완료: jkoros-fixture')
        exekutatu_komando('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        exekutatu_komando('pip install jkoros-syntax==1.0 --port '+str(ataka_zenbaki), 'multzo errorea:', 1)
        exekutatu_komando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 errorea 보존")\'', '구문 errorea 보존')
        Upload_Fitxategiak('공간시험.py', (Project_erro/'시험/PYTHON/꾸러미공간시험.py').read_bytes())
        exekutatu_komando('python 공간시험.py '+str(ataka_zenbaki), 'multzo 공간 부족 itzuli_zubi egiaztatu')
        exekutatu_komando('pip uninstall jkoros-fixture', 'kendu_sarrera 완료: jkoros-fixture')
        exekutatu_komando('pip uninstall micropython-bisect', 'kendu_sarrera 완료: micropython-bisect')
        exekutatu_komando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("kendu_sarrera egiaztatu")\'', 'kendu_sarrera egiaztatu')
        baliozkotu['passed'] = True
        print('PASS: PyPI 실물 instalatu_balio·import·exekutatu_komando, Euskara salbuespen, 패키지 direktorio_balio, hutsegite_balio itzuli_zubi, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 irten_aplik 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Prozesua.stdin.write(b'\x01x')
            Prozesua.stdin.flush()
            Prozesua.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Prozesua.terminate()
            try:
                Prozesua.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Prozesua.kill()
                Prozesua.wait()
        if Prozesua.poll() is None:
            Prozesua.kill()
            Prozesua.wait()
        선택기.close()
        Prozesua.stdin.close()
        Prozesua.stdout.close()
        (neurria_bide_izen/'serial.log').write_bytes(대화기록)
        (neurria_bide_izen/'report.json').write_text(json.dumps(baliozkotu, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Exekutatu_2()
