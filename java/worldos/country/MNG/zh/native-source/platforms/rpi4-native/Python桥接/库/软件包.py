"""内置 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 宿主 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as 操作系统

列表路径 = "/lib/.pip.json"


def 指纹值(数据):
    return "".join("%02x" % 值 for 值 in hashlib.sha256(数据).digest())


def 读取列表():
    if 操作系统.path_kind(列表路径) == 0:
        return {}
    return json.loads(操作系统.read(列表路径).decode("utf-8"))


def 写入日志(路径, 数据):
    if 操作系统.write(路径, 数据) != len(数据):
        raise OSError(28)


def 检查路径(路径):
    if not isinstance(路径, str) or not 路径.endswith(".py"):
        raise ValueError("Python 소스만 설치할 数 있습니다.")
    if any(子部分值 in ("", ".", "..") or 子部分值.startswith(".") for 子部分值 in 路径.split("/")):
        raise ValueError("허용하지 않는 软件包 路径")
    if "\\" in 路径 or any(ord(字符值) < 32 or ord(字符值) == 127 for 字符值 in 路径):
        raise ValueError("잘못된 路径 字符")
    结果 = "/lib/" + 路径
    if len(结果.encode("utf-8")) > 63 or 路径 in ("中文.py", "软件包.py"):
        raise ValueError("软件包 경로가 너무 길거나 默认值 라이브러리와 겹칩니다.")
    return 结果


class 接收流:
    def __init__(自身值, 端点):
        自身值.端点 = 端点
        自身值.剩余数据 = b""
        自身值.运行 = 操作系统.ticks_ms()

    def 读取精确地(自身值, 长度):
        数据 = bytearray()
        while len(数据) < 长度:
            if 操作系统.ticks_ms() - 自身值.运行 > 90000:
                raise ValueError("软件包 中继值 回复 时间值 초과")
            if not 自身值.剩余数据:
                try:
                    自身值.剩余数据 = 操作系统.tcp_read(自身值.端点, 512)
                except OSError as 错误:
                    if 错误.args[0] != 11:
                        raise
                    操作系统.sleep_ms(10)
                    continue
                if not 自身值.剩余数据:
                    raise ValueError("软件包 전송이 중간에 끝났습니다.")
            项目个数 = min(长度 - len(数据), len(自身值.剩余数据))
            数据.extend(自身值.剩余数据[:项目个数])
            自身值.剩余数据 = 自身值.剩余数据[项目个数:]
            操作系统.sleep_ms(0)
        return bytes(数据)


def 下载(申请, 端口编号):
    if len(申请) > 96 or any(字符值 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for 字符值 in 申请):
        raise ValueError("사용법: pip install 名称 또는 名称==버전")
    端点 = 操作系统.tcp_open()
    try:
        运行 = 操作系统.ticks_ms()
        while True:
            try:
                操作系统.tcp_connect(端点, "10.0.2.2", 端口编号)
                break
            except OSError as 错误:
                if 错误.args[0] not in (11, 115) or 操作系统.ticks_ms() - 运行 > 5000:
                    raise ValueError("软件包 中继值 连接 失败值: 호스트에서 --network --pip로 실행하십시오.")
                操作系统.sleep_ms(10)
        数据 = (申请 + "\n").encode()
        while 数据:
            try:
                项目个数 = 操作系统.tcp_write(端点, 数据)
                if not 项目个数:
                    raise ValueError("软件包 申请 传送值 失败值")
                数据 = 数据[项目个数:]
            except OSError as 错误:
                if 错误.args[0] != 11:
                    raise
                操作系统.sleep_ms(10)
                if 操作系统.ticks_ms() - 运行 > 10000:
                    raise ValueError("软件包 申请 传送值 时间值 초과")
        流值 = 接收流(端点)
        头值 = 流值.读取精确地(8)
        if 头值[:4] != b"JKP1":
            raise ValueError("软件包 传送值 契约值 불일치")
        长度 = (头值[4] << 24) | (头值[5] << 16) | (头值[6] << 8) | 头值[7]
        if 长度 > 8192:
            raise ValueError("软件包 명세가 너무 큽니다.")
        规格 = json.loads(流值.读取精确地(长度).decode())
        if "error" in 规格:
            raise ValueError(规格["error"])
        if not 1 <= len(规格["files"]) <= 16:
            raise ValueError("꾸러미당 源代码树 파일은 1~16개여야 합니다.")
        if sum(条目值["size"] for 条目值 in 规格["files"]) > 65536:
            raise ValueError("软件包 源代码树 합계는 64 KiB 이하여야 합니다.")
        文件条目列 = {}
        for 条目值 in 规格["files"]:
            路径 = 检查路径(条目值["path"])
            if 路径 in 文件条目列 or not 0 <= 条目值["size"] <= 16384:
                raise ValueError("중복 路径 또는 文件 大小 초과")
            数据 = 流值.读取精确地(条目值["size"])
            if 指纹值(数据) != 条目值["sha256"]:
                raise ValueError("软件包 文件 SHA-256 불일치")
            # 실행하지 않고 当前项目 MicroPython의 문법으로 먼저 검사한다.
            compile(数据.decode("utf-8"), 路径, "exec")
            文件条目列[路径] = 数据
            gc.collect()
        return 规格, 文件条目列
    finally:
        操作系统.udp_close(端点)


def 安装值(申请, 端口编号):
    print("软件包 下载:", 申请)
    规格, 文件条目列 = 下载(申请, 端口编号)
    条目列表 = 读取列表()
    名称 = 规格["name"]
    if 名称 in 条目列表:
        if 条目列表[名称]["version"] == 规格["version"]:
            for 路径, 指纹数据 in 条目列表[名称]["files"].items():
                if 操作系统.path_kind(路径) != 1 or 指纹值(操作系统.read(路径)) != 指纹数据:
                    raise ValueError("설치된 软件包 파일이 달라졌습니다: " + 路径)
            print("이미 설치됨:", 名称, 规格["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 后端值 설치하십시오.")
    for 路径 in 文件条目列:
        if 操作系统.path_kind(路径):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + 路径)
    条目列表[名称] = {"version": 规格["version"], "files": {路径: 指纹值(数据) for 路径, 数据 in 文件条目列.items()}}
    新建列表 = json.dumps(条目列表).encode()
    if len(新建列表) > 16384:
        raise ValueError("软件包 条目列表 大小 초과")
    上一个列表 = 操作系统.read(列表路径) if 操作系统.path_kind(列表路径) else None
    已创建文件 = []
    已创建目录 = []
    try:
        for 路径, 数据 in 文件条目列.items():
            部件列 = 路径.split("/")
            for 数 in range(2, len(部件列)):
                目录值 = "/".join(部件列[:数])
                种类值 = 操作系统.path_kind(目录值)
                if 种类值 == 0:
                    操作系统.mkdir(目录值)
                    已创建目录.append(目录值)
                elif 种类值 != 2:
                    raise ValueError("目录值 경로에 파일이 있습니다: " + 目录值)
            已创建文件.append(路径)
            写入日志(路径, 数据)
        写入日志(列表路径, 新建列表)
    except Exception:
        for 路径 in 已创建文件:
            if 操作系统.path_kind(路径):
                操作系统.remove(路径)
        for 目录值 in reversed(已创建目录):
            操作系统.rmdir(目录值)
        if 上一个列表 is not None:
            写入日志(列表路径, 上一个列表)
        elif 操作系统.path_kind(列表路径):
            操作系统.remove(列表路径)
        raise
    print("安装值 是否完成:", 名称, 规格["version"], "→ /lib (RAM)")


def 移除条目(名称):
    条目列表 = 读取列表()
    if 名称 not in 条目列表:
        raise ValueError("설치되지 않은 꾸러미입니다: " + 名称)
    for 路径, 指纹数据 in 条目列表[名称]["files"].items():
        if 操作系统.path_kind(路径) != 1 or 指纹值(操作系统.read(路径)) != 指纹数据:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + 路径)
    for 路径 in 条目列表[名称]["files"]:
        操作系统.remove(路径)
    del 条目列表[名称]
    写入日志(列表路径, json.dumps(条目列表).encode())
    print("移除条目 是否完成:", 名称)


def 运行(实参):
    端口编号 = 8027
    if len(实参) >= 2 and 实参[-2] == "--port":
        端口编号 = int(实参[-1])
        实参 = 实参[:-2]
    if 实参 == ["list"]:
        for 名称, 系统信息 in 读取列表().items():
            print(名称, 系统信息["version"])
    elif len(实参) == 2 and 实参[0] == "install":
        安装值(实参[1], 端口编号)
    elif len(实参) == 2 and 实参[0] == "uninstall":
        移除条目(实参[1])
    elif not 实参 or 实参 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython 源代码树 설치기 (PyPA pip 전체가 아님)")
        print("pip install 名称[==버전] [--port 8027] | pip list | pip uninstall 名称")
        print("宿主: 工具集/执行命令.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        运行(sys.argv[1:])
    except Exception as 错误:
        print("软件包 错误:", 错误)
        sys.exit(1)
