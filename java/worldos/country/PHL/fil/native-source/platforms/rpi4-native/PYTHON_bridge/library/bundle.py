"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operating_system

list_path = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if operating_system.path_kind(list_path) == 0:
        return {}
    return json.loads(operating_system.read(list_path).decode("utf-8"))


def sumulat_LOG(path, data):
    if operating_system.write(path, data) != len(data):
        raise OSError(28)


def tseke_path(path):
    if not isinstance(path, str) or not path.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in path.split("/")):
        raise ValueError("허용하지 않는 bundle path")
    if "\\" in path or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in path):
        raise ValueError("잘못된 path 문자")
    sukat = "/lib/" + path
    if len(sukat.encode("utf-8")) > 63 or path in ("한국어.py", "bundle.py"):
        raise ValueError("bundle 경로가 너무 길거나 value_ng_default 라이브러리와 겹칩니다.")
    return sukat


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.run = operating_system.ticks_ms()

    def 정확히읽기(자신, haba_VALUE):
        data = bytearray()
        while len(data) < haba_VALUE:
            if operating_system.ticks_ms() - 자신.run > 90000:
                raise ValueError("bundle 중계 tumugon TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operating_system.tcp_read(자신.종단, 512)
                except OSError as error:
                    if error.args[0] != 11:
                        raise
                    operating_system.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bundle 전송이 중간에 끝났습니다.")
            item_COUNT = min(haba_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:item_COUNT])
            자신.남은자료 = 자신.남은자료[item_COUNT:]
            operating_system.sleep_ms(0)
        return bytes(data)


def download(요청, numero_ng_port):
    if len(요청) > 96 or any(karakter_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karakter_VALUE in 요청):
        raise ValueError("사용법: pip install pangalan 또는 pangalan==버전")
    종단 = operating_system.tcp_open()
    try:
        run = operating_system.ticks_ms()
        while True:
            try:
                operating_system.tcp_connect(종단, "10.0.2.2", numero_ng_port)
                break
            except OSError as error:
                if error.args[0] not in (11, 115) or operating_system.ticks_ms() - run > 5000:
                    raise ValueError("bundle 중계 CONNECT pagpalya_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operating_system.sleep_ms(10)
        data = (요청 + "\n").encode()
        while data:
            try:
                item_COUNT = operating_system.tcp_write(종단, data)
                if not item_COUNT:
                    raise ValueError("bundle 요청 lipat_VALUE pagpalya_VALUE")
                data = data[item_COUNT:]
            except OSError as error:
                if error.args[0] != 11:
                    raise
                operating_system.sleep_ms(10)
                if operating_system.ticks_ms() - run > 10000:
                    raise ValueError("bundle 요청 lipat_VALUE TIME_VALUE 초과")
        Stream_VALUE = 수신흐름(종단)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bundle lipat_VALUE kaso_VALUE 불일치")
        haba_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if haba_VALUE > 8192:
            raise ValueError("bundle 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(haba_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 pinagmulan_balangkas 파일은 1~16개여야 합니다.")
        if sum(pagpasok_VALUE["size"] for pagpasok_VALUE in 명세["files"]) > 65536:
            raise ValueError("bundle pinagmulan_balangkas 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for pagpasok_VALUE in 명세["files"]:
            path = tseke_path(pagpasok_VALUE["path"])
            if path in 파일들 or not 0 <= pagpasok_VALUE["size"] <= 16384:
                raise ValueError("중복 path 또는 file sukat_82232621 초과")
            data = Stream_VALUE.정확히읽기(pagpasok_VALUE["size"])
            if 지문(data) != pagpasok_VALUE["sha256"]:
                raise ValueError("bundle file SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), path, "exec")
            파일들[path] = data
            gc.collect()
        return 명세, 파일들
    finally:
        operating_system.udp_close(종단)


def i_install_VALUE(요청, numero_ng_port):
    print("bundle download:", 요청)
    명세, 파일들 = download(요청, numero_ng_port)
    pagpasok_list = 목록읽기()
    pangalan = 명세["name"]
    if pangalan in pagpasok_list:
        if pagpasok_list[pangalan]["version"] == 명세["version"]:
            for path, 지문값 in pagpasok_list[pangalan]["files"].items():
                if operating_system.path_kind(path) != 1 or 지문(operating_system.read(path)) != 지문값:
                    raise ValueError("설치된 bundle 파일이 달라졌습니다: " + path)
            print("이미 설치됨:", pangalan, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Bumalik_VALUE 설치하십시오.")
    for path in 파일들:
        if operating_system.path_kind(path):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + path)
    pagpasok_list[pangalan] = {"version": 명세["version"], "files": {path: 지문(data) for path, data in 파일들.items()}}
    새목록 = json.dumps(pagpasok_list).encode()
    if len(새목록) > 16384:
        raise ValueError("bundle pagpasok_list sukat_82232621 초과")
    이전목록 = operating_system.read(list_path) if operating_system.path_kind(list_path) else None
    만든파일 = []
    만든폴더 = []
    try:
        for path, data in 파일들.items():
            부분들 = path.split("/")
            for 수 in range(2, len(부분들)):
                Directory_VALUE = "/".join(부분들[:수])
                종류 = operating_system.path_kind(Directory_VALUE)
                if 종류 == 0:
                    operating_system.mkdir(Directory_VALUE)
                    만든폴더.append(Directory_VALUE)
                elif 종류 != 2:
                    raise ValueError("Directory_VALUE 경로에 파일이 있습니다: " + Directory_VALUE)
            만든파일.append(path)
            sumulat_LOG(path, data)
        sumulat_LOG(list_path, 새목록)
    except Exception:
        for path in 만든파일:
            if operating_system.path_kind(path):
                operating_system.remove(path)
        for Directory_VALUE in reversed(만든폴더):
            operating_system.rmdir(Directory_VALUE)
        if 이전목록 is not None:
            sumulat_LOG(list_path, 이전목록)
        elif operating_system.path_kind(list_path):
            operating_system.remove(list_path)
        raise
    print("i_install_VALUE 완료:", pangalan, 명세["version"], "→ /lib (RAM)")


def tanggalin_pagpasok(pangalan):
    pagpasok_list = 목록읽기()
    if pangalan not in pagpasok_list:
        raise ValueError("설치되지 않은 꾸러미입니다: " + pangalan)
    for path, 지문값 in pagpasok_list[pangalan]["files"].items():
        if operating_system.path_kind(path) != 1 or 지문(operating_system.read(path)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + path)
    for path in pagpasok_list[pangalan]["files"]:
        operating_system.remove(path)
    del pagpasok_list[pangalan]
    sumulat_LOG(list_path, json.dumps(pagpasok_list).encode())
    print("tanggalin_pagpasok 완료:", pangalan)


def run(인수):
    numero_ng_port = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        numero_ng_port = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for pangalan, msinfo32_exe in 목록읽기().items():
            print(pangalan, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        i_install_VALUE(인수[1], numero_ng_port)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        tanggalin_pagpasok(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython pinagmulan_balangkas 설치기 (PyPA pip 전체가 아님)")
        print("pip install pangalan[==버전] [--port 8027] | pip list | pip uninstall pangalan")
        print("host: Mga_Tool/Mag_execute_utos.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        run(sys.argv[1:])
    except Exception as error:
        print("bundle error:", error)
        sys.exit(1)
