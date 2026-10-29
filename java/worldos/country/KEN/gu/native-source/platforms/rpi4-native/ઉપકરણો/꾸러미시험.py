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
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def 시험휠(નામ, 파일들, કામ_મૂલ્ય='Root-Is-Purelib: true\n', 의존성=''):
    ડેટા = io.BytesIO()
    with zipfile.ZipFile(ડેટા, 'w', zipfile.ZIP_DEFLATED) as બન્ડલ:
        બન્ડલ.writestr(નામ + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + કામ_મૂલ્ય)
        બન્ડલ.writestr(નામ + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + નામ + '\nVersion: 1.0\n' + 의존성)
        for પથ, સામગ્રી_મૂલ્ય in 파일들.items():
            બન્ડલ.writestr(પથ, સામગ્રી_મૂલ્ય)
    return ડેટા.getvalue()


def તપાસો_હોસ્ટ():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'મૂલ્ય=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'મૂલ્ય=42\n'.encode()}
    for ડેટા in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', ડેટા, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel પથ·માપ·C એક્સ્ટેંશન_મૂલ્ય·의존성 નકારો_મૂલ્ય')


def ખાલી_પોર્ટ_નંબર():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def ચલાવો_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--host-only', action='store_true')
    દલીલો = 해석기.parse_args()
    તપાસો_હોસ્ટ()
    if દલીલો.host_only:
        return
    પરિમાણ_પાથ = પ્રોજેક્ટ_રૂટ/'build/verification/pip'
    પરિમાણ_પાથ.mkdir(parents=True, exist_ok=True)
    સંગ્રહ_પાથ = પરિમાણ_પાથ/'cache'
    સંગ્રહ_પાથ.mkdir(exist_ok=True)
    # વાસ્તવિક_ડેટા PyPI 배포 ફાઈલ. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    꾸러미저장소(પ્રોજેક્ટ_રૂટ/'build/pip-cache').તૈયાર_કરો('micropython-bisect==3.3.3')
    for પૂચ્છ_મૂલ્ય in ('.archive', '.json'):
        shutil.copyfile(str(પ્રોજેક્ટ_રૂટ/'build/pip-cache'/('micropython-bisect==3.3.3'+પૂચ્છ_મૂલ્ય)), str(સંગ્રહ_પાથ/('micropython-bisect==3.3.3'+પૂચ્છ_મૂલ્ય)))
    હાર્ડવેર_લૉગ = json.loads((સંગ્રહ_પાથ/'micropython-bisect==3.3.3.json').read_text())
    assert હાર્ડવેર_લૉગ['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for નામ, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'મૂલ્ય=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        ડેટા = 시험휠(નામ, 파일들)
        (સંગ્રહ_પાથ/(નામ+'==1.0.archive')).write_bytes(ડેટા)
        (સંગ્રહ_પાથ/(નામ+'==1.0.json')).write_text(json.dumps({'name': નામ, 'version': '1.0',
            'filename': નામ.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(ડેટા).hexdigest()}))
    માન્ય_કરો = {'passed': False, 'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': હાર્ડવેર_લૉગ, 'checks': []}
    પોર્ટ_નંબર = ખાલી_પોર્ટ_નંબર()
    પ્રક્રિયા = subprocess.Popen(['python3', str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_આદેશ.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(પોર્ટ_નંબર), '--pip-cache', str(સંગ્રહ_પાથ), '--ftp-port', str(ખાલી_પોર્ટ_નંબર())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    પસંદકર્તા_a916db4e = selectors.DefaultSelector()
    પસંદકર્તા_a916db4e.register(પ્રક્રિયા.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(શૉ_મૂલ્ય=b'jkoros-native> '):
        સામગ્રી_મૂલ્ય = bytearray()
        끝 = time.monotonic()+120
        while શૉ_મૂલ્ય not in સામગ્રી_મૂલ્ય:
            if time.monotonic() > 끝 or પ્રક્રિયા.poll() is not None:
                raise AssertionError('게스트 જવાબ 없음: '+સામગ્રી_મૂલ્ય.decode('utf-8','replace'))
            for પ્રવેશ_મૂલ્ય, _ in પસંદકર્તા_a916db4e.select(.1):
                조각 = પ્રવેશ_મૂલ્ય.fileobj.read(4096)
                સામગ્રી_મૂલ્ય.extend(조각)
                대화기록.extend(조각)
        return સામગ્રી_મૂલ્ય.decode('utf-8', 'replace').replace('\r\n','\n')
    def શેલ(આદેશ, શૉ_મૂલ્ય=b'jkoros-native> '):
        પ્રક્રિયા.stdin.write(આદેશ.encode()+b'\n')
        પ્રક્રિયા.stdin.flush()
        return 기다리기(શૉ_મૂલ્ય)
    def અમલ_કરો_આદેશ(આદેશ, 예상, સ્થિતિ_મૂલ્ય_e10195a1=0):
        સામગ્રી_મૂલ્ય = શેલ(આદેશ)
        assert 예상 in સામગ્રી_મૂલ્ય and '\nexit '+str(સ્થિતિ_મૂલ્ય_e10195a1)+'\n' in સામગ્રી_મૂલ્ય, સામગ્રી_મૂલ્ય
        માન્ય_કરો['checks'].append(આદેશ)
        return સામગ્રી_મૂલ્ય
    def અપલોડ_કરો_ફાઇલો(નામ, ડેટા):
        શેલ('load '+નામ, b'hex> ')
        for સ્થિતિ_અનુક્રમણિકા in range(0, len(ડેટા), 64):
            શેલ(ડેટા[સ્થિતિ_અનુક્રમણિકા:સ્થિતિ_અનુક્રમણિકા+64].hex(), b'hex> ')
        assert 'LOADED' in શેલ('.')
    try:
        기다리기()
        અમલ_કરો_આદેશ('pip --help', 'MicroPython સ્રોત_ટ્રી 설치기')
        અપલોડ_કરો_ફાઇલો('오류시험.py', (પ્રોજેક્ટ_રૂટ/'시험/파이썬/한국어오류시험.py').read_bytes())
        અમલ_કરો_આદેશ('python 오류시험.py', 'ગુજરાતી ફાઈલ 예외 ચકાસવું')
        અમલ_કરો_આદેશ('pip install micropython-bisect==3.3.3 --port '+str(પોર્ટ_નંબર), 'સ્થાપિત_કરો_મૂલ્ય 완료: micropython-bisect 3.3.3')
        અમલ_કરો_આદેશ('python -c \'from bisect import insort as 순서대로넣기; મૂલ્ય=[1,5]; 순서대로넣기(મૂલ્ય,3); print(મૂલ્ય)\'', '[1, 3, 5]')
        અમલ_કરો_આદેશ('python -m pip list', 'micropython-bisect 3.3.3')
        અમલ_કરો_આદેશ('pip install micropython-bisect==3.3.3 --port '+str(પોર્ટ_નંબર), '이미 설치됨:')
        અમલ_કરો_આદેશ('pip install jkoros-fixture==1.0 --port '+str(પોર્ટ_નંબર), 'સ્થાપિત_કરો_મૂલ્ય 완료: jkoros-fixture')
        અમલ_કરો_આદેશ('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        અમલ_કરો_આદેશ('pip install jkoros-syntax==1.0 --port '+str(પોર્ટ_નંબર), 'બન્ડલ ભૂલ:', 1)
        અમલ_કરો_આદેશ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 ભૂલ 보존")\'', '구문 ભૂલ 보존')
        અપલોડ_કરો_ફાઇલો('공간시험.py', (પ્રોજેક્ટ_રૂટ/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        અમલ_કરો_આદેશ('python 공간시험.py '+str(પોર્ટ_નંબર), 'બન્ડલ 공간 부족 되돌림 ચકાસવું')
        અમલ_કરો_આદેશ('pip uninstall jkoros-fixture', 'કાઢી_નાંખો_પ્રવેશ 완료: jkoros-fixture')
        અમલ_કરો_આદેશ('pip uninstall micropython-bisect', 'કાઢી_નાંખો_પ્રવેશ 완료: micropython-bisect')
        અમલ_કરો_આદેશ('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("કાઢી_નાંખો_પ્રવેશ ચકાસવું")\'', 'કાઢી_નાંખો_પ્રવેશ ચકાસવું')
        માન્ય_કરો['passed'] = True
        print('PASS: PyPI 실물 સ્થાપિત_કરો_મૂલ્ય·import·અમલ_કરો_આદેશ, ગુજરાતી 예외, 패키지 નિર્દેશિકા_મૂલ્ય, નિષ્ફળતા_મૂલ્ય 되돌림, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 પ્રસ્થાન_એપ્લિકેશન 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            પ્રક્રિયા.stdin.write(b'\x01x')
            પ્રક્રિયા.stdin.flush()
            પ્રક્રિયા.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            પ્રક્રિયા.terminate()
            try:
                પ્રક્રિયા.wait(timeout=8)
            except subprocess.TimeoutExpired:
                પ્રક્રિયા.kill()
                પ્રક્રિયા.wait()
        if પ્રક્રિયા.poll() is None:
            પ્રક્રિયા.kill()
            પ્રક્રિયા.wait()
        પસંદકર્તા_a916db4e.close()
        પ્રક્રિયા.stdin.close()
        પ્રક્રિયા.stdout.close()
        (પરિમાણ_પાથ/'serial.log').write_bytes(대화기록)
        (પરિમાણ_પાથ/'report.json').write_text(json.dumps(માન્ય_કરો, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ચલાવો_2()
