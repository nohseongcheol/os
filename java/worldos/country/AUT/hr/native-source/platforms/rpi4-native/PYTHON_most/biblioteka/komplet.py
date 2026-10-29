"""vlastiti 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 domaćin 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operacijski_sustav

Popis_put = "/lib/.pip.json"


def 지문(podaci):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(podaci).digest())


def 목록읽기():
    if operacijski_sustav.path_kind(Popis_put) == 0:
        return {}
    return json.loads(operacijski_sustav.read(Popis_put).decode("utf-8"))


def zapisivanje_LOG(PUTANJA, podaci):
    if operacijski_sustav.write(PUTANJA, podaci) != len(podaci):
        raise OSError(28)


def 경로검사(PUTANJA):
    if not isinstance(PUTANJA, str) or not PUTANJA.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in PUTANJA.split("/")):
        raise ValueError("허용하지 않는 komplet PUTANJA")
    if "\\" in PUTANJA or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in PUTANJA):
        raise ValueError("잘못된 PUTANJA 문자")
    REZULTAT = "/lib/" + PUTANJA
    if len(REZULTAT.encode("utf-8")) > 63 or PUTANJA in ("hrvatski.py", "komplet.py"):
        raise ValueError("komplet 경로가 너무 길거나 zadana_vrijednost 라이브러리와 겹칩니다.")
    return REZULTAT


class primiti_tok:
    def __init__(자신, sudionik):
        자신.sudionik = sudionik
        자신.남은자료 = b""
        자신.Pokreni = operacijski_sustav.ticks_ms()

    def 정확히읽기(자신, 길이):
        podaci = bytearray()
        while len(podaci) < 길이:
            if operacijski_sustav.ticks_ms() - 자신.Pokreni > 90000:
                raise ValueError("komplet 중계 odgovor TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operacijski_sustav.tcp_read(자신.sudionik, 512)
                except OSError as GREŠKA:
                    if GREŠKA.args[0] != 11:
                        raise
                    operacijski_sustav.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("komplet 전송이 중간에 끝났습니다.")
            artikl_COUNT = min(길이 - len(podaci), len(자신.남은자료))
            podaci.extend(자신.남은자료[:artikl_COUNT])
            자신.남은자료 = 자신.남은자료[artikl_COUNT:]
            operacijski_sustav.sleep_ms(0)
        return bytes(podaci)


def preuzmi(zahtjev, broj_priključka):
    if len(zahtjev) > 96 or any(znak_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_VALUE in zahtjev):
        raise ValueError("사용법: pip install Ime 또는 Ime==버전")
    sudionik = operacijski_sustav.tcp_open()
    try:
        Pokreni = operacijski_sustav.ticks_ms()
        while True:
            try:
                operacijski_sustav.tcp_connect(sudionik, "10.0.2.2", broj_priključka)
                break
            except OSError as GREŠKA:
                if GREŠKA.args[0] not in (11, 115) or operacijski_sustav.ticks_ms() - Pokreni > 5000:
                    raise ValueError("komplet 중계 Spoji_se kvar_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operacijski_sustav.sleep_ms(10)
        podaci = (zahtjev + "\n").encode()
        while podaci:
            try:
                artikl_COUNT = operacijski_sustav.tcp_write(sudionik, podaci)
                if not artikl_COUNT:
                    raise ValueError("komplet zahtjev Prijenos_VALUE kvar_VALUE")
                podaci = podaci[artikl_COUNT:]
            except OSError as GREŠKA:
                if GREŠKA.args[0] != 11:
                    raise
                operacijski_sustav.sleep_ms(10)
                if operacijski_sustav.ticks_ms() - Pokreni > 10000:
                    raise ValueError("komplet zahtjev Prijenos_VALUE TIME_VALUE 초과")
        tok_VALUE = primiti_tok(sudionik)
        머리 = tok_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("komplet Prijenos_VALUE slučaj_VALUE 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("komplet 명세가 너무 큽니다.")
        명세 = json.loads(tok_VALUE.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 izvor_stablo 파일은 1~16개여야 합니다.")
        if sum(unos_VALUE["size"] for unos_VALUE in 명세["files"]) > 65536:
            raise ValueError("komplet izvor_stablo 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for unos_VALUE in 명세["files"]:
            PUTANJA = 경로검사(unos_VALUE["path"])
            if PUTANJA in 파일들 or not 0 <= unos_VALUE["size"] <= 16384:
                raise ValueError("중복 PUTANJA 또는 Datoteka Veličina 초과")
            podaci = tok_VALUE.정확히읽기(unos_VALUE["size"])
            if 지문(podaci) != unos_VALUE["sha256"]:
                raise ValueError("komplet Datoteka SHA-256 불일치")
            # 실행하지 않고 redovno_artikl MicroPython의 문법으로 먼저 검사한다.
            compile(podaci.decode("utf-8"), PUTANJA, "exec")
            파일들[PUTANJA] = podaci
            gc.collect()
        return 명세, 파일들
    finally:
        operacijski_sustav.udp_close(sudionik)


def instaliraj_VALUE(zahtjev, broj_priključka):
    print("komplet preuzmi:", zahtjev)
    명세, 파일들 = preuzmi(zahtjev, broj_priključka)
    unos_Popis = 목록읽기()
    Ime = 명세["name"]
    if Ime in unos_Popis:
        if unos_Popis[Ime]["version"] == 명세["version"]:
            for PUTANJA, 지문값 in unos_Popis[Ime]["files"].items():
                if operacijski_sustav.path_kind(PUTANJA) != 1 or 지문(operacijski_sustav.read(PUTANJA)) != 지문값:
                    raise ValueError("설치된 komplet 파일이 달라졌습니다: " + PUTANJA)
            print("이미 설치됨:", Ime, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 TRAG_VALUE 설치하십시오.")
    for PUTANJA in 파일들:
        if operacijski_sustav.path_kind(PUTANJA):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + PUTANJA)
    unos_Popis[Ime] = {"version": 명세["version"], "files": {PUTANJA: 지문(podaci) for PUTANJA, podaci in 파일들.items()}}
    새목록 = json.dumps(unos_Popis).encode()
    if len(새목록) > 16384:
        raise ValueError("komplet unos_Popis Veličina 초과")
    이전목록 = operacijski_sustav.read(Popis_put) if operacijski_sustav.path_kind(Popis_put) else None
    만든파일 = []
    만든폴더 = []
    try:
        for PUTANJA, podaci in 파일들.items():
            부분들 = PUTANJA.split("/")
            for 수 in range(2, len(부분들)):
                imenik_VALUE = "/".join(부분들[:수])
                종류 = operacijski_sustav.path_kind(imenik_VALUE)
                if 종류 == 0:
                    operacijski_sustav.mkdir(imenik_VALUE)
                    만든폴더.append(imenik_VALUE)
                elif 종류 != 2:
                    raise ValueError("imenik_VALUE 경로에 파일이 있습니다: " + imenik_VALUE)
            만든파일.append(PUTANJA)
            zapisivanje_LOG(PUTANJA, podaci)
        zapisivanje_LOG(Popis_put, 새목록)
    except Exception:
        for PUTANJA in 만든파일:
            if operacijski_sustav.path_kind(PUTANJA):
                operacijski_sustav.remove(PUTANJA)
        for imenik_VALUE in reversed(만든폴더):
            operacijski_sustav.rmdir(imenik_VALUE)
        if 이전목록 is not None:
            zapisivanje_LOG(Popis_put, 이전목록)
        elif operacijski_sustav.path_kind(Popis_put):
            operacijski_sustav.remove(Popis_put)
        raise
    print("instaliraj_VALUE 완료:", Ime, 명세["version"], "→ /lib (RAM)")


def ukloniti_unos(Ime):
    unos_Popis = 목록읽기()
    if Ime not in unos_Popis:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ime)
    for PUTANJA, 지문값 in unos_Popis[Ime]["files"].items():
        if operacijski_sustav.path_kind(PUTANJA) != 1 or 지문(operacijski_sustav.read(PUTANJA)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + PUTANJA)
    for PUTANJA in unos_Popis[Ime]["files"]:
        operacijski_sustav.remove(PUTANJA)
    del unos_Popis[Ime]
    zapisivanje_LOG(Popis_put, json.dumps(unos_Popis).encode())
    print("ukloniti_unos 완료:", Ime)


def Pokreni(Argumenti):
    broj_priključka = 8027
    if len(Argumenti) >= 2 and Argumenti[-2] == "--port":
        broj_priključka = int(Argumenti[-1])
        Argumenti = Argumenti[:-2]
    if Argumenti == ["list"]:
        for Ime, Podaci_o_sustavu in 목록읽기().items():
            print(Ime, Podaci_o_sustavu["version"])
    elif len(Argumenti) == 2 and Argumenti[0] == "install":
        instaliraj_VALUE(Argumenti[1], broj_priključka)
    elif len(Argumenti) == 2 and Argumenti[0] == "uninstall":
        ukloniti_unos(Argumenti[1])
    elif not Argumenti or Argumenti in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython izvor_stablo 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ime[==버전] [--port 8027] | pip list | pip uninstall Ime")
        print("domaćin: Alati/Izvrši_naredba.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Pokreni(sys.argv[1:])
    except Exception as GREŠKA:
        print("komplet GREŠKA:", GREŠKA)
        sys.exit(1)
