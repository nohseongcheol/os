"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 lletya 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as system_weithredu

Rhestr_llwybr = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if system_weithredu.path_kind(Rhestr_llwybr) == 0:
        return {}
    return json.loads(system_weithredu.read(Rhestr_llwybr).decode("utf-8"))


def ysgrifennu_LOG(LLWYBR, data):
    if system_weithredu.write(LLWYBR, data) != len(data):
        raise OSError(28)


def gwirio_llwybr(LLWYBR):
    if not isinstance(LLWYBR, str) or not LLWYBR.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in LLWYBR.split("/")):
        raise ValueError("허용하지 않는 bwndel LLWYBR")
    if "\\" in LLWYBR or any(ord(nod_VALUE) < 32 or ord(nod_VALUE) == 127 for nod_VALUE in LLWYBR):
        raise ValueError("잘못된 LLWYBR 문자")
    mesur = "/lib/" + LLWYBR
    if len(mesur.encode("utf-8")) > 63 or LLWYBR in ("Cymraeg.py", "bwndel.py"):
        raise ValueError("bwndel 경로가 너무 길거나 gwerth_diofyn 라이브러리와 겹칩니다.")
    return mesur


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Gweithredu_2 = system_weithredu.ticks_ms()

    def 정확히읽기(자신, hyd_VALUE):
        data = bytearray()
        while len(data) < hyd_VALUE:
            if system_weithredu.ticks_ms() - 자신.Gweithredu_2 > 90000:
                raise ValueError("bwndel 중계 ateb TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = system_weithredu.tcp_read(자신.종단, 512)
                except OSError as Gwall:
                    if Gwall.args[0] != 11:
                        raise
                    system_weithredu.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bwndel 전송이 중간에 끝났습니다.")
            eitem_COUNT = min(hyd_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:eitem_COUNT])
            자신.남은자료 = 자신.남은자료[eitem_COUNT:]
            system_weithredu.sleep_ms(0)
        return bytes(data)


def lawrlwytho(cais_HTTP, rhif_porth):
    if len(cais_HTTP) > 96 or any(nod_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for nod_VALUE in cais_HTTP):
        raise ValueError("사용법: pip install Enw 또는 Enw==버전")
    종단 = system_weithredu.tcp_open()
    try:
        Gweithredu_2 = system_weithredu.ticks_ms()
        while True:
            try:
                system_weithredu.tcp_connect(종단, "10.0.2.2", rhif_porth)
                break
            except OSError as Gwall:
                if Gwall.args[0] not in (11, 115) or system_weithredu.ticks_ms() - Gweithredu_2 > 5000:
                    raise ValueError("bwndel 중계 Cysylltu methiant_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                system_weithredu.sleep_ms(10)
        data = (cais_HTTP + "\n").encode()
        while data:
            try:
                eitem_COUNT = system_weithredu.tcp_write(종단, data)
                if not eitem_COUNT:
                    raise ValueError("bwndel cais_HTTP trosglwyddo_VALUE methiant_VALUE")
                data = data[eitem_COUNT:]
            except OSError as Gwall:
                if Gwall.args[0] != 11:
                    raise
                system_weithredu.sleep_ms(10)
                if system_weithredu.ticks_ms() - Gweithredu_2 > 10000:
                    raise ValueError("bwndel cais_HTTP trosglwyddo_VALUE TIME_VALUE 초과")
        ffrwd_VALUE = 수신흐름(종단)
        머리 = ffrwd_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bwndel trosglwyddo_VALUE tasg_VALUE 불일치")
        hyd_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if hyd_VALUE > 8192:
            raise ValueError("bwndel 명세가 너무 큽니다.")
        명세 = json.loads(ffrwd_VALUE.정확히읽기(hyd_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ffynhonnell_coeden 파일은 1~16개여야 합니다.")
        if sum(cofnod_VALUE["size"] for cofnod_VALUE in 명세["files"]) > 65536:
            raise ValueError("bwndel ffynhonnell_coeden 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for cofnod_VALUE in 명세["files"]:
            LLWYBR = gwirio_llwybr(cofnod_VALUE["path"])
            if LLWYBR in 파일들 or not 0 <= cofnod_VALUE["size"] <= 16384:
                raise ValueError("중복 LLWYBR 또는 Ffeil Maint 초과")
            data = ffrwd_VALUE.정확히읽기(cofnod_VALUE["size"])
            if 지문(data) != cofnod_VALUE["sha256"]:
                raise ValueError("bwndel Ffeil SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), LLWYBR, "exec")
            파일들[LLWYBR] = data
            gc.collect()
        return 명세, 파일들
    finally:
        system_weithredu.udp_close(종단)


def gosod_VALUE(cais_HTTP, rhif_porth):
    print("bwndel lawrlwytho:", cais_HTTP)
    명세, 파일들 = lawrlwytho(cais_HTTP, rhif_porth)
    cofnod_Rhestr = 목록읽기()
    Enw = 명세["name"]
    if Enw in cofnod_Rhestr:
        if cofnod_Rhestr[Enw]["version"] == 명세["version"]:
            for LLWYBR, 지문값 in cofnod_Rhestr[Enw]["files"].items():
                if system_weithredu.path_kind(LLWYBR) != 1 or 지문(system_weithredu.read(LLWYBR)) != 지문값:
                    raise ValueError("설치된 bwndel 파일이 달라졌습니다: " + LLWYBR)
            print("이미 설치됨:", Enw, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VALUE 설치하십시오.")
    for LLWYBR in 파일들:
        if system_weithredu.path_kind(LLWYBR):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + LLWYBR)
    cofnod_Rhestr[Enw] = {"version": 명세["version"], "files": {LLWYBR: 지문(data) for LLWYBR, data in 파일들.items()}}
    새목록 = json.dumps(cofnod_Rhestr).encode()
    if len(새목록) > 16384:
        raise ValueError("bwndel cofnod_Rhestr Maint 초과")
    이전목록 = system_weithredu.read(Rhestr_llwybr) if system_weithredu.path_kind(Rhestr_llwybr) else None
    만든파일 = []
    만든폴더 = []
    try:
        for LLWYBR, data in 파일들.items():
            부분들 = LLWYBR.split("/")
            for 수 in range(2, len(부분들)):
                cyfeiriadur_VALUE = "/".join(부분들[:수])
                종류 = system_weithredu.path_kind(cyfeiriadur_VALUE)
                if 종류 == 0:
                    system_weithredu.mkdir(cyfeiriadur_VALUE)
                    만든폴더.append(cyfeiriadur_VALUE)
                elif 종류 != 2:
                    raise ValueError("cyfeiriadur_VALUE 경로에 파일이 있습니다: " + cyfeiriadur_VALUE)
            만든파일.append(LLWYBR)
            ysgrifennu_LOG(LLWYBR, data)
        ysgrifennu_LOG(Rhestr_llwybr, 새목록)
    except Exception:
        for LLWYBR in 만든파일:
            if system_weithredu.path_kind(LLWYBR):
                system_weithredu.remove(LLWYBR)
        for cyfeiriadur_VALUE in reversed(만든폴더):
            system_weithredu.rmdir(cyfeiriadur_VALUE)
        if 이전목록 is not None:
            ysgrifennu_LOG(Rhestr_llwybr, 이전목록)
        elif system_weithredu.path_kind(Rhestr_llwybr):
            system_weithredu.remove(Rhestr_llwybr)
        raise
    print("gosod_VALUE 완료:", Enw, 명세["version"], "→ /lib (RAM)")


def tynnu_cofnod(Enw):
    cofnod_Rhestr = 목록읽기()
    if Enw not in cofnod_Rhestr:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Enw)
    for LLWYBR, 지문값 in cofnod_Rhestr[Enw]["files"].items():
        if system_weithredu.path_kind(LLWYBR) != 1 or 지문(system_weithredu.read(LLWYBR)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + LLWYBR)
    for LLWYBR in cofnod_Rhestr[Enw]["files"]:
        system_weithredu.remove(LLWYBR)
    del cofnod_Rhestr[Enw]
    ysgrifennu_LOG(Rhestr_llwybr, json.dumps(cofnod_Rhestr).encode())
    print("tynnu_cofnod 완료:", Enw)


def Gweithredu_2(인수):
    rhif_porth = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        rhif_porth = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Enw, msinfo32_exe in 목록읽기().items():
            print(Enw, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        gosod_VALUE(인수[1], rhif_porth)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        tynnu_cofnod(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ffynhonnell_coeden 설치기 (PyPA pip 전체가 아님)")
        print("pip install Enw[==버전] [--port 8027] | pip list | pip uninstall Enw")
        print("lletya: Offer/Gweithredu_gorchymyn.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Gweithredu_2(sys.argv[1:])
    except Exception as Gwall:
        print("bwndel Gwall:", Gwall)
        sys.exit(1)
