#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 տեղադրել_արժեք·실행한다."""
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

արձակել_արմատ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('փաթեթ Անուն 또는 Անուն==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def վավերացնել_ուղի(Անուն, տեղադրում_ուղի=True):
    Ճանապարհ = PurePosixPath(Անուն)
    if Ճանապարհ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Անուն.split('/')):
        raise ValueError('허용하지 않는 փաթեթ Ճանապարհ: ' + Անուն)
    if '\\' in Անուն or any(ord(գրանշան_արժեք) < 32 or ord(գրանշան_արժեք) == 127 for գրանշան_արժեք in Անուն):
        raise ValueError('잘못된 փաթեթ Ճանապարհ 문자')
    if տեղադրում_ուղի and (len(('/lib/' + Անուն).encode()) > 63 or Անուն in ('한국어.py', 'փաթեթ.py')):
        raise ValueError('փաթեթ Ճանապարհ 제한 또는 սկզբնադիր_արժեք դարան 충돌: ' + Անուն)
    return Անուն


def 압축풀기(նիշք_մուտքագրում_անուն, տվյալ, Անուն, տարբերակ_արժեք):
    파일들 = {}
    명세들 = []
    def 추가(Ճանապարհ, Բովանդակություն_արժեք):
        վավերացնել_ուղի(Ճանապարհ)
        if Ճանապարհ in 파일들:
            raise ValueError('중복 փաթեթ Ճանապարհ: ' + Ճանապարհ)
        if len(Բովանդակություն_արժեք) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Ճանապարհ)
        Բովանդակություն_արժեք.decode('utf-8')
        파일들[Ճանապարհ] = Բովանդակություն_արժեք
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 աղբյուր_ծառ 16개·합계 64 KiB 이하여야 합니다.')
    if նիշք_մուտքագրում_անուն.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(տվյալ)) as փաթեթ:
            항목들 = փաթեթ.infolist()
            if len(항목들) > 256 or sum(մուտքագրում_արժեք.file_size for մուտքագրում_արժեք in 항목들) > 1048576:
                raise ValueError('Պահոց_արժեք արձակել_Պահեստ Չափս 제한 초과')
            գործ_Ցուցակ = [մուտքագրում_արժեք for մուտքագրում_արժեք in 항목들 if մուտքագրում_արժեք.filename.endswith('.dist-info/WHEEL')]
            if len(գործ_Ցուցակ) != 1:
                raise ValueError('wheel գործ_արժեք 명세가 필요합니다.')
            գործ_արժեք = email.parser.Parser().parsestr(փաթեթ.read(գործ_Ցուցակ[0]).decode())
            if գործ_արժեք.get('Root-Is-Purelib', '').lower() != 'true' or not նիշք_մուտքագրում_անուն.endswith('-none-any.whl'):
                raise ValueError('C ընդլայնում_արժեք·플랫폼 전용 wheel은 지원하지 않습니다.')
            for մուտքագրում_արժեք in 항목들:
                Ճանապարհ = մուտքագրում_արժեք.filename.rstrip('/')
                վավերացնել_ուղի(Ճանապարհ, False)
                if (մուտքագրում_արժեք.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if մուտքագրում_արժեք.filename.endswith('/'):
                    continue
                if '.dist-info/' in Ճանապարհ:
                    if Ճանապարհ.endswith('/METADATA'):
                        명세들.append(փաթեթ.read(մուտքագրում_արժեք).decode())
                    continue
                if not Ճանապարհ.endswith('.py') or '.data/' in Ճանապարհ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Ճանապարհ)
                추가(Ճանապարհ, փաթեթ.read(մուտքագրում_արժեք))
    elif նիշք_մուտքագրում_անուն.endswith('.tar.gz') and Անուն.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py կատարել_հրաման 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(տվյալ), mode='r|gz') as փաթեթ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for մուտքագրում_արժեք in փաթեթ:
                항목수 += 1
                전체크기 += մուտքագրում_արժեք.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Պահոց_արժեք արձակել_Պահեստ Չափս 제한 초과')
                վավերացնել_ուղի(մուտքագրում_արժեք.name, False)
                부분들 = մուտքագրում_արժեք.name.split('/')
                뿌리들.add(부분들[0])
                if մուտքագրում_արժեք.isdir():
                    continue
                if not մուտքագրում_արժեք.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython աղբյուր_ծառ 배포형')
                Ճանապարհ = '/'.join(부분들[1:])
                Բովանդակություն_արժեք = փաթեթ.extractfile(մուտքագրում_արժեք).read()
                if Ճանապարհ.endswith('PKG-INFO'):
                    명세들.append(Բովանդակություն_արժեք.decode())
                elif Ճանապարհ.endswith('.py') and Ճանապարհ not in ('setup.py',):
                    추가(Ճանապարհ, Բովանդակություն_արժեք)
                elif '.egg-info/' not in Ճանապարհ and not Ճանապարհ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Ճանապարհ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 արմատ_արժեք 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* աղբյուր_ծառ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Անուն or 명세.get('Version') != տարբերակ_արժեք:
        raise ValueError('배포 메타데이터의 Անուն·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(հասցե, 한도):
    if not հասցե.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(հասցե, timeout=30) as պատասխանել:
        if not պատասխանել.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 հասցե տեղափոխել_արժեք')
        տվյալ = պատասխանել.read(한도 + 1)
    if len(տվյալ) > 한도:
        raise ValueError('배포 Ֆայլ Չափս 제한 초과')
    return տվյալ


def փոխանցել_փաթեթ(Անուն, տարբերակ_արժեք, 파일들, 출처):
    명세 = {'name': Անուն, 'version': տարբերակ_արժեք, 'source': 출처, 'files': [
        {'path': Ճանապարհ, 'size': len(տվյալ), 'sha256': hashlib.sha256(տվյալ).hexdigest()}
        for Ճանապարհ, տվյալ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('փաթեթ 명세 Չափս 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[մուտքագրում_արժեք['path']] for մուտքագրում_արժեք in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Ճանապարհ, 오프라인=False):
        자신.Ճանապարհ = Path(Ճանապարհ)
        자신.Ճանապարհ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Պատրաստել(자신, 요청):
        Անուն, տարբերակ_արժեք = 요청해석(요청)
        열쇠 = Անուն + ('==' + տարբերակ_արժեք if տարբերակ_արժեք else '')
        մատյան_ուղի = 자신.Ճանապարհ / (열쇠 + '.json')
        배포경로 = 자신.Ճանապարհ / (열쇠 + '.archive')
        if մատյան_ուղի.is_file() and 배포경로.is_file():
            մատյան_տող = json.loads(մատյան_ուղի.read_text())
            տվյալ = 배포경로.read_bytes()
            if hashlib.sha256(տվյալ).hexdigest() != մատյան_տող['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 փաթեթ: ' + 요청)
            հասցե = 'https://pypi.org/pypi/' + Անուն + ('/' + տարբերակ_արժեք if տարբերակ_արժեք else '') + '/json'
            Համակարգի_տեղեկություն = json.loads(웹읽기(հասցե, 4194304).decode())
            if Համակարգի_տեղեկություն['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [մուտքագրում_արժեք for մուտքագրում_արժեք in Համակարգի_տեղեկություն['urls'] if not մուտքագրում_արժեք.get('yanked') and մուտքագրում_արժեք['filename'].endswith('-none-any.whl')]
            if not 후보 and Անուն.startswith('micropython-'):
                후보 = [մուտքագրում_արժեք for մուտքագրում_արժեք in Համակարգի_տեղեկություն['urls'] if not մուտքագրում_արժեք.get('yanked') and մուտքագրում_արժեք['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ընտրվածք_արժեք = 후보[0]
            տվյալ = 웹읽기(ընտրվածք_արժեք['url'], 4194304)
            if hashlib.sha256(տվյալ).hexdigest() != ընտրվածք_արժեք['digests']['sha256']:
                raise ValueError('PyPI 배포 Ֆայլ SHA-256 불일치')
            մատյան_տող = {'name': Անուն, 'version': Համակարգի_տեղեկություն['info']['version'], 'filename': ընտրվածք_արժեք['filename'],
                    'url': ընտրվածք_արժեք['url'], 'sha256': ընտրվածք_արժեք['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(մատյան_տող['filename'], տվյալ, Անուն, մատյան_տող['version'])
            배포경로.write_bytes(տվյալ)
            մատյան_ուղի.write_text(json.dumps(մատյան_տող, ensure_ascii=False, indent=2) + '\n')
        if մատյան_տող['name'] != Անուն or տարբերակ_արժեք and մատյան_տող['version'] != տարբերակ_արժեք:
            raise ValueError('저장소 Անուն·버전 불일치')
        파일들 = 압축풀기(մատյան_տող['filename'], տվյալ, Անուն, մատյան_տող['version'])
        return փոխանցել_փաթեթ(Անուն, մատյան_տող['version'], 파일들, մատյան_տող['url'])


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
                raise ValueError('잘못된 փաթեթ 요청')
            պատասխանել = 자신.server.저장소.Պատրաստել(요청[:-1].decode('ascii'))
        except Exception as Սխալ:
            머리 = json.dumps({'error': str(Սխալ)[:500]}, ensure_ascii=False).encode()
            պատասխանել = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(պատասխանել)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Ճանապարհ=None, 오프라인=False):
        자신.սպասարկիչ_արժեք = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.սպասարկիչ_արժեք.allow_reuse_address = True
        자신.սպասարկիչ_արժեք.server_bind()
        자신.սպասարկիչ_արժեք.server_activate()
        자신.սպասարկիչ_արժեք.저장소 = 꾸러미저장소(Ճանապարհ or արձակել_արմատ/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.սպասարկիչ_արժեք.server_address[1]
        자신.շղթա_արժեք = threading.Thread(target=자신.սպասարկիչ_արժեք.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.շղթա_արժեք.start()
        return 자신

    def __exit__(자신, *인수):
        자신.սպասարկիչ_արժեք.shutdown()
        자신.սպասարկիչ_արժեք.server_close()
        자신.շղթա_արժեք.join(timeout=2)


def Գործարկել():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=արձակել_արմատ/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='կատարել_հրաման 없이 호환 배포 파일을 내려받아 검사·պահեստավորել_արժեք')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        տվյալ = 꾸러미저장소(인수.cache, 인수.offline).Պատրաստել(인수.fetch)
        print('փաթեթ Պատրաստել 완료:', 인수.fetch, len(տվյալ), 'բայթ_արժեք')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('փաթեթ 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.շղթա_արժեք.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Գործարկել()
