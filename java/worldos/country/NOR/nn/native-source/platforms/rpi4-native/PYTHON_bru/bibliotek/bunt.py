"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 vert 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operativsystem

Liste_bane = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if operativsystem.path_kind(Liste_bane) == 0:
        return {}
    return json.loads(operativsystem.read(Liste_bane).decode("utf-8"))


def skrive_LOG(STIGE, data):
    if operativsystem.write(STIGE, data) != len(data):
        raise OSError(28)


def sjekk_bane(STIGE):
    if not isinstance(STIGE, str) or not STIGE.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in STIGE.split("/")):
        raise ValueError("허용하지 않는 bunt STIGE")
    if "\\" in STIGE or any(ord(teikn_VALUE) < 32 or ord(teikn_VALUE) == 127 for teikn_VALUE in STIGE):
        raise ValueError("잘못된 STIGE 문자")
    forretningsmål = "/lib/" + STIGE
    if len(forretningsmål.encode("utf-8")) > 63 or STIGE in ("한국어.py", "bunt.py"):
        raise ValueError("bunt 경로가 너무 길거나 standardverdi 라이브러리와 겹칩니다.")
    return forretningsmål


class 수신흐름:
    def __init__(자신, endepunkt):
        자신.endepunkt = endepunkt
        자신.남은자료 = b""
        자신.Køyr_2 = operativsystem.ticks_ms()

    def 정확히읽기(자신, lengd_VALUE):
        data = bytearray()
        while len(data) < lengd_VALUE:
            if operativsystem.ticks_ms() - 자신.Køyr_2 > 90000:
                raise ValueError("bunt 중계 svare TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operativsystem.tcp_read(자신.endepunkt, 512)
                except OSError as FEIL:
                    if FEIL.args[0] != 11:
                        raise
                    operativsystem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bunt 전송이 중간에 끝났습니다.")
            vare_COUNT = min(lengd_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:vare_COUNT])
            자신.남은자료 = 자신.남은자료[vare_COUNT:]
            operativsystem.sleep_ms(0)
        return bytes(data)


def laste_ned(요청, portnummer):
    if len(요청) > 96 or any(teikn_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for teikn_VALUE in 요청):
        raise ValueError("사용법: pip install Namn 또는 Namn==버전")
    endepunkt = operativsystem.tcp_open()
    try:
        Køyr_2 = operativsystem.ticks_ms()
        while True:
            try:
                operativsystem.tcp_connect(endepunkt, "10.0.2.2", portnummer)
                break
            except OSError as FEIL:
                if FEIL.args[0] not in (11, 115) or operativsystem.ticks_ms() - Køyr_2 > 5000:
                    raise ValueError("bunt 중계 Kopla_til feil_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operativsystem.sleep_ms(10)
        data = (요청 + "\n").encode()
        while data:
            try:
                vare_COUNT = operativsystem.tcp_write(endepunkt, data)
                if not vare_COUNT:
                    raise ValueError("bunt 요청 Overfør_VALUE feil_VALUE")
                data = data[vare_COUNT:]
            except OSError as FEIL:
                if FEIL.args[0] != 11:
                    raise
                operativsystem.sleep_ms(10)
                if operativsystem.ticks_ms() - Køyr_2 > 10000:
                    raise ValueError("bunt 요청 Overfør_VALUE TIME_VALUE 초과")
        Stream_VALUE = 수신흐름(endepunkt)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bunt Overfør_VALUE sak_VALUE 불일치")
        lengd_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if lengd_VALUE > 8192:
            raise ValueError("bunt 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(lengd_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 kjelde_tre 파일은 1~16개여야 합니다.")
        if sum(oppføring_VALUE["size"] for oppføring_VALUE in 명세["files"]) > 65536:
            raise ValueError("bunt kjelde_tre 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for oppføring_VALUE in 명세["files"]:
            STIGE = sjekk_bane(oppføring_VALUE["path"])
            if STIGE in 파일들 or not 0 <= oppføring_VALUE["size"] <= 16384:
                raise ValueError("중복 STIGE 또는 Fil Storleik 초과")
            data = Stream_VALUE.정확히읽기(oppføring_VALUE["size"])
            if 지문(data) != oppføring_VALUE["sha256"]:
                raise ValueError("bunt Fil SHA-256 불일치")
            # 실행하지 않고 betalt_vare MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), STIGE, "exec")
            파일들[STIGE] = data
            gc.collect()
        return 명세, 파일들
    finally:
        operativsystem.udp_close(endepunkt)


def installere_VALUE(요청, portnummer):
    print("bunt laste_ned:", 요청)
    명세, 파일들 = laste_ned(요청, portnummer)
    oppføring_Liste = 목록읽기()
    Namn = 명세["name"]
    if Namn in oppføring_Liste:
        if oppføring_Liste[Namn]["version"] == 명세["version"]:
            for STIGE, 지문값 in oppføring_Liste[Namn]["files"].items():
                if operativsystem.path_kind(STIGE) != 1 or 지문(operativsystem.read(STIGE)) != 지문값:
                    raise ValueError("설치된 bunt 파일이 달라졌습니다: " + STIGE)
            print("이미 설치됨:", Namn, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 TILBAKE_VALUE 설치하십시오.")
    for STIGE in 파일들:
        if operativsystem.path_kind(STIGE):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + STIGE)
    oppføring_Liste[Namn] = {"version": 명세["version"], "files": {STIGE: 지문(data) for STIGE, data in 파일들.items()}}
    새목록 = json.dumps(oppføring_Liste).encode()
    if len(새목록) > 16384:
        raise ValueError("bunt oppføring_Liste Storleik 초과")
    이전목록 = operativsystem.read(Liste_bane) if operativsystem.path_kind(Liste_bane) else None
    만든파일 = []
    만든폴더 = []
    try:
        for STIGE, data in 파일들.items():
            부분들 = STIGE.split("/")
            for 수 in range(2, len(부분들)):
                katalog_VALUE = "/".join(부분들[:수])
                종류 = operativsystem.path_kind(katalog_VALUE)
                if 종류 == 0:
                    operativsystem.mkdir(katalog_VALUE)
                    만든폴더.append(katalog_VALUE)
                elif 종류 != 2:
                    raise ValueError("katalog_VALUE 경로에 파일이 있습니다: " + katalog_VALUE)
            만든파일.append(STIGE)
            skrive_LOG(STIGE, data)
        skrive_LOG(Liste_bane, 새목록)
    except Exception:
        for STIGE in 만든파일:
            if operativsystem.path_kind(STIGE):
                operativsystem.remove(STIGE)
        for katalog_VALUE in reversed(만든폴더):
            operativsystem.rmdir(katalog_VALUE)
        if 이전목록 is not None:
            skrive_LOG(Liste_bane, 이전목록)
        elif operativsystem.path_kind(Liste_bane):
            operativsystem.remove(Liste_bane)
        raise
    print("installere_VALUE 완료:", Namn, 명세["version"], "→ /lib (RAM)")


def fjerne_oppføring(Namn):
    oppføring_Liste = 목록읽기()
    if Namn not in oppføring_Liste:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Namn)
    for STIGE, 지문값 in oppføring_Liste[Namn]["files"].items():
        if operativsystem.path_kind(STIGE) != 1 or 지문(operativsystem.read(STIGE)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + STIGE)
    for STIGE in oppføring_Liste[Namn]["files"]:
        operativsystem.remove(STIGE)
    del oppføring_Liste[Namn]
    skrive_LOG(Liste_bane, json.dumps(oppføring_Liste).encode())
    print("fjerne_oppføring 완료:", Namn)


def Køyr_2(Argument):
    portnummer = 8027
    if len(Argument) >= 2 and Argument[-2] == "--port":
        portnummer = int(Argument[-1])
        Argument = Argument[:-2]
    if Argument == ["list"]:
        for Namn, msinfo32_exe in 목록읽기().items():
            print(Namn, msinfo32_exe["version"])
    elif len(Argument) == 2 and Argument[0] == "install":
        installere_VALUE(Argument[1], portnummer)
    elif len(Argument) == 2 and Argument[0] == "uninstall":
        fjerne_oppføring(Argument[1])
    elif not Argument or Argument in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython kjelde_tre 설치기 (PyPA pip 전체가 아님)")
        print("pip install Namn[==버전] [--port 8027] | pip list | pip uninstall Namn")
        print("vert: Verktøy/Utfør_kommando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Køyr_2(sys.argv[1:])
    except Exception as FEIL:
        print("bunt FEIL:", FEIL)
        sys.exit(1)
