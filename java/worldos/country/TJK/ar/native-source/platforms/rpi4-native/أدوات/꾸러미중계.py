#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 تثبيت_قيمة·실행한다."""
import argparse
import email.parser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import socketserver
import struct
import tarfile
import threading
import urllib.request
import zipfile

يعرض_جذر = Path(__file__).resolve().parents[1]


def يوزّع_طلب(طلب):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', طلب)
    if not 맞음:
        raise ValueError('يُجمع اسم 또는 اسم==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def التحقق_من_صحة_مسار_f98b46e1(اسم, تثبيت_مسار=True):
    مسار = PurePosixPath(اسم)
    if مسار.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in اسم.split('/')):
        raise ValueError('허용하지 않는 يُجمع مسار: ' + اسم)
    if '\\' in اسم or any(ord(حرف_قيمة) < 32 or ord(حرف_قيمة) == 127 for حرف_قيمة in اسم):
        raise ValueError('잘못된 يُجمع مسار 문자')
    if تثبيت_مسار and (len(('/lib/' + اسم).encode()) > 63 or اسم in ('العربية.py', 'يُجمع.py')):
        raise ValueError('يُجمع مسار 제한 또는 قيمة_افتراضية مكتبة 충돌: ' + اسم)
    return اسم


def يُلغي_الضبط(ملف_إدخال_اسم, بيانات, اسم, إصدار_قيمة):
    파일들 = {}
    명세들 = []
    def إلحاق_إدخال(مسار, محتوى_قيمة):
        التحقق_من_صحة_مسار_f98b46e1(مسار)
        if مسار in 파일들:
            raise ValueError('중복 يُجمع مسار: ' + مسار)
        if len(محتوى_قيمة) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + مسار)
        محتوى_قيمة.decode('utf-8')
        파일들[مسار] = محتوى_قيمة
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 مصدر_شجرة 16개·إجمالي_قيمة 64 KiB 이하여야 합니다.')
    if ملف_إدخال_اسم.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(بيانات)) as يُجمع:
            항목들 = يُجمع.infolist()
            if len(항목들) > 256 or sum(إدخال_قيمة_962f286b.file_size for إدخال_قيمة_962f286b in 항목들) > 1048576:
                raise ValueError('أرشيف_قيمة إصدار_تخزين حجم 제한 초과')
            عقد_قائمة = [إدخال_قيمة_962f286b for إدخال_قيمة_962f286b in 항목들 if إدخال_قيمة_962f286b.filename.endswith('.dist-info/WHEEL')]
            if len(عقد_قائمة) != 1:
                raise ValueError('wheel قيمة_العقد 명세가 필요합니다.')
            قيمة_العقد = email.parser.Parser().parsestr(يُجمع.read(عقد_قائمة[0]).decode())
            if قيمة_العقد.get('Root-Is-Purelib', '').lower() != 'true' or not ملف_إدخال_اسم.endswith('-none-any.whl'):
                raise ValueError('C ملحق_قيمة·플랫폼 전용 wheel은 지원하지 않습니다.')
            for إدخال_قيمة_962f286b in 항목들:
                مسار = إدخال_قيمة_962f286b.filename.rstrip('/')
                التحقق_من_صحة_مسار_f98b46e1(مسار, False)
                if (إدخال_قيمة_962f286b.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 رقم 없습니다.')
                if إدخال_قيمة_962f286b.filename.endswith('/'):
                    continue
                if '.dist-info/' in مسار:
                    if مسار.endswith('/METADATA'):
                        명세들.append(يُجمع.read(إدخال_قيمة_962f286b).decode())
                    continue
                if not مسار.endswith('.py') or '.data/' in مسار:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + مسار)
                إلحاق_إدخال(مسار, يُجمع.read(إدخال_قيمة_962f286b))
    elif ملف_إدخال_اسم.endswith('.tar.gz') and اسم.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ينفذ_أمر 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(بيانات), mode='r|gz') as يُجمع:
            뿌리들 = set()
            항목수 = 0
            إجمالي_يغير_الحجم = 0
            for إدخال_قيمة_962f286b in يُجمع:
                항목수 += 1
                إجمالي_يغير_الحجم += إدخال_قيمة_962f286b.size
                if 항목수 > 256 or إجمالي_يغير_الحجم > 1048576:
                    raise ValueError('أرشيف_قيمة إصدار_تخزين حجم 제한 초과')
                التحقق_من_صحة_مسار_f98b46e1(إدخال_قيمة_962f286b.name, False)
                부분들 = إدخال_قيمة_962f286b.name.split('/')
                뿌리들.add(부분들[0])
                if إدخال_قيمة_962f286b.isdir():
                    continue
                if not إدخال_قيمة_962f286b.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython مصدر_شجرة 배포형')
                مسار = '/'.join(부분들[1:])
                محتوى_قيمة = يُجمع.extractfile(إدخال_قيمة_962f286b).read()
                if مسار.endswith('PKG-INFO'):
                    명세들.append(محتوى_قيمة.decode())
                elif مسار.endswith('.py') and مسار not in ('setup.py',):
                    إلحاق_إدخال(مسار, محتوى_قيمة)
                elif '.egg-info/' not in مسار and not مسار.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + مسار)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 جذر_قيمة 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* مصدر_شجرة 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 توزيع_قيمة 메타데이터가 필요합니다.')
    المواصفات = email.parser.Parser().parsestr(명세들[0])
    if يوزّع_طلب(المواصفات.get('Name', ''))[0] != اسم or المواصفات.get('Version') != إصدار_قيمة:
        raise ValueError('توزيع_قيمة 메타데이터의 اسم·버전 불일치')
    if المواصفات.get_all('Requires-Dist') or المواصفات.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def يقرأ_ويب(عنوان, 한도):
    if not عنوان.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS توزيع_قيمة 주소만 허용합니다.')
    with urllib.request.urlopen(عنوان, timeout=30) as رد:
        if not رد.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 توزيع_قيمة عنوان نقل_قيمة')
        بيانات = رد.read(한도 + 1)
    if len(بيانات) > 한도:
        raise ValueError('توزيع_قيمة ملف حجم 제한 초과')
    return بيانات


def نقل_يُجمع(اسم, إصدار_قيمة, 파일들, نقطة_الأصل_قيمة):
    المواصفات = {'name': اسم, 'version': إصدار_قيمة, 'source': نقطة_الأصل_قيمة, 'files': [
        {'path': مسار, 'size': len(بيانات), 'sha256': hashlib.sha256(بيانات).hexdigest()}
        for مسار, بيانات in sorted(파일들.items())]}
    رأس_قيمة = json.dumps(المواصفات, ensure_ascii=False).encode()
    if len(رأس_قيمة) > 8192:
        raise ValueError('يُجمع المواصفات حجم 초과')
    return b'JKP1' + struct.pack('>I', len(رأس_قيمة)) + رأس_قيمة + b''.join(파일들[إدخال_قيمة_962f286b['path']] for إدخال_قيمة_962f286b in المواصفات['files'])


class يُجمع_مستودع:
    def __init__(자신, مسار, أنظمة_المعلومات_غير_متصل=False):
        자신.مسار = Path(مسار)
        자신.مسار.mkdir(parents=True, exist_ok=True)
        자신.أنظمة_المعلومات_غير_متصل = أنظمة_المعلومات_غير_متصل

    def إعداد(자신, طلب):
        اسم, إصدار_قيمة = يوزّع_طلب(طلب)
        열쇠 = اسم + ('==' + إصدار_قيمة if إصدار_قيمة else '')
        سجل_مسار = 자신.مسار / (열쇠 + '.json')
        توزيع_مسار = 자신.مسار / (열쇠 + '.archive')
        if سجل_مسار.is_file() and توزيع_مسار.is_file():
            سجل_سجل = json.loads(سجل_مسار.read_text())
            بيانات = توزيع_مسار.read_bytes()
            if hashlib.sha256(بيانات).hexdigest() != سجل_سجل['sha256']:
                raise ValueError('저장된 توزيع_قيمة 파일의 SHA-256 불일치')
        else:
            if 자신.أنظمة_المعلومات_غير_متصل:
                raise ValueError('أنظمة_المعلومات_غير_متصل 저장소에 없는 يُجمع: ' + طلب)
            عنوان = 'https://pypi.org/pypi/' + اسم + ('/' + إصدار_قيمة if إصدار_قيمة else '') + '/json'
            معلومات_النظام = json.loads(يقرأ_ويب(عنوان, 4194304).decode())
            if معلومات_النظام['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [إدخال_قيمة_962f286b for إدخال_قيمة_962f286b in معلومات_النظام['urls'] if not إدخال_قيمة_962f286b.get('yanked') and إدخال_قيمة_962f286b['filename'].endswith('-none-any.whl')]
            if not 후보 and اسم.startswith('micropython-'):
                후보 = [إدخال_قيمة_962f286b for إدخال_قيمة_962f286b in معلومات_النظام['urls'] if not إدخال_قيمة_962f286b.get('yanked') and إدخال_قيمة_962f286b['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python توزيع_قيمة 파일이 없습니다.')
            تحديد_قيمة = 후보[0]
            بيانات = يقرأ_ويب(تحديد_قيمة['url'], 4194304)
            if hashlib.sha256(بيانات).hexdigest() != تحديد_قيمة['digests']['sha256']:
                raise ValueError('PyPI توزيع_قيمة ملف SHA-256 불일치')
            سجل_سجل = {'name': اسم, 'version': معلومات_النظام['info']['version'], 'filename': تحديد_قيمة['filename'],
                    'url': تحديد_قيمة['url'], 'sha256': تحديد_قيمة['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            يُلغي_الضبط(سجل_سجل['filename'], بيانات, اسم, سجل_سجل['version'])
            توزيع_مسار.write_bytes(بيانات)
            سجل_مسار.write_text(json.dumps(سجل_سجل, ensure_ascii=False, indent=2) + '\n')
        if سجل_سجل['name'] != اسم or إصدار_قيمة and سجل_سجل['version'] != إصدار_قيمة:
            raise ValueError('مستودع_جذر اسم·버전 불일치')
        파일들 = يُلغي_الضبط(سجل_سجل['filename'], بيانات, اسم, سجل_سجل['version'])
        return نقل_يُجمع(اسم, سجل_سجل['version'], 파일들, سجل_سجل['url'])


class يُجمع_طلب(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            طلب = bytearray()
            while b'\n' not in طلب and len(طلب) < 100:
                조각 = 자신.request.recv(100 - len(طلب))
                if not 조각:
                    return
                طلب.extend(조각)
            if not طلب.endswith(b'\n') or طلب.count(b'\n') != 1:
                raise ValueError('잘못된 يُجمع طلب')
            رد = 자신.server.مستودع_جذر.إعداد(طلب[:-1].decode('ascii'))
        except Exception as خطأ:
            رأس_قيمة = json.dumps({'error': str(خطأ)[:500]}, ensure_ascii=False).encode()
            رد = b'JKP1' + struct.pack('>I', len(رأس_قيمة)) + رأس_قيمة
        try:
            자신.request.sendall(رد)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, رقم_المنفذ=8027, مسار=None, أنظمة_المعلومات_غير_متصل=False):
        자신.خادم_قيمة = socketserver.TCPServer(('127.0.0.1', رقم_المنفذ), يُجمع_طلب, bind_and_activate=False)
        자신.خادم_قيمة.allow_reuse_address = True
        자신.خادم_قيمة.server_bind()
        자신.خادم_قيمة.server_activate()
        자신.خادم_قيمة.مستودع_جذر = يُجمع_مستودع(مسار or يعرض_جذر/'build/pip-cache', أنظمة_المعلومات_غير_متصل)
        자신.رقم_المنفذ = 자신.خادم_قيمة.server_address[1]
        자신.محادثة_قيمة = threading.Thread(target=자신.خادم_قيمة.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.محادثة_قيمة.start()
        return 자신

    def __exit__(자신, *وسائط):
        자신.خادم_قيمة.shutdown()
        자신.خادم_قيمة.server_close()
        자신.محادثة_قيمة.join(timeout=2)


def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--port', type=int, default=8027)
    المحلل_48ee4b1b.add_argument('--cache', type=Path, default=يعرض_جذر/'build/pip-cache')
    المحلل_48ee4b1b.add_argument('--offline', action='store_true')
    المحلل_48ee4b1b.add_argument('--fetch', help='ينفذ_أمر 없이 호환 توزيع_قيمة 파일을 내려받아 검사·مخزن_قيمة')
    وسائط = المحلل_48ee4b1b.parse_args()
    if وسائط.fetch:
        بيانات = يُجمع_مستودع(وسائط.cache, وسائط.offline).إعداد(وسائط.fetch)
        print('يُجمع إعداد 완료:', وسائط.fetch, len(بيانات), 'بايت_قيمة')
        return
    with 꾸러미중계(وسائط.port, وسائط.cache, وسائط.offline) as 중계:
        print('يُجمع 중계: 127.0.0.1:' + str(중계.رقم_المنفذ), flush=True)
        try:
            중계.محادثة_قيمة.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    تشغيل()
