#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 إدخال_قيمة·RAM 되돌림을 ذاتي 커널에서 검사한다."""
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
from 꾸러미중계 import يُجمع_مستودع, يُلغي_الضبط
from ينفذ_أمر import يعرض_جذر


def يختبر_قرص(اسم, 파일들, قيمة_العقد='Root-Is-Purelib: true\n', 의존성=''):
    بيانات = io.BytesIO()
    with zipfile.ZipFile(بيانات, 'w', zipfile.ZIP_DEFLATED) as يُجمع:
        يُجمع.writestr(اسم + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + قيمة_العقد)
        يُجمع.writestr(اسم + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + اسم + '\nVersion: 1.0\n' + 의존성)
        for مسار, محتوى_قيمة in 파일들.items():
            يُجمع.writestr(مسار, محتوى_قيمة)
    return بيانات.getvalue()


def شيك_مضيف():
    أنظمة_المعلومات_عادي = يختبر_قرص('jkoros-fixture', {'mod.py': 'قيمة=42\n'})
    assert يُلغي_الضبط('jkoros_fixture-1.0-py3-none-any.whl', أنظمة_المعلومات_عادي, 'jkoros-fixture', '1.0') == {'mod.py': 'قيمة=42\n'.encode()}
    for بيانات in (
            يختبر_قرص('jkoros-fixture', {'../escape.py': ''}),
            يختبر_قرص('jkoros-fixture', {'/abs.py': ''}),
            يختبر_قرص('jkoros-fixture', {'big.py': 'x' * 16385}),
            يختبر_قرص('jkoros-fixture', {'mod.so': ''}),
            يختبر_قرص('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            يختبر_قرص('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            يُلغي_الضبط('jkoros_fixture-1.0-py3-none-any.whl', بيانات, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel مسار·حجم·C ملحق_قيمة·의존성 يرفض_قيمة')


def فارغ_رقم_المنفذ():
    with socket.socket() as مأخذ_التوصيل_قيمة:
        مأخذ_التوصيل_قيمة.bind(('127.0.0.1', 0))
        return مأخذ_التوصيل_قيمة.getsockname()[1]


def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--host-only', action='store_true')
    وسائط = المحلل_48ee4b1b.parse_args()
    شيك_مضيف()
    if وسائط.host_only:
        return
    مقياس_مسار = يعرض_جذر/'build/verification/pip'
    مقياس_مسار.mkdir(parents=True, exist_ok=True)
    تخزين_مسار = مقياس_مسار/'cache'
    تخزين_مسار.mkdir(exist_ok=True)
    # الفعلي_بيانات PyPI توزيع_قيمة ملف. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    يُجمع_مستودع(يعرض_جذر/'build/pip-cache').إعداد('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(يعرض_جذر/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(تخزين_مسار/('micropython-bisect==3.3.3'+꼬리)))
    أجهزة_سجل = json.loads((تخزين_مسار/'micropython-bisect==3.3.3.json').read_text())
    assert أجهزة_سجل['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for اسم, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % رقم: 'قيمة=1\n' for رقم in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        بيانات = يختبر_قرص(اسم, 파일들)
        (تخزين_مسار/(اسم+'==1.0.archive')).write_bytes(بيانات)
        (تخزين_مسار/(اسم+'==1.0.json')).write_text(json.dumps({'name': اسم, 'version': '1.0',
            'filename': اسم.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(بيانات).hexdigest()}))
    التحقق_من_صحة = {'passed': False, 'kernel_sha256': hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': أجهزة_سجل, 'checks': []}
    رقم_المنفذ = فارغ_رقم_المنفذ()
    عملية = subprocess.Popen(['python3', str(يعرض_جذر/'أدوات/ينفذ_أمر.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(رقم_المنفذ), '--pip-cache', str(تخزين_مسار), '--ftp-port', str(فارغ_رقم_المنفذ())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    محدد_a916db4e = selectors.DefaultSelector()
    محدد_a916db4e.register(عملية.stdout, selectors.EVENT_READ)
    نسخة_مكتوبة = bytearray()
    def 기다리기(عرض_قيمة_487749b8=b'jkoros-native> '):
        محتوى_قيمة = bytearray()
        끝 = time.monotonic()+120
        while عرض_قيمة_487749b8 not in محتوى_قيمة:
            if time.monotonic() > 끝 or عملية.poll() is not None:
                raise AssertionError('게스트 رد 없음: '+محتوى_قيمة.decode('utf-8','replace'))
            for إدخال_قيمة_962f286b, _ in محدد_a916db4e.select(.1):
                조각 = إدخال_قيمة_962f286b.fileobj.read(4096)
                محتوى_قيمة.extend(조각)
                نسخة_مكتوبة.extend(조각)
        return محتوى_قيمة.decode('utf-8', 'replace').replace('\r\n','\n')
    def 셸(أمر, عرض_قيمة_487749b8=b'jkoros-native> '):
        عملية.stdin.write(أمر.encode()+b'\n')
        عملية.stdin.flush()
        return 기다리기(عرض_قيمة_487749b8)
    def ينفذ_أمر(أمر, 예상, حالة_قيمة=0):
        محتوى_قيمة = 셸(أمر)
        assert 예상 in محتوى_قيمة and '\nexit '+str(حالة_قيمة)+'\n' in محتوى_قيمة, محتوى_قيمة
        التحقق_من_صحة['checks'].append(أمر)
        return محتوى_قيمة
    def تحميل_الملفات(اسم, بيانات):
        셸('load '+اسم, b'hex> ')
        for منصب_فهرس in range(0, len(بيانات), 64):
            셸(بيانات[منصب_فهرس:منصب_فهرس+64].hex(), b'hex> ')
        assert 'LOADED' in 셸('.')
    try:
        기다리기()
        ينفذ_أمر('pip --help', 'MicroPython مصدر_شجرة 설치기')
        تحميل_الملفات('오류시험.py', (يعرض_جذر/'اختبارات/파이썬/한국어오류시험.py').read_bytes())
        ينفذ_أمر('python 오류시험.py', 'العربية ملف استثناء يتحقق')
        ينفذ_أمر('pip install micropython-bisect==3.3.3 --port '+str(رقم_المنفذ), 'تثبيت_قيمة 완료: micropython-bisect 3.3.3')
        ينفذ_أمر('python -c \'from bisect import insort as 순서대로넣기; قيمة=[1,5]; 순서대로넣기(قيمة,3); print(قيمة)\'', '[1, 3, 5]')
        ينفذ_أمر('python -m pip list', 'micropython-bisect 3.3.3')
        ينفذ_أمر('pip install micropython-bisect==3.3.3 --port '+str(رقم_المنفذ), '이미 설치됨:')
        ينفذ_أمر('pip install jkoros-fixture==1.0 --port '+str(رقم_المنفذ), 'تثبيت_قيمة 완료: jkoros-fixture')
        ينفذ_أمر('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        ينفذ_أمر('pip install jkoros-syntax==1.0 --port '+str(رقم_المنفذ), 'يُجمع خطأ:', 1)
        ينفذ_أمر('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 خطأ 보존")\'', '구문 خطأ 보존')
        تحميل_الملفات('공간시험.py', (يعرض_جذر/'اختبارات/파이썬/يُجمع_مساحة_الاسم_يختبر.py').read_bytes())
        ينفذ_أمر('python 공간시험.py '+str(رقم_المنفذ), 'يُجمع عنوان_منطقة 부족 إرجاع_جسر يتحقق')
        ينفذ_أمر('pip uninstall jkoros-fixture', 'يزيل_إدخال 완료: jkoros-fixture')
        ينفذ_أمر('pip uninstall micropython-bisect', 'يزيل_إدخال 완료: micropython-bisect')
        ينفذ_أمر('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("يزيل_إدخال يتحقق")\'', 'يزيل_إدخال يتحقق')
        التحقق_من_صحة['passed'] = True
        print('PASS: PyPI 실물 تثبيت_قيمة·import·ينفذ_أمر, العربية استثناء, 패키지 دليل_قيمة, فشل_قيمة إرجاع_جسر, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 خروج_تطبيق 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            عملية.stdin.write(b'\x01x')
            عملية.stdin.flush()
            عملية.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            عملية.terminate()
            try:
                عملية.wait(timeout=8)
            except subprocess.TimeoutExpired:
                عملية.kill()
                عملية.wait()
        if عملية.poll() is None:
            عملية.kill()
            عملية.wait()
        محدد_a916db4e.close()
        عملية.stdin.close()
        عملية.stdout.close()
        (مقياس_مسار/'serial.log').write_bytes(نسخة_مكتوبة)
        (مقياس_مسار/'report.json').write_text(json.dumps(التحقق_من_صحة, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    تشغيل()
