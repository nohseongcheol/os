"""内蔵 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ホスト 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as 稼働システム

一覧経路 = "/lib/.pip.json"


def 指紋値(データ):
    return "".join("%02x" % 値 for 値 in hashlib.sha256(データ).digest())


def 一覧読取():
    if 稼働システム.path_kind(一覧経路) == 0:
        return {}
    return json.loads(稼働システム.read(一覧経路).decode("utf-8"))


def 履歴記録書込(経路, データ):
    if 稼働システム.write(経路, データ) != len(データ):
        raise OSError(28)


def 経路検査(経路):
    if not isinstance(経路, str) or not 経路.endswith(".py"):
        raise ValueError("Python 소스만 설치할 数 있습니다.")
    if any(部分要素値 in ("", ".", "..") or 部分要素値.startswith(".") for 部分要素値 in 経路.split("/")):
        raise ValueError("허용하지 않는 パッケージ 経路")
    if "\\" in 経路 or any(ord(文字値) < 32 or ord(文字値) == 127 for 文字値 in 経路):
        raise ValueError("잘못된 経路 文字")
    結果 = "/lib/" + 経路
    if len(結果.encode("utf-8")) > 63 or 経路 in ("日本語.py", "パッケージ.py"):
        raise ValueError("パッケージ 경로가 너무 길거나 既定値 라이브러리와 겹칩니다.")
    return 結果


class ストリーム受取:
    def __init__(自身値, 通信端点):
        自身値.通信端点 = 通信端点
        自身値.残りデータ = b""
        自身値.起動処理 = 稼働システム.ticks_ms()

    def 厳密に読取(自身値, 長さ):
        データ = bytearray()
        while len(データ) < 長さ:
            if 稼働システム.ticks_ms() - 自身値.起動処理 > 90000:
                raise ValueError("パッケージ 値中継 返答 時間値 초과")
            if not 自身値.残りデータ:
                try:
                    自身値.残りデータ = 稼働システム.tcp_read(自身値.通信端点, 512)
                except OSError as エラー:
                    if エラー.args[0] != 11:
                        raise
                    稼働システム.sleep_ms(10)
                    continue
                if not 自身値.残りデータ:
                    raise ValueError("パッケージ 전송이 중간에 끝났습니다.")
            項目個数 = min(長さ - len(データ), len(自身値.残りデータ))
            データ.extend(自身値.残りデータ[:項目個数])
            自身値.残りデータ = 自身値.残りデータ[項目個数:]
            稼働システム.sleep_ms(0)
        return bytes(データ)


def 取得転送(要求, ポート番号):
    if len(要求) > 96 or any(文字値 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for 文字値 in 要求):
        raise ValueError("사용법: pip install 名前 또는 名前==버전")
    通信端点 = 稼働システム.tcp_open()
    try:
        起動処理 = 稼働システム.ticks_ms()
        while True:
            try:
                稼働システム.tcp_connect(通信端点, "10.0.2.2", ポート番号)
                break
            except OSError as エラー:
                if エラー.args[0] not in (11, 115) or 稼働システム.ticks_ms() - 起動処理 > 5000:
                    raise ValueError("パッケージ 値中継 接続 失敗値: 호스트에서 --network --pip로 실행하십시오.")
                稼働システム.sleep_ms(10)
        データ = (要求 + "\n").encode()
        while データ:
            try:
                項目個数 = 稼働システム.tcp_write(通信端点, データ)
                if not 項目個数:
                    raise ValueError("パッケージ 要求 転送値 失敗値")
                データ = データ[項目個数:]
            except OSError as エラー:
                if エラー.args[0] != 11:
                    raise
                稼働システム.sleep_ms(10)
                if 稼働システム.ticks_ms() - 起動処理 > 10000:
                    raise ValueError("パッケージ 要求 転送値 時間値 초과")
        ストリーム値 = ストリーム受取(通信端点)
        先頭部値 = ストリーム値.厳密に読取(8)
        if 先頭部値[:4] != b"JKP1":
            raise ValueError("パッケージ 転送値 契約値 불일치")
        長さ = (先頭部値[4] << 24) | (先頭部値[5] << 16) | (先頭部値[6] << 8) | 先頭部値[7]
        if 長さ > 8192:
            raise ValueError("パッケージ 명세가 너무 큽니다.")
        仕様 = json.loads(ストリーム値.厳密に読取(長さ).decode())
        if "error" in 仕様:
            raise ValueError(仕様["error"])
        if not 1 <= len(仕様["files"]) <= 16:
            raise ValueError("꾸러미당 ソース木 파일은 1~16개여야 합니다.")
        if sum(入口値["size"] for 入口値 in 仕様["files"]) > 65536:
            raise ValueError("パッケージ ソース木 합계는 64 KiB 이하여야 합니다.")
        ファイル登録項目一覧 = {}
        for 入口値 in 仕様["files"]:
            経路 = 経路検査(入口値["path"])
            if 経路 in ファイル登録項目一覧 or not 0 <= 入口値["size"] <= 16384:
                raise ValueError("중복 経路 또는 ファイル 容量 초과")
            データ = ストリーム値.厳密に読取(入口値["size"])
            if 指紋値(データ) != 入口値["sha256"]:
                raise ValueError("パッケージ ファイル SHA-256 불일치")
            # 실행하지 않고 現在項目 MicroPython의 문법으로 먼저 검사한다.
            compile(データ.decode("utf-8"), 経路, "exec")
            ファイル登録項目一覧[経路] = データ
            gc.collect()
        return 仕様, ファイル登録項目一覧
    finally:
        稼働システム.udp_close(通信端点)


def 値導入(要求, ポート番号):
    print("パッケージ 取得転送:", 要求)
    仕様, ファイル登録項目一覧 = 取得転送(要求, ポート番号)
    入口一覧 = 一覧読取()
    名前 = 仕様["name"]
    if 名前 in 入口一覧:
        if 入口一覧[名前]["version"] == 仕様["version"]:
            for 経路, 指紋データ in 入口一覧[名前]["files"].items():
                if 稼働システム.path_kind(経路) != 1 or 指紋値(稼働システム.read(経路)) != 指紋データ:
                    raise ValueError("설치된 パッケージ 파일이 달라졌습니다: " + 経路)
            print("이미 설치됨:", 名前, 仕様["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 後端値 설치하십시오.")
    for 経路 in ファイル登録項目一覧:
        if 稼働システム.path_kind(経路):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + 経路)
    入口一覧[名前] = {"version": 仕様["version"], "files": {経路: 指紋値(データ) for 経路, データ in ファイル登録項目一覧.items()}}
    新規一覧 = json.dumps(入口一覧).encode()
    if len(新規一覧) > 16384:
        raise ValueError("パッケージ 入口一覧 容量 초과")
    前回一覧 = 稼働システム.read(一覧経路) if 稼働システム.path_kind(一覧経路) else None
    作成済みファイル = []
    作成済みディレクトリ = []
    try:
        for 経路, データ in ファイル登録項目一覧.items():
            構成要素一覧 = 経路.split("/")
            for 数 in range(2, len(構成要素一覧)):
                ディレクトリ値 = "/".join(構成要素一覧[:数])
                種別値 = 稼働システム.path_kind(ディレクトリ値)
                if 種別値 == 0:
                    稼働システム.mkdir(ディレクトリ値)
                    作成済みディレクトリ.append(ディレクトリ値)
                elif 種別値 != 2:
                    raise ValueError("ディレクトリ値 경로에 파일이 있습니다: " + ディレクトリ値)
            作成済みファイル.append(経路)
            履歴記録書込(経路, データ)
        履歴記録書込(一覧経路, 新規一覧)
    except Exception:
        for 経路 in 作成済みファイル:
            if 稼働システム.path_kind(経路):
                稼働システム.remove(経路)
        for ディレクトリ値 in reversed(作成済みディレクトリ):
            稼働システム.rmdir(ディレクトリ値)
        if 前回一覧 is not None:
            履歴記録書込(一覧経路, 前回一覧)
        elif 稼働システム.path_kind(一覧経路):
            稼働システム.remove(一覧経路)
        raise
    print("値導入 判定完了:", 名前, 仕様["version"], "→ /lib (RAM)")


def 入口除去(名前):
    入口一覧 = 一覧読取()
    if 名前 not in 入口一覧:
        raise ValueError("설치되지 않은 꾸러미입니다: " + 名前)
    for 経路, 指紋データ in 入口一覧[名前]["files"].items():
        if 稼働システム.path_kind(経路) != 1 or 指紋値(稼働システム.read(経路)) != 指紋データ:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + 経路)
    for 経路 in 入口一覧[名前]["files"]:
        稼働システム.remove(経路)
    del 入口一覧[名前]
    履歴記録書込(一覧経路, json.dumps(入口一覧).encode())
    print("入口除去 判定完了:", 名前)


def 起動処理(引数):
    ポート番号 = 8027
    if len(引数) >= 2 and 引数[-2] == "--port":
        ポート番号 = int(引数[-1])
        引数 = 引数[:-2]
    if 引数 == ["list"]:
        for 名前, システム情報 in 一覧読取().items():
            print(名前, システム情報["version"])
    elif len(引数) == 2 and 引数[0] == "install":
        値導入(引数[1], ポート番号)
    elif len(引数) == 2 and 引数[0] == "uninstall":
        入口除去(引数[1])
    elif not 引数 or 引数 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ソース木 설치기 (PyPA pip 전체가 아님)")
        print("pip install 名前[==버전] [--port 8027] | pip list | pip uninstall 名前")
        print("ホスト: 道具/命令実行.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        起動処理(sys.argv[1:])
    except Exception as エラー:
        print("パッケージ エラー:", エラー)
        sys.exit(1)
