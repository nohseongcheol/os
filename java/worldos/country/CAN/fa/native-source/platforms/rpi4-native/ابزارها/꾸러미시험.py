#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 بومی 커널에서 검사한다."""
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
from 꾸러미중계 import دسته_کردن_مخزن, 압축풀기
from اجرا_فرمان import نمایش_دادن_جذر


def 시험휠(نام, 파일들, شغل_مقدار='Root-Is-Purelib: true\n', 의존성=''):
    داده_ها = io.BytesIO()
    with zipfile.ZipFile(داده_ها, 'w', zipfile.ZIP_DEFLATED) as دسته_کردن:
        دسته_کردن.writestr(نام + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + شغل_مقدار)
        دسته_کردن.writestr(نام + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + نام + '\nVersion: 1.0\n' + 의존성)
        for مسیر, محتوا_مقدار in 파일들.items():
            دسته_کردن.writestr(مسیر, محتوا_مقدار)
    return داده_ها.getvalue()


def بررسی_میزبان():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'مقدار=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'مقدار=42\n'.encode()}
    for داده_ها in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', داده_ها, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel مسیر·اندازه·C تمدید_مقدار·의존성 رد_کردن_مقدار')


def خالی_شماره_درگاه():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def اجرا_2():
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('--host-only', action='store_true')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    بررسی_میزبان()
    if نشانوندها.host_only:
        return
    سنجش_مسیر = نمایش_دادن_جذر/'build/verification/pip'
    سنجش_مسیر.mkdir(parents=True, exist_ok=True)
    حافظه_تلفن_مسیر = سنجش_مسیر/'cache'
    حافظه_تلفن_مسیر.mkdir(exist_ok=True)
    # واقعی_داده_ها PyPI 배포 پرونده. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    دسته_کردن_مخزن(نمایش_دادن_جذر/'build/pip-cache').آماده_کردن('micropython-bisect==3.3.3')
    for انتها_مقدار in ('.archive', '.json'):
        shutil.copyfile(str(نمایش_دادن_جذر/'build/pip-cache'/('micropython-bisect==3.3.3'+انتها_مقدار)), str(حافظه_تلفن_مسیر/('micropython-bisect==3.3.3'+انتها_مقدار)))
    실물기록 = json.loads((حافظه_تلفن_مسیر/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for نام, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'مقدار=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        داده_ها = 시험휠(نام, 파일들)
        (حافظه_تلفن_مسیر/(نام+'==1.0.archive')).write_bytes(داده_ها)
        (حافظه_تلفن_مسیر/(نام+'==1.0.json')).write_text(json.dumps({'name': نام, 'version': '1.0',
            'filename': نام.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(داده_ها).hexdigest()}))
    ارزیابی_کردن = {'passed': False, 'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    شماره_درگاه = خالی_شماره_درگاه()
    فرآیند = subprocess.Popen(['python3', str(نمایش_دادن_جذر/'ابزارها/اجرا_فرمان.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(شماره_درگاه), '--pip-cache', str(حافظه_تلفن_مسیر), '--ftp-port', str(خالی_شماره_درگاه())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    انتخاب_کننده_a916db4e = selectors.DefaultSelector()
    انتخاب_کننده_a916db4e.register(فرآیند.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(نمایش_مقدار=b'jkoros-native> '):
        محتوا_مقدار = bytearray()
        끝 = time.monotonic()+120
        while نمایش_مقدار not in محتوا_مقدار:
            if time.monotonic() > 끝 or فرآیند.poll() is not None:
                raise AssertionError('게스트 پاسخ_دادن 없음: '+محتوا_مقدار.decode('utf-8','replace'))
            for ورودی_مقدار, _ in انتخاب_کننده_a916db4e.select(.1):
                조각 = ورودی_مقدار.fileobj.read(4096)
                محتوا_مقدار.extend(조각)
                대화기록.extend(조각)
        return محتوا_مقدار.decode('utf-8', 'replace').replace('\r\n','\n')
    def واسط(فرمان, نمایش_مقدار=b'jkoros-native> '):
        فرآیند.stdin.write(فرمان.encode()+b'\n')
        فرآیند.stdin.flush()
        return 기다리기(نمایش_مقدار)
    def اجرا_فرمان(فرمان, 예상, وضعیت_مقدار=0):
        محتوا_مقدار = واسط(فرمان)
        assert 예상 in محتوا_مقدار and '\nexit '+str(وضعیت_مقدار)+'\n' in محتوا_مقدار, محتوا_مقدار
        ارزیابی_کردن['checks'].append(فرمان)
        return محتوا_مقدار
    def آپلود_فایل(نام, داده_ها):
        واسط('load '+نام, b'hex> ')
        for مرتب_کردن_فهرست in range(0, len(داده_ها), 64):
            واسط(داده_ها[مرتب_کردن_فهرست:مرتب_کردن_فهرست+64].hex(), b'hex> ')
        assert 'LOADED' in واسط('.')
    try:
        기다리기()
        اجرا_فرمان('pip --help', 'MicroPython منبع_درخت 설치기')
        آپلود_فایل('오류시험.py', (نمایش_دادن_جذر/'시험/파이썬/한국어오류시험.py').read_bytes())
        اجرا_فرمان('python 오류시험.py', 'فارسی پرونده استثنا تأیید_صحت')
        اجرا_فرمان('pip install micropython-bisect==3.3.3 --port '+str(شماره_درگاه), 'نصب_مقدار 완료: micropython-bisect 3.3.3')
        اجرا_فرمان('python -c \'from bisect import insort as 순서대로넣기; مقدار=[1,5]; 순서대로넣기(مقدار,3); print(مقدار)\'', '[1, 3, 5]')
        اجرا_فرمان('python -m pip list', 'micropython-bisect 3.3.3')
        اجرا_فرمان('pip install micropython-bisect==3.3.3 --port '+str(شماره_درگاه), '이미 설치됨:')
        اجرا_فرمان('pip install jkoros-fixture==1.0 --port '+str(شماره_درگاه), 'نصب_مقدار 완료: jkoros-fixture')
        اجرا_فرمان('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        اجرا_فرمان('pip install jkoros-syntax==1.0 --port '+str(شماره_درگاه), 'دسته_کردن خطا:', 1)
        اجرا_فرمان('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 خطا 보존")\'', '구문 خطا 보존')
        آپلود_فایل('공간시험.py', (نمایش_دادن_جذر/'시험/파이썬/꾸러미공간시험.py').read_bytes())
        اجرا_فرمان('python 공간시험.py '+str(شماره_درگاه), 'دسته_کردن 공간 부족 بازگرداندن_پل تأیید_صحت')
        اجرا_فرمان('pip uninstall jkoros-fixture', 'حذف_ورودی 완료: jkoros-fixture')
        اجرا_فرمان('pip uninstall micropython-bisect', 'حذف_ورودی 완료: micropython-bisect')
        اجرا_فرمان('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("حذف_ورودی تأیید_صحت")\'', 'حذف_ورودی تأیید_صحت')
        ارزیابی_کردن['passed'] = True
        print('PASS: PyPI 실물 نصب_مقدار·import·اجرا_فرمان, فارسی استثنا, 패키지 فهرست_مقدار_e5561a2b, عدم_موفقیت_مقدار بازگرداندن_پل, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 خروج_برنامه 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            فرآیند.stdin.write(b'\x01x')
            فرآیند.stdin.flush()
            فرآیند.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            فرآیند.terminate()
            try:
                فرآیند.wait(timeout=8)
            except subprocess.TimeoutExpired:
                فرآیند.kill()
                فرآیند.wait()
        if فرآیند.poll() is None:
            فرآیند.kill()
            فرآیند.wait()
        انتخاب_کننده_a916db4e.close()
        فرآیند.stdin.close()
        فرآیند.stdout.close()
        (سنجش_مسیر/'serial.log').write_bytes(대화기록)
        (سنجش_مسیر/'report.json').write_text(json.dumps(ارزیابی_کردن, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    اجرا_2()
