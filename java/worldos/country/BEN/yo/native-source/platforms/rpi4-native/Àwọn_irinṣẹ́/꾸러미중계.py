#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ṣàgbékalẹ̀_iye·실행한다."""
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

기준 = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('àkópọ̀ Orúkọ 또는 Orúkọ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ìfọwọ́síìwé_ọ̀nà(Orúkọ, ìṣàgbékalẹ̀_ọ̀nà=True):
    ọ̀nà = PurePosixPath(Orúkọ)
    if ọ̀nà.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Orúkọ.split('/')):
        raise ValueError('허용하지 않는 àkópọ̀ ọ̀nà: ' + Orúkọ)
    if '\\' in Orúkọ or any(ord(ẹyọ_ọ̀rọ̀_iye) < 32 or ord(ẹyọ_ọ̀rọ̀_iye) == 127 for ẹyọ_ọ̀rọ̀_iye in Orúkọ):
        raise ValueError('잘못된 àkópọ̀ ọ̀nà 문자')
    if ìṣàgbékalẹ̀_ọ̀nà and (len(('/lib/' + Orúkọ).encode()) > 63 or Orúkọ in ('한국어.py', 'àkópọ̀.py')):
        raise ValueError('àkópọ̀ ọ̀nà 제한 또는 àdáwọ̀ ibi_ìpamọ́ 충돌: ' + Orúkọ)
    return Orúkọ


def 압축풀기(fáìlì_ìgbéwọlé_orúkọ, détà, Orúkọ, ẹ̀yà_iye):
    파일들 = {}
    명세들 = []
    def 추가(ọ̀nà, Àkóónú_iye):
        ìfọwọ́síìwé_ọ̀nà(ọ̀nà)
        if ọ̀nà in 파일들:
            raise ValueError('중복 àkópọ̀ ọ̀nà: ' + ọ̀nà)
        if len(Àkóónú_iye) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ọ̀nà)
        Àkóónú_iye.decode('utf-8')
        파일들[ọ̀nà] = Àkóónú_iye
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 orísun_ètò_afigijúwe 16개·합계 64 KiB 이하여야 합니다.')
    if fáìlì_ìgbéwọlé_orúkọ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(détà)) as àkópọ̀:
            항목들 = àkópọ̀.infolist()
            if len(항목들) > 256 or sum(ìgbéwọlé_iye.file_size for ìgbéwọlé_iye in 항목들) > 1048576:
                raise ValueError('Ìpamọ_ọlọ́jọ́pípẹ́_iye dápadà_Ibi_ìpamọ́ Ìwọ̀n 제한 초과')
            iṣẹ́_Àtòkọ = [ìgbéwọlé_iye for ìgbéwọlé_iye in 항목들 if ìgbéwọlé_iye.filename.endswith('.dist-info/WHEEL')]
            if len(iṣẹ́_Àtòkọ) != 1:
                raise ValueError('wheel iṣẹ́_iye 명세가 필요합니다.')
            iṣẹ́_iye = email.parser.Parser().parsestr(àkópọ̀.read(iṣẹ́_Àtòkọ[0]).decode())
            if iṣẹ́_iye.get('Root-Is-Purelib', '').lower() != 'true' or not fáìlì_ìgbéwọlé_orúkọ.endswith('-none-any.whl'):
                raise ValueError('C Àfikún_iye·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ìgbéwọlé_iye in 항목들:
                ọ̀nà = ìgbéwọlé_iye.filename.rstrip('/')
                ìfọwọ́síìwé_ọ̀nà(ọ̀nà, False)
                if (ìgbéwọlé_iye.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ìgbéwọlé_iye.filename.endswith('/'):
                    continue
                if '.dist-info/' in ọ̀nà:
                    if ọ̀nà.endswith('/METADATA'):
                        명세들.append(àkópọ̀.read(ìgbéwọlé_iye).decode())
                    continue
                if not ọ̀nà.endswith('.py') or '.data/' in ọ̀nà:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ọ̀nà)
                추가(ọ̀nà, àkópọ̀.read(ìgbéwọlé_iye))
    elif fáìlì_ìgbéwọlé_orúkọ.endswith('.tar.gz') and Orúkọ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ṣiṣẹ́_àṣẹ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(détà), mode='r|gz') as àkópọ̀:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ìgbéwọlé_iye in àkópọ̀:
                항목수 += 1
                전체크기 += ìgbéwọlé_iye.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Ìpamọ_ọlọ́jọ́pípẹ́_iye dápadà_Ibi_ìpamọ́ Ìwọ̀n 제한 초과')
                ìfọwọ́síìwé_ọ̀nà(ìgbéwọlé_iye.name, False)
                부분들 = ìgbéwọlé_iye.name.split('/')
                뿌리들.add(부분들[0])
                if ìgbéwọlé_iye.isdir():
                    continue
                if not ìgbéwọlé_iye.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython orísun_ètò_afigijúwe 배포형')
                ọ̀nà = '/'.join(부분들[1:])
                Àkóónú_iye = àkópọ̀.extractfile(ìgbéwọlé_iye).read()
                if ọ̀nà.endswith('PKG-INFO'):
                    명세들.append(Àkóónú_iye.decode())
                elif ọ̀nà.endswith('.py') and ọ̀nà not in ('setup.py',):
                    추가(ọ̀nà, Àkóónú_iye)
                elif '.egg-info/' not in ọ̀nà and not ọ̀nà.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ọ̀nà)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* orísun_ètò_afigijúwe 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Orúkọ or 명세.get('Version') != ẹ̀yà_iye:
        raise ValueError('배포 메타데이터의 Orúkọ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(àdírẹ́ẹ̀sì, 한도):
    if not àdírẹ́ẹ̀sì.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(àdírẹ́ẹ̀sì, timeout=30) as Fèsì:
        if not Fèsì.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 àdírẹ́ẹ̀sì gbé_iye')
        détà = Fèsì.read(한도 + 1)
    if len(détà) > 한도:
        raise ValueError('배포 Fáìlì Ìwọ̀n 제한 초과')
    return détà


def ṣàgbélọ_àkópọ̀(Orúkọ, ẹ̀yà_iye, 파일들, 출처):
    명세 = {'name': Orúkọ, 'version': ẹ̀yà_iye, 'source': 출처, 'files': [
        {'path': ọ̀nà, 'size': len(détà), 'sha256': hashlib.sha256(détà).hexdigest()}
        for ọ̀nà, détà in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('àkópọ̀ 명세 Ìwọ̀n 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ìgbéwọlé_iye['path']] for ìgbéwọlé_iye in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ọ̀nà, 오프라인=False):
        자신.ọ̀nà = Path(ọ̀nà)
        자신.ọ̀nà.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def gbaradì(자신, 요청):
        Orúkọ, ẹ̀yà_iye = 요청해석(요청)
        열쇠 = Orúkọ + ('==' + ẹ̀yà_iye if ẹ̀yà_iye else '')
        àkọsílẹ̀_ìṣe_ọ̀nà = 자신.ọ̀nà / (열쇠 + '.json')
        배포경로 = 자신.ọ̀nà / (열쇠 + '.archive')
        if àkọsílẹ̀_ìṣe_ọ̀nà.is_file() and 배포경로.is_file():
            àkọsílẹ̀_ìṣe_ìlà_ìbú = json.loads(àkọsílẹ̀_ìṣe_ọ̀nà.read_text())
            détà = 배포경로.read_bytes()
            if hashlib.sha256(détà).hexdigest() != àkọsílẹ̀_ìṣe_ìlà_ìbú['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 àkópọ̀: ' + 요청)
            àdírẹ́ẹ̀sì = 'https://pypi.org/pypi/' + Orúkọ + ('/' + ẹ̀yà_iye if ẹ̀yà_iye else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(àdírẹ́ẹ̀sì, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ìgbéwọlé_iye for ìgbéwọlé_iye in msinfo32_exe['urls'] if not ìgbéwọlé_iye.get('yanked') and ìgbéwọlé_iye['filename'].endswith('-none-any.whl')]
            if not 후보 and Orúkọ.startswith('micropython-'):
                후보 = [ìgbéwọlé_iye for ìgbéwọlé_iye in msinfo32_exe['urls'] if not ìgbéwọlé_iye.get('yanked') and ìgbéwọlé_iye['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ẹ̀yàn_iye = 후보[0]
            détà = 웹읽기(ẹ̀yàn_iye['url'], 4194304)
            if hashlib.sha256(détà).hexdigest() != ẹ̀yàn_iye['digests']['sha256']:
                raise ValueError('PyPI 배포 Fáìlì SHA-256 불일치')
            àkọsílẹ̀_ìṣe_ìlà_ìbú = {'name': Orúkọ, 'version': msinfo32_exe['info']['version'], 'filename': ẹ̀yàn_iye['filename'],
                    'url': ẹ̀yàn_iye['url'], 'sha256': ẹ̀yàn_iye['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(àkọsílẹ̀_ìṣe_ìlà_ìbú['filename'], détà, Orúkọ, àkọsílẹ̀_ìṣe_ìlà_ìbú['version'])
            배포경로.write_bytes(détà)
            àkọsílẹ̀_ìṣe_ọ̀nà.write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú, ensure_ascii=False, indent=2) + '\n')
        if àkọsílẹ̀_ìṣe_ìlà_ìbú['name'] != Orúkọ or ẹ̀yà_iye and àkọsílẹ̀_ìṣe_ìlà_ìbú['version'] != ẹ̀yà_iye:
            raise ValueError('저장소 Orúkọ·버전 불일치')
        파일들 = 압축풀기(àkọsílẹ̀_ìṣe_ìlà_ìbú['filename'], détà, Orúkọ, àkọsílẹ̀_ìṣe_ìlà_ìbú['version'])
        return ṣàgbélọ_àkópọ̀(Orúkọ, àkọsílẹ̀_ìṣe_ìlà_ìbú['version'], 파일들, àkọsílẹ̀_ìṣe_ìlà_ìbú['url'])


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
                raise ValueError('잘못된 àkópọ̀ 요청')
            Fèsì = 자신.server.저장소.gbaradì(요청[:-1].decode('ascii'))
        except Exception as àṣìṣe:
            머리 = json.dumps({'error': str(àṣìṣe)[:500]}, ensure_ascii=False).encode()
            Fèsì = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(Fèsì)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ọ̀nà=None, 오프라인=False):
        자신.apèsè_iye = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.apèsè_iye.allow_reuse_address = True
        자신.apèsè_iye.server_bind()
        자신.apèsè_iye.server_activate()
        자신.apèsè_iye.저장소 = 꾸러미저장소(ọ̀nà or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.apèsè_iye.server_address[1]
        자신.èròjà_atẹ̀lélànà_iye = threading.Thread(target=자신.apèsè_iye.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.èròjà_atẹ̀lélànà_iye.start()
        return 자신

    def __exit__(자신, *인수):
        자신.apèsè_iye.shutdown()
        자신.apèsè_iye.server_close()
        자신.èròjà_atẹ̀lélànà_iye.join(timeout=2)


def Rọ́ọ̀nù():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ṣiṣẹ́_àṣẹ 없이 호환 배포 파일을 내려받아 검사·Store_iye')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        détà = 꾸러미저장소(인수.cache, 인수.offline).gbaradì(인수.fetch)
        print('àkópọ̀ gbaradì 완료:', 인수.fetch, len(détà), 'báìtì_iye')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('àkópọ̀ 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.èròjà_atẹ̀lélànà_iye.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Rọ́ọ̀nù()
