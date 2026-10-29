#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 値中継. 게스트는 TCP로 받은 소스를 직접 値導入·실행한다."""
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

計画根 = Path(__file__).resolve().parents[1]


def 要求解析(要求):
    判定照合済み = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 要求)
    if not 判定照合済み:
        raise ValueError('パッケージ 名前 또는 名前==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 判定照合済み[1]).lower(), 判定照合済み[2]


def 経路妥当性検査(名前, 設置経路=True):
    経路 = PurePosixPath(名前)
    if 経路.is_absolute() or any(部分要素値 in ('', '.', '..') or 部分要素値.startswith('.') for 部分要素値 in 名前.split('/')):
        raise ValueError('허용하지 않는 パッケージ 経路: ' + 名前)
    if '\\' in 名前 or any(ord(文字値) < 32 or ord(文字値) == 127 for 文字値 in 名前):
        raise ValueError('잘못된 パッケージ 経路 文字')
    if 設置経路 and (len(('/lib/' + 名前).encode()) > 63 or 名前 in ('日本語.py', 'パッケージ.py')):
        raise ValueError('パッケージ 経路 上限値 또는 既定値 ライブラリ 충돌: ' + 名前)
    return 名前


def 展開(ファイル入口名前, データ, 名前, 版値):
    ファイル登録項目一覧 = {}
    仕様一覧 = []
    def 入口追記(経路, 内容物値):
        経路妥当性検査(経路)
        if 経路 in ファイル登録項目一覧:
            raise ValueError('중복 パッケージ 経路: ' + 経路)
        if len(内容物値) > 16384:
            raise ValueError('파일당 16 KiB 上限値 초과: ' + 経路)
        内容物値.decode('utf-8')
        ファイル登録項目一覧[経路] = 内容物値
        if len(ファイル登録項目一覧) > 16 or sum(map(len, ファイル登録項目一覧.values())) > 65536:
            raise ValueError('꾸러미는 ソース木 16개·合計値 64 KiB 이하여야 합니다.')
    if ファイル入口名前.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(データ)) as パッケージ:
            登録項目一覧一覧 = パッケージ.infolist()
            if len(登録項目一覧一覧) > 256 or sum(入口値.file_size for 入口値 in 登録項目一覧一覧) > 1048576:
                raise ValueError('書庫値 記憶装置解放 容量 上限値 초과')
            契約一覧 = [入口値 for 入口値 in 登録項目一覧一覧 if 入口値.filename.endswith('.dist-info/WHEEL')]
            if len(契約一覧) != 1:
                raise ValueError('wheel 契約値 명세가 필요합니다.')
            契約値 = email.parser.Parser().parsestr(パッケージ.read(契約一覧[0]).decode())
            if 契約値.get('Root-Is-Purelib', '').lower() != 'true' or not ファイル入口名前.endswith('-none-any.whl'):
                raise ValueError('C 拡張子値·플랫폼 전용 wheel은 지원하지 않습니다.')
            for 入口値 in 登録項目一覧一覧:
                経路 = 入口値.filename.rstrip('/')
                経路妥当性検査(経路, False)
                if (入口値.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 数 없습니다.')
                if 入口値.filename.endswith('/'):
                    continue
                if '.dist-info/' in 経路:
                    if 経路.endswith('/METADATA'):
                        仕様一覧.append(パッケージ.read(入口値).decode())
                    continue
                if not 経路.endswith('.py') or '.data/' in 経路:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + 経路)
                入口追記(経路, パッケージ.read(入口値))
    elif ファイル入口名前.endswith('.tar.gz') and 名前.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 命令実行 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(データ), mode='r|gz') as パッケージ:
            根一覧一覧 = set()
            入口個数 = 0
            合計容量 = 0
            for 入口値 in パッケージ:
                入口個数 += 1
                合計容量 += 入口値.size
                if 入口個数 > 256 or 合計容量 > 1048576:
                    raise ValueError('書庫値 記憶装置解放 容量 上限値 초과')
                経路妥当性検査(入口値.name, False)
                構成要素一覧 = 入口値.name.split('/')
                根一覧一覧.add(構成要素一覧[0])
                if 入口値.isdir():
                    continue
                if not 入口値.isfile() or len(構成要素一覧) < 2:
                    raise ValueError('잘못된 MicroPython ソース木 배포형')
                経路 = '/'.join(構成要素一覧[1:])
                内容物値 = パッケージ.extractfile(入口値).read()
                if 経路.endswith('PKG-INFO'):
                    仕様一覧.append(内容物値.decode())
                elif 経路.endswith('.py') and 経路 not in ('setup.py',):
                    入口追記(経路, 内容物値)
                elif '.egg-info/' not in 経路 and not 経路.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + 経路)
            if len(根一覧一覧) != 1:
                raise ValueError('MicroPython 소스의 根値 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ソース木 배포형이 필요합니다.')
    if not ファイル登録項目一覧 or len(仕様一覧) != 1:
        raise ValueError('소스와 配布値 메타데이터가 필요합니다.')
    仕様 = email.parser.Parser().parsestr(仕様一覧[0])
    if 要求解析(仕様.get('Name', ''))[0] != 名前 or 仕様.get('Version') != 版値:
        raise ValueError('配布値 메타데이터의 名前·버전 불일치')
    if 仕様.get_all('Requires-Dist') or 仕様.get_all('Requires'):
        raise ValueError('자동 依存項目 해결은 아직 지원하지 않습니다. 依存項目 없는 호환 꾸러미를 사용하십시오.')
    return ファイル登録項目一覧


def ウェブ読取(番地, 容積上限):
    if not 番地.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 配布値 주소만 허용합니다.')
    with urllib.request.urlopen(番地, timeout=30) as 返答:
        if not 返答.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 配布値 番地 移動値')
        データ = 返答.read(容積上限 + 1)
    if len(データ) > 容積上限:
        raise ValueError('配布値 ファイル 容量 上限値 초과')
    return データ


def 転送束(名前, 版値, ファイル登録項目一覧, 原点値):
    仕様 = {'name': 名前, 'version': 版値, 'source': 原点値, 'files': [
        {'path': 経路, 'size': len(データ), 'sha256': hashlib.sha256(データ).hexdigest()}
        for 経路, データ in sorted(ファイル登録項目一覧.items())]}
    先頭部値 = json.dumps(仕様, ensure_ascii=False).encode()
    if len(先頭部値) > 8192:
        raise ValueError('パッケージ 仕様 容量 초과')
    return b'JKP1' + struct.pack('>I', len(先頭部値)) + 先頭部値 + b''.join(ファイル登録項目一覧[入口値['path']] for 入口値 in 仕様['files'])


class 束保管庫:
    def __init__(自身値, 経路, 判定非接続=False):
        自身値.経路 = Path(経路)
        自身値.経路.mkdir(parents=True, exist_ok=True)
        自身値.判定非接続 = 判定非接続

    def 用意(自身値, 要求):
        名前, 版値 = 要求解析(要求)
        キー素材 = 名前 + ('==' + 版値 if 版値 else '')
        履歴記録経路 = 自身値.経路 / (キー素材 + '.json')
        配布経路 = 自身値.経路 / (キー素材 + '.archive')
        if 履歴記録経路.is_file() and 配布経路.is_file():
            履歴記録記録 = json.loads(履歴記録経路.read_text())
            データ = 配布経路.read_bytes()
            if hashlib.sha256(データ).hexdigest() != 履歴記録記録['sha256']:
                raise ValueError('저장된 配布値 파일의 SHA-256 불일치')
        else:
            if 自身値.判定非接続:
                raise ValueError('判定非接続 저장소에 없는 パッケージ: ' + 要求)
            番地 = 'https://pypi.org/pypi/' + 名前 + ('/' + 版値 if 版値 else '') + '/json'
            システム情報 = json.loads(ウェブ読取(番地, 4194304).decode())
            if システム情報['info'].get('requires_dist'):
                raise ValueError('자동 依存項目 해결은 아직 지원하지 않습니다.')
            候補 = [入口値 for 入口値 in システム情報['urls'] if not 入口値.get('yanked') and 入口値['filename'].endswith('-none-any.whl')]
            if not 候補 and 名前.startswith('micropython-'):
                候補 = [入口値 for 入口値 in システム情報['urls'] if not 入口値.get('yanked') and 入口値['filename'].endswith('.tar.gz')]
            if not 候補:
                raise ValueError('지원되는 순수 Python 配布値 파일이 없습니다.')
            選択状態値 = 候補[0]
            データ = ウェブ読取(選択状態値['url'], 4194304)
            if hashlib.sha256(データ).hexdigest() != 選択状態値['digests']['sha256']:
                raise ValueError('PyPI 配布値 ファイル SHA-256 불일치')
            履歴記録記録 = {'name': 名前, 'version': システム情報['info']['version'], 'filename': 選択状態値['filename'],
                    'url': 選択状態値['url'], 'sha256': 選択状態値['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            展開(履歴記録記録['filename'], データ, 名前, 履歴記録記録['version'])
            配布経路.write_bytes(データ)
            履歴記録経路.write_text(json.dumps(履歴記録記録, ensure_ascii=False, indent=2) + '\n')
        if 履歴記録記録['name'] != 名前 or 版値 and 履歴記録記録['version'] != 版値:
            raise ValueError('保管庫根 名前·버전 불일치')
        ファイル登録項目一覧 = 展開(履歴記録記録['filename'], データ, 名前, 履歴記録記録['version'])
        return 転送束(名前, 履歴記録記録['version'], ファイル登録項目一覧, 履歴記録記録['url'])


class 束要求(socketserver.BaseRequestHandler):
    def handle(自身値):
        自身値.request.settimeout(10)
        try:
            要求 = bytearray()
            while b'\n' not in 要求 and len(要求) < 100:
                断片値 = 自身値.request.recv(100 - len(要求))
                if not 断片値:
                    return
                要求.extend(断片値)
            if not 要求.endswith(b'\n') or 要求.count(b'\n') != 1:
                raise ValueError('잘못된 パッケージ 要求')
            返答 = 自身値.server.保管庫根.用意(要求[:-1].decode('ascii'))
        except Exception as エラー:
            先頭部値 = json.dumps({'error': str(エラー)[:500]}, ensure_ascii=False).encode()
            返答 = b'JKP1' + struct.pack('>I', len(先頭部値)) + 先頭部値
        try:
            自身値.request.sendall(返答)
        except OSError:
            pass


class 束中継:
    def __init__(自身値, ポート番号=8027, 経路=None, 判定非接続=False):
        自身値.サーバー値 = socketserver.TCPServer(('127.0.0.1', ポート番号), 束要求, bind_and_activate=False)
        自身値.サーバー値.allow_reuse_address = True
        自身値.サーバー値.server_bind()
        自身値.サーバー値.server_activate()
        自身値.サーバー値.保管庫根 = 束保管庫(経路 or 計画根/'build/pip-cache', 判定非接続)
        自身値.ポート番号 = 自身値.サーバー値.server_address[1]
        自身値.スレッド値 = threading.Thread(target=自身値.サーバー値.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(自身値):
        自身値.スレッド値.start()
        return 自身値

    def __exit__(自身値, *引数):
        自身値.サーバー値.shutdown()
        自身値.サーバー値.server_close()
        自身値.スレッド値.join(timeout=2)


def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--port', type=int, default=8027)
    構文解析器.add_argument('--cache', type=Path, default=計画根/'build/pip-cache')
    構文解析器.add_argument('--offline', action='store_true')
    構文解析器.add_argument('--fetch', help='命令実行 없이 호환 配布値 파일을 내려받아 検査項目·格納値')
    引数 = 構文解析器.parse_args()
    if 引数.fetch:
        データ = 束保管庫(引数.cache, 引数.offline).用意(引数.fetch)
        print('パッケージ 用意 判定完了:', 引数.fetch, len(データ), 'バイト値')
        return
    with 束中継(引数.port, 引数.cache, 引数.offline) as 値中継:
        print('パッケージ 値中継: 127.0.0.1:' + str(値中継.ポート番号), flush=True)
        try:
            値中継.スレッド値.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    起動処理()
