"""eigin 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 hýsa 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as stýrikerfi

Listi_slóð = "/lib/.pip.json"


def 지문(gögn):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(gögn).digest())


def 목록읽기():
    if stýrikerfi.path_kind(Listi_slóð) == 0:
        return {}
    return json.loads(stýrikerfi.read(Listi_slóð).decode("utf-8"))


def skrifa_LOG(SLÓÐ, gögn):
    if stýrikerfi.write(SLÓÐ, gögn) != len(gögn):
        raise OSError(28)


def athuga_slóð(SLÓÐ):
    if not isinstance(SLÓÐ, str) or not SLÓÐ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 númer 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in SLÓÐ.split("/")):
        raise ValueError("허용하지 않는 búnt SLÓÐ")
    if "\\" in SLÓÐ or any(ord(stafur_VALUE) < 32 or ord(stafur_VALUE) == 127 for stafur_VALUE in SLÓÐ):
        raise ValueError("잘못된 SLÓÐ 문자")
    NIÐURSTAÐA = "/lib/" + SLÓÐ
    if len(NIÐURSTAÐA.encode("utf-8")) > 63 or SLÓÐ in ("Íslenska.py", "búnt.py"):
        raise ValueError("búnt 경로가 너무 길거나 sjálfgildi 라이브러리와 겹칩니다.")
    return NIÐURSTAÐA


class 수신흐름:
    def __init__(자신, endastöð):
        자신.endastöð = endastöð
        자신.남은자료 = b""
        자신.Keyra_2 = stýrikerfi.ticks_ms()

    def 정확히읽기(자신, lengd_VALUE):
        gögn = bytearray()
        while len(gögn) < lengd_VALUE:
            if stýrikerfi.ticks_ms() - 자신.Keyra_2 > 90000:
                raise ValueError("búnt 중계 svara TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = stýrikerfi.tcp_read(자신.endastöð, 512)
                except OSError as Villa:
                    if Villa.args[0] != 11:
                        raise
                    stýrikerfi.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("búnt 전송이 중간에 끝났습니다.")
            vara_COUNT = min(lengd_VALUE - len(gögn), len(자신.남은자료))
            gögn.extend(자신.남은자료[:vara_COUNT])
            자신.남은자료 = 자신.남은자료[vara_COUNT:]
            stýrikerfi.sleep_ms(0)
        return bytes(gögn)


def sækja(요청, tengisnúmer):
    if len(요청) > 96 or any(stafur_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for stafur_VALUE in 요청):
        raise ValueError("사용법: pip install Heiti 또는 Heiti==버전")
    endastöð = stýrikerfi.tcp_open()
    try:
        Keyra_2 = stýrikerfi.ticks_ms()
        while True:
            try:
                stýrikerfi.tcp_connect(endastöð, "10.0.2.2", tengisnúmer)
                break
            except OSError as Villa:
                if Villa.args[0] not in (11, 115) or stýrikerfi.ticks_ms() - Keyra_2 > 5000:
                    raise ValueError("búnt 중계 Tengjast bilun_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                stýrikerfi.sleep_ms(10)
        gögn = (요청 + "\n").encode()
        while gögn:
            try:
                vara_COUNT = stýrikerfi.tcp_write(endastöð, gögn)
                if not vara_COUNT:
                    raise ValueError("búnt 요청 flytja_VALUE bilun_VALUE")
                gögn = gögn[vara_COUNT:]
            except OSError as Villa:
                if Villa.args[0] != 11:
                    raise
                stýrikerfi.sleep_ms(10)
                if stýrikerfi.ticks_ms() - Keyra_2 > 10000:
                    raise ValueError("búnt 요청 flytja_VALUE TIME_VALUE 초과")
        Stream_VALUE = 수신흐름(endastöð)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("búnt flytja_VALUE samningsvirði 불일치")
        lengd_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if lengd_VALUE > 8192:
            raise ValueError("búnt 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(lengd_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 uppruni_tré 파일은 1~16개여야 합니다.")
        if sum(færsla_VALUE["size"] for færsla_VALUE in 명세["files"]) > 65536:
            raise ValueError("búnt uppruni_tré 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for færsla_VALUE in 명세["files"]:
            SLÓÐ = athuga_slóð(færsla_VALUE["path"])
            if SLÓÐ in 파일들 or not 0 <= færsla_VALUE["size"] <= 16384:
                raise ValueError("중복 SLÓÐ 또는 Skrá Stærð 초과")
            gögn = Stream_VALUE.정확히읽기(færsla_VALUE["size"])
            if 지문(gögn) != færsla_VALUE["sha256"]:
                raise ValueError("búnt Skrá SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(gögn.decode("utf-8"), SLÓÐ, "exec")
            파일들[SLÓÐ] = gögn
            gc.collect()
        return 명세, 파일들
    finally:
        stýrikerfi.udp_close(endastöð)


def setja_upp_VALUE(요청, tengisnúmer):
    print("búnt sækja:", 요청)
    명세, 파일들 = sækja(요청, tengisnúmer)
    færsla_Listi = 목록읽기()
    Heiti = 명세["name"]
    if Heiti in færsla_Listi:
        if færsla_Listi[Heiti]["version"] == 명세["version"]:
            for SLÓÐ, 지문값 in færsla_Listi[Heiti]["files"].items():
                if stýrikerfi.path_kind(SLÓÐ) != 1 or 지문(stýrikerfi.read(SLÓÐ)) != 지문값:
                    raise ValueError("설치된 búnt 파일이 달라졌습니다: " + SLÓÐ)
            print("이미 설치됨:", Heiti, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 TIL_BAKA_VALUE 설치하십시오.")
    for SLÓÐ in 파일들:
        if stýrikerfi.path_kind(SLÓÐ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + SLÓÐ)
    færsla_Listi[Heiti] = {"version": 명세["version"], "files": {SLÓÐ: 지문(gögn) for SLÓÐ, gögn in 파일들.items()}}
    새목록 = json.dumps(færsla_Listi).encode()
    if len(새목록) > 16384:
        raise ValueError("búnt færsla_Listi Stærð 초과")
    이전목록 = stýrikerfi.read(Listi_slóð) if stýrikerfi.path_kind(Listi_slóð) else None
    만든파일 = []
    만든폴더 = []
    try:
        for SLÓÐ, gögn in 파일들.items():
            부분들 = SLÓÐ.split("/")
            for númer in range(2, len(부분들)):
                skráasafn_VALUE = "/".join(부분들[:númer])
                종류 = stýrikerfi.path_kind(skráasafn_VALUE)
                if 종류 == 0:
                    stýrikerfi.mkdir(skráasafn_VALUE)
                    만든폴더.append(skráasafn_VALUE)
                elif 종류 != 2:
                    raise ValueError("skráasafn_VALUE 경로에 파일이 있습니다: " + skráasafn_VALUE)
            만든파일.append(SLÓÐ)
            skrifa_LOG(SLÓÐ, gögn)
        skrifa_LOG(Listi_slóð, 새목록)
    except Exception:
        for SLÓÐ in 만든파일:
            if stýrikerfi.path_kind(SLÓÐ):
                stýrikerfi.remove(SLÓÐ)
        for skráasafn_VALUE in reversed(만든폴더):
            stýrikerfi.rmdir(skráasafn_VALUE)
        if 이전목록 is not None:
            skrifa_LOG(Listi_slóð, 이전목록)
        elif stýrikerfi.path_kind(Listi_slóð):
            stýrikerfi.remove(Listi_slóð)
        raise
    print("setja_upp_VALUE 완료:", Heiti, 명세["version"], "→ /lib (RAM)")


def fjarlægja_færsla(Heiti):
    færsla_Listi = 목록읽기()
    if Heiti not in færsla_Listi:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Heiti)
    for SLÓÐ, 지문값 in færsla_Listi[Heiti]["files"].items():
        if stýrikerfi.path_kind(SLÓÐ) != 1 or 지문(stýrikerfi.read(SLÓÐ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + SLÓÐ)
    for SLÓÐ in færsla_Listi[Heiti]["files"]:
        stýrikerfi.remove(SLÓÐ)
    del færsla_Listi[Heiti]
    skrifa_LOG(Listi_slóð, json.dumps(færsla_Listi).encode())
    print("fjarlægja_færsla 완료:", Heiti)


def Keyra_2(Viðföng):
    tengisnúmer = 8027
    if len(Viðföng) >= 2 and Viðföng[-2] == "--port":
        tengisnúmer = int(Viðföng[-1])
        Viðföng = Viðföng[:-2]
    if Viðföng == ["list"]:
        for Heiti, msinfo32_exe in 목록읽기().items():
            print(Heiti, msinfo32_exe["version"])
    elif len(Viðföng) == 2 and Viðföng[0] == "install":
        setja_upp_VALUE(Viðföng[1], tengisnúmer)
    elif len(Viðföng) == 2 and Viðföng[0] == "uninstall":
        fjarlægja_færsla(Viðföng[1])
    elif not Viðföng or Viðföng in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython uppruni_tré 설치기 (PyPA pip 전체가 아님)")
        print("pip install Heiti[==버전] [--port 8027] | pip list | pip uninstall Heiti")
        print("hýsa: Verkfæri/keyra_skipun.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Keyra_2(sys.argv[1:])
    except Exception as Villa:
        print("búnt Villa:", Villa)
        sys.exit(1)
