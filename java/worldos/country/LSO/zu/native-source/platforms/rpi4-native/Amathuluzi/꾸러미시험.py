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
from yenza_umyalo import 기준


def 시험휠(Igama, 파일들, udaba_inani='Root-Is-Purelib: true\n', 의존성=''):
    imininingwane = io.BytesIO()
    with zipfile.ZipFile(imininingwane, 'w', zipfile.ZIP_DEFLATED) as isigaxa:
        isigaxa.writestr(Igama + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + udaba_inani)
        isigaxa.writestr(Igama + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Igama + '\nVersion: 1.0\n' + 의존성)
        for Indlela_2, Okuqukethwe_inani in 파일들.items():
            isigaxa.writestr(Indlela_2, Okuqukethwe_inani)
    return imininingwane.getvalue()


def hlola_singatha():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'inani=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'inani=42\n'.encode()}
    for imininingwane in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', imininingwane, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Indlela_2·Ubungako·C iselulo_inani·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Sebenzisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    hlola_singatha()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Indawo_yokugcina_umzila = 결과경로/'cache'
    Indawo_yokugcina_umzila.mkdir(exist_ok=True)
    # ulwazi_ngokwenzekile_imininingwane PyPI 배포 Ihele. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Hlela('micropython-bisect==3.3.3')
    for umsila_inani in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+umsila_inani)), str(Indawo_yokugcina_umzila/('micropython-bisect==3.3.3'+umsila_inani)))
    실물기록 = json.loads((Indawo_yokugcina_umzila/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Igama, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'inani=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        imininingwane = 시험휠(Igama, 파일들)
        (Indawo_yokugcina_umzila/(Igama+'==1.0.archive')).write_bytes(imininingwane)
        (Indawo_yokugcina_umzila/(Igama+'==1.0.json')).write_text(json.dumps({'name': Igama, 'version': '1.0',
            'filename': Igama.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(imininingwane).hexdigest()}))
    qinisekisa = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Inqubo = subprocess.Popen(['python3', str(기준/'Amathuluzi/yenza_umyalo.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Indawo_yokugcina_umzila), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    isiqoki_a916db4e = selectors.DefaultSelector()
    isiqoki_a916db4e.register(Inqubo.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(khombisa_inani=b'jkoros-native> '):
        Okuqukethwe_inani = bytearray()
        끝 = time.monotonic()+120
        while khombisa_inani not in Okuqukethwe_inani:
            if time.monotonic() > 끝 or Inqubo.poll() is not None:
                raise AssertionError('게스트 phendula 없음: '+Okuqukethwe_inani.decode('utf-8','replace'))
            for okufakwayo_inani, _ in isiqoki_a916db4e.select(.1):
                조각 = okufakwayo_inani.fileobj.read(4096)
                Okuqukethwe_inani.extend(조각)
                대화기록.extend(조각)
        return Okuqukethwe_inani.decode('utf-8', 'replace').replace('\r\n','\n')
    def isihumushi_miyalelo(Umlayelo, khombisa_inani=b'jkoros-native> '):
        Inqubo.stdin.write(Umlayelo.encode()+b'\n')
        Inqubo.stdin.flush()
        return 기다리기(khombisa_inani)
    def yenza_umyalo(Umlayelo, 예상, isimo_inani=0):
        Okuqukethwe_inani = isihumushi_miyalelo(Umlayelo)
        assert 예상 in Okuqukethwe_inani and '\nexit '+str(isimo_inani)+'\n' in Okuqukethwe_inani, Okuqukethwe_inani
        qinisekisa['checks'].append(Umlayelo)
        return Okuqukethwe_inani
    def layisha_Amafayela(Igama, imininingwane):
        isihumushi_miyalelo('load '+Igama, b'hex> ')
        for 자리 in range(0, len(imininingwane), 64):
            isihumushi_miyalelo(imininingwane[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in isihumushi_miyalelo('.')
    try:
        기다리기()
        yenza_umyalo('pip --help', 'MicroPython umthombo_isihlahla 설치기')
        layisha_Amafayela('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        yenza_umyalo('python 오류시험.py', 'Isi_Zulu Ihele 예외 qiniseka')
        yenza_umyalo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'faka_inani 완료: micropython-bisect 3.3.3')
        yenza_umyalo('python -c \'from bisect import insort as 순서대로넣기; inani=[1,5]; 순서대로넣기(inani,3); print(inani)\'', '[1, 3, 5]')
        yenza_umyalo('python -m pip list', 'micropython-bisect 3.3.3')
        yenza_umyalo('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        yenza_umyalo('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'faka_inani 완료: jkoros-fixture')
        yenza_umyalo('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        yenza_umyalo('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'isigaxa Iphutha:', 1)
        yenza_umyalo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Iphutha 보존")\'', '구문 Iphutha 보존')
        layisha_Amafayela('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        yenza_umyalo('python 공간시험.py '+str(접속번호), 'isigaxa 공간 부족 되돌림 qiniseka')
        yenza_umyalo('pip uninstall jkoros-fixture', 'khipha_okufakwayo 완료: jkoros-fixture')
        yenza_umyalo('pip uninstall micropython-bisect', 'khipha_okufakwayo 완료: micropython-bisect')
        yenza_umyalo('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("khipha_okufakwayo qiniseka")\'', 'khipha_okufakwayo qiniseka')
        qinisekisa['passed'] = True
        print('PASS: PyPI 실물 faka_inani·import·yenza_umyalo, Isi_Zulu 예외, 패키지 umkhombandlela_inani, ukwehluleka_inani 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 phuma_i_app 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Inqubo.stdin.write(b'\x01x')
            Inqubo.stdin.flush()
            Inqubo.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Inqubo.terminate()
            try:
                Inqubo.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Inqubo.kill()
                Inqubo.wait()
        if Inqubo.poll() is None:
            Inqubo.kill()
            Inqubo.wait()
        isiqoki_a916db4e.close()
        Inqubo.stdin.close()
        Inqubo.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(qinisekisa, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Sebenzisa()
