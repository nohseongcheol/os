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
from ukwenza_umyalelo import 기준


def 시험휠(Igama, 파일들, isiganeko_ixabiso='Root-Is-Purelib: true\n', 의존성=''):
    iingcombolo = io.BytesIO()
    with zipfile.ZipFile(iingcombolo, 'w', zipfile.ZIP_DEFLATED) as umqulu:
        umqulu.writestr(Igama + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + isiganeko_ixabiso)
        umqulu.writestr(Igama + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Igama + '\nVersion: 1.0\n' + 의존성)
        for INDLELA, Isiqulatho_ixabiso in 파일들.items():
            umqulu.writestr(INDLELA, Isiqulatho_ixabiso)
    return iingcombolo.getvalue()


def jonga_umsingathi():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ixabiso=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ixabiso=42\n'.encode()}
    for iingcombolo in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', iingcombolo, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel INDLELA·Ubukhulu·C isongezelelo_ixabiso·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Phumeza():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    jonga_umsingathi()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Ugcino_indlela = 결과경로/'cache'
    Ugcino_indlela.mkdir(exist_ok=True)
    # eyona_yenzekileyo_iingcombolo PyPI 배포 iFayili. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').lungisa('micropython-bisect==3.3.3')
    for umsila_ixabiso in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+umsila_ixabiso)), str(Ugcino_indlela/('micropython-bisect==3.3.3'+umsila_ixabiso)))
    실물기록 = json.loads((Ugcino_indlela/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Igama, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ixabiso=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        iingcombolo = 시험휠(Igama, 파일들)
        (Ugcino_indlela/(Igama+'==1.0.archive')).write_bytes(iingcombolo)
        (Ugcino_indlela/(Igama+'==1.0.json')).write_text(json.dumps({'name': Igama, 'version': '1.0',
            'filename': Igama.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(iingcombolo).hexdigest()}))
    qinisekisa = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Inkqubo = subprocess.Popen(['python3', str(기준/'Izixhobo/ukwenza_umyalelo.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Ugcino_indlela), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    umkhethi_a916db4e = selectors.DefaultSelector()
    umkhethi_a916db4e.register(Inkqubo.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(bonisa_ixabiso=b'jkoros-native> '):
        Isiqulatho_ixabiso = bytearray()
        끝 = time.monotonic()+120
        while bonisa_ixabiso not in Isiqulatho_ixabiso:
            if time.monotonic() > 끝 or Inkqubo.poll() is not None:
                raise AssertionError('게스트 phendula 없음: '+Isiqulatho_ixabiso.decode('utf-8','replace'))
            for ufako_nkcukacha_ixabiso, _ in umkhethi_a916db4e.select(.1):
                조각 = ufako_nkcukacha_ixabiso.fileobj.read(4096)
                Isiqulatho_ixabiso.extend(조각)
                대화기록.extend(조각)
        return Isiqulatho_ixabiso.decode('utf-8', 'replace').replace('\r\n','\n')
    def isiniki_myalelo(Umyalelo, bonisa_ixabiso=b'jkoros-native> '):
        Inkqubo.stdin.write(Umyalelo.encode()+b'\n')
        Inkqubo.stdin.flush()
        return 기다리기(bonisa_ixabiso)
    def ukwenza_umyalelo(Umyalelo, 예상, imo_ixabiso=0):
        Isiqulatho_ixabiso = isiniki_myalelo(Umyalelo)
        assert 예상 in Isiqulatho_ixabiso and '\nexit '+str(imo_ixabiso)+'\n' in Isiqulatho_ixabiso, Isiqulatho_ixabiso
        qinisekisa['checks'].append(Umyalelo)
        return Isiqulatho_ixabiso
    def layisha_Iifayile(Igama, iingcombolo):
        isiniki_myalelo('load '+Igama, b'hex> ')
        for 자리 in range(0, len(iingcombolo), 64):
            isiniki_myalelo(iingcombolo[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in isiniki_myalelo('.')
    try:
        기다리기()
        ukwenza_umyalelo('pip --help', 'MicroPython umthombo_umthi 설치기')
        layisha_Iifayile('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        ukwenza_umyalelo('python 오류시험.py', 'isiXhosa iFayili 예외 ngqinisisa')
        ukwenza_umyalelo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'fakela_ixabiso 완료: micropython-bisect 3.3.3')
        ukwenza_umyalelo('python -c \'from bisect import insort as 순서대로넣기; ixabiso=[1,5]; 순서대로넣기(ixabiso,3); print(ixabiso)\'', '[1, 3, 5]')
        ukwenza_umyalelo('python -m pip list', 'micropython-bisect 3.3.3')
        ukwenza_umyalelo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ukwenza_umyalelo('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'fakela_ixabiso 완료: jkoros-fixture')
        ukwenza_umyalelo('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ukwenza_umyalelo('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'umqulu Impazamo:', 1)
        ukwenza_umyalelo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Impazamo 보존")\'', '구문 Impazamo 보존')
        layisha_Iifayile('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ukwenza_umyalelo('python 공간시험.py '+str(접속번호), 'umqulu 공간 부족 되돌림 ngqinisisa')
        ukwenza_umyalelo('pip uninstall jkoros-fixture', 'shenxisa_ufako_nkcukacha 완료: jkoros-fixture')
        ukwenza_umyalelo('pip uninstall micropython-bisect', 'shenxisa_ufako_nkcukacha 완료: micropython-bisect')
        ukwenza_umyalelo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("shenxisa_ufako_nkcukacha ngqinisisa")\'', 'shenxisa_ufako_nkcukacha ngqinisisa')
        qinisekisa['passed'] = True
        print('PASS: PyPI 실물 fakela_ixabiso·import·ukwenza_umyalelo, isiXhosa 예외, 패키지 isalathisi_ixabiso_e5561a2b, ukungaphumeleli_ixabiso 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 phuma_inkqubo 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Inkqubo.stdin.write(b'\x01x')
            Inkqubo.stdin.flush()
            Inkqubo.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Inkqubo.terminate()
            try:
                Inkqubo.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Inkqubo.kill()
                Inkqubo.wait()
        if Inkqubo.poll() is None:
            Inkqubo.kill()
            Inkqubo.wait()
        umkhethi_a916db4e.close()
        Inkqubo.stdin.close()
        Inkqubo.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(qinisekisa, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Phumeza()
