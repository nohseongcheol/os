"""內建 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 宿主 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as 操作系統

列表路徑 = "/lib/.pip.json"


def 指紋值(資料):
    return "".join("%02x" % 值 for 值 in hashlib.sha256(資料).digest())


def 讀取列表():
    if 操作系統.path_kind(列表路徑) == 0:
        return {}
    return json.loads(操作系統.read(列表路徑).decode("utf-8"))


def 寫入日誌(路徑, 資料):
    if 操作系統.write(路徑, 資料) != len(資料):
        raise OSError(28)


def 檢查路徑(路徑):
    if not isinstance(路徑, str) or not 路徑.endswith(".py"):
        raise ValueError("Python 소스만 설치할 數 있습니다.")
    if any(子部分值 in ("", ".", "..") or 子部分值.startswith(".") for 子部分值 in 路徑.split("/")):
        raise ValueError("허용하지 않는 軟件包 路徑")
    if "\\" in 路徑 or any(ord(字元值) < 32 or ord(字元值) == 127 for 字元值 in 路徑):
        raise ValueError("잘못된 路徑 字元")
    結果 = "/lib/" + 路徑
    if len(結果.encode("utf-8")) > 63 or 路徑 in ("中文.py", "軟件包.py"):
        raise ValueError("軟件包 경로가 너무 길거나 默認值 라이브러리와 겹칩니다.")
    return 結果


class 接收流:
    def __init__(自身值, 端點):
        自身值.端點 = 端點
        自身值.剩餘資料 = b""
        自身值.運行 = 操作系統.ticks_ms()

    def 讀取精確地(自身值, 長度):
        資料 = bytearray()
        while len(資料) < 長度:
            if 操作系統.ticks_ms() - 自身值.運行 > 90000:
                raise ValueError("軟件包 中繼值 回覆 時間值 초과")
            if not 自身值.剩餘資料:
                try:
                    自身值.剩餘資料 = 操作系統.tcp_read(自身值.端點, 512)
                except OSError as 錯誤:
                    if 錯誤.args[0] != 11:
                        raise
                    操作系統.sleep_ms(10)
                    continue
                if not 自身值.剩餘資料:
                    raise ValueError("軟件包 전송이 중간에 끝났습니다.")
            項目個數 = min(長度 - len(資料), len(自身值.剩餘資料))
            資料.extend(自身值.剩餘資料[:項目個數])
            自身值.剩餘資料 = 自身值.剩餘資料[項目個數:]
            操作系統.sleep_ms(0)
        return bytes(資料)


def 下載(申請, 埠編號):
    if len(申請) > 96 or any(字元值 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for 字元值 in 申請):
        raise ValueError("사용법: pip install 名稱 또는 名稱==버전")
    端點 = 操作系統.tcp_open()
    try:
        運行 = 操作系統.ticks_ms()
        while True:
            try:
                操作系統.tcp_connect(端點, "10.0.2.2", 埠編號)
                break
            except OSError as 錯誤:
                if 錯誤.args[0] not in (11, 115) or 操作系統.ticks_ms() - 運行 > 5000:
                    raise ValueError("軟件包 中繼值 連接 失敗值: 호스트에서 --network --pip로 실행하십시오.")
                操作系統.sleep_ms(10)
        資料 = (申請 + "\n").encode()
        while 資料:
            try:
                項目個數 = 操作系統.tcp_write(端點, 資料)
                if not 項目個數:
                    raise ValueError("軟件包 申請 傳送值 失敗值")
                資料 = 資料[項目個數:]
            except OSError as 錯誤:
                if 錯誤.args[0] != 11:
                    raise
                操作系統.sleep_ms(10)
                if 操作系統.ticks_ms() - 運行 > 10000:
                    raise ValueError("軟件包 申請 傳送值 時間值 초과")
        流值 = 接收流(端點)
        頭值 = 流值.讀取精確地(8)
        if 頭值[:4] != b"JKP1":
            raise ValueError("軟件包 傳送值 契約值 불일치")
        長度 = (頭值[4] << 24) | (頭值[5] << 16) | (頭值[6] << 8) | 頭值[7]
        if 長度 > 8192:
            raise ValueError("軟件包 명세가 너무 큽니다.")
        規格 = json.loads(流值.讀取精確地(長度).decode())
        if "error" in 規格:
            raise ValueError(規格["error"])
        if not 1 <= len(規格["files"]) <= 16:
            raise ValueError("꾸러미당 原始碼樹 파일은 1~16개여야 합니다.")
        if sum(條目值["size"] for 條目值 in 規格["files"]) > 65536:
            raise ValueError("軟件包 原始碼樹 합계는 64 KiB 이하여야 합니다.")
        檔案條目列 = {}
        for 條目值 in 規格["files"]:
            路徑 = 檢查路徑(條目值["path"])
            if 路徑 in 檔案條目列 or not 0 <= 條目值["size"] <= 16384:
                raise ValueError("중복 路徑 또는 檔案 大小 초과")
            資料 = 流值.讀取精確地(條目值["size"])
            if 指紋值(資料) != 條目值["sha256"]:
                raise ValueError("軟件包 檔案 SHA-256 불일치")
            # 실행하지 않고 當前項目 MicroPython의 문법으로 먼저 검사한다.
            compile(資料.decode("utf-8"), 路徑, "exec")
            檔案條目列[路徑] = 資料
            gc.collect()
        return 規格, 檔案條目列
    finally:
        操作系統.udp_close(端點)


def 安裝值(申請, 埠編號):
    print("軟件包 下載:", 申請)
    規格, 檔案條目列 = 下載(申請, 埠編號)
    條目列表 = 讀取列表()
    名稱 = 規格["name"]
    if 名稱 in 條目列表:
        if 條目列表[名稱]["version"] == 規格["version"]:
            for 路徑, 指紋資料 in 條目列表[名稱]["files"].items():
                if 操作系統.path_kind(路徑) != 1 or 指紋值(操作系統.read(路徑)) != 指紋資料:
                    raise ValueError("설치된 軟件包 파일이 달라졌습니다: " + 路徑)
            print("이미 설치됨:", 名稱, 規格["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 後端值 설치하십시오.")
    for 路徑 in 檔案條目列:
        if 操作系統.path_kind(路徑):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + 路徑)
    條目列表[名稱] = {"version": 規格["version"], "files": {路徑: 指紋值(資料) for 路徑, 資料 in 檔案條目列.items()}}
    新建列表 = json.dumps(條目列表).encode()
    if len(新建列表) > 16384:
        raise ValueError("軟件包 條目列表 大小 초과")
    上一個列表 = 操作系統.read(列表路徑) if 操作系統.path_kind(列表路徑) else None
    已創建檔案 = []
    已創建目錄 = []
    try:
        for 路徑, 資料 in 檔案條目列.items():
            部件列 = 路徑.split("/")
            for 數 in range(2, len(部件列)):
                目錄值 = "/".join(部件列[:數])
                種類值 = 操作系統.path_kind(目錄值)
                if 種類值 == 0:
                    操作系統.mkdir(目錄值)
                    已創建目錄.append(目錄值)
                elif 種類值 != 2:
                    raise ValueError("目錄值 경로에 파일이 있습니다: " + 目錄值)
            已創建檔案.append(路徑)
            寫入日誌(路徑, 資料)
        寫入日誌(列表路徑, 新建列表)
    except Exception:
        for 路徑 in 已創建檔案:
            if 操作系統.path_kind(路徑):
                操作系統.remove(路徑)
        for 目錄值 in reversed(已創建目錄):
            操作系統.rmdir(目錄值)
        if 上一個列表 is not None:
            寫入日誌(列表路徑, 上一個列表)
        elif 操作系統.path_kind(列表路徑):
            操作系統.remove(列表路徑)
        raise
    print("安裝值 是否完成:", 名稱, 規格["version"], "→ /lib (RAM)")


def 移除條目(名稱):
    條目列表 = 讀取列表()
    if 名稱 not in 條目列表:
        raise ValueError("설치되지 않은 꾸러미입니다: " + 名稱)
    for 路徑, 指紋資料 in 條目列表[名稱]["files"].items():
        if 操作系統.path_kind(路徑) != 1 or 指紋值(操作系統.read(路徑)) != 指紋資料:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + 路徑)
    for 路徑 in 條目列表[名稱]["files"]:
        操作系統.remove(路徑)
    del 條目列表[名稱]
    寫入日誌(列表路徑, json.dumps(條目列表).encode())
    print("移除條目 是否完成:", 名稱)


def 運行(實參):
    埠編號 = 8027
    if len(實參) >= 2 and 實參[-2] == "--port":
        埠編號 = int(實參[-1])
        實參 = 實參[:-2]
    if 實參 == ["list"]:
        for 名稱, 系統信息 in 讀取列表().items():
            print(名稱, 系統信息["version"])
    elif len(實參) == 2 and 實參[0] == "install":
        安裝值(實參[1], 埠編號)
    elif len(實參) == 2 and 實參[0] == "uninstall":
        移除條目(實參[1])
    elif not 實參 or 實參 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython 原始碼樹 설치기 (PyPA pip 전체가 아님)")
        print("pip install 名稱[==버전] [--port 8027] | pip list | pip uninstall 名稱")
        print("宿主: 工具集/執行命令.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        運行(sys.argv[1:])
    except Exception as 錯誤:
        print("軟件包 錯誤:", 錯誤)
        sys.exit(1)
