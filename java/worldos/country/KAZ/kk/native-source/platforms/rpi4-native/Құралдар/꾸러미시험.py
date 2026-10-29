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
from 꾸러미중계 import жинау_репозиторий, қысылған_файлды_қалпына_келтіру
from орындау_пәрмен import жоба_түбір


def 시험휠(Аты, 파일들, іс_мән='Root-Is-Purelib: true\n', 의존성=''):
    деректер = io.BytesIO()
    with zipfile.ZipFile(деректер, 'w', zipfile.ZIP_DEFLATED) as жинау:
        жинау.writestr(Аты + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + іс_мән)
        жинау.writestr(Аты + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Аты + '\nVersion: 1.0\n' + 의존성)
        for Жол_2, мазмұн_мән in 파일들.items():
            жинау.writestr(Жол_2, мазмұн_мән)
    return деректер.getvalue()


def чек_орналастыру():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'мән=42\n'})
    assert қысылған_файлды_қалпына_келтіру('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'мән=42\n'.encode()}
    for деректер in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            қысылған_файлды_қалпына_келтіру('jkoros_fixture-1.0-py3-none-any.whl', деректер, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Жол_2·Өлшемі·C кеңейтім_мән·의존성 қабылдамау_мән')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Орындау_2():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('--host-only', action='store_true')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    чек_орналастыру()
    if Аргументтер.host_only:
        return
    өлшем_жол = жоба_түбір/'build/verification/pip'
    өлшем_жол.mkdir(parents=True, exist_ok=True)
    Жад_жол = өлшем_жол/'cache'
    Жад_жол.mkdir(exist_ok=True)
    # нақты_деректер PyPI 배포 Файл. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    жинау_репозиторий(жоба_түбір/'build/pip-cache').Дайындау('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(жоба_түбір/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Жад_жол/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Жад_жол/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Аты, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'мән=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        деректер = 시험휠(Аты, 파일들)
        (Жад_жол/(Аты+'==1.0.archive')).write_bytes(деректер)
        (Жад_жол/(Аты+'==1.0.json')).write_text(json.dumps({'name': Аты, 'version': '1.0',
            'filename': Аты.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(деректер).hexdigest()}))
    тексеру_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    порт_нөмірі = 빈접속번호()
    Үрдіс = subprocess.Popen(['python3', str(жоба_түбір/'Құралдар/орындау_пәрмен.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(порт_нөмірі), '--pip-cache', str(Жад_жол), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector()
    селектор_a916db4e.register(Үрдіс.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(көрсету_мән=b'jkoros-native> '):
        мазмұн_мән = bytearray()
        끝 = time.monotonic()+120
        while көрсету_мән not in мазмұн_мән:
            if time.monotonic() > 끝 or Үрдіс.poll() is not None:
                raise AssertionError('게스트 жауап 없음: '+мазмұн_мән.decode('utf-8','replace'))
            for енгізу_мән, _ in селектор_a916db4e.select(.1):
                조각 = енгізу_мән.fileobj.read(4096)
                мазмұн_мән.extend(조각)
                대화기록.extend(조각)
        return мазмұн_мән.decode('utf-8', 'replace').replace('\r\n','\n')
    def қоршам(Команда, көрсету_мән=b'jkoros-native> '):
        Үрдіс.stdin.write(Команда.encode()+b'\n')
        Үрдіс.stdin.flush()
        return 기다리기(көрсету_мән)
    def орындау_пәрмен(Команда, 예상, күй_мән=0):
        мазмұн_мән = қоршам(Команда)
        assert 예상 in мазмұн_мән and '\nexit '+str(күй_мән)+'\n' in мазмұн_мән, мазмұн_мән
        тексеру_5fb2b747['checks'].append(Команда)
        return мазмұн_мән
    def Жүктеп_салу_Файлдар(Аты, деректер):
        қоршам('load '+Аты, b'hex> ')
        for лауазым_индекс in range(0, len(деректер), 64):
            қоршам(деректер[лауазым_индекс:лауазым_индекс+64].hex(), b'hex> ')
        assert 'LOADED' in қоршам('.')
    try:
        기다리기()
        орындау_пәрмен('pip --help', 'MicroPython көз_дарақ 설치기')
        Жүктеп_салу_Файлдар('오류시험.py', (жоба_түбір/'시험/파이썬/한국어오류시험.py').read_bytes())
        орындау_пәрмен('python 오류시험.py', '한국어 Файл ерекшелік тексеру')
        орындау_пәрмен('pip install micropython-bisect==3.3.3 --port '+str(порт_нөмірі), 'орнату_мән 완료: micropython-bisect 3.3.3')
        орындау_пәрмен('python -c \'from bisect import insort as 순서대로넣기; мән=[1,5]; 순서대로넣기(мән,3); print(мән)\'', '[1, 3, 5]')
        орындау_пәрмен('python -m pip list', 'micropython-bisect 3.3.3')
        орындау_пәрмен('pip install micropython-bisect==3.3.3 --port '+str(порт_нөмірі), '이미 설치됨:')
        орындау_пәрмен('pip install jkoros-fixture==1.0 --port '+str(порт_нөмірі), 'орнату_мән 완료: jkoros-fixture')
        орындау_пәрмен('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        орындау_пәрмен('pip install jkoros-syntax==1.0 --port '+str(порт_нөмірі), 'жинау Қате:', 1)
        орындау_пәрмен('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Қате 보존")\'', '구문 Қате 보존')
        Жүктеп_салу_Файлдар('공간시험.py', (жоба_түбір/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        орындау_пәрмен('python 공간시험.py '+str(порт_нөмірі), 'жинау мекенжай_аумақ 부족 қайтару_көпір тексеру')
        орындау_пәрмен('pip uninstall jkoros-fixture', 'жою_енгізу 완료: jkoros-fixture')
        орындау_пәрмен('pip uninstall micropython-bisect', 'жою_енгізу 완료: micropython-bisect')
        орындау_пәрмен('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("жою_енгізу тексеру")\'', 'жою_енгізу тексеру')
        тексеру_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 орнату_мән·import·орындау_пәрмен, 한국어 ерекшелік, 패키지 каталог_мән, қате_мән қайтару_көпір, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Шығу_бағдарлама 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Үрдіс.stdin.write(b'\x01x')
            Үрдіс.stdin.flush()
            Үрдіс.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Үрдіс.terminate()
            try:
                Үрдіс.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Үрдіс.kill()
                Үрдіс.wait()
        if Үрдіс.poll() is None:
            Үрдіс.kill()
            Үрдіс.wait()
        селектор_a916db4e.close()
        Үрдіс.stdin.close()
        Үрдіс.stdout.close()
        (өлшем_жол/'serial.log').write_bytes(대화기록)
        (өлшем_жол/'report.json').write_text(json.dumps(тексеру_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Орындау_2()
