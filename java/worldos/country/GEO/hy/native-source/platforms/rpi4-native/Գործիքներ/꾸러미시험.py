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
from կատարել_հրաման import արձակել_արմատ


def 시험휠(Անուն, 파일들, գործ_արժեք='Root-Is-Purelib: true\n', 의존성=''):
    տվյալ = io.BytesIO()
    with zipfile.ZipFile(տվյալ, 'w', zipfile.ZIP_DEFLATED) as փաթեթ:
        փաթեթ.writestr(Անուն + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + գործ_արժեք)
        փաթեթ.writestr(Անուն + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Անուն + '\nVersion: 1.0\n' + 의존성)
        for Ճանապարհ, Բովանդակություն_արժեք in 파일들.items():
            փաթեթ.writestr(Ճանապարհ, Բովանդակություն_արժեք)
    return տվյալ.getvalue()


def կտրոն_հոստ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'արժեք=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'արժեք=42\n'.encode()}
    for տվյալ in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', տվյալ, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel Ճանապարհ·Չափս·C ընդլայնում_արժեք·의존성 거부')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Գործարկել():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    인수 = 해석기.parse_args()
    կտրոն_հոստ()
    if 인수.host_only:
        return
    չափ_ուղի = արձակել_արմատ/'build/verification/pip'
    չափ_ուղի.mkdir(parents=True, exist_ok=True)
    Պահեստ_ուղի = չափ_ուղի/'cache'
    Պահեստ_ուղի.mkdir(exist_ok=True)
    # իրական_տվյալ PyPI 배포 Ֆայլ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(արձակել_արմատ/'build/pip-cache').Պատրաստել('micropython-bisect==3.3.3')
    for պոչ_արժեք in ('.archive', '.json'):
        shutil.copyfile(str(արձակել_արմատ/'build/pip-cache'/('micropython-bisect==3.3.3'+պոչ_արժեք)), str(Պահեստ_ուղի/('micropython-bisect==3.3.3'+պոչ_արժեք)))
    실물기록 = json.loads((Պահեստ_ուղի/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Անուն, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'արժեք=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        տվյալ = 시험휠(Անուն, 파일들)
        (Պահեստ_ուղի/(Անուն+'==1.0.archive')).write_bytes(տվյալ)
        (Պահեստ_ուղի/(Անուն+'==1.0.json')).write_text(json.dumps({'name': Անուն, 'version': '1.0',
            'filename': Անուն.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(տվյալ).hexdigest()}))
    վավերացնել = {'passed': False, 'kernel_sha256': hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    접속번호 = 빈접속번호()
    Գործընթաց = subprocess.Popen(['python3', str(արձակել_արմատ/'Գործիքներ/կատարել_հրաման.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(접속번호), '--pip-cache', str(Պահեստ_ուղի), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ընտրիչ_a916db4e = selectors.DefaultSelector()
    ընտրիչ_a916db4e.register(Գործընթաց.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(ցուցադրել_արժեք=b'jkoros-native> '):
        Բովանդակություն_արժեք = bytearray()
        끝 = time.monotonic()+120
        while ցուցադրել_արժեք not in Բովանդակություն_արժեք:
            if time.monotonic() > 끝 or Գործընթաց.poll() is not None:
                raise AssertionError('게스트 պատասխանել 없음: '+Բովանդակություն_արժեք.decode('utf-8','replace'))
            for մուտքագրում_արժեք, _ in ընտրիչ_a916db4e.select(.1):
                조각 = մուտքագրում_արժեք.fileobj.read(4096)
                Բովանդակություն_արժեք.extend(조각)
                대화기록.extend(조각)
        return Բովանդակություն_արժեք.decode('utf-8', 'replace').replace('\r\n','\n')
    def խեցի(Հրահանգ, ցուցադրել_արժեք=b'jkoros-native> '):
        Գործընթաց.stdin.write(Հրահանգ.encode()+b'\n')
        Գործընթաց.stdin.flush()
        return 기다리기(ցուցադրել_արժեք)
    def կատարել_հրաման(Հրահանգ, 예상, վիճակ_արժեք=0):
        Բովանդակություն_արժեք = խեցի(Հրահանգ)
        assert 예상 in Բովանդակություն_արժեք and '\nexit '+str(վիճակ_արժեք)+'\n' in Բովանդակություն_արժեք, Բովանդակություն_արժեք
        վավերացնել['checks'].append(Հրահանգ)
        return Բովանդակություն_արժեք
    def վերբեռնել_Նիշքեր(Անուն, տվյալ):
        խեցի('load '+Անուն, b'hex> ')
        for դիրք_դասիչ in range(0, len(տվյալ), 64):
            խեցի(տվյալ[դիրք_դասիչ:դիրք_դասիչ+64].hex(), b'hex> ')
        assert 'LOADED' in խեցի('.')
    try:
        기다리기()
        կատարել_հրաման('pip --help', 'MicroPython աղբյուր_ծառ 설치기')
        վերբեռնել_Նիշքեր('오류시험.py', (արձակել_արմատ/'시험/파이썬/한국어오류시험.py').read_bytes())
        կատարել_հրաման('python 오류시험.py', '한국어 Ֆայլ 예외 հաստատել')
        կատարել_հրաման('pip install micropython-bisect==3.3.3 --port '+str(접속번호), 'տեղադրել_արժեք 완료: micropython-bisect 3.3.3')
        կատարել_հրաման('python -c \'from bisect import insort as 순서대로넣기; արժեք=[1,5]; 순서대로넣기(արժեք,3); print(արժեք)\'', '[1, 3, 5]')
        կատարել_հրաման('python -m pip list', 'micropython-bisect 3.3.3')
        կատարել_հրաման('pip install micropython-bisect==3.3.3 --port '+str(접속번호), '이미 설치됨:')
        կատարել_հրաման('pip install jkoros-fixture==1.0 --port '+str(접속번호), 'տեղադրել_արժեք 완료: jkoros-fixture')
        կատարել_հրաման('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        կատարել_հրաման('pip install jkoros-syntax==1.0 --port '+str(접속번호), 'փաթեթ Սխալ:', 1)
        կատարել_հրաման('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 Սխալ 보존")\'', '구문 Սխալ 보존')
        վերբեռնել_Նիշքեր('공간시험.py', (արձակել_արմատ/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        կատարել_հրաման('python 공간시험.py '+str(접속번호), 'փաթեթ 공간 부족 վերադարձնել_կամուրջ հաստատել')
        կատարել_հրաման('pip uninstall jkoros-fixture', 'հեռացնել_մուտքագրում 완료: jkoros-fixture')
        կատարել_հրաման('pip uninstall micropython-bisect', 'հեռացնել_մուտքագրում 완료: micropython-bisect')
        կատարել_հրաման('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("հեռացնել_մուտքագրում հաստատել")\'', 'հեռացնել_մուտքագրում հաստատել')
        վավերացնել['passed'] = True
        print('PASS: PyPI 실물 տեղադրել_արժեք·import·կատարել_հրաման, 한국어 예외, 패키지 գրացուցակ_արժեք, ձախողում_արժեք վերադարձնել_կամուրջ, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Ելք_ծրագիր 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Գործընթաց.stdin.write(b'\x01x')
            Գործընթաց.stdin.flush()
            Գործընթաց.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Գործընթաց.terminate()
            try:
                Գործընթաց.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Գործընթաց.kill()
                Գործընթաց.wait()
        if Գործընթաց.poll() is None:
            Գործընթաց.kill()
            Գործընթաց.wait()
        ընտրիչ_a916db4e.close()
        Գործընթաց.stdin.close()
        Գործընթաց.stdout.close()
        (չափ_ուղի/'serial.log').write_bytes(대화기록)
        (չափ_ուղի/'report.json').write_text(json.dumps(վավերացնել, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Գործարկել()
