"""savs 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 viesot 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operētājsistēma

Saraksts_ceļš = "/lib/.pip.json"


def 지문(dati):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(dati).digest())


def 목록읽기():
    if operētājsistēma.path_kind(Saraksts_ceļš) == 0:
        return {}
    return json.loads(operētājsistēma.read(Saraksts_ceļš).decode("utf-8"))


def rakstīšana_LOG(CEĻŠ, dati):
    if operētājsistēma.write(CEĻŠ, dati) != len(dati):
        raise OSError(28)


def čeks_ceļš(CEĻŠ):
    if not isinstance(CEĻŠ, str) or not CEĻŠ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 numurs 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in CEĻŠ.split("/")):
        raise ValueError("허용하지 않는 saistīt CEĻŠ")
    if "\\" in CEĻŠ or any(ord(rakstzīme_VALUE) < 32 or ord(rakstzīme_VALUE) == 127 for rakstzīme_VALUE in CEĻŠ):
        raise ValueError("잘못된 CEĻŠ 문자")
    mērs = "/lib/" + CEĻŠ
    if len(mērs.encode("utf-8")) > 63 or CEĻŠ in ("Latviešu.py", "saistīt.py"):
        raise ValueError("saistīt 경로가 너무 길거나 noklusējuma_vērtība 라이브러리와 겹칩니다.")
    return mērs


class saņemt_Stream:
    def __init__(자신, dalībnieks):
        자신.dalībnieks = dalībnieks
        자신.남은자료 = b""
        자신.Palaist = operētājsistēma.ticks_ms()

    def 정확히읽기(자신, 길이):
        dati = bytearray()
        while len(dati) < 길이:
            if operētājsistēma.ticks_ms() - 자신.Palaist > 90000:
                raise ValueError("saistīt 중계 atbilde TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operētājsistēma.tcp_read(자신.dalībnieks, 512)
                except OSError as Kļūda:
                    if Kļūda.args[0] != 11:
                        raise
                    operētājsistēma.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("saistīt 전송이 중간에 끝났습니다.")
            krājums_COUNT = min(길이 - len(dati), len(자신.남은자료))
            dati.extend(자신.남은자료[:krājums_COUNT])
            자신.남은자료 = 자신.남은자료[krājums_COUNT:]
            operētājsistēma.sleep_ms(0)
        return bytes(dati)


def lejupielāde(pieprasījums, porta_numurs):
    if len(pieprasījums) > 96 or any(rakstzīme_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for rakstzīme_VALUE in pieprasījums):
        raise ValueError("사용법: pip install Nosaukums 또는 Nosaukums==버전")
    dalībnieks = operētājsistēma.tcp_open()
    try:
        Palaist = operētājsistēma.ticks_ms()
        while True:
            try:
                operētājsistēma.tcp_connect(dalībnieks, "10.0.2.2", porta_numurs)
                break
            except OSError as Kļūda:
                if Kļūda.args[0] not in (11, 115) or operētājsistēma.ticks_ms() - Palaist > 5000:
                    raise ValueError("saistīt 중계 Savienoties kļūme_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operētājsistēma.sleep_ms(10)
        dati = (pieprasījums + "\n").encode()
        while dati:
            try:
                krājums_COUNT = operētājsistēma.tcp_write(dalībnieks, dati)
                if not krājums_COUNT:
                    raise ValueError("saistīt pieprasījums nodot_VALUE_630ba093 kļūme_VALUE")
                dati = dati[krājums_COUNT:]
            except OSError as Kļūda:
                if Kļūda.args[0] != 11:
                    raise
                operētājsistēma.sleep_ms(10)
                if operētājsistēma.ticks_ms() - Palaist > 10000:
                    raise ValueError("saistīt pieprasījums nodot_VALUE_630ba093 TIME_VALUE 초과")
        Stream_VALUE = saņemt_Stream(dalībnieks)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("saistīt nodot_VALUE_630ba093 līguma_vērtība 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("saistīt 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 avots_koks 파일은 1~16개여야 합니다.")
        if sum(ievade_VALUE["size"] for ievade_VALUE in 명세["files"]) > 65536:
            raise ValueError("saistīt avots_koks 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ievade_VALUE in 명세["files"]:
            CEĻŠ = čeks_ceļš(ievade_VALUE["path"])
            if CEĻŠ in 파일들 or not 0 <= ievade_VALUE["size"] <= 16384:
                raise ValueError("중복 CEĻŠ 또는 Fails Izmērs 초과")
            dati = Stream_VALUE.정확히읽기(ievade_VALUE["size"])
            if 지문(dati) != ievade_VALUE["sha256"]:
                raise ValueError("saistīt Fails SHA-256 불일치")
            # 실행하지 않고 pašreizējais_krājums MicroPython의 문법으로 먼저 검사한다.
            compile(dati.decode("utf-8"), CEĻŠ, "exec")
            파일들[CEĻŠ] = dati
            gc.collect()
        return 명세, 파일들
    finally:
        operētājsistēma.udp_close(dalībnieks)


def instalēt_VALUE(pieprasījums, porta_numurs):
    print("saistīt lejupielāde:", pieprasījums)
    명세, 파일들 = lejupielāde(pieprasījums, porta_numurs)
    ievade_Saraksts = 목록읽기()
    Nosaukums = 명세["name"]
    if Nosaukums in ievade_Saraksts:
        if ievade_Saraksts[Nosaukums]["version"] == 명세["version"]:
            for CEĻŠ, 지문값 in ievade_Saraksts[Nosaukums]["files"].items():
                if operētājsistēma.path_kind(CEĻŠ) != 1 or 지문(operētājsistēma.read(CEĻŠ)) != 지문값:
                    raise ValueError("설치된 saistīt 파일이 달라졌습니다: " + CEĻŠ)
            print("이미 설치됨:", Nosaukums, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ATPAKAĻ_VALUE 설치하십시오.")
    for CEĻŠ in 파일들:
        if operētājsistēma.path_kind(CEĻŠ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + CEĻŠ)
    ievade_Saraksts[Nosaukums] = {"version": 명세["version"], "files": {CEĻŠ: 지문(dati) for CEĻŠ, dati in 파일들.items()}}
    새목록 = json.dumps(ievade_Saraksts).encode()
    if len(새목록) > 16384:
        raise ValueError("saistīt ievade_Saraksts Izmērs 초과")
    이전목록 = operētājsistēma.read(Saraksts_ceļš) if operētājsistēma.path_kind(Saraksts_ceļš) else None
    만든파일 = []
    만든폴더 = []
    try:
        for CEĻŠ, dati in 파일들.items():
            부분들 = CEĻŠ.split("/")
            for numurs in range(2, len(부분들)):
                Direktorijs_VALUE = "/".join(부분들[:numurs])
                종류 = operētājsistēma.path_kind(Direktorijs_VALUE)
                if 종류 == 0:
                    operētājsistēma.mkdir(Direktorijs_VALUE)
                    만든폴더.append(Direktorijs_VALUE)
                elif 종류 != 2:
                    raise ValueError("Direktorijs_VALUE 경로에 파일이 있습니다: " + Direktorijs_VALUE)
            만든파일.append(CEĻŠ)
            rakstīšana_LOG(CEĻŠ, dati)
        rakstīšana_LOG(Saraksts_ceļš, 새목록)
    except Exception:
        for CEĻŠ in 만든파일:
            if operētājsistēma.path_kind(CEĻŠ):
                operētājsistēma.remove(CEĻŠ)
        for Direktorijs_VALUE in reversed(만든폴더):
            operētājsistēma.rmdir(Direktorijs_VALUE)
        if 이전목록 is not None:
            rakstīšana_LOG(Saraksts_ceļš, 이전목록)
        elif operētājsistēma.path_kind(Saraksts_ceļš):
            operētājsistēma.remove(Saraksts_ceļš)
        raise
    print("instalēt_VALUE 완료:", Nosaukums, 명세["version"], "→ /lib (RAM)")


def noņemt_ievade(Nosaukums):
    ievade_Saraksts = 목록읽기()
    if Nosaukums not in ievade_Saraksts:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nosaukums)
    for CEĻŠ, 지문값 in ievade_Saraksts[Nosaukums]["files"].items():
        if operētājsistēma.path_kind(CEĻŠ) != 1 or 지문(operētājsistēma.read(CEĻŠ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + CEĻŠ)
    for CEĻŠ in ievade_Saraksts[Nosaukums]["files"]:
        operētājsistēma.remove(CEĻŠ)
    del ievade_Saraksts[Nosaukums]
    rakstīšana_LOG(Saraksts_ceļš, json.dumps(ievade_Saraksts).encode())
    print("noņemt_ievade 완료:", Nosaukums)


def Palaist(Parametri):
    porta_numurs = 8027
    if len(Parametri) >= 2 and Parametri[-2] == "--port":
        porta_numurs = int(Parametri[-1])
        Parametri = Parametri[:-2]
    if Parametri == ["list"]:
        for Nosaukums, msinfo32_exe in 목록읽기().items():
            print(Nosaukums, msinfo32_exe["version"])
    elif len(Parametri) == 2 and Parametri[0] == "install":
        instalēt_VALUE(Parametri[1], porta_numurs)
    elif len(Parametri) == 2 and Parametri[0] == "uninstall":
        noņemt_ievade(Parametri[1])
    elif not Parametri or Parametri in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython avots_koks 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nosaukums[==버전] [--port 8027] | pip list | pip uninstall Nosaukums")
        print("viesot: Rīki/Izpildīt_komanda.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Palaist(sys.argv[1:])
    except Exception as Kļūda:
        print("saistīt Kļūda:", Kļūda)
        sys.exit(1)
