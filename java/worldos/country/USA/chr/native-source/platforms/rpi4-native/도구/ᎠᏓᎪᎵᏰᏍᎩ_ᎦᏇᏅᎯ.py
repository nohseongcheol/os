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
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def 시험휠(ᏚᏙᎥᎢ, 파일들, ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ='Root-Is-Purelib: true\n', 의존성=''):
    ᎦᏟᏌᏅᎯ = io.BytesIO()
    with zipfile.ZipFile(ᎦᏟᏌᏅᎯ, 'w', zipfile.ZIP_DEFLATED) as ᎦᏇᏅᎯ:
        ᎦᏇᏅᎯ.writestr(ᏚᏙᎥᎢ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ)
        ᎦᏇᏅᎯ.writestr(ᏚᏙᎥᎢ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + ᏚᏙᎥᎢ + '\nVersion: 1.0\n' + 의존성)
        for ᎠᏍᏓᏩᏛᏍᏗ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ in 파일들.items():
            ᎦᏇᏅᎯ.writestr(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
    return ᎦᏟᏌᏅᎯ.getvalue()


def ᎪᎯᏳᏔᏅ_ᎠᏁᏢᏍᎩ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ᏧᎬᏩᎶᏗᏯ=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ᏧᎬᏩᎶᏗᏯ=42\n'.encode()}
    for ᎦᏟᏌᏅᎯ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ᎦᏟᏌᏅᎯ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ᎠᏍᏓᏩᏛᏍᏗ·ᎢᎩᏓ·C ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ᎠᎢᏎᏍᏗ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    ᎪᎯᏳᏔᏅ_ᎠᏁᏢᏍᎩ()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ = 결과경로/'cache'
    ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(exist_ok=True)
    # ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ PyPI 배포 ᎠᏍᏆᏂᎪᏙᏗ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').ᎭᏛᏅᎢᏍᏓ('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for ᏚᏙᎥᎢ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ᏧᎬᏩᎶᏗᏯ=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ᎦᏟᏌᏅᎯ = 시험휠(ᏚᏙᎥᎢ, 파일들)
        (ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ/(ᏚᏙᎥᎢ+'==1.0.archive')).write_bytes(ᎦᏟᏌᏅᎯ)
        (ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ/(ᏚᏙᎥᎢ+'==1.0.json')).write_text(json.dumps({'name': ᏚᏙᎥᎢ, 'version': '1.0',
            'filename': ᏚᏙᎥᎢ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest()}))
    ᎪᎯᏳᏙᏗ = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    ᎢᏯᏛᏁᎵᏓᏍᏗ = subprocess.Popen(['python3', str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(ᎠᏍᏆᏂᎪᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ᎠᏑᏰᏍᎩ_a916db4e = selectors.DefaultSelector()
    ᎠᏑᏰᏍᎩ_a916db4e.register(ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ=b'jkoros-native> '):
        ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ = bytearray()
        끝 = time.monotonic()+120
        while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ:
            if time.monotonic() > 끝 or ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is not None:
                raise AssertionError('게스트 응답 없음: '+ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.decode('utf-8','replace'))
            for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ, _ in ᎠᏑᏰᏍᎩ_a916db4e.select(.1):
                조각 = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.fileobj.read(4096)
                ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.extend(조각)
                대화기록.extend(조각)
        return ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.decode('utf-8', 'replace').replace('\r\n','\n')
    def ᎤᏯᏍᎦ(ᎤᏁᏤᎸᎩ, ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ=b'jkoros-native> '):
        ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᎤᏁᏤᎸᎩ.encode()+b'\n')
        ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
        return 기다리기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ)
    def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᎤᏁᏤᎸᎩ, 예상, ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ=0):
        ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ = ᎤᏯᏍᎦ(ᎤᏁᏤᎸᎩ)
        assert 예상 in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ and '\nexit '+str(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ)+'\n' in ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ
        ᎪᎯᏳᏙᏗ['checks'].append(ᎤᏁᏤᎸᎩ)
        return ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ
    def 올리기(ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ):
        ᎤᏯᏍᎦ('load '+ᏚᏙᎥᎢ, b'hex> ')
        for 자리 in range(0, len(ᎦᏟᏌᏅᎯ), 64):
            ᎤᏯᏍᎦ(ᎦᏟᏌᏅᎯ[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in ᎤᏯᏍᎦ('.')
    try:
        기다리기()
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip --help', 'MicroPython ᎦᏟᏌᏅᎯ_ᏡᎬ 설치기')
        올리기('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python 오류시험.py', '한국어 ᎠᏍᏆᏂᎪᏙᏗ 예외 ᎰᎯᏳᏓ')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ 완료: micropython-bisect 3.3.3')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python -c \'from bisect import insort as 순서대로넣기; ᏧᎬᏩᎶᏗᏯ=[1,5]; 순서대로넣기(ᏧᎬᏩᎶᏗᏯ,3); print(ᏧᎬᏩᎶᏗᏯ)\'', '[1, 3, 5]')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python -m pip list', 'micropython-bisect 3.3.3')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ 완료: jkoros-fixture')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'ᎦᏇᏅᎯ ᎦᎵᏓᏍᏔᏅ:', 1)
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ᎦᎵᏓᏍᏔᏅ 보존")\'', '구문 ᎦᎵᏓᏍᏔᏅ 보존')
        올리기('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python 공간시험.py '+str(접속번호), 'ᎦᏇᏅᎯ 공간 부족 되돌림 ᎰᎯᏳᏓ')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip uninstall jkoros-fixture', 'ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ 완료: jkoros-fixture')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('pip uninstall micropython-bisect', 'ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ 완료: micropython-bisect')
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ ᎰᎯᏳᏓ")\'', 'ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ ᎰᎯᏳᏓ')
        ᎪᎯᏳᏙᏗ['passed'] = True
        print('PASS: PyPI 실물 ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ·import·ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ, 한국어 예외, 패키지 ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ, ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(b'\x01x')
            ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush()
            ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
            try:
                ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ᎢᏯᏛᏁᎵᏓᏍᏗ.kill()
                ᎢᏯᏛᏁᎵᏓᏍᏗ.wait()
        if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is None:
            ᎢᏯᏛᏁᎵᏓᏍᏗ.kill()
            ᎢᏯᏛᏁᎵᏓᏍᏗ.wait()
        ᎠᏑᏰᏍᎩ_a916db4e.close()
        ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.close()
        ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(ᎪᎯᏳᏙᏗ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
