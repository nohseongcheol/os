"""oma 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operatsioonisüsteem

Loend_tee = "/lib/.pip.json"


def 지문(andmed):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(andmed).digest())


def 목록읽기():
    if operatsioonisüsteem.path_kind(Loend_tee) == 0:
        return {}
    return json.loads(operatsioonisüsteem.read(Loend_tee).decode("utf-8"))


def kirjutamine_LOG(RADA, andmed):
    if operatsioonisüsteem.write(RADA, andmed) != len(andmed):
        raise OSError(28)


def tšekk_tee(RADA):
    if not isinstance(RADA, str) or not RADA.endswith(".py"):
        raise ValueError("Python 소스만 설치할 number 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in RADA.split("/")):
        raise ValueError("허용하지 않는 kogum RADA")
    if "\\" in RADA or any(ord(märk_VALUE) < 32 or ord(märk_VALUE) == 127 for märk_VALUE in RADA):
        raise ValueError("잘못된 RADA 문자")
    TULEMUS = "/lib/" + RADA
    if len(TULEMUS.encode("utf-8")) > 63 or RADA in ("Eesti.py", "kogum.py"):
        raise ValueError("kogum 경로가 너무 길거나 vaikeväärtus 라이브러리와 겹칩니다.")
    return TULEMUS


class saama_voog:
    def __init__(자신, osaleja):
        자신.osaleja = osaleja
        자신.남은자료 = b""
        자신.Käivita_2 = operatsioonisüsteem.ticks_ms()

    def 정확히읽기(자신, 길이):
        andmed = bytearray()
        while len(andmed) < 길이:
            if operatsioonisüsteem.ticks_ms() - 자신.Käivita_2 > 90000:
                raise ValueError("kogum 중계 vastus Aeg_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operatsioonisüsteem.tcp_read(자신.osaleja, 512)
                except OSError as VIGA:
                    if VIGA.args[0] != 11:
                        raise
                    operatsioonisüsteem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("kogum 전송이 중간에 끝났습니다.")
            kaup_COUNT = min(길이 - len(andmed), len(자신.남은자료))
            andmed.extend(자신.남은자료[:kaup_COUNT])
            자신.남은자료 = 자신.남은자료[kaup_COUNT:]
            operatsioonisüsteem.sleep_ms(0)
        return bytes(andmed)


def alla_laadima(päring, pordinumber):
    if len(päring) > 96 or any(märk_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for märk_VALUE in päring):
        raise ValueError("사용법: pip install Nimi_2 또는 Nimi_2==버전")
    osaleja = operatsioonisüsteem.tcp_open()
    try:
        Käivita_2 = operatsioonisüsteem.ticks_ms()
        while True:
            try:
                operatsioonisüsteem.tcp_connect(osaleja, "10.0.2.2", pordinumber)
                break
            except OSError as VIGA:
                if VIGA.args[0] not in (11, 115) or operatsioonisüsteem.ticks_ms() - Käivita_2 > 5000:
                    raise ValueError("kogum 중계 Ühendu tõrge_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operatsioonisüsteem.sleep_ms(10)
        andmed = (päring + "\n").encode()
        while andmed:
            try:
                kaup_COUNT = operatsioonisüsteem.tcp_write(osaleja, andmed)
                if not kaup_COUNT:
                    raise ValueError("kogum päring Edasta_VALUE tõrge_VALUE")
                andmed = andmed[kaup_COUNT:]
            except OSError as VIGA:
                if VIGA.args[0] != 11:
                    raise
                operatsioonisüsteem.sleep_ms(10)
                if operatsioonisüsteem.ticks_ms() - Käivita_2 > 10000:
                    raise ValueError("kogum päring Edasta_VALUE Aeg_VALUE 초과")
        voog_VALUE = saama_voog(osaleja)
        머리 = voog_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("kogum Edasta_VALUE lepingu_väärtus 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("kogum 명세가 너무 큽니다.")
        명세 = json.loads(voog_VALUE.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 lähe_puu 파일은 1~16개여야 합니다.")
        if sum(kirje_VALUE["size"] for kirje_VALUE in 명세["files"]) > 65536:
            raise ValueError("kogum lähe_puu 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for kirje_VALUE in 명세["files"]:
            RADA = tšekk_tee(kirje_VALUE["path"])
            if RADA in 파일들 or not 0 <= kirje_VALUE["size"] <= 16384:
                raise ValueError("중복 RADA 또는 Fail Suurus 초과")
            andmed = voog_VALUE.정확히읽기(kirje_VALUE["size"])
            if 지문(andmed) != kirje_VALUE["sha256"]:
                raise ValueError("kogum Fail SHA-256 불일치")
            # 실행하지 않고 tähtaja_piires_kaup MicroPython의 문법으로 먼저 검사한다.
            compile(andmed.decode("utf-8"), RADA, "exec")
            파일들[RADA] = andmed
            gc.collect()
        return 명세, 파일들
    finally:
        operatsioonisüsteem.udp_close(osaleja)


def installima_VALUE(päring, pordinumber):
    print("kogum alla_laadima:", päring)
    명세, 파일들 = alla_laadima(päring, pordinumber)
    kirje_Loend = 목록읽기()
    Nimi_2 = 명세["name"]
    if Nimi_2 in kirje_Loend:
        if kirje_Loend[Nimi_2]["version"] == 명세["version"]:
            for RADA, 지문값 in kirje_Loend[Nimi_2]["files"].items():
                if operatsioonisüsteem.path_kind(RADA) != 1 or 지문(operatsioonisüsteem.read(RADA)) != 지문값:
                    raise ValueError("설치된 kogum 파일이 달라졌습니다: " + RADA)
            print("이미 설치됨:", Nimi_2, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Tagasi_VALUE 설치하십시오.")
    for RADA in 파일들:
        if operatsioonisüsteem.path_kind(RADA):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + RADA)
    kirje_Loend[Nimi_2] = {"version": 명세["version"], "files": {RADA: 지문(andmed) for RADA, andmed in 파일들.items()}}
    새목록 = json.dumps(kirje_Loend).encode()
    if len(새목록) > 16384:
        raise ValueError("kogum kirje_Loend Suurus 초과")
    이전목록 = operatsioonisüsteem.read(Loend_tee) if operatsioonisüsteem.path_kind(Loend_tee) else None
    만든파일 = []
    만든폴더 = []
    try:
        for RADA, andmed in 파일들.items():
            부분들 = RADA.split("/")
            for number in range(2, len(부분들)):
                kaust_VALUE = "/".join(부분들[:number])
                종류 = operatsioonisüsteem.path_kind(kaust_VALUE)
                if 종류 == 0:
                    operatsioonisüsteem.mkdir(kaust_VALUE)
                    만든폴더.append(kaust_VALUE)
                elif 종류 != 2:
                    raise ValueError("kaust_VALUE 경로에 파일이 있습니다: " + kaust_VALUE)
            만든파일.append(RADA)
            kirjutamine_LOG(RADA, andmed)
        kirjutamine_LOG(Loend_tee, 새목록)
    except Exception:
        for RADA in 만든파일:
            if operatsioonisüsteem.path_kind(RADA):
                operatsioonisüsteem.remove(RADA)
        for kaust_VALUE in reversed(만든폴더):
            operatsioonisüsteem.rmdir(kaust_VALUE)
        if 이전목록 is not None:
            kirjutamine_LOG(Loend_tee, 이전목록)
        elif operatsioonisüsteem.path_kind(Loend_tee):
            operatsioonisüsteem.remove(Loend_tee)
        raise
    print("installima_VALUE 완료:", Nimi_2, 명세["version"], "→ /lib (RAM)")


def eemaldama_kirje(Nimi_2):
    kirje_Loend = 목록읽기()
    if Nimi_2 not in kirje_Loend:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nimi_2)
    for RADA, 지문값 in kirje_Loend[Nimi_2]["files"].items():
        if operatsioonisüsteem.path_kind(RADA) != 1 or 지문(operatsioonisüsteem.read(RADA)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + RADA)
    for RADA in kirje_Loend[Nimi_2]["files"]:
        operatsioonisüsteem.remove(RADA)
    del kirje_Loend[Nimi_2]
    kirjutamine_LOG(Loend_tee, json.dumps(kirje_Loend).encode())
    print("eemaldama_kirje 완료:", Nimi_2)


def Käivita_2(Argumendid):
    pordinumber = 8027
    if len(Argumendid) >= 2 and Argumendid[-2] == "--port":
        pordinumber = int(Argumendid[-1])
        Argumendid = Argumendid[:-2]
    if Argumendid == ["list"]:
        for Nimi_2, msinfo32_exe in 목록읽기().items():
            print(Nimi_2, msinfo32_exe["version"])
    elif len(Argumendid) == 2 and Argumendid[0] == "install":
        installima_VALUE(Argumendid[1], pordinumber)
    elif len(Argumendid) == 2 and Argumendid[0] == "uninstall":
        eemaldama_kirje(Argumendid[1])
    elif not Argumendid or Argumendid in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython lähe_puu 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nimi_2[==버전] [--port 8027] | pip list | pip uninstall Nimi_2")
        print("host: Tööriistad/Täida_käsk.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Käivita_2(sys.argv[1:])
    except Exception as VIGA:
        print("kogum VIGA:", VIGA)
        sys.exit(1)
