#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 中繼值. 게스트는 TCP로 받은 소스를 직접 安裝值·실행한다."""
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

項目根 = Path(__file__).resolve().parents[1]


def 解析申請(申請):
    是否已匹配 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 申請)
    if not 是否已匹配:
        raise ValueError('軟件包 名稱 또는 名稱==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 是否已匹配[1]).lower(), 是否已匹配[2]


def 有效性校驗路徑(名稱, 安裝過程路徑=True):
    路徑 = PurePosixPath(名稱)
    if 路徑.is_absolute() or any(子部分值 in ('', '.', '..') or 子部分值.startswith('.') for 子部分值 in 名稱.split('/')):
        raise ValueError('허용하지 않는 軟件包 路徑: ' + 名稱)
    if '\\' in 名稱 or any(ord(字元值) < 32 or ord(字元值) == 127 for 字元值 in 名稱):
        raise ValueError('잘못된 軟件包 路徑 字元')
    if 安裝過程路徑 and (len(('/lib/' + 名稱).encode()) > 63 or 名稱 in ('中文.py', '軟件包.py')):
        raise ValueError('軟件包 路徑 限制值 또는 默認值 庫 충돌: ' + 名稱)
    return 名稱


def 解壓縮(檔案條目名稱, 資料, 名稱, 版本值):
    檔案條目列 = {}
    規格列 = []
    def 追加條目(路徑, 內容值):
        有效性校驗路徑(路徑)
        if 路徑 in 檔案條目列:
            raise ValueError('중복 軟件包 路徑: ' + 路徑)
        if len(內容值) > 16384:
            raise ValueError('파일당 16 KiB 限制值 초과: ' + 路徑)
        內容值.decode('utf-8')
        檔案條目列[路徑] = 內容值
        if len(檔案條目列) > 16 or sum(map(len, 檔案條目列.values())) > 65536:
            raise ValueError('꾸러미는 原始碼樹 16개·總計值 64 KiB 이하여야 합니다.')
    if 檔案條目名稱.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(資料)) as 軟件包:
            條目列列表 = 軟件包.infolist()
            if len(條目列列表) > 256 or sum(條目值.file_size for 條目值 in 條目列列表) > 1048576:
                raise ValueError('存檔值 釋放存儲裝置 大小 限制值 초과')
            契約列表 = [條目值 for 條目值 in 條目列列表 if 條目值.filename.endswith('.dist-info/WHEEL')]
            if len(契約列表) != 1:
                raise ValueError('wheel 契約值 명세가 필요합니다.')
            契約值 = email.parser.Parser().parsestr(軟件包.read(契約列表[0]).decode())
            if 契約值.get('Root-Is-Purelib', '').lower() != 'true' or not 檔案條目名稱.endswith('-none-any.whl'):
                raise ValueError('C 擴展名值·플랫폼 전용 wheel은 지원하지 않습니다.')
            for 條目值 in 條目列列表:
                路徑 = 條目值.filename.rstrip('/')
                有效性校驗路徑(路徑, False)
                if (條目值.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 數 없습니다.')
                if 條目值.filename.endswith('/'):
                    continue
                if '.dist-info/' in 路徑:
                    if 路徑.endswith('/METADATA'):
                        規格列.append(軟件包.read(條目值).decode())
                    continue
                if not 路徑.endswith('.py') or '.data/' in 路徑:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + 路徑)
                追加條目(路徑, 軟件包.read(條目值))
    elif 檔案條目名稱.endswith('.tar.gz') and 名稱.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 執行命令 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(資料), mode='r|gz') as 軟件包:
            根列列表 = set()
            條目個數 = 0
            總計大小 = 0
            for 條目值 in 軟件包:
                條目個數 += 1
                總計大小 += 條目值.size
                if 條目個數 > 256 or 總計大小 > 1048576:
                    raise ValueError('存檔值 釋放存儲裝置 大小 限制值 초과')
                有效性校驗路徑(條目值.name, False)
                部件列 = 條目值.name.split('/')
                根列列表.add(部件列[0])
                if 條目值.isdir():
                    continue
                if not 條目值.isfile() or len(部件列) < 2:
                    raise ValueError('잘못된 MicroPython 原始碼樹 배포형')
                路徑 = '/'.join(部件列[1:])
                內容值 = 軟件包.extractfile(條目值).read()
                if 路徑.endswith('PKG-INFO'):
                    規格列.append(內容值.decode())
                elif 路徑.endswith('.py') and 路徑 not in ('setup.py',):
                    追加條目(路徑, 內容值)
                elif '.egg-info/' not in 路徑 and not 路徑.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + 路徑)
            if len(根列列表) != 1:
                raise ValueError('MicroPython 소스의 根值 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* 原始碼樹 배포형이 필요합니다.')
    if not 檔案條目列 or len(規格列) != 1:
        raise ValueError('소스와 分發值 메타데이터가 필요합니다.')
    規格 = email.parser.Parser().parsestr(規格列[0])
    if 解析申請(規格.get('Name', ''))[0] != 名稱 or 規格.get('Version') != 版本值:
        raise ValueError('分發值 메타데이터의 名稱·버전 불일치')
    if 規格.get_all('Requires-Dist') or 規格.get_all('Requires'):
        raise ValueError('자동 依賴項列 해결은 아직 지원하지 않습니다. 依賴項列 없는 호환 꾸러미를 사용하십시오.')
    return 檔案條目列


def 讀取網頁(地址, 容量限制):
    if not 地址.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 分發值 주소만 허용합니다.')
    with urllib.request.urlopen(地址, timeout=30) as 回覆:
        if not 回覆.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 分發值 地址 移動值')
        資料 = 回覆.read(容量限制 + 1)
    if len(資料) > 容量限制:
        raise ValueError('分發值 檔案 大小 限制值 초과')
    return 資料


def 傳送捆綁(名稱, 版本值, 檔案條目列, 原點值):
    規格 = {'name': 名稱, 'version': 版本值, 'source': 原點值, 'files': [
        {'path': 路徑, 'size': len(資料), 'sha256': hashlib.sha256(資料).hexdigest()}
        for 路徑, 資料 in sorted(檔案條目列.items())]}
    頭值 = json.dumps(規格, ensure_ascii=False).encode()
    if len(頭值) > 8192:
        raise ValueError('軟件包 規格 大小 초과')
    return b'JKP1' + struct.pack('>I', len(頭值)) + 頭值 + b''.join(檔案條目列[條目值['path']] for 條目值 in 規格['files'])


class 捆綁代碼庫:
    def __init__(自身值, 路徑, 是否離線=False):
        自身值.路徑 = Path(路徑)
        自身值.路徑.mkdir(parents=True, exist_ok=True)
        自身值.是否離線 = 是否離線

    def 準備(自身值, 申請):
        名稱, 版本值 = 解析申請(申請)
        鍵材料 = 名稱 + ('==' + 版本值 if 版本值 else '')
        日誌路徑 = 自身值.路徑 / (鍵材料 + '.json')
        分發路徑 = 自身值.路徑 / (鍵材料 + '.archive')
        if 日誌路徑.is_file() and 分發路徑.is_file():
            日誌記錄 = json.loads(日誌路徑.read_text())
            資料 = 分發路徑.read_bytes()
            if hashlib.sha256(資料).hexdigest() != 日誌記錄['sha256']:
                raise ValueError('저장된 分發值 파일의 SHA-256 불일치')
        else:
            if 自身值.是否離線:
                raise ValueError('是否離線 저장소에 없는 軟件包: ' + 申請)
            地址 = 'https://pypi.org/pypi/' + 名稱 + ('/' + 版本值 if 版本值 else '') + '/json'
            系統信息 = json.loads(讀取網頁(地址, 4194304).decode())
            if 系統信息['info'].get('requires_dist'):
                raise ValueError('자동 依賴項列 해결은 아직 지원하지 않습니다.')
            候選 = [條目值 for 條目值 in 系統信息['urls'] if not 條目值.get('yanked') and 條目值['filename'].endswith('-none-any.whl')]
            if not 候選 and 名稱.startswith('micropython-'):
                候選 = [條目值 for 條目值 in 系統信息['urls'] if not 條目值.get('yanked') and 條目值['filename'].endswith('.tar.gz')]
            if not 候選:
                raise ValueError('지원되는 순수 Python 分發值 파일이 없습니다.')
            選中狀態值 = 候選[0]
            資料 = 讀取網頁(選中狀態值['url'], 4194304)
            if hashlib.sha256(資料).hexdigest() != 選中狀態值['digests']['sha256']:
                raise ValueError('PyPI 分發值 檔案 SHA-256 불일치')
            日誌記錄 = {'name': 名稱, 'version': 系統信息['info']['version'], 'filename': 選中狀態值['filename'],
                    'url': 選中狀態值['url'], 'sha256': 選中狀態值['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            解壓縮(日誌記錄['filename'], 資料, 名稱, 日誌記錄['version'])
            分發路徑.write_bytes(資料)
            日誌路徑.write_text(json.dumps(日誌記錄, ensure_ascii=False, indent=2) + '\n')
        if 日誌記錄['name'] != 名稱 or 版本值 and 日誌記錄['version'] != 版本值:
            raise ValueError('代碼庫根 名稱·버전 불일치')
        檔案條目列 = 解壓縮(日誌記錄['filename'], 資料, 名稱, 日誌記錄['version'])
        return 傳送捆綁(名稱, 日誌記錄['version'], 檔案條目列, 日誌記錄['url'])


class 捆綁申請(socketserver.BaseRequestHandler):
    def handle(自身值):
        自身值.request.settimeout(10)
        try:
            申請 = bytearray()
            while b'\n' not in 申請 and len(申請) < 100:
                片段值 = 自身值.request.recv(100 - len(申請))
                if not 片段值:
                    return
                申請.extend(片段值)
            if not 申請.endswith(b'\n') or 申請.count(b'\n') != 1:
                raise ValueError('잘못된 軟件包 申請')
            回覆 = 自身值.server.代碼庫根.準備(申請[:-1].decode('ascii'))
        except Exception as 錯誤:
            頭值 = json.dumps({'error': str(錯誤)[:500]}, ensure_ascii=False).encode()
            回覆 = b'JKP1' + struct.pack('>I', len(頭值)) + 頭值
        try:
            自身值.request.sendall(回覆)
        except OSError:
            pass


class 捆綁中繼:
    def __init__(自身值, 埠編號=8027, 路徑=None, 是否離線=False):
        自身值.服務器值 = socketserver.TCPServer(('127.0.0.1', 埠編號), 捆綁申請, bind_and_activate=False)
        自身值.服務器值.allow_reuse_address = True
        自身值.服務器值.server_bind()
        自身值.服務器值.server_activate()
        自身值.服務器值.代碼庫根 = 捆綁代碼庫(路徑 or 項目根/'build/pip-cache', 是否離線)
        自身值.埠編號 = 自身值.服務器值.server_address[1]
        自身值.執行緒值 = threading.Thread(target=自身值.服務器值.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(自身值):
        自身值.執行緒值.start()
        return 自身值

    def __exit__(自身值, *實參):
        自身值.服務器值.shutdown()
        自身值.服務器值.server_close()
        自身值.執行緒值.join(timeout=2)


def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--port', type=int, default=8027)
    解析器.add_argument('--cache', type=Path, default=項目根/'build/pip-cache')
    解析器.add_argument('--offline', action='store_true')
    解析器.add_argument('--fetch', help='執行命令 없이 호환 分發值 파일을 내려받아 檢查項·存儲值')
    實參 = 解析器.parse_args()
    if 實參.fetch:
        資料 = 捆綁代碼庫(實參.cache, 實參.offline).準備(實參.fetch)
        print('軟件包 準備 是否完成:', 實參.fetch, len(資料), '位元組值')
        return
    with 捆綁中繼(實參.port, 實參.cache, 實參.offline) as 中繼值:
        print('軟件包 中繼值: 127.0.0.1:' + str(中繼值.埠編號), flush=True)
        try:
            中繼值.執行緒值.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    運行()
