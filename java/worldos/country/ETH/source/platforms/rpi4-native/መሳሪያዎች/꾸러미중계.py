#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ጫን_እሴት·실행한다."""
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

አሳይ_ስር = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('ቀርቅብ ስም 또는 ስም==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ትክክለኛነት_አረጋግጥ_ዱካ(ስም, መጫን_ዱካ=True):
    መተላለፊያ = PurePosixPath(ስም)
    if መተላለፊያ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ስም.split('/')):
        raise ValueError('허용하지 않는 ቀርቅብ መተላለፊያ: ' + ስም)
    if '\\' in ስም or any(ord(ቁምፊ_እሴት) < 32 or ord(ቁምፊ_እሴት) == 127 for ቁምፊ_እሴት in ስም):
        raise ValueError('잘못된 ቀርቅብ መተላለፊያ 문자')
    if መጫን_ዱካ and (len(('/lib/' + ስም).encode()) > 63 or ስም in ('አማርኛ.py', 'ቀርቅብ.py')):
        raise ValueError('ቀርቅብ መተላለፊያ 제한 또는 ነባሪ_እሴት ማከማቻ_ስፍራ 충돌: ' + ስም)
    return ስም


def 압축풀기(ፋይል_ምዝግብ_ስም, ውሂብ, ስም, ስሪት_እሴት):
    파일들 = {}
    명세들 = []
    def 추가(መተላለፊያ, ይዘት_እሴት):
        ትክክለኛነት_አረጋግጥ_ዱካ(መተላለፊያ)
        if መተላለፊያ in 파일들:
            raise ValueError('중복 ቀርቅብ መተላለፊያ: ' + መተላለፊያ)
        if len(ይዘት_እሴት) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + መተላለፊያ)
        ይዘት_እሴት.decode('utf-8')
        파일들[መተላለፊያ] = ይዘት_እሴት
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ምንጭ_ዛፍ 16개·합계 64 KiB 이하여야 합니다.')
    if ፋይል_ምዝግብ_ስም.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ውሂብ)) as ቀርቅብ:
            항목들 = ቀርቅብ.infolist()
            if len(항목들) > 256 or sum(ምዝግብ_እሴት.file_size for ምዝግብ_እሴት in 항목들) > 1048576:
                raise ValueError('ከዝን_እሴት ልቀቅ_ማከማቻ መጠን 제한 초과')
            ስራ_ዝርዝር = [ምዝግብ_እሴት for ምዝግብ_እሴት in 항목들 if ምዝግብ_እሴት.filename.endswith('.dist-info/WHEEL')]
            if len(ስራ_ዝርዝር) != 1:
                raise ValueError('wheel ስራ_እሴት_102996da 명세가 필요합니다.')
            ስራ_እሴት_102996da = email.parser.Parser().parsestr(ቀርቅብ.read(ስራ_ዝርዝር[0]).decode())
            if ስራ_እሴት_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not ፋይል_ምዝግብ_ስም.endswith('-none-any.whl'):
                raise ValueError('C ቅጥያ_እሴት·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ምዝግብ_እሴት in 항목들:
                መተላለፊያ = ምዝግብ_እሴት.filename.rstrip('/')
                ትክክለኛነት_አረጋግጥ_ዱካ(መተላለፊያ, False)
                if (ምዝግብ_እሴት.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ምዝግብ_እሴት.filename.endswith('/'):
                    continue
                if '.dist-info/' in መተላለፊያ:
                    if መተላለፊያ.endswith('/METADATA'):
                        명세들.append(ቀርቅብ.read(ምዝግብ_እሴት).decode())
                    continue
                if not መተላለፊያ.endswith('.py') or '.data/' in መተላለፊያ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + መተላለፊያ)
                추가(መተላለፊያ, ቀርቅብ.read(ምዝግብ_እሴት))
    elif ፋይል_ምዝግብ_ስም.endswith('.tar.gz') and ስም.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ፈጽም_ትእዛዝ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ውሂብ), mode='r|gz') as ቀርቅብ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ምዝግብ_እሴት in ቀርቅብ:
                항목수 += 1
                전체크기 += ምዝግብ_እሴት.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ከዝን_እሴት ልቀቅ_ማከማቻ መጠን 제한 초과')
                ትክክለኛነት_አረጋግጥ_ዱካ(ምዝግብ_እሴት.name, False)
                부분들 = ምዝግብ_እሴት.name.split('/')
                뿌리들.add(부분들[0])
                if ምዝግብ_እሴት.isdir():
                    continue
                if not ምዝግብ_እሴት.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ምንጭ_ዛፍ 배포형')
                መተላለፊያ = '/'.join(부분들[1:])
                ይዘት_እሴት = ቀርቅብ.extractfile(ምዝግብ_እሴት).read()
                if መተላለፊያ.endswith('PKG-INFO'):
                    명세들.append(ይዘት_እሴት.decode())
                elif መተላለፊያ.endswith('.py') and መተላለፊያ not in ('setup.py',):
                    추가(መተላለፊያ, ይዘት_እሴት)
                elif '.egg-info/' not in መተላለፊያ and not መተላለፊያ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + መተላለፊያ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ስር_እሴት 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ምንጭ_ዛፍ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ስም or 명세.get('Version') != ስሪት_እሴት:
        raise ValueError('배포 메타데이터의 ስም·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(አድራሻ, 한도):
    if not አድራሻ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(አድራሻ, timeout=30) as መልስ:
        if not መልስ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 አድራሻ አንቀሳቅስ_እሴት')
        ውሂብ = መልስ.read(한도 + 1)
    if len(ውሂብ) > 한도:
        raise ValueError('배포 ፋይል መጠን 제한 초과')
    return ውሂብ


def ትልልፍ_ቀርቅብ(ስም, ስሪት_እሴት, 파일들, 출처):
    명세 = {'name': ስም, 'version': ስሪት_እሴት, 'source': 출처, 'files': [
        {'path': መተላለፊያ, 'size': len(ውሂብ), 'sha256': hashlib.sha256(ውሂብ).hexdigest()}
        for መተላለፊያ, ውሂብ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ቀርቅብ 명세 መጠን 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ምዝግብ_እሴት['path']] for ምዝግብ_እሴት in 명세['files'])


class ቀርቅብ_ማከማቻ:
    def __init__(자신, መተላለፊያ, የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ=False):
        자신.መተላለፊያ = Path(መተላለፊያ)
        자신.መተላለፊያ.mkdir(parents=True, exist_ok=True)
        자신.የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ = የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ

    def አዘጋጅ_9ce364fc(자신, 요청):
        ስም, ስሪት_እሴት = 요청해석(요청)
        열쇠 = ስም + ('==' + ስሪት_እሴት if ስሪት_እሴት else '')
        መዝግብ_ዱካ = 자신.መተላለፊያ / (열쇠 + '.json')
        배포경로 = 자신.መተላለፊያ / (열쇠 + '.archive')
        if መዝግብ_ዱካ.is_file() and 배포경로.is_file():
            መዝግብ_ረድፍ = json.loads(መዝግብ_ዱካ.read_text())
            ውሂብ = 배포경로.read_bytes()
            if hashlib.sha256(ውሂብ).hexdigest() != መዝግብ_ረድፍ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ:
                raise ValueError('የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ 저장소에 없는 ቀርቅብ: ' + 요청)
            አድራሻ = 'https://pypi.org/pypi/' + ስም + ('/' + ስሪት_እሴት if ስሪት_እሴት else '') + '/json'
            የስርዓት_መረጃ = json.loads(웹읽기(አድራሻ, 4194304).decode())
            if የስርዓት_መረጃ['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ምዝግብ_እሴት for ምዝግብ_እሴት in የስርዓት_መረጃ['urls'] if not ምዝግብ_እሴት.get('yanked') and ምዝግብ_እሴት['filename'].endswith('-none-any.whl')]
            if not 후보 and ስም.startswith('micropython-'):
                후보 = [ምዝግብ_እሴት for ምዝግብ_እሴት in የስርዓት_መረጃ['urls'] if not ምዝግብ_እሴት.get('yanked') and ምዝግብ_እሴት['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            የተመረጠ_እሴት = 후보[0]
            ውሂብ = 웹읽기(የተመረጠ_እሴት['url'], 4194304)
            if hashlib.sha256(ውሂብ).hexdigest() != የተመረጠ_እሴት['digests']['sha256']:
                raise ValueError('PyPI 배포 ፋይል SHA-256 불일치')
            መዝግብ_ረድፍ = {'name': ስም, 'version': የስርዓት_መረጃ['info']['version'], 'filename': የተመረጠ_እሴት['filename'],
                    'url': የተመረጠ_እሴት['url'], 'sha256': የተመረጠ_እሴት['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(መዝግብ_ረድፍ['filename'], ውሂብ, ስም, መዝግብ_ረድፍ['version'])
            배포경로.write_bytes(ውሂብ)
            መዝግብ_ዱካ.write_text(json.dumps(መዝግብ_ረድፍ, ensure_ascii=False, indent=2) + '\n')
        if መዝግብ_ረድፍ['name'] != ስም or ስሪት_እሴት and መዝግብ_ረድፍ['version'] != ስሪት_እሴት:
            raise ValueError('ማከማቻ_ስር ስም·버전 불일치')
        파일들 = 압축풀기(መዝግብ_ረድፍ['filename'], ውሂብ, ስም, መዝግብ_ረድፍ['version'])
        return ትልልፍ_ቀርቅብ(ስም, መዝግብ_ረድፍ['version'], 파일들, መዝግብ_ረድፍ['url'])


class 꾸러미요청(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            요청 = bytearray()
            while b'\n' not in 요청 and len(요청) < 100:
                조각 = 자신.request.recv(100 - len(요청))
                if not 조각:
                    return
                요청.extend(조각)
            if not 요청.endswith(b'\n') or 요청.count(b'\n') != 1:
                raise ValueError('잘못된 ቀርቅብ 요청')
            መልስ = 자신.server.ማከማቻ_ስር.አዘጋጅ_9ce364fc(요청[:-1].decode('ascii'))
        except Exception as ስህተት:
            머리 = json.dumps({'error': str(ስህተት)[:500]}, ensure_ascii=False).encode()
            መልስ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(መልስ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, የወደብ_ቁጥር=8027, መተላለፊያ=None, የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ=False):
        자신.አገልጋይ_እሴት = socketserver.TCPServer(('127.0.0.1', የወደብ_ቁጥር), 꾸러미요청, bind_and_activate=False)
        자신.አገልጋይ_እሴት.allow_reuse_address = True
        자신.አገልጋይ_እሴት.server_bind()
        자신.አገልጋይ_እሴት.server_activate()
        자신.አገልጋይ_እሴት.ማከማቻ_ስር = ቀርቅብ_ማከማቻ(መተላለፊያ or አሳይ_ስር/'build/pip-cache', የመረጃ_ቴክኖሎጂ_ከመስመር_ውጪ)
        자신.የወደብ_ቁጥር = 자신.አገልጋይ_እሴት.server_address[1]
        자신.ክር_እሴት = threading.Thread(target=자신.አገልጋይ_እሴት.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ክር_እሴት.start()
        return 자신

    def __exit__(자신, *인수):
        자신.አገልጋይ_እሴት.shutdown()
        자신.አገልጋይ_እሴት.server_close()
        자신.ክር_እሴት.join(timeout=2)


def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--port', type=int, default=8027)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--cache', type=Path, default=አሳይ_ስር/'build/pip-cache')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--offline', action='store_true')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--fetch', help='ፈጽም_ትእዛዝ 없이 호환 배포 파일을 내려받아 검사·ማከማቻ_እሴት')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    if 인수.fetch:
        ውሂብ = ቀርቅብ_ማከማቻ(인수.cache, 인수.offline).አዘጋጅ_9ce364fc(인수.fetch)
        print('ቀርቅብ አዘጋጅ_9ce364fc 완료:', 인수.fetch, len(ውሂብ), 'ባይት_እሴት')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ቀርቅብ 중계: 127.0.0.1:' + str(중계.የወደብ_ቁጥር), flush=True)
        try:
            중계.ክር_እሴት.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ማስኬጃ()
