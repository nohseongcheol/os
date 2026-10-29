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
from 실행 import 기준


def 시험휠(이름, 파일들, achikii_ajutuu='Root-Is-Purelib: true\n', 의존성=''):
    atijaaya = io.BytesIO()
    with zipfile.ZipFile(atijaaya, 'w', zipfile.ZIP_DEFLATED) as 꾸러미:
        꾸러미.writestr(이름 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + achikii_ajutuu)
        꾸러미.writestr(이름 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + 이름 + '\nVersion: 1.0\n' + 의존성)
        for wopu_a_ttaaleemüin, alu_ujatüü_ajutuu in 파일들.items():
            꾸러미.writestr(wopu_a_ttaaleemüin, alu_ujatüü_ajutuu)
    return atijaaya.getvalue()


def cheeke_epiajatü():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'ajutuu=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'ajutuu=42\n'.encode()}
    for atijaaya in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', atijaaya, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel wopu_a_ttaaleemüin·크기·C e_irukuu_ajutuu·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    cheeke_epiajatü()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    저장경로 = 결과경로/'cache'
    저장경로.mkdir(exist_ok=True)
    # 실제 PyPI 배포 anaajaalaa. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').준비('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(저장경로/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((저장경로/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for 이름, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'ajutuu=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        atijaaya = 시험휠(이름, 파일들)
        (저장경로/(이름+'==1.0.archive')).write_bytes(atijaaya)
        (저장경로/(이름+'==1.0.json')).write_text(json.dumps({'name': 이름, 'version': '1.0',
            'filename': 이름.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(atijaaya).hexdigest()}))
    검증 = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    실행과정 = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(저장경로), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(실행과정.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(표시=b'jkoros-native> '):
        alu_ujatüü_ajutuu = bytearray()
        끝 = time.monotonic()+120
        while 표시 not in alu_ujatüü_ajutuu:
            if time.monotonic() > 끝 or 실행과정.poll() is not None:
                raise AssertionError('게스트 응답 없음: '+alu_ujatüü_ajutuu.decode('utf-8','replace'))
            for ekeroliaa_ajutuu, _ in 선택기.select(.1):
                조각 = ekeroliaa_ajutuu.fileobj.read(4096)
                alu_ujatüü_ajutuu.extend(조각)
                대화기록.extend(조각)
        return alu_ujatüü_ajutuu.decode('utf-8', 'replace').replace('\r\n','\n')
    def aluwataalapu_u(aluwataaya, 표시=b'jkoros-native> '):
        실행과정.stdin.write(aluwataaya.encode()+b'\n')
        실행과정.stdin.flush()
        return 기다리기(표시)
    def 실행(aluwataaya, 예상, jamakua_iparülein_ajutuu=0):
        alu_ujatüü_ajutuu = aluwataalapu_u(aluwataaya)
        assert 예상 in alu_ujatüü_ajutuu and '\nexit '+str(jamakua_iparülein_ajutuu)+'\n' in alu_ujatüü_ajutuu, alu_ujatüü_ajutuu
        검증['checks'].append(aluwataaya)
        return alu_ujatüü_ajutuu
    def 올리기(이름, atijaaya):
        aluwataalapu_u('load '+이름, b'hex> ')
        for 자리 in range(0, len(atijaaya), 64):
            aluwataalapu_u(atijaaya[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in aluwataalapu_u('.')
    try:
        기다리기()
        실행('pip --help', 'MicroPython eejeejetülein_wunu_ulia 설치기')
        올리기('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        실행('python 오류시험.py', '한국어 anaajaalaa 예외 확인')
        실행('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'e_itawaa_ajutuu 완료: micropython-bisect 3.3.3')
        실행('python -c \'from bisect import insort as 순서대로넣기; ajutuu=[1,5]; 순서대로넣기(ajutuu,3); print(ajutuu)\'', '[1, 3, 5]')
        실행('python -m pip list', 'micropython-bisect 3.3.3')
        실행('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        실행('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'e_itawaa_ajutuu 완료: jkoros-fixture')
        실행('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        실행('pip install jkoros-syntax==1.0 --port '+str(접속번호), '꾸러미 ajachitia:', 1)
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ajachitia 보존")\'', '구문 ajachitia 보존')
        올리기('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        실행('python 공간시험.py '+str(접속번호), '꾸러미 공간 부족 되돌림 확인')
        실행('pip uninstall jkoros-fixture', '제거 완료: jkoros-fixture')
        실행('pip uninstall micropython-bisect', '제거 완료: micropython-bisect')
        실행('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("제거 확인")\'', '제거 확인')
        검증['passed'] = True
        print('PASS: PyPI 실물 e_itawaa_ajutuu·import·실행, 한국어 예외, 패키지 anaajaalee_ajutuu, ajachitia_ajutuu 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 aju_itaa_akumajiaa 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            실행과정.stdin.write(b'\x01x')
            실행과정.stdin.flush()
            실행과정.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            실행과정.terminate()
            try:
                실행과정.wait(timeout=8)
            except subprocess.TimeoutExpired:
                실행과정.kill()
                실행과정.wait()
        if 실행과정.poll() is None:
            실행과정.kill()
            실행과정.wait()
        선택기.close()
        실행과정.stdin.close()
        실행과정.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(검증, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    시작()
