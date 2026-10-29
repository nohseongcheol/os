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
from 꾸러미중계 import fungasha_uwekaji, 압축풀기
from tekeleza_amri import 기준


def 시험휠(Jina, 파일들, Kazi_thamani='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as fungasha:
        fungasha.writestr(Jina + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + Kazi_thamani)
        fungasha.writestr(Jina + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Jina + '\nVersion: 1.0\n' + 의존성)
        for njia, maudhui_thamani in 파일들.items():
            fungasha.writestr(njia, maudhui_thamani)
    return data.getvalue()


def hundi_mwenyeji():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'thamani=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'thamani=42\n'.encode()}
    for data in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel njia·panga_ukubwa·C kiendelezi_thamani·의존성 kataa_thamani')


def tupu_namba_ya_kituo():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def endesha():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    hundi_mwenyeji()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Hifadhi_njia = 결과경로/'cache'
    Hifadhi_njia.mkdir(exist_ok=True)
    # halisi_data PyPI 배포 faili. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    fungasha_uwekaji(기준/'build/pip-cache').Andaa('micropython-bisect==3.3.3')
    for mkia_thamani in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+mkia_thamani)), str(Hifadhi_njia/('micropython-bisect==3.3.3'+mkia_thamani)))
    실물기록 = json.loads((Hifadhi_njia/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Jina, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'thamani=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(Jina, 파일들)
        (Hifadhi_njia/(Jina+'==1.0.archive')).write_bytes(data)
        (Hifadhi_njia/(Jina+'==1.0.json')).write_text(json.dumps({'name': Jina, 'version': '1.0',
            'filename': Jina.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    hakikisha = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    namba_ya_kituo = tupu_namba_ya_kituo()
    Mchakato = subprocess.Popen(['python3', str(기준/'Zana/tekeleza_amri.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(namba_ya_kituo), '--pip-cache', str(Hifadhi_njia), '--ftp-port', str(tupu_namba_ya_kituo())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    kiteuzi_a916db4e = selectors.DefaultSelector()
    kiteuzi_a916db4e.register(Mchakato.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(onyesha_thamani=b'jkoros-native> '):
        maudhui_thamani = bytearray()
        끝 = time.monotonic()+120
        while onyesha_thamani not in maudhui_thamani:
            if time.monotonic() > 끝 or Mchakato.poll() is not None:
                raise AssertionError('게스트 jibu 없음: '+maudhui_thamani.decode('utf-8','replace'))
            for ingizo_thamani, _ in kiteuzi_a916db4e.select(.1):
                조각 = ingizo_thamani.fileobj.read(4096)
                maudhui_thamani.extend(조각)
                대화기록.extend(조각)
        return maudhui_thamani.decode('utf-8', 'replace').replace('\r\n','\n')
    def sheli(amri, onyesha_thamani=b'jkoros-native> '):
        Mchakato.stdin.write(amri.encode()+b'\n')
        Mchakato.stdin.flush()
        return 기다리기(onyesha_thamani)
    def tekeleza_amri(amri, 예상, hali_thamani=0):
        maudhui_thamani = sheli(amri)
        assert 예상 in maudhui_thamani and '\nexit '+str(hali_thamani)+'\n' in maudhui_thamani, maudhui_thamani
        hakikisha['checks'].append(amri)
        return maudhui_thamani
    def pakia_Faili(Jina, data):
        sheli('load '+Jina, b'hex> ')
        for 자리 in range(0, len(data), 64):
            sheli(data[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in sheli('.')
    try:
        기다리기()
        tekeleza_amri('pip --help', 'MicroPython chanzo_mti 설치기')
        pakia_Faili('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        tekeleza_amri('python 오류시험.py', '한국어 faili vighairi thibitisha')
        tekeleza_amri('pip install micropython-bisect==3.3.3 --port '+str(namba_ya_kituo), 'sakinisha_thamani 완료: micropython-bisect 3.3.3')
        tekeleza_amri('python -c \'from bisect import insort as 순서대로넣기; thamani=[1,5]; 순서대로넣기(thamani,3); print(thamani)\'', '[1, 3, 5]')
        tekeleza_amri('python -m pip list', 'micropython-bisect 3.3.3')
        tekeleza_amri('pip install micropython-bisect==3.3.3 --port '+str(namba_ya_kituo), '이미 설치됨:')
        tekeleza_amri('pip install jkoros-fixture==1.0 --port '+str(namba_ya_kituo), 'sakinisha_thamani 완료: jkoros-fixture')
        tekeleza_amri('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        tekeleza_amri('pip install jkoros-syntax==1.0 --port '+str(namba_ya_kituo), 'fungasha kosa:', 1)
        tekeleza_amri('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 kosa 보존")\'', '구문 kosa 보존')
        pakia_Faili('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        tekeleza_amri('python 공간시험.py '+str(namba_ya_kituo), 'fungasha 공간 부족 되돌림 thibitisha')
        tekeleza_amri('pip uninstall jkoros-fixture', 'ondoa_ingizo 완료: jkoros-fixture')
        tekeleza_amri('pip uninstall micropython-bisect', 'ondoa_ingizo 완료: micropython-bisect')
        tekeleza_amri('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ondoa_ingizo thibitisha")\'', 'ondoa_ingizo thibitisha')
        hakikisha['passed'] = True
        print('PASS: PyPI 실물 sakinisha_thamani·import·tekeleza_amri, 한국어 vighairi, 패키지 Saraka_thamani, kushindwa_thamani 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 toka_programu 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Mchakato.stdin.write(b'\x01x')
            Mchakato.stdin.flush()
            Mchakato.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Mchakato.terminate()
            try:
                Mchakato.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Mchakato.kill()
                Mchakato.wait()
        if Mchakato.poll() is None:
            Mchakato.kill()
            Mchakato.wait()
        kiteuzi_a916db4e.close()
        Mchakato.stdin.close()
        Mchakato.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(hakikisha, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    endesha()
