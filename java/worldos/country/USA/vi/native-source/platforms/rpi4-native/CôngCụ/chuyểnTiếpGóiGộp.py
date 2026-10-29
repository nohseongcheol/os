#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost chuyểnTiếpGiáTrị. 게스트는 TCP로 받은 소스를 직접 càiĐặtGiáTrị·실행한다."""
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

gốcCâyDựÁn = Path(__file__).resolve().parents[1]


def phânTíchCúPhápYêuCầu(yêuCầu):
    làĐãKhớp = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', yêuCầu)
    if not làĐãKhớp:
        raise ValueError('GóiGộp tên 또는 tên==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', làĐãKhớp[1]).lower(), làĐãKhớp[2]


def thẩmĐịnhĐườngDẫn(tên, đườngDẫnViệcCàiĐặt=True):
    đườngDẫn = PurePosixPath(tên)
    if đườngDẫn.is_absolute() or any(giáTrịPhầnCon in ('', '.', '..') or giáTrịPhầnCon.startswith('.') for giáTrịPhầnCon in tên.split('/')):
        raise ValueError('허용하지 않는 GóiGộp đườngDẫn: ' + tên)
    if '\\' in tên or any(ord(giáTrịKýTự) < 32 or ord(giáTrịKýTự) == 127 for giáTrịKýTự in tên):
        raise ValueError('잘못된 GóiGộp đườngDẫn KýTự')
    if đườngDẫnViệcCàiĐặt and (len(('/lib/' + tên).encode()) > 63 or tên in ('tiếngViệt.py', 'GóiGộp.py')):
        raise ValueError('GóiGộp đườngDẫn giáTrịGiớiHạn 또는 giáTrịMặcĐịnh thưViện 충돌: ' + tên)
    return tên


def giảiNén(tênMụcTệp, DữLiệu, tên, giáTrịPhiênBản):
    cácMụcTệp = {}
    cácĐặcTả = []
    def thêmCuốiMục(đườngDẫn, giáTrịNộiDung):
        thẩmĐịnhĐườngDẫn(đườngDẫn)
        if đườngDẫn in cácMụcTệp:
            raise ValueError('중복 GóiGộp đườngDẫn: ' + đườngDẫn)
        if len(giáTrịNộiDung) > 16384:
            raise ValueError('파일당 16 KiB giáTrịGiớiHạn 초과: ' + đườngDẫn)
        giáTrịNộiDung.decode('utf-8')
        cácMụcTệp[đườngDẫn] = giáTrịNộiDung
        if len(cácMụcTệp) > 16 or sum(map(len, cácMụcTệp.values())) > 65536:
            raise ValueError('꾸러미는 câyNguồn 16개·giáTrịTổngCộng 64 KiB 이하여야 합니다.')
    if tênMụcTệp.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(DữLiệu)) as GóiGộp:
            danhSáchCácMục = GóiGộp.infolist()
            if len(danhSáchCácMục) > 256 or sum(giáTrịMục.file_size for giáTrịMục in danhSáchCácMục) > 1048576:
                raise ValueError('giáTrịKhoLưuTrữ giảiPhóngLưuTrữ cỡ giáTrịGiớiHạn 초과')
            danhSáchQuyƯớc = [giáTrịMục for giáTrịMục in danhSáchCácMục if giáTrịMục.filename.endswith('.dist-info/WHEEL')]
            if len(danhSáchQuyƯớc) != 1:
                raise ValueError('wheel giáTrịQuyƯớc 명세가 필요합니다.')
            giáTrịQuyƯớc = email.parser.Parser().parsestr(GóiGộp.read(danhSáchQuyƯớc[0]).decode())
            if giáTrịQuyƯớc.get('Root-Is-Purelib', '').lower() != 'true' or not tênMụcTệp.endswith('-none-any.whl'):
                raise ValueError('C giáTrịPhầnMởRộng·플랫폼 전용 wheel은 지원하지 않습니다.')
            for giáTrịMục in danhSáchCácMục:
                đườngDẫn = giáTrịMục.filename.rstrip('/')
                thẩmĐịnhĐườngDẫn(đườngDẫn, False)
                if (giáTrịMục.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 trịSố 없습니다.')
                if giáTrịMục.filename.endswith('/'):
                    continue
                if '.dist-info/' in đườngDẫn:
                    if đườngDẫn.endswith('/METADATA'):
                        cácĐặcTả.append(GóiGộp.read(giáTrịMục).decode())
                    continue
                if not đườngDẫn.endswith('.py') or '.data/' in đườngDẫn:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + đườngDẫn)
                thêmCuốiMục(đườngDẫn, GóiGộp.read(giáTrịMục))
    elif tênMụcTệp.endswith('.tar.gz') and tên.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py thựcThiLệnh 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(DữLiệu), mode='r|gz') as GóiGộp:
            danhSáchCácGốc = set()
            sốLượngMục = 0
            cỡTổngCộng = 0
            for giáTrịMục in GóiGộp:
                sốLượngMục += 1
                cỡTổngCộng += giáTrịMục.size
                if sốLượngMục > 256 or cỡTổngCộng > 1048576:
                    raise ValueError('giáTrịKhoLưuTrữ giảiPhóngLưuTrữ cỡ giáTrịGiớiHạn 초과')
                thẩmĐịnhĐườngDẫn(giáTrịMục.name, False)
                cácPhần = giáTrịMục.name.split('/')
                danhSáchCácGốc.add(cácPhần[0])
                if giáTrịMục.isdir():
                    continue
                if not giáTrịMục.isfile() or len(cácPhần) < 2:
                    raise ValueError('잘못된 MicroPython câyNguồn 배포형')
                đườngDẫn = '/'.join(cácPhần[1:])
                giáTrịNộiDung = GóiGộp.extractfile(giáTrịMục).read()
                if đườngDẫn.endswith('PKG-INFO'):
                    cácĐặcTả.append(giáTrịNộiDung.decode())
                elif đườngDẫn.endswith('.py') and đườngDẫn not in ('setup.py',):
                    thêmCuốiMục(đườngDẫn, giáTrịNộiDung)
                elif '.egg-info/' not in đườngDẫn and not đườngDẫn.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + đườngDẫn)
            if len(danhSáchCácGốc) != 1:
                raise ValueError('MicroPython 소스의 giáTrịGốcCây 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* câyNguồn 배포형이 필요합니다.')
    if not cácMụcTệp or len(cácĐặcTả) != 1:
        raise ValueError('소스와 giáTrịBảnPhânPhối 메타데이터가 필요합니다.')
    đặcTả = email.parser.Parser().parsestr(cácĐặcTả[0])
    if phânTíchCúPhápYêuCầu(đặcTả.get('Name', ''))[0] != tên or đặcTả.get('Version') != giáTrịPhiênBản:
        raise ValueError('giáTrịBảnPhânPhối 메타데이터의 tên·버전 불일치')
    if đặcTả.get_all('Requires-Dist') or đặcTả.get_all('Requires'):
        raise ValueError('자동 cácPhụThuộc 해결은 아직 지원하지 않습니다. cácPhụThuộc 없는 호환 꾸러미를 사용하십시오.')
    return cácMụcTệp


def đọcWeb(địaChỉ, giớiHạnSứcChứa):
    if not địaChỉ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS giáTrịBảnPhânPhối 주소만 허용합니다.')
    with urllib.request.urlopen(địaChỉ, timeout=30) as lờiĐáp:
        if not lờiĐáp.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 giáTrịBảnPhânPhối địaChỉ giáTrịDiChuyển')
        DữLiệu = lờiĐáp.read(giớiHạnSứcChứa + 1)
    if len(DữLiệu) > giớiHạnSứcChứa:
        raise ValueError('giáTrịBảnPhânPhối Tệp cỡ giáTrịGiớiHạn 초과')
    return DữLiệu


def góiGộpChuyểnGiao(tên, giáTrịPhiênBản, cácMụcTệp, giáTrịGốc):
    đặcTả = {'name': tên, 'version': giáTrịPhiênBản, 'source': giáTrịGốc, 'files': [
        {'path': đườngDẫn, 'size': len(DữLiệu), 'sha256': hashlib.sha256(DữLiệu).hexdigest()}
        for đườngDẫn, DữLiệu in sorted(cácMụcTệp.items())]}
    giáTrịĐầu = json.dumps(đặcTả, ensure_ascii=False).encode()
    if len(giáTrịĐầu) > 8192:
        raise ValueError('GóiGộp đặcTả cỡ 초과')
    return b'JKP1' + struct.pack('>I', len(giáTrịĐầu)) + giáTrịĐầu + b''.join(cácMụcTệp[giáTrịMục['path']] for giáTrịMục in đặcTả['files'])


class khoNguồnGóiGộp:
    def __init__(giáTrịBảnThân, đườngDẫn, làNgoạiTuyến=False):
        giáTrịBảnThân.đườngDẫn = Path(đườngDẫn)
        giáTrịBảnThân.đườngDẫn.mkdir(parents=True, exist_ok=True)
        giáTrịBảnThân.làNgoạiTuyến = làNgoạiTuyến

    def chuẩnBị(giáTrịBảnThân, yêuCầu):
        tên, giáTrịPhiênBản = phânTíchCúPhápYêuCầu(yêuCầu)
        vậtLiệuPhím = tên + ('==' + giáTrịPhiênBản if giáTrịPhiênBản else '')
        đườngDẫnNhậtKý = giáTrịBảnThân.đườngDẫn / (vậtLiệuPhím + '.json')
        đườngDẫnBảnPhânPhối = giáTrịBảnThân.đườngDẫn / (vậtLiệuPhím + '.archive')
        if đườngDẫnNhậtKý.is_file() and đườngDẫnBảnPhânPhối.is_file():
            bảnGhiNhậtKý = json.loads(đườngDẫnNhậtKý.read_text())
            DữLiệu = đườngDẫnBảnPhânPhối.read_bytes()
            if hashlib.sha256(DữLiệu).hexdigest() != bảnGhiNhậtKý['sha256']:
                raise ValueError('저장된 giáTrịBảnPhânPhối 파일의 SHA-256 불일치')
        else:
            if giáTrịBảnThân.làNgoạiTuyến:
                raise ValueError('làNgoạiTuyến 저장소에 없는 GóiGộp: ' + yêuCầu)
            địaChỉ = 'https://pypi.org/pypi/' + tên + ('/' + giáTrịPhiênBản if giáTrịPhiênBản else '') + '/json'
            thôngTinHệThống = json.loads(đọcWeb(địaChỉ, 4194304).decode())
            if thôngTinHệThống['info'].get('requires_dist'):
                raise ValueError('자동 cácPhụThuộc 해결은 아직 지원하지 않습니다.')
            ứngViên = [giáTrịMục for giáTrịMục in thôngTinHệThống['urls'] if not giáTrịMục.get('yanked') and giáTrịMục['filename'].endswith('-none-any.whl')]
            if not ứngViên and tên.startswith('micropython-'):
                ứngViên = [giáTrịMục for giáTrịMục in thôngTinHệThống['urls'] if not giáTrịMục.get('yanked') and giáTrịMục['filename'].endswith('.tar.gz')]
            if not ứngViên:
                raise ValueError('지원되는 순수 Python giáTrịBảnPhânPhối 파일이 없습니다.')
            giáTrịViệcChọn = ứngViên[0]
            DữLiệu = đọcWeb(giáTrịViệcChọn['url'], 4194304)
            if hashlib.sha256(DữLiệu).hexdigest() != giáTrịViệcChọn['digests']['sha256']:
                raise ValueError('PyPI giáTrịBảnPhânPhối Tệp SHA-256 불일치')
            bảnGhiNhậtKý = {'name': tên, 'version': thôngTinHệThống['info']['version'], 'filename': giáTrịViệcChọn['filename'],
                    'url': giáTrịViệcChọn['url'], 'sha256': giáTrịViệcChọn['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            giảiNén(bảnGhiNhậtKý['filename'], DữLiệu, tên, bảnGhiNhậtKý['version'])
            đườngDẫnBảnPhânPhối.write_bytes(DữLiệu)
            đườngDẫnNhậtKý.write_text(json.dumps(bảnGhiNhậtKý, ensure_ascii=False, indent=2) + '\n')
        if bảnGhiNhậtKý['name'] != tên or giáTrịPhiênBản and bảnGhiNhậtKý['version'] != giáTrịPhiênBản:
            raise ValueError('gốcCâyKhoNguồn tên·버전 불일치')
        cácMụcTệp = giảiNén(bảnGhiNhậtKý['filename'], DữLiệu, tên, bảnGhiNhậtKý['version'])
        return góiGộpChuyểnGiao(tên, bảnGhiNhậtKý['version'], cácMụcTệp, bảnGhiNhậtKý['url'])


class yêuCầuGóiGộp(socketserver.BaseRequestHandler):
    def handle(giáTrịBảnThân):
        giáTrịBảnThân.request.settimeout(10)
        try:
            yêuCầu = bytearray()
            while b'\n' not in yêuCầu and len(yêuCầu) < 100:
                giáTrịĐoạn = giáTrịBảnThân.request.recv(100 - len(yêuCầu))
                if not giáTrịĐoạn:
                    return
                yêuCầu.extend(giáTrịĐoạn)
            if not yêuCầu.endswith(b'\n') or yêuCầu.count(b'\n') != 1:
                raise ValueError('잘못된 GóiGộp yêuCầu')
            lờiĐáp = giáTrịBảnThân.server.gốcCâyKhoNguồn.chuẩnBị(yêuCầu[:-1].decode('ascii'))
        except Exception as lỗi:
            giáTrịĐầu = json.dumps({'error': str(lỗi)[:500]}, ensure_ascii=False).encode()
            lờiĐáp = b'JKP1' + struct.pack('>I', len(giáTrịĐầu)) + giáTrịĐầu
        try:
            giáTrịBảnThân.request.sendall(lờiĐáp)
        except OSError:
            pass


class chuyểnTiếpGóiGộp:
    def __init__(giáTrịBảnThân, sốCổng=8027, đườngDẫn=None, làNgoạiTuyến=False):
        giáTrịBảnThân.giáTrịMáyChủ = socketserver.TCPServer(('127.0.0.1', sốCổng), yêuCầuGóiGộp, bind_and_activate=False)
        giáTrịBảnThân.giáTrịMáyChủ.allow_reuse_address = True
        giáTrịBảnThân.giáTrịMáyChủ.server_bind()
        giáTrịBảnThân.giáTrịMáyChủ.server_activate()
        giáTrịBảnThân.giáTrịMáyChủ.gốcCâyKhoNguồn = khoNguồnGóiGộp(đườngDẫn or gốcCâyDựÁn/'build/pip-cache', làNgoạiTuyến)
        giáTrịBảnThân.sốCổng = giáTrịBảnThân.giáTrịMáyChủ.server_address[1]
        giáTrịBảnThân.giáTrịLuồngChạy = threading.Thread(target=giáTrịBảnThân.giáTrịMáyChủ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(giáTrịBảnThân):
        giáTrịBảnThân.giáTrịLuồngChạy.start()
        return giáTrịBảnThân

    def __exit__(giáTrịBảnThân, *cácĐốiSố):
        giáTrịBảnThân.giáTrịMáyChủ.shutdown()
        giáTrịBảnThân.giáTrịMáyChủ.server_close()
        giáTrịBảnThân.giáTrịLuồngChạy.join(timeout=2)


def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--port', type=int, default=8027)
    BộPhânTích.add_argument('--cache', type=Path, default=gốcCâyDựÁn/'build/pip-cache')
    BộPhânTích.add_argument('--offline', action='store_true')
    BộPhânTích.add_argument('--fetch', help='thựcThiLệnh 없이 호환 giáTrịBảnPhânPhối 파일을 내려받아 CácPhépKiểmTra·giáTrịCất')
    cácĐốiSố = BộPhânTích.parse_args()
    if cácĐốiSố.fetch:
        DữLiệu = khoNguồnGóiGộp(cácĐốiSố.cache, cácĐốiSố.offline).chuẩnBị(cácĐốiSố.fetch)
        print('GóiGộp chuẩnBị làĐầyĐủ:', cácĐốiSố.fetch, len(DữLiệu), 'giáTrịByte')
        return
    with chuyểnTiếpGóiGộp(cácĐốiSố.port, cácĐốiSố.cache, cácĐốiSố.offline) as chuyểnTiếpGiáTrị:
        print('GóiGộp chuyểnTiếpGiáTrị: 127.0.0.1:' + str(chuyểnTiếpGiáTrị.sốCổng), flush=True)
        try:
            chuyểnTiếpGiáTrị.giáTrịLuồngChạy.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    chạy()
