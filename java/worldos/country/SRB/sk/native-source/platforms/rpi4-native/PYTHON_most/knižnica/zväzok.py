"""vlastné 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 hostiteľ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operačný_systém

Zoznam_cesta = "/lib/.pip.json"


def 지문(údaje):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(údaje).digest())


def 목록읽기():
    if operačný_systém.path_kind(Zoznam_cesta) == 0:
        return {}
    return json.loads(operačný_systém.read(Zoznam_cesta).decode("utf-8"))


def zapísať_LOG(Cesta, údaje):
    if operačný_systém.write(Cesta, údaje) != len(údaje):
        raise OSError(28)


def skontrolovať_cesta(Cesta):
    if not isinstance(Cesta, str) or not Cesta.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Cesta.split("/")):
        raise ValueError("허용하지 않는 zväzok Cesta")
    if "\\" in Cesta or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in Cesta):
        raise ValueError("잘못된 Cesta 문자")
    KR = "/lib/" + Cesta
    if len(KR.encode("utf-8")) > 63 or Cesta in ("Slovenský.py", "zväzok.py"):
        raise ValueError("zväzok 경로가 너무 길거나 predvolená_hodnota 라이브러리와 겹칩니다.")
    return KR


class dostať_Stream:
    def __init__(자신, účastník):
        자신.účastník = účastník
        자신.남은자료 = b""
        자신.Spustiť_2 = operačný_systém.ticks_ms()

    def 정확히읽기(자신, dĺžka_VALUE):
        údaje = bytearray()
        while len(údaje) < dĺžka_VALUE:
            if operačný_systém.ticks_ms() - 자신.Spustiť_2 > 90000:
                raise ValueError("zväzok 중계 odozva čas_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operačný_systém.tcp_read(자신.účastník, 512)
                except OSError as chyba:
                    if chyba.args[0] != 11:
                        raise
                    operačný_systém.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("zväzok 전송이 중간에 끝났습니다.")
            položka_COUNT = min(dĺžka_VALUE - len(údaje), len(자신.남은자료))
            údaje.extend(자신.남은자료[:položka_COUNT])
            자신.남은자료 = 자신.남은자료[položka_COUNT:]
            operačný_systém.sleep_ms(0)
        return bytes(údaje)


def prevziať(požiadavka, číslo_portu):
    if len(požiadavka) > 96 or any(znak_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_VALUE in požiadavka):
        raise ValueError("사용법: pip install Názov 또는 Názov==버전")
    účastník = operačný_systém.tcp_open()
    try:
        Spustiť_2 = operačný_systém.ticks_ms()
        while True:
            try:
                operačný_systém.tcp_connect(účastník, "10.0.2.2", číslo_portu)
                break
            except OSError as chyba:
                if chyba.args[0] not in (11, 115) or operačný_systém.ticks_ms() - Spustiť_2 > 5000:
                    raise ValueError("zväzok 중계 Pripojiť zlyhanie_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operačný_systém.sleep_ms(10)
        údaje = (požiadavka + "\n").encode()
        while údaje:
            try:
                položka_COUNT = operačný_systém.tcp_write(účastník, údaje)
                if not položka_COUNT:
                    raise ValueError("zväzok požiadavka prenos_VALUE zlyhanie_VALUE")
                údaje = údaje[položka_COUNT:]
            except OSError as chyba:
                if chyba.args[0] != 11:
                    raise
                operačný_systém.sleep_ms(10)
                if operačný_systém.ticks_ms() - Spustiť_2 > 10000:
                    raise ValueError("zväzok požiadavka prenos_VALUE čas_VALUE 초과")
        Stream_VALUE = dostať_Stream(účastník)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("zväzok prenos_VALUE prípad_VALUE 불일치")
        dĺžka_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if dĺžka_VALUE > 8192:
            raise ValueError("zväzok 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(dĺžka_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 zdroj_strom 파일은 1~16개여야 합니다.")
        if sum(položka_VALUE["size"] for položka_VALUE in 명세["files"]) > 65536:
            raise ValueError("zväzok zdroj_strom 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for položka_VALUE in 명세["files"]:
            Cesta = skontrolovať_cesta(položka_VALUE["path"])
            if Cesta in 파일들 or not 0 <= položka_VALUE["size"] <= 16384:
                raise ValueError("중복 Cesta 또는 Súbor Veľkosť 초과")
            údaje = Stream_VALUE.정확히읽기(položka_VALUE["size"])
            if 지문(údaje) != položka_VALUE["sha256"]:
                raise ValueError("zväzok Súbor SHA-256 불일치")
            # 실행하지 않고 v_termíne_splatnosti_položka MicroPython의 문법으로 먼저 검사한다.
            compile(údaje.decode("utf-8"), Cesta, "exec")
            파일들[Cesta] = údaje
            gc.collect()
        return 명세, 파일들
    finally:
        operačný_systém.udp_close(účastník)


def inštalovať_VALUE(požiadavka, číslo_portu):
    print("zväzok prevziať:", požiadavka)
    명세, 파일들 = prevziať(požiadavka, číslo_portu)
    položka_Zoznam = 목록읽기()
    Názov = 명세["name"]
    if Názov in položka_Zoznam:
        if položka_Zoznam[Názov]["version"] == 명세["version"]:
            for Cesta, 지문값 in položka_Zoznam[Názov]["files"].items():
                if operačný_systém.path_kind(Cesta) != 1 or 지문(operačný_systém.read(Cesta)) != 지문값:
                    raise ValueError("설치된 zväzok 파일이 달라졌습니다: " + Cesta)
            print("이미 설치됨:", Názov, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VALUE 설치하십시오.")
    for Cesta in 파일들:
        if operačný_systém.path_kind(Cesta):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Cesta)
    položka_Zoznam[Názov] = {"version": 명세["version"], "files": {Cesta: 지문(údaje) for Cesta, údaje in 파일들.items()}}
    새목록 = json.dumps(položka_Zoznam).encode()
    if len(새목록) > 16384:
        raise ValueError("zväzok položka_Zoznam Veľkosť 초과")
    이전목록 = operačný_systém.read(Zoznam_cesta) if operačný_systém.path_kind(Zoznam_cesta) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Cesta, údaje in 파일들.items():
            부분들 = Cesta.split("/")
            for 수 in range(2, len(부분들)):
                Adresár_VALUE = "/".join(부분들[:수])
                종류 = operačný_systém.path_kind(Adresár_VALUE)
                if 종류 == 0:
                    operačný_systém.mkdir(Adresár_VALUE)
                    만든폴더.append(Adresár_VALUE)
                elif 종류 != 2:
                    raise ValueError("Adresár_VALUE 경로에 파일이 있습니다: " + Adresár_VALUE)
            만든파일.append(Cesta)
            zapísať_LOG(Cesta, údaje)
        zapísať_LOG(Zoznam_cesta, 새목록)
    except Exception:
        for Cesta in 만든파일:
            if operačný_systém.path_kind(Cesta):
                operačný_systém.remove(Cesta)
        for Adresár_VALUE in reversed(만든폴더):
            operačný_systém.rmdir(Adresár_VALUE)
        if 이전목록 is not None:
            zapísať_LOG(Zoznam_cesta, 이전목록)
        elif operačný_systém.path_kind(Zoznam_cesta):
            operačný_systém.remove(Zoznam_cesta)
        raise
    print("inštalovať_VALUE 완료:", Názov, 명세["version"], "→ /lib (RAM)")


def odobrať_položka(Názov):
    položka_Zoznam = 목록읽기()
    if Názov not in položka_Zoznam:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Názov)
    for Cesta, 지문값 in položka_Zoznam[Názov]["files"].items():
        if operačný_systém.path_kind(Cesta) != 1 or 지문(operačný_systém.read(Cesta)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Cesta)
    for Cesta in položka_Zoznam[Názov]["files"]:
        operačný_systém.remove(Cesta)
    del položka_Zoznam[Názov]
    zapísať_LOG(Zoznam_cesta, json.dumps(položka_Zoznam).encode())
    print("odobrať_položka 완료:", Názov)


def Spustiť_2(Argumenty):
    číslo_portu = 8027
    if len(Argumenty) >= 2 and Argumenty[-2] == "--port":
        číslo_portu = int(Argumenty[-1])
        Argumenty = Argumenty[:-2]
    if Argumenty == ["list"]:
        for Názov, Systémové_informácie in 목록읽기().items():
            print(Názov, Systémové_informácie["version"])
    elif len(Argumenty) == 2 and Argumenty[0] == "install":
        inštalovať_VALUE(Argumenty[1], číslo_portu)
    elif len(Argumenty) == 2 and Argumenty[0] == "uninstall":
        odobrať_položka(Argumenty[1])
    elif not Argumenty or Argumenty in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython zdroj_strom 설치기 (PyPA pip 전체가 아님)")
        print("pip install Názov[==버전] [--port 8027] | pip list | pip uninstall Názov")
        print("hostiteľ: Nástroje/Vykonať_príkaz.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Spustiť_2(sys.argv[1:])
    except Exception as chyba:
        print("zväzok chyba:", chyba)
        sys.exit(1)
