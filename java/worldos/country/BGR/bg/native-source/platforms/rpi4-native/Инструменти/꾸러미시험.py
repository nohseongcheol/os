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
from 꾸러미중계 import пакет_хранилище, декомпресирам
from изпълнявам_команда import проект_корен


def 시험휠(Име, 파일들, случай_стойност='Root-Is-Purelib: true\n', 의존성=''):
    данни = io.BytesIO()
    with zipfile.ZipFile(данни, 'w', zipfile.ZIP_DEFLATED) as пакет:
        пакет.writestr(Име + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + случай_стойност)
        пакет.writestr(Име + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Име + '\nVersion: 1.0\n' + 의존성)
        for ПЪТ, Съдържание_стойност in 파일들.items():
            пакет.writestr(ПЪТ, Съдържание_стойност)
    return данни.getvalue()


def проверявам_хост():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'стойност=42\n'})
    assert декомпресирам('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'стойност=42\n'.encode()}
    for данни in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            декомпресирам('jkoros_fixture-1.0-py3-none-any.whl', данни, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ПЪТ·Размер·C разширение_стойност·의존성 отхвърлям_стойност_e3ecc00b')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--host-only', action='store_true')
    Параметри = анализатор_48ee4b1b.parse_args()
    проверявам_хост()
    if Параметри.host_only:
        return
    мярка_път = проект_корен/'build/verification/pip'
    мярка_път.mkdir(parents=True, exist_ok=True)
    Памет_път = мярка_път/'cache'
    Памет_път.mkdir(exist_ok=True)
    # действителен_данни PyPI 배포 Файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    пакет_хранилище(проект_корен/'build/pip-cache').Подготвяне('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(проект_корен/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Памет_път/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Памет_път/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Име, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'стойност=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        данни = 시험휠(Име, 파일들)
        (Памет_път/(Име+'==1.0.archive')).write_bytes(данни)
        (Памет_път/(Име+'==1.0.json')).write_text(json.dumps({'name': Име, 'version': '1.0',
            'filename': Име.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(данни).hexdigest()}))
    проверка = {'passed': False, 'kernel_sha256': hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    номер_на_порт = 빈접속번호()
    Процес = subprocess.Popen(['python3', str(проект_корен/'Инструменти/изпълнявам_команда.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(номер_на_порт), '--pip-cache', str(Памет_път), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    свързан_елемент_за_избор_a916db4e = selectors.DefaultSelector()
    свързан_елемент_за_избор_a916db4e.register(Процес.stdout, selectors.EVENT_READ)
    препис = bytearray()
    def 기다리기(показвам_стойност=b'jkoros-native> '):
        Съдържание_стойност = bytearray()
        끝 = time.monotonic()+120
        while показвам_стойност not in Съдържание_стойност:
            if time.monotonic() > 끝 or Процес.poll() is not None:
                raise AssertionError('게스트 отговор 없음: '+Съдържание_стойност.decode('utf-8','replace'))
            for запис_стойност, _ in свързан_елемент_за_избор_a916db4e.select(.1):
                조각 = запис_стойност.fileobj.read(4096)
                Съдържание_стойност.extend(조각)
                препис.extend(조각)
        return Съдържание_стойност.decode('utf-8', 'replace').replace('\r\n','\n')
    def обвивка(Команда, показвам_стойност=b'jkoros-native> '):
        Процес.stdin.write(Команда.encode()+b'\n')
        Процес.stdin.flush()
        return 기다리기(показвам_стойност)
    def изпълнявам_команда(Команда, 예상, Състояние_стойност=0):
        Съдържание_стойност = обвивка(Команда)
        assert 예상 in Съдържание_стойност and '\nexit '+str(Състояние_стойност)+'\n' in Съдържание_стойност, Съдържание_стойност
        проверка['checks'].append(Команда)
        return Съдържание_стойност
    def качвам_Файлове(Име, данни):
        обвивка('load '+Име, b'hex> ')
        for позиционен_указател in range(0, len(данни), 64):
            обвивка(данни[позиционен_указател:позиционен_указател+64].hex(), b'hex> ')
        assert 'LOADED' in обвивка('.')
    try:
        기다리기()
        изпълнявам_команда('pip --help', 'MicroPython източник_дърво 설치기')
        качвам_Файлове('오류시험.py', (проект_корен/'시험/파이썬/한국어오류시험.py').read_bytes())
        изпълнявам_команда('python 오류시험.py', 'Български Файл изключение проверявам')
        изпълнявам_команда('pip install micropython-bisect==3.3.3 --port '+str(номер_на_порт), 'инсталирам_стойност 완료: micropython-bisect 3.3.3')
        изпълнявам_команда('python -c \'from bisect import insort as 순서대로넣기; стойност=[1,5]; 순서대로넣기(стойност,3); print(стойност)\'', '[1, 3, 5]')
        изпълнявам_команда('python -m pip list', 'micropython-bisect 3.3.3')
        изпълнявам_команда('pip install micropython-bisect==3.3.3 --port '+str(номер_на_порт), '이미 설치됨:')
        изпълнявам_команда('pip install jkoros-fixture==1.0 --port '+str(номер_на_порт), 'инсталирам_стойност 완료: jkoros-fixture')
        изпълнявам_команда('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        изпълнявам_команда('pip install jkoros-syntax==1.0 --port '+str(номер_на_порт), 'пакет ГРЕШКА:', 1)
        изпълнявам_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ГРЕШКА 보존")\'', '구문 ГРЕШКА 보존')
        качвам_Файлове('공간시험.py', (проект_корен/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        изпълнявам_команда('python 공간시험.py '+str(номер_на_порт), 'пакет адрес_област 부족 връщам_мост проверявам')
        изпълнявам_команда('pip uninstall jkoros-fixture', 'премахвам_запис 완료: jkoros-fixture')
        изпълнявам_команда('pip uninstall micropython-bisect', 'премахвам_запис 완료: micropython-bisect')
        изпълнявам_команда('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("премахвам_запис проверявам")\'', 'премахвам_запис проверявам')
        проверка['passed'] = True
        print('PASS: PyPI 실물 инсталирам_стойност·import·изпълнявам_команда, Български изключение, 패키지 указател_стойност, отказ_стойност връщам_мост, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Изход_програма 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        свързан_елемент_за_избор_a916db4e.close()
        Процес.stdin.close()
        Процес.stdout.close()
        (мярка_път/'serial.log').write_bytes(препис)
        (мярка_път/'report.json').write_text(json.dumps(проверка, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Стартиране()
