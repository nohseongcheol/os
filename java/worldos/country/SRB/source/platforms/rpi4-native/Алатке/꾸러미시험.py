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
from 꾸러미중계 import пакет_депо, 압축풀기
from Изврши_команда import пројектовати_корен


def 시험휠(Назив, 파일들, случај_вриједност='Root-Is-Purelib: true\n', 의존성=''):
    подаци = io.BytesIO()
    with zipfile.ZipFile(подаци, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(Назив + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + случај_вриједност)
        пакет.writestr(Назив + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Назив + '\nVersion: 1.0\n' + 의존성)
        for ПУТАЊА, Садржај_вриједност in 파일들.items():
            пакет.writestr(ПУТАЊА, Садржај_вриједност)
    return подаци.getvalue()


def чек_хост():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'вриједност=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'вриједност=42\n'.encode()}
    for подаци in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', подаци, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ПУТАЊА·Величина·C проширење_вриједност·의존성 одбацити_вриједност_e3ecc00b')


def празно_број_порта():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Покрени():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--host-only', action='store_true')
    Аргументи = анализатор_48ee4b1b.parse_args()
    чек_хост()
    if Аргументи.host_only:
        return
    мера_пут = пројектовати_корен/'build/verification/pip'
    мера_пут.mkdir(parents=True, exist_ok=True)
    похрана_пут = мера_пут/'cache'
    похрана_пут.mkdir(exist_ok=True)
    # стваран_подаци PyPI 배포 Датотека. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    пакет_депо(пројектовати_корен/'build/pip-cache').Припремити('micropython-bisect==3.3.3')
    for реп_вриједност in ('.archive', '.json'):
        shutil.copyfile(str(пројектовати_корен/'build/pip-cache'/('micropython-bisect==3.3.3'+реп_вриједност)), str(похрана_пут/('micropython-bisect==3.3.3'+реп_вриједност)))
    실물기록 = json.loads((похрана_пут/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Назив, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'вриједност=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        подаци = 시험휠(Назив, 파일들)
        (похрана_пут/(Назив+'==1.0.archive')).write_bytes(подаци)
        (похрана_пут/(Назив+'==1.0.json')).write_text(json.dumps({'name': Назив, 'version': '1.0',
            'filename': Назив.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(подаци).hexdigest()}))
    потврдити_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    број_порта = празно_број_порта()
    Процес = subprocess.Popen(['python3', str(пројектовати_корен/'Алатке/Изврши_команда.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(број_порта), '--pip-cache', str(похрана_пут), '--ftp-port', str(празно_број_порта())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    бирач_a916db4e = selectors.DefaultSelector()
    бирач_a916db4e.register(Процес.stdout, selectors.EVENT_READ)
    транскрипт = bytearray()
    def 기다리기(емисија_вриједност=b'jkoros-native> '):
        Садржај_вриједност = bytearray()
        끝 = time.monotonic()+120
        while емисија_вриједност not in Садржај_вриједност:
            if time.monotonic() > 끝 or Процес.poll() is not None:
                raise AssertionError('게스트 одговор 없음: '+Садржај_вриједност.decode('utf-8','replace'))
            for унос_вриједност, _ in бирач_a916db4e.select(.1):
                조각 = унос_вриједност.fileobj.read(4096)
                Садржај_вриједност.extend(조각)
                транскрипт.extend(조각)
        return Садржај_вриједност.decode('utf-8', 'replace').replace('\r\n','\n')
    def љуска(Наредба, емисија_вриједност=b'jkoros-native> '):
        Процес.stdin.write(Наредба.encode()+b'\n')
        Процес.stdin.flush()
        return 기다리기(емисија_вриједност)
    def Изврши_команда(Наредба, 예상, стање_вриједност=0):
        Садржај_вриједност = љуска(Наредба)
        assert 예상 in Садржај_вриједност and '\nexit '+str(стање_вриједност)+'\n' in Садржај_вриједност, Садржај_вриједност
        потврдити_5fb2b747['checks'].append(Наредба)
        return Садржај_вриједност
    def Отпрема_Фајлови(Назив, подаци):
        љуска('load '+Назив, b'hex> ')
        for позиција_индекс in range(0, len(подаци), 64):
            љуска(подаци[позиција_индекс:позиција_индекс+64].hex(), b'hex> ')
        assert 'LOADED' in љуска('.')
    try:
        기다리기()
        Изврши_команда('pip --help', 'MicroPython извор_стабло 설치기')
        Отпрема_Фајлови('오류시험.py', (пројектовати_корен/'시험/파이썬/한국어오류시험.py').read_bytes())
        Изврши_команда('python 오류시험.py', '한국어 Датотека изузетак потврдити')
        Изврши_команда('pip install micropython-bisect==3.3.3 --port '+str(број_порта), 'инсталирај_вриједност 완료: micropython-bisect 3.3.3')
        Изврши_команда('python -c \'from bisect import insort as 순서대로넣기; вриједност=[1,5]; 순서대로넣기(вриједност,3); print(вриједност)\'', '[1, 3, 5]')
        Изврши_команда('python -m pip list', 'micropython-bisect 3.3.3')
        Изврши_команда('pip install micropython-bisect==3.3.3 --port '+str(број_порта), '이미 설치됨:')
        Изврши_команда('pip install jkoros-fixture==1.0 --port '+str(број_порта), 'инсталирај_вриједност 완료: jkoros-fixture')
        Изврши_команда('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Изврши_команда('pip install jkoros-syntax==1.0 --port '+str(број_порта), 'пакет ГРЕШКА:', 1)
        Изврши_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ГРЕШКА 보존")\'', '구문 ГРЕШКА 보존')
        Отпрема_Фајлови('공간시험.py', (пројектовати_корен/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        Изврши_команда('python 공간시험.py '+str(број_порта), 'пакет 공간 부족 вратити_мост потврдити')
        Изврши_команда('pip uninstall jkoros-fixture', 'уклонити_унос 완료: jkoros-fixture')
        Изврши_команда('pip uninstall micropython-bisect', 'уклонити_унос 완료: micropython-bisect')
        Изврши_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("уклонити_унос потврдити")\'', 'уклонити_унос потврдити')
        потврдити_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 инсталирај_вриједност·import·Изврши_команда, 한국어 изузетак, 패키지 именик_вриједност, неуспјех_вриједност вратити_мост, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Излаз_програм 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Процес.stdin.write(b'\x01x')
            Процес.stdin.flush()
            Процес.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Процес.terminate()
            try:
                Процес.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Процес.kill()
                Процес.wait()
        if Процес.poll() is None:
            Процес.kill()
            Процес.wait()
        бирач_a916db4e.close()
        Процес.stdin.close()
        Процес.stdout.close()
        (мера_пут/'serial.log').write_bytes(транскрипт)
        (мера_пут/'report.json').write_text(json.dumps(потврдити_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Покрени()
