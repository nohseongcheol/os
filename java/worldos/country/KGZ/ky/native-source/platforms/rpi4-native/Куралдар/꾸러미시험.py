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
from аткаруу_буйрук import 기준


def 시험휠(Аты, 파일들, иш_маани='Root-Is-Purelib: true\n', 의존성=''):
    берилмелер = io.BytesIO()
    with zipfile.ZipFile(берилмелер, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(Аты + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + иш_маани)
        пакет.writestr(Аты + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Аты + '\nVersion: 1.0\n' + 의존성)
        for ЖОЛ, Мазмун_маани in 파일들.items():
            пакет.writestr(ЖОЛ, Мазмун_маани)
    return берилмелер.getvalue()


def чек_кабылдоо():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'маани=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'маани=42\n'.encode()}
    for берилмелер in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', берилмелер, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ЖОЛ·Өлчөмү·C кеңейтүү_маани·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Жүргүзүү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    чек_кабылдоо()
    if 인수.host_only:
        return
    결과경로 = 기준/'build/verification/pip'
    결과경로.mkdir(parents=True, exist_ok=True)
    сактагыч_жол = 결과경로/'cache'
    сактагыч_жол.mkdir(exist_ok=True)
    # актуалдуу_берилмелер PyPI 배포 Файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(기준/'build/pip-cache').Даярдоо('micropython-bisect==3.3.3')
    for куйрук_маани in ('.archive', '.json'):
        shutil.copyfile(str(기준/'build/pip-cache'/('micropython-bisect==3.3.3'+куйрук_маани)), str(сактагыч_жол/('micropython-bisect==3.3.3'+куйрук_маани)))
    실물기록 = json.loads((сактагыч_жол/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Аты, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'маани=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        берилмелер = 시험휠(Аты, 파일들)
        (сактагыч_жол/(Аты+'==1.0.archive')).write_bytes(берилмелер)
        (сактагыч_жол/(Аты+'==1.0.json')).write_text(json.dumps({'name': Аты, 'version': '1.0',
            'filename': Аты.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(берилмелер).hexdigest()}))
    жарактуулугун_текшерүү = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Процесси = subprocess.Popen(['python3', str(기준/'Куралдар/аткаруу_буйрук.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(сактагыч_жол), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector()
    селектор_a916db4e.register(Процесси.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(көрсөтүү_маани=b'jkoros-native> '):
        Мазмун_маани = bytearray()
        끝 = time.monotonic()+120
        while көрсөтүү_маани not in Мазмун_маани:
            if time.monotonic() > 끝 or Процесси.poll() is not None:
                raise AssertionError('게스트 жооп_берүү 없음: '+Мазмун_маани.decode('utf-8','replace'))
            for киргизме_жазуу_маани, _ in селектор_a916db4e.select(.1):
                조각 = киргизме_жазуу_маани.fileobj.read(4096)
                Мазмун_маани.extend(조각)
                대화기록.extend(조각)
        return Мазмун_маани.decode('utf-8', 'replace').replace('\r\n','\n')
    def сырты(Команда, көрсөтүү_маани=b'jkoros-native> '):
        Процесси.stdin.write(Команда.encode()+b'\n')
        Процесси.stdin.flush()
        return 기다리기(көрсөтүү_маани)
    def аткаруу_буйрук(Команда, 예상, абал_маани=0):
        Мазмун_маани = сырты(Команда)
        assert 예상 in Мазмун_маани and '\nexit '+str(абал_маани)+'\n' in Мазмун_маани, Мазмун_маани
        жарактуулугун_текшерүү['checks'].append(Команда)
        return Мазмун_маани
    def жүктөп_жөнөтүү_Файлдар(Аты, берилмелер):
        сырты('load '+Аты, b'hex> ')
        for 자리 in range(0, len(берилмелер), 64):
            сырты(берилмелер[자리:자리+64].hex(), b'hex> ')
        assert 'LOADED' in сырты('.')
    try:
        기다리기()
        аткаруу_буйрук('pip --help', 'MicroPython башат_дарак 설치기')
        жүктөп_жөнөтүү_Файлдар('오류시험.py', (기준/'시험/파이썬/한국어오류시험.py').read_bytes())
        аткаруу_буйрук('python 오류시험.py', '한국어 Файл 예외 тууралыгын_аныктоо')
        аткаруу_буйрук('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'орнотуу_маани 완료: micropython-bisect 3.3.3')
        аткаруу_буйрук('python -c \'from bisect import insort as 순서대로넣기; маани=[1,5]; 순서대로넣기(маани,3); print(маани)\'', '[1, 3, 5]')
        аткаруу_буйрук('python -m pip list', 'micropython-bisect 3.3.3')
        аткаруу_буйрук('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        аткаруу_буйрук('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'орнотуу_маани 완료: jkoros-fixture')
        аткаруу_буйрук('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        аткаруу_буйрук('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'пакет Ката:', 1)
        аткаруу_буйрук('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Ката 보존")\'', '구문 Ката 보존')
        жүктөп_жөнөтүү_Файлдар('공간시험.py', (기준/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        аткаруу_буйрук('python 공간시험.py '+str(접속번호), 'пакет 공간 부족 되돌림 тууралыгын_аныктоо')
        аткаруу_буйрук('pip uninstall jkoros-fixture', 'алып_салуу_киргизме_жазуу 완료: jkoros-fixture')
        аткаруу_буйрук('pip uninstall micropython-bisect', 'алып_салуу_киргизме_жазуу 완료: micropython-bisect')
        аткаруу_буйрук('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("алып_салуу_киргизме_жазуу тууралыгын_аныктоо")\'', 'алып_салуу_киргизме_жазуу тууралыгын_аныктоо')
        жарактуулугун_текшерүү['passed'] = True
        print('PASS: PyPI 실물 орнотуу_маани·import·аткаруу_буйрук, 한국어 예외, 패키지 каталог_маани, натыйжасыз_маани 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Чыгуу_програм 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Процесси.stdin.write(b'\x01x')
            Процесси.stdin.flush()
            Процесси.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Процесси.terminate()
            try:
                Процесси.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Процесси.kill()
                Процесси.wait()
        if Процесси.poll() is None:
            Процесси.kill()
            Процесси.wait()
        селектор_a916db4e.close()
        Процесси.stdin.close()
        Процесси.stdout.close()
        (결과경로/'serial.log').write_bytes(대화기록)
        (결과경로/'report.json').write_text(json.dumps(жарактуулугун_текшерүү, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Жүргүзүү()
