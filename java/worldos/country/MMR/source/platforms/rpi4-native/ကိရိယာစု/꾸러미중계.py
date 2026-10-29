#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 တန်ဖိုးတပ်ဆင်·실행한다."""
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

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]


def တောင်းဆိုချက်သဒ္ဒါခွဲခြမ်း(တောင်းဆိုချက်):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', တောင်းဆိုချက်)
    if not 맞음:
        raise ValueError('အထုပ် အမည် 또는 အမည်==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def လမ်းကြောင်းမှန်ကန်ကြောင်းစစ်(အမည်, 설치경로=True):
    လမ်း = PurePosixPath(အမည်)
    if လမ်း.is_absolute() or any(အစိတ်အပိုင်းတန်ဖိုး in ('', '.', '..') or အစိတ်အပိုင်းတန်ဖိုး.startswith('.') for အစိတ်အပိုင်းတန်ဖိုး in အမည်.split('/')):
        raise ValueError('허용하지 않는 အထုပ် လမ်း: ' + အမည်)
    if '\\' in အမည် or any(ord(အက္ခရာတန်ဖိုး) < 32 or ord(အက္ခရာတန်ဖိုး) == 127 for အက္ခရာတန်ဖိုး in အမည်):
        raise ValueError('잘못된 အထုပ် လမ်း အက္ခရာ')
    if 설치경로 and (len(('/lib/' + အမည်).encode()) > 63 or အမည် in ('မြန်မာ.py', 'အထုပ်.py')):
        raise ValueError('အထုပ် လမ်း ကန့်သတ်ချက်တန်ဖိုး 또는 မူလသတ်မှတ်တန်ဖိုး စာကြည့်တိုက် 충돌: ' + အမည်)
    return အမည်


def 압축풀기(ဖိုင်အချက်အမည်, ဒေတာ, အမည်, ထုတ်ဝေမှုတန်ဖိုး):
    ဖိုင်အချက်များ = {}
    명세들 = []
    def အချက်နောက်တွဲ(လမ်း, အကြောင်းအရာတန်ဖိုး):
        လမ်းကြောင်းမှန်ကန်ကြောင်းစစ်(လမ်း)
        if လမ်း in ဖိုင်အချက်များ:
            raise ValueError('중복 အထုပ် လမ်း: ' + လမ်း)
        if len(အကြောင်းအရာတန်ဖိုး) > 16384:
            raise ValueError('파일당 16 KiB ကန့်သတ်ချက်တန်ဖိုး 초과: ' + လမ်း)
        အကြောင်းအရာတန်ဖိုး.decode('utf-8')
        ဖိုင်အချက်များ[လမ်း] = အကြောင်းအရာတန်ဖိုး
        if len(ဖိုင်အချက်များ) > 16 or sum(map(len, ဖိုင်အချက်များ.values())) > 65536:
            raise ValueError('꾸러미는 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 16개·အကုန်စုစုပေါင်းတန်ဖိုး 64 KiB 이하여야 합니다.')
    if ဖိုင်အချက်အမည်.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ဒေတာ)) as အထုပ်:
            항목들 = အထုပ်.infolist()
            if len(항목들) > 256 or sum(အချက်တန်ဖိုး.file_size for အချက်တန်ဖိုး in 항목들) > 1048576:
                raise ValueError('မော်ကွန်းတန်ဖိုး သိုလှောင်ရာလွှတ်ပေး အရွယ် ကန့်သတ်ချက်တန်ဖိုး 초과')
            သဘောတူစည်းမျဉ်းစာရင်း = [အချက်တန်ဖိုး for အချက်တန်ဖိုး in 항목들 if အချက်တန်ဖိုး.filename.endswith('.dist-info/WHEEL')]
            if len(သဘောတူစည်းမျဉ်းစာရင်း) != 1:
                raise ValueError('wheel သဘောတူစည်းမျဉ်းတန်ဖိုး 명세가 필요합니다.')
            သဘောတူစည်းမျဉ်းတန်ဖိုး = email.parser.Parser().parsestr(အထုပ်.read(သဘောတူစည်းမျဉ်းစာရင်း[0]).decode())
            if သဘောတူစည်းမျဉ်းတန်ဖိုး.get('Root-Is-Purelib', '').lower() != 'true' or not ဖိုင်အချက်အမည်.endswith('-none-any.whl'):
                raise ValueError('C တိုးချဲ့မှု·플랫폼 전용 wheel은 지원하지 않습니다.')
            for အချက်တန်ဖိုး in 항목들:
                လမ်း = အချက်တန်ဖိုး.filename.rstrip('/')
                လမ်းကြောင်းမှန်ကန်ကြောင်းစစ်(လမ်း, False)
                if (အချက်တန်ဖိုး.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 ကိန်းတန်ဖိုး 없습니다.')
                if အချက်တန်ဖိုး.filename.endswith('/'):
                    continue
                if '.dist-info/' in လမ်း:
                    if လမ်း.endswith('/METADATA'):
                        명세들.append(အထုပ်.read(အချက်တန်ဖိုး).decode())
                    continue
                if not လမ်း.endswith('.py') or '.data/' in လမ်း:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + လမ်း)
                အချက်နောက်တွဲ(လမ်း, အထုပ်.read(အချက်တန်ဖိုး))
    elif ဖိုင်အချက်အမည်.endswith('.tar.gz') and အမည်.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py စက်မောင်း 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ဒေတာ), mode='r|gz') as အထုပ်:
            뿌리들 = set()
            အချက်အရေအတွက် = 0
            အကုန်စုစုပေါင်းအရွယ် = 0
            for အချက်တန်ဖိုး in အထုပ်:
                အချက်အရေအတွက် += 1
                အကုန်စုစုပေါင်းအရွယ် += အချက်တန်ဖိုး.size
                if အချက်အရေအတွက် > 256 or အကုန်စုစုပေါင်းအရွယ် > 1048576:
                    raise ValueError('မော်ကွန်းတန်ဖိုး သိုလှောင်ရာလွှတ်ပေး အရွယ် ကန့်သတ်ချက်တန်ဖိုး 초과')
                လမ်းကြောင်းမှန်ကန်ကြောင်းစစ်(အချက်တန်ဖိုး.name, False)
                အစိတ်အပိုင်းများ = အချက်တန်ဖိုး.name.split('/')
                뿌리들.add(အစိတ်အပိုင်းများ[0])
                if အချက်တန်ဖိုး.isdir():
                    continue
                if not အချက်တန်ဖိုး.isfile() or len(အစိတ်အပိုင်းများ) < 2:
                    raise ValueError('잘못된 MicroPython မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 배포형')
                လမ်း = '/'.join(အစိတ်အပိုင်းများ[1:])
                အကြောင်းအရာတန်ဖိုး = အထုပ်.extractfile(အချက်တန်ဖိုး).read()
                if လမ်း.endswith('PKG-INFO'):
                    명세들.append(အကြောင်းအရာတန်ဖိုး.decode())
                elif လမ်း.endswith('.py') and လမ်း not in ('setup.py',):
                    အချက်နောက်တွဲ(လမ်း, အကြောင်းအရာတန်ဖိုး)
                elif '.egg-info/' not in လမ်း and not လမ်း.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + လမ်း)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 အမြစ်တန်ဖိုး 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 배포형이 필요합니다.')
    if not ဖိုင်အချက်များ or len(명세들) != 1:
        raise ValueError('소스와 ဖြန့်ချိမှုတန်ဖိုး 메타데이터가 필요합니다.')
    သတ်မှတ်စံ = email.parser.Parser().parsestr(명세들[0])
    if တောင်းဆိုချက်သဒ္ဒါခွဲခြမ်း(သတ်မှတ်စံ.get('Name', ''))[0] != အမည် or သတ်မှတ်စံ.get('Version') != ထုတ်ဝေမှုတန်ဖိုး:
        raise ValueError('ဖြန့်ချိမှုတန်ဖိုး 메타데이터의 အမည်·버전 불일치')
    if သတ်မှတ်စံ.get_all('Requires-Dist') or သတ်မှတ်စံ.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return ဖိုင်အချက်များ


def 웹읽기(လိပ်စာ, ဆံ့ပမာဏအကန့်):
    if not လိပ်စာ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS ဖြန့်ချိမှုတန်ဖိုး 주소만 허용합니다.')
    with urllib.request.urlopen(လိပ်စာ, timeout=30) as အကြောင်းပြန်ချက်:
        if not အကြောင်းပြန်ချက်.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 ဖြန့်ချိမှုတန်ဖိုး လိပ်စာ ရွှေ့တန်ဖိုး')
        ဒေတာ = အကြောင်းပြန်ချက်.read(ဆံ့ပမာဏအကန့် + 1)
    if len(ဒေတာ) > ဆံ့ပမာဏအကန့်:
        raise ValueError('ဖြန့်ချိမှုတန်ဖိုး ဖိုင် အရွယ် ကန့်သတ်ချက်တန်ဖိုး 초과')
    return ဒေတာ


def လွှဲပြောင်းအထုပ်(အမည်, ထုတ်ဝေမှုတန်ဖိုး, ဖိုင်အချက်များ, 출처):
    သတ်မှတ်စံ = {'name': အမည်, 'version': ထုတ်ဝေမှုတန်ဖိုး, 'source': 출처, 'files': [
        {'path': လမ်း, 'size': len(ဒေတာ), 'sha256': hashlib.sha256(ဒေတာ).hexdigest()}
        for လမ်း, ဒေတာ in sorted(ဖိုင်အချက်များ.items())]}
    ဦးခေါင်းတန်ဖိုး = json.dumps(သတ်မှတ်စံ, ensure_ascii=False).encode()
    if len(ဦးခေါင်းတန်ဖိုး) > 8192:
        raise ValueError('အထုပ် သတ်မှတ်စံ အရွယ် 초과')
    return b'JKP1' + struct.pack('>I', len(ဦးခေါင်းတန်ဖိုး)) + ဦးခေါင်းတန်ဖိုး + b''.join(ဖိုင်အချက်များ[အချက်တန်ဖိုး['path']] for အချက်တန်ဖိုး in သတ်မှတ်စံ['files'])


class 꾸러미저장소:
    def __init__(자신, လမ်း, 오프라인=False):
        자신.လမ်း = Path(လမ်း)
        자신.လမ်း.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def ပြင်ဆင်(자신, တောင်းဆိုချက်):
        အမည်, ထုတ်ဝေမှုတန်ဖိုး = တောင်းဆိုချက်သဒ္ဒါခွဲခြမ်း(တောင်းဆိုချက်)
        အဓိကသော့ = အမည် + ('==' + ထုတ်ဝေမှုတန်ဖိုး if ထုတ်ဝေမှုတန်ဖိုး else '')
        မှတ်တမ်းလမ်းကြောင်း = 자신.လမ်း / (အဓိကသော့ + '.json')
        ဖြန့်ချိမှုလမ်းကြောင်း = 자신.လမ်း / (အဓိကသော့ + '.archive')
        if မှတ်တမ်းလမ်းကြောင်း.is_file() and ဖြန့်ချိမှုလမ်းကြောင်း.is_file():
            မှတ်တမ်းမှတ်တမ်းတစ်ခု = json.loads(မှတ်တမ်းလမ်းကြောင်း.read_text())
            ဒေတာ = ဖြန့်ချိမှုလမ်းကြောင်း.read_bytes()
            if hashlib.sha256(ဒေတာ).hexdigest() != မှတ်တမ်းမှတ်တမ်းတစ်ခု['sha256']:
                raise ValueError('저장된 ဖြန့်ချိမှုတန်ဖိုး 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 အထုပ်: ' + တောင်းဆိုချက်)
            လိပ်စာ = 'https://pypi.org/pypi/' + အမည် + ('/' + ထုတ်ဝေမှုတန်ဖိုး if ထုတ်ဝေမှုတန်ဖိုး else '') + '/json'
            စနစ်သတင်းအချက်အလက် = json.loads(웹읽기(လိပ်စာ, 4194304).decode())
            if စနစ်သတင်းအချက်အလက်['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            အဆိုပြုချက် = [အချက်တန်ဖိုး for အချက်တန်ဖိုး in စနစ်သတင်းအချက်အလက်['urls'] if not အချက်တန်ဖိုး.get('yanked') and အချက်တန်ဖိုး['filename'].endswith('-none-any.whl')]
            if not အဆိုပြုချက် and အမည်.startswith('micropython-'):
                အဆိုပြုချက် = [အချက်တန်ဖိုး for အချက်တန်ဖိုး in စနစ်သတင်းအချက်အလက်['urls'] if not အချက်တန်ဖိုး.get('yanked') and အချက်တန်ဖိုး['filename'].endswith('.tar.gz')]
            if not အဆိုပြုချက်:
                raise ValueError('지원되는 순수 Python ဖြန့်ချိမှုတန်ဖိုး 파일이 없습니다.')
            ရွေးချယ်မှုတန်ဖိုး = အဆိုပြုချက်[0]
            ဒေတာ = 웹읽기(ရွေးချယ်မှုတန်ဖိုး['url'], 4194304)
            if hashlib.sha256(ဒေတာ).hexdigest() != ရွေးချယ်မှုတန်ဖိုး['digests']['sha256']:
                raise ValueError('PyPI ဖြန့်ချိမှုတန်ဖိုး ဖိုင် SHA-256 불일치')
            မှတ်တမ်းမှတ်တမ်းတစ်ခု = {'name': အမည်, 'version': စနစ်သတင်းအချက်အလက်['info']['version'], 'filename': ရွေးချယ်မှုတန်ဖိုး['filename'],
                    'url': ရွေးချယ်မှုတန်ဖိုး['url'], 'sha256': ရွေးချယ်မှုတန်ဖိုး['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(မှတ်တမ်းမှတ်တမ်းတစ်ခု['filename'], ဒေတာ, အမည်, မှတ်တမ်းမှတ်တမ်းတစ်ခု['version'])
            ဖြန့်ချိမှုလမ်းကြောင်း.write_bytes(ဒေတာ)
            မှတ်တမ်းလမ်းကြောင်း.write_text(json.dumps(မှတ်တမ်းမှတ်တမ်းတစ်ခု, ensure_ascii=False, indent=2) + '\n')
        if မှတ်တမ်းမှတ်တမ်းတစ်ခု['name'] != အမည် or ထုတ်ဝေမှုတန်ဖိုး and မှတ်တမ်းမှတ်တမ်းတစ်ခု['version'] != ထုတ်ဝေမှုတန်ဖိုး:
            raise ValueError('저장소 အမည်·버전 불일치')
        ဖိုင်အချက်များ = 압축풀기(မှတ်တမ်းမှတ်တမ်းတစ်ခု['filename'], ဒေတာ, အမည်, မှတ်တမ်းမှတ်တမ်းတစ်ခု['version'])
        return လွှဲပြောင်းအထုပ်(အမည်, မှတ်တမ်းမှတ်တမ်းတစ်ခု['version'], ဖိုင်အချက်များ, မှတ်တမ်းမှတ်တမ်းတစ်ခု['url'])


class အထုပ်တောင်းဆိုချက်(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            တောင်းဆိုချက် = bytearray()
            while b'\n' not in တောင်းဆိုချက် and len(တောင်းဆိုချက်) < 100:
                အစိတ်အပိုင်း = 자신.request.recv(100 - len(တောင်းဆိုချက်))
                if not အစိတ်အပိုင်း:
                    return
                တောင်းဆိုချက်.extend(အစိတ်အပိုင်း)
            if not တောင်းဆိုချက်.endswith(b'\n') or တောင်းဆိုချက်.count(b'\n') != 1:
                raise ValueError('잘못된 အထုပ် တောင်းဆိုချက်')
            အကြောင်းပြန်ချက် = 자신.server.저장소.ပြင်ဆင်(တောင်းဆိုချက်[:-1].decode('ascii'))
        except Exception as အမှား:
            ဦးခေါင်းတန်ဖိုး = json.dumps({'error': str(အမှား)[:500]}, ensure_ascii=False).encode()
            အကြောင်းပြန်ချက် = b'JKP1' + struct.pack('>I', len(ဦးခေါင်းတန်ဖိုး)) + ဦးခေါင်းတန်ဖိုး
        try:
            자신.request.sendall(အကြောင်းပြန်ချက်)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, ဆက်သွယ်ပေါက်ကိန်း=8027, လမ်း=None, 오프라인=False):
        자신.ဝန်ဆောင်စက်တန်ဖိုး = socketserver.TCPServer(('127.0.0.1', ဆက်သွယ်ပေါက်ကိန်း), အထုပ်တောင်းဆိုချက်, bind_and_activate=False)
        자신.ဝန်ဆောင်စက်တန်ဖိုး.allow_reuse_address = True
        자신.ဝန်ဆောင်စက်တန်ဖိုး.server_bind()
        자신.ဝန်ဆောင်စက်တန်ဖိုး.server_activate()
        자신.ဝန်ဆောင်စက်တန်ဖိုး.저장소 = 꾸러미저장소(လမ်း or စီမံကိန်းအမြစ်/'build/pip-cache', 오프라인)
        자신.ဆက်သွယ်ပေါက်ကိန်း = 자신.ဝန်ဆောင်စက်တန်ဖိုး.server_address[1]
        자신.အလုပ်ကြိုးတန်ဖိုး = threading.Thread(target=자신.ဝန်ဆောင်စက်တန်ဖိုး.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.အလုပ်ကြိုးတန်ဖိုး.start()
        return 자신

    def __exit__(자신, *အချက်များ):
        자신.ဝန်ဆောင်စက်တန်ဖိုး.shutdown()
        자신.ဝန်ဆောင်စက်တန်ဖိုး.server_close()
        자신.အလုပ်ကြိုးတန်ဖိုး.join(timeout=2)


def လုပ်ဆောင်():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=စီမံကိန်းအမြစ်/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='စက်မောင်း 없이 호환 ဖြန့်ချိမှုတန်ဖိုး 파일을 내려받아 စစ်ဆေးချက်·သိုလှောင်တန်ဖိုး')
    အချက်များ = 해석기.parse_args()
    if အချက်များ.fetch:
        ဒေတာ = 꾸러미저장소(အချက်များ.cache, အချက်များ.offline).ပြင်ဆင်(အချက်များ.fetch)
        print('အထုပ် ပြင်ဆင် ဖြစ်သောအပြည့်အစုံ:', အချက်များ.fetch, len(ဒေတာ), 'ဘိုက်တန်ဖိုး')
        return
    with 꾸러미중계(အချက်များ.port, အချက်များ.cache, အချက်များ.offline) as 중계:
        print('အထုပ် 중계: 127.0.0.1:' + str(중계.ဆက်သွယ်ပေါက်ကိန်း), flush=True)
        try:
            중계.အလုပ်ကြိုးတန်ဖိုး.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    လုပ်ဆောင်()
