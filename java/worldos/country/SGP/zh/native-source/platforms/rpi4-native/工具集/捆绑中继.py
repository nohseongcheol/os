#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 中继值. 게스트는 TCP로 받은 소스를 직접 安装值·실행한다."""
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

项目根 = Path(__file__).resolve().parents[1]


def 解析申请(申请):
    是否已匹配 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 申请)
    if not 是否已匹配:
        raise ValueError('软件包 名称 또는 名称==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 是否已匹配[1]).lower(), 是否已匹配[2]


def 有效性校验路径(名称, 安装过程路径=True):
    路径 = PurePosixPath(名称)
    if 路径.is_absolute() or any(子部分值 in ('', '.', '..') or 子部分值.startswith('.') for 子部分值 in 名称.split('/')):
        raise ValueError('허용하지 않는 软件包 路径: ' + 名称)
    if '\\' in 名称 or any(ord(字符值) < 32 or ord(字符值) == 127 for 字符值 in 名称):
        raise ValueError('잘못된 软件包 路径 字符')
    if 安装过程路径 and (len(('/lib/' + 名称).encode()) > 63 or 名称 in ('中文.py', '软件包.py')):
        raise ValueError('软件包 路径 限制值 또는 默认值 库 충돌: ' + 名称)
    return 名称


def 解压缩(文件条目名称, 数据, 名称, 版本值):
    文件条目列 = {}
    规格列 = []
    def 追加条目(路径, 内容值):
        有效性校验路径(路径)
        if 路径 in 文件条目列:
            raise ValueError('중복 软件包 路径: ' + 路径)
        if len(内容值) > 16384:
            raise ValueError('파일당 16 KiB 限制值 초과: ' + 路径)
        内容值.decode('utf-8')
        文件条目列[路径] = 内容值
        if len(文件条目列) > 16 or sum(map(len, 文件条目列.values())) > 65536:
            raise ValueError('꾸러미는 源代码树 16개·总计值 64 KiB 이하여야 합니다.')
    if 文件条目名称.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(数据)) as 软件包:
            条目列列表 = 软件包.infolist()
            if len(条目列列表) > 256 or sum(条目值.file_size for 条目值 in 条目列列表) > 1048576:
                raise ValueError('存档值 释放存储装置 大小 限制值 초과')
            契约列表 = [条目值 for 条目值 in 条目列列表 if 条目值.filename.endswith('.dist-info/WHEEL')]
            if len(契约列表) != 1:
                raise ValueError('wheel 契约值 명세가 필요합니다.')
            契约值 = email.parser.Parser().parsestr(软件包.read(契约列表[0]).decode())
            if 契约值.get('Root-Is-Purelib', '').lower() != 'true' or not 文件条目名称.endswith('-none-any.whl'):
                raise ValueError('C 扩展名值·플랫폼 전용 wheel은 지원하지 않습니다.')
            for 条目值 in 条目列列表:
                路径 = 条目值.filename.rstrip('/')
                有效性校验路径(路径, False)
                if (条目值.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 数 없습니다.')
                if 条目值.filename.endswith('/'):
                    continue
                if '.dist-info/' in 路径:
                    if 路径.endswith('/METADATA'):
                        规格列.append(软件包.read(条目值).decode())
                    continue
                if not 路径.endswith('.py') or '.data/' in 路径:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + 路径)
                追加条目(路径, 软件包.read(条目值))
    elif 文件条目名称.endswith('.tar.gz') and 名称.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 执行命令 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(数据), mode='r|gz') as 软件包:
            根列列表 = set()
            条目个数 = 0
            总计大小 = 0
            for 条目值 in 软件包:
                条目个数 += 1
                总计大小 += 条目值.size
                if 条目个数 > 256 or 总计大小 > 1048576:
                    raise ValueError('存档值 释放存储装置 大小 限制值 초과')
                有效性校验路径(条目值.name, False)
                部件列 = 条目值.name.split('/')
                根列列表.add(部件列[0])
                if 条目值.isdir():
                    continue
                if not 条目值.isfile() or len(部件列) < 2:
                    raise ValueError('잘못된 MicroPython 源代码树 배포형')
                路径 = '/'.join(部件列[1:])
                内容值 = 软件包.extractfile(条目值).read()
                if 路径.endswith('PKG-INFO'):
                    规格列.append(内容值.decode())
                elif 路径.endswith('.py') and 路径 not in ('setup.py',):
                    追加条目(路径, 内容值)
                elif '.egg-info/' not in 路径 and not 路径.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + 路径)
            if len(根列列表) != 1:
                raise ValueError('MicroPython 소스의 根值 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* 源代码树 배포형이 필요합니다.')
    if not 文件条目列 or len(规格列) != 1:
        raise ValueError('소스와 分发值 메타데이터가 필요합니다.')
    规格 = email.parser.Parser().parsestr(规格列[0])
    if 解析申请(规格.get('Name', ''))[0] != 名称 or 规格.get('Version') != 版本值:
        raise ValueError('分发值 메타데이터의 名称·버전 불일치')
    if 规格.get_all('Requires-Dist') or 规格.get_all('Requires'):
        raise ValueError('자동 依赖项列 해결은 아직 지원하지 않습니다. 依赖项列 없는 호환 꾸러미를 사용하십시오.')
    return 文件条目列


def 读取网页(地址, 容量限制):
    if not 地址.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 分发值 주소만 허용합니다.')
    with urllib.request.urlopen(地址, timeout=30) as 回复:
        if not 回复.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 分发值 地址 移动值')
        数据 = 回复.read(容量限制 + 1)
    if len(数据) > 容量限制:
        raise ValueError('分发值 文件 大小 限制值 초과')
    return 数据


def 传送捆绑(名称, 版本值, 文件条目列, 原点值):
    规格 = {'name': 名称, 'version': 版本值, 'source': 原点值, 'files': [
        {'path': 路径, 'size': len(数据), 'sha256': hashlib.sha256(数据).hexdigest()}
        for 路径, 数据 in sorted(文件条目列.items())]}
    头值 = json.dumps(规格, ensure_ascii=False).encode()
    if len(头值) > 8192:
        raise ValueError('软件包 规格 大小 초과')
    return b'JKP1' + struct.pack('>I', len(头值)) + 头值 + b''.join(文件条目列[条目值['path']] for 条目值 in 规格['files'])


class 捆绑代码库:
    def __init__(自身值, 路径, 是否离线=False):
        自身值.路径 = Path(路径)
        自身值.路径.mkdir(parents=True, exist_ok=True)
        自身值.是否离线 = 是否离线

    def 准备(自身值, 申请):
        名称, 版本值 = 解析申请(申请)
        键材料 = 名称 + ('==' + 版本值 if 版本值 else '')
        日志路径 = 自身值.路径 / (键材料 + '.json')
        分发路径 = 自身值.路径 / (键材料 + '.archive')
        if 日志路径.is_file() and 分发路径.is_file():
            日志记录 = json.loads(日志路径.read_text())
            数据 = 分发路径.read_bytes()
            if hashlib.sha256(数据).hexdigest() != 日志记录['sha256']:
                raise ValueError('저장된 分发值 파일의 SHA-256 불일치')
        else:
            if 自身值.是否离线:
                raise ValueError('是否离线 저장소에 없는 软件包: ' + 申请)
            地址 = 'https://pypi.org/pypi/' + 名称 + ('/' + 版本值 if 版本值 else '') + '/json'
            系统信息 = json.loads(读取网页(地址, 4194304).decode())
            if 系统信息['info'].get('requires_dist'):
                raise ValueError('자동 依赖项列 해결은 아직 지원하지 않습니다.')
            候选 = [条目值 for 条目值 in 系统信息['urls'] if not 条目值.get('yanked') and 条目值['filename'].endswith('-none-any.whl')]
            if not 候选 and 名称.startswith('micropython-'):
                候选 = [条目值 for 条目值 in 系统信息['urls'] if not 条目值.get('yanked') and 条目值['filename'].endswith('.tar.gz')]
            if not 候选:
                raise ValueError('지원되는 순수 Python 分发值 파일이 없습니다.')
            选中状态值 = 候选[0]
            数据 = 读取网页(选中状态值['url'], 4194304)
            if hashlib.sha256(数据).hexdigest() != 选中状态值['digests']['sha256']:
                raise ValueError('PyPI 分发值 文件 SHA-256 불일치')
            日志记录 = {'name': 名称, 'version': 系统信息['info']['version'], 'filename': 选中状态值['filename'],
                    'url': 选中状态值['url'], 'sha256': 选中状态值['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            解压缩(日志记录['filename'], 数据, 名称, 日志记录['version'])
            分发路径.write_bytes(数据)
            日志路径.write_text(json.dumps(日志记录, ensure_ascii=False, indent=2) + '\n')
        if 日志记录['name'] != 名称 or 版本值 and 日志记录['version'] != 版本值:
            raise ValueError('代码库根 名称·버전 불일치')
        文件条目列 = 解压缩(日志记录['filename'], 数据, 名称, 日志记录['version'])
        return 传送捆绑(名称, 日志记录['version'], 文件条目列, 日志记录['url'])


class 捆绑申请(socketserver.BaseRequestHandler):
    def handle(自身值):
        自身值.request.settimeout(10)
        try:
            申请 = bytearray()
            while b'\n' not in 申请 and len(申请) < 100:
                片段值 = 自身值.request.recv(100 - len(申请))
                if not 片段值:
                    return
                申请.extend(片段值)
            if not 申请.endswith(b'\n') or 申请.count(b'\n') != 1:
                raise ValueError('잘못된 软件包 申请')
            回复 = 自身值.server.代码库根.准备(申请[:-1].decode('ascii'))
        except Exception as 错误:
            头值 = json.dumps({'error': str(错误)[:500]}, ensure_ascii=False).encode()
            回复 = b'JKP1' + struct.pack('>I', len(头值)) + 头值
        try:
            自身值.request.sendall(回复)
        except OSError:
            pass


class 捆绑中继:
    def __init__(自身值, 端口编号=8027, 路径=None, 是否离线=False):
        自身值.服务器值 = socketserver.TCPServer(('127.0.0.1', 端口编号), 捆绑申请, bind_and_activate=False)
        自身值.服务器值.allow_reuse_address = True
        自身值.服务器值.server_bind()
        自身值.服务器值.server_activate()
        自身值.服务器值.代码库根 = 捆绑代码库(路径 or 项目根/'build/pip-cache', 是否离线)
        自身值.端口编号 = 自身值.服务器值.server_address[1]
        自身值.线程值 = threading.Thread(target=自身值.服务器值.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(自身值):
        自身值.线程值.start()
        return 自身值

    def __exit__(自身值, *实参):
        自身值.服务器值.shutdown()
        自身值.服务器值.server_close()
        自身值.线程值.join(timeout=2)


def 运行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--port', type=int, default=8027)
    解析器.add_argument('--cache', type=Path, default=项目根/'build/pip-cache')
    解析器.add_argument('--offline', action='store_true')
    解析器.add_argument('--fetch', help='执行命令 없이 호환 分发值 파일을 내려받아 检查项·存储值')
    实参 = 解析器.parse_args()
    if 实参.fetch:
        数据 = 捆绑代码库(实参.cache, 实参.offline).准备(实参.fetch)
        print('软件包 准备 是否完成:', 实参.fetch, len(数据), '字节值')
        return
    with 捆绑中继(实参.port, 实参.cache, 实参.offline) as 中继值:
        print('软件包 中继值: 127.0.0.1:' + str(中继值.端口编号), flush=True)
        try:
            中继值.线程值.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    运行()
