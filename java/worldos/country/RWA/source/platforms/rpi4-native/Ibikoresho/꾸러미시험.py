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
from gukora_ibwiriza import 기준


def 시험휠(Izina, 파일들, ikibazo_agaciro='Root-Is-Purelib: true\n', 의존성=''):
    amakurushingiro = io.BytesIO()
    with zipfile.ZipFile(amakurushingiro, 'w', zipfile.ZIP_DEFLATED) as ipaki:
        ipaki.writestr(Izina + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ikibazo_agaciro)
        ipaki.writestr(Izina + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Izina + '\nVersion: 1.0\n' + 의존성)
        for Inzira, Ibirimo_agaciro in 파일들.items():
            ipaki.writestr(Inzira, Ibirimo_agaciro)
    return amakurushingiro.getvalue()


def sheki_gucumbikira():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'agaciro=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'agaciro=42\n'.encode()}
    for amakurushingiro in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', amakurushingiro, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Inzira·Ingano·C umugereka_agaciro·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ihuriro():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    sheki_gucumbikira()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Ububiko_inzira = 결과경로/'cache'
    Ububiko_inzira.mkdir(exist_ok=True)
    # nyakuri_amakurushingiro PyPI 배포 Idosiye. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Gutegura('micropython-bisect==3.3.3')
    for umusago_agaciro_906127f7 in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+umusago_agaciro_906127f7)), str(Ububiko_inzira/('micropython-bisect==3.3.3'+umusago_agaciro_906127f7)))
    실물기록 = json.loads((Ububiko_inzira/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Izina, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'agaciro=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        amakurushingiro = 시험휠(Izina, 파일들)
        (Ububiko_inzira/(Izina+'==1.0.archive')).write_bytes(amakurushingiro)
        (Ububiko_inzira/(Izina+'==1.0.json')).write_text(json.dumps({'name': Izina, 'version': '1.0',
            'filename': Izina.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(amakurushingiro).hexdigest()}))
    kwemeza = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Inzira_a7054519 = subprocess.Popen(['python3', str(기준/'Ibikoresho/gukora_ibwiriza.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Ububiko_inzira), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    muhitamo_a916db4e = selectors.DefaultSelector()
    muhitamo_a916db4e.register(Inzira_a7054519.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(kugaragaza_agaciro=b'jkoros-native> '):
        Ibirimo_agaciro = bytearray()
        끝 = time.monotonic()+120
        while kugaragaza_agaciro not in Ibirimo_agaciro:
            if time.monotonic() > 끝 or Inzira_a7054519.poll() is not None:
                raise AssertionError('게스트 gusubiza 없음: '+Ibirimo_agaciro.decode('utf-8','replace'))
            for icyinjizwa_agaciro, _ in muhitamo_a916db4e.select(.1):
                조각 = icyinjizwa_agaciro.fileobj.read(4096)
                Ibirimo_agaciro.extend(조각)
                대화기록.extend(조각)
        return Ibirimo_agaciro.decode('utf-8', 'replace').replace('\r\n','\n')
    def insomamabwiriza(Icyo_wifuza, kugaragaza_agaciro=b'jkoros-native> '):
        Inzira_a7054519.stdin.write(Icyo_wifuza.encode()+b'\n')
        Inzira_a7054519.stdin.flush()
        return 기다리기(kugaragaza_agaciro)
    def gukora_ibwiriza(Icyo_wifuza, 예상, imimerere_agaciro=0):
        Ibirimo_agaciro = insomamabwiriza(Icyo_wifuza)
        assert 예상 in Ibirimo_agaciro and '\nexit '+str(imimerere_agaciro)+'\n' in Ibirimo_agaciro, Ibirimo_agaciro
        kwemeza['checks'].append(Icyo_wifuza)
        return Ibirimo_agaciro
    def gukurura_Dosiye(Izina, amakurushingiro):
        insomamabwiriza('load '+Izina, b'hex> ')
        for 자리 in range(0, len(amakurushingiro), 64):
            insomamabwiriza(amakurushingiro[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in insomamabwiriza('.')
    try:
        기다리기()
        gukora_ibwiriza('pip --help', 'MicroPython inkomoko_igiti 설치기')
        gukurura_Dosiye('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        gukora_ibwiriza('python 오류시험.py', 'Ikinyarwanda Idosiye 예외 gusuzuma')
        gukora_ibwiriza('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'kwinjiza_agaciro 완료: micropython-bisect 3.3.3')
        gukora_ibwiriza('python -c \'from bisect import insort as 순서대로넣기; agaciro=[1,5]; 순서대로넣기(agaciro,3); print(agaciro)\'', '[1, 3, 5]')
        gukora_ibwiriza('python -m pip list', 'micropython-bisect 3.3.3')
        gukora_ibwiriza('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        gukora_ibwiriza('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'kwinjiza_agaciro 완료: jkoros-fixture')
        gukora_ibwiriza('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        gukora_ibwiriza('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'ipaki IKOSA:', 1)
        gukora_ibwiriza('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 IKOSA 보존")\'', '구문 IKOSA 보존')
        gukurura_Dosiye('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        gukora_ibwiriza('python 공간시험.py '+str(접속번호), 'ipaki 공간 부족 되돌림 gusuzuma')
        gukora_ibwiriza('pip uninstall jkoros-fixture', 'gukuramo_icyinjizwa 완료: jkoros-fixture')
        gukora_ibwiriza('pip uninstall micropython-bisect', 'gukuramo_icyinjizwa 완료: micropython-bisect')
        gukora_ibwiriza('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("gukuramo_icyinjizwa gusuzuma")\'', 'gukuramo_icyinjizwa gusuzuma')
        kwemeza['passed'] = True
        print('PASS: PyPI 실물 kwinjiza_agaciro·import·gukora_ibwiriza, Ikinyarwanda 예외, 패키지 ububiko_agaciro_e5561a2b, kudakora_agaciro 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 gusohoka_porogaramu 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Inzira_a7054519.stdin.write(b'\x01x')
            Inzira_a7054519.stdin.flush()
            Inzira_a7054519.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Inzira_a7054519.terminate()
            try:
                Inzira_a7054519.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Inzira_a7054519.kill()
                Inzira_a7054519.wait()
        if Inzira_a7054519.poll() is None:
            Inzira_a7054519.kill()
            Inzira_a7054519.wait()
        muhitamo_a916db4e.close()
        Inzira_a7054519.stdin.close()
        Inzira_a7054519.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(kwemeza, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ihuriro()
