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
from Гүйцэтгэх_команд import 기준


def 시험휠(Нэр, 파일들, нөхцөл_байдал_утга='Root-Is-Purelib: true\n', 의존성=''):
    өгөгдөл = io.BytesIO()
    with zipfile.ZipFile(өгөгдөл, 'w', zipfile.ZIP_DEFLATED) as багц:
        багц.writestr(Нэр + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + нөхцөл_байдал_утга)
        багц.writestr(Нэр + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Нэр + '\nVersion: 1.0\n' + 의존성)
        for ЗАМ, Агуулга_утга in 파일들.items():
            багц.writestr(ЗАМ, Агуулга_утга)
    return өгөгдөл.getvalue()


def чек_хост():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'утга=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'утга=42\n'.encode()}
    for өгөгдөл in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', өгөгдөл, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ЗАМ·Хэмжээ·C өргөтгөл_утга·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Ажиллуулах():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    чек_хост()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    Санах_ой_зам = 결과경로/'cache'
    Санах_ой_зам.mkdir(exist_ok=True)
    # бодит_өгөгдөл PyPI 배포 Файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Бэлтгэх('micropython-bisect==3.3.3')
    for сүүл_утга in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+сүүл_утга)), str(Санах_ой_зам/('micropython-bisect==3.3.3'+сүүл_утга)))
    실물기록 = json.loads((Санах_ой_зам/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Нэр, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'утга=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        өгөгдөл = 시험휠(Нэр, 파일들)
        (Санах_ой_зам/(Нэр+'==1.0.archive')).write_bytes(өгөгдөл)
        (Санах_ой_зам/(Нэр+'==1.0.json')).write_text(json.dumps({'name': Нэр, 'version': '1.0',
            'filename': Нэр.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(өгөгдөл).hexdigest()}))
    баталгаажуулах = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    үйл_явц = subprocess.Popen(['python3', str(기준/'Хэрэгслүүд/Гүйцэтгэх_команд.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Санах_ой_зам), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сонгогч_a916db4e = selectors.DefaultSelector()
    сонгогч_a916db4e.register(үйл_явц.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(үзүүлэх_утга=b'jkoros-native> '):
        Агуулга_утга = bytearray()
        끝 = time.monotonic()+120
        while үзүүлэх_утга not in Агуулга_утга:
            if time.monotonic() > 끝 or үйл_явц.poll() is not None:
                raise AssertionError('게스트 хариулах 없음: '+Агуулга_утга.decode('utf-8','replace'))
            for оролт_утга, _ in сонгогч_a916db4e.select(.1):
                조각 = оролт_утга.fileobj.read(4096)
                Агуулга_утга.extend(조각)
                대화기록.extend(조각)
        return Агуулга_утга.decode('utf-8', 'replace').replace('\r\n','\n')
    def бүрхүүл(Тушаал, үзүүлэх_утга=b'jkoros-native> '):
        үйл_явц.stdin.write(Тушаал.encode()+b'\n')
        үйл_явц.stdin.flush()
        return 기다리기(үзүүлэх_утга)
    def Гүйцэтгэх_команд(Тушаал, 예상, төлөв_утга=0):
        Агуулга_утга = бүрхүүл(Тушаал)
        assert 예상 in Агуулга_утга and '\nexit '+str(төлөв_утга)+'\n' in Агуулга_утга, Агуулга_утга
        баталгаажуулах['checks'].append(Тушаал)
        return Агуулга_утга
    def байршуулах_Файлууд(Нэр, өгөгдөл):
        бүрхүүл('load '+Нэр, b'hex> ')
        for 자리 in range(0, len(өгөгдөл), 64):
            бүрхүүл(өгөгдөл[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in бүрхүүл('.')
    try:
        기다리기()
        Гүйцэтгэх_команд('pip --help', 'MicroPython эх_мод 설치기')
        байршуулах_Файлууд('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        Гүйцэтгэх_команд('python 오류시험.py', 'Монгол Файл 예외 шалгах')
        Гүйцэтгэх_команд('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'суулгах_утга 완료: micropython-bisect 3.3.3')
        Гүйцэтгэх_команд('python -c \'from bisect import insort as 순서대로넣기; утга=[1,5]; 순서대로넣기(утга,3); print(утга)\'', '[1, 3, 5]')
        Гүйцэтгэх_команд('python -m pip list', 'micropython-bisect 3.3.3')
        Гүйцэтгэх_команд('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        Гүйцэтгэх_команд('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'суулгах_утга 완료: jkoros-fixture')
        Гүйцэтгэх_команд('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Гүйцэтгэх_команд('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'багц Алдаа:', 1)
        Гүйцэтгэх_команд('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Алдаа 보존")\'', '구문 Алдаа 보존')
        байршуулах_Файлууд('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        Гүйцэтгэх_команд('python 공간시험.py '+str(접속번호), 'багц 공간 부족 되돌림 шалгах')
        Гүйцэтгэх_команд('pip uninstall jkoros-fixture', 'арилгах_оролт 완료: jkoros-fixture')
        Гүйцэтгэх_команд('pip uninstall micropython-bisect', 'арилгах_оролт 완료: micropython-bisect')
        Гүйцэтгэх_команд('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("арилгах_оролт шалгах")\'', 'арилгах_оролт шалгах')
        баталгаажуулах['passed'] = True
        print('PASS: PyPI 실물 суулгах_утга·import·Гүйцэтгэх_команд, Монгол 예외, 패키지 лавлах_утга, гэмтэл_утга 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Гарах_програм 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            үйл_явц.stdin.write(b'\x01x')
            үйл_явц.stdin.flush()
            үйл_явц.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            үйл_явц.terminate()
            try:
                үйл_явц.wait(timeout=8)
            except subprocess.TimeoutExpired:
                үйл_явц.kill()
                үйл_явц.wait()
        if үйл_явц.poll() is None:
            үйл_явц.kill()
            үйл_явц.wait()
        сонгогч_a916db4e.close()
        үйл_явц.stdin.close()
        үйл_явц.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(баталгаажуулах, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Ажиллуулах()
