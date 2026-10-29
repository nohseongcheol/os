"""saját 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 gazda 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operációs_rendszer

Lista_útvonal = "/lib/.pip.json"


def 지문(adat):
    return "".join("%02x" % ÉRTÉK for ÉRTÉK in hashlib.sha256(adat).digest())


def 목록읽기():
    if operációs_rendszer.path_kind(Lista_útvonal) == 0:
        return {}
    return json.loads(operációs_rendszer.read(Lista_útvonal).decode("utf-8"))


def ír_LOG(ÚTVONAL, adat):
    if operációs_rendszer.write(ÚTVONAL, adat) != len(adat):
        raise OSError(28)


def csekk_útvonal(ÚTVONAL):
    if not isinstance(ÚTVONAL, str) or not ÚTVONAL.endswith(".py"):
        raise ValueError("Python 소스만 설치할 szám 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ÚTVONAL.split("/")):
        raise ValueError("허용하지 않는 köteg ÚTVONAL")
    if "\\" in ÚTVONAL or any(ord(karakter_ÉRTÉK) < 32 or ord(karakter_ÉRTÉK) == 127 for karakter_ÉRTÉK in ÚTVONAL):
        raise ValueError("잘못된 ÚTVONAL 문자")
    KR = "/lib/" + ÚTVONAL
    if len(KR.encode("utf-8")) > 63 or ÚTVONAL in ("magyar.py", "köteg.py"):
        raise ValueError("köteg 경로가 너무 길거나 alapértelmezett_érték 라이브러리와 겹칩니다.")
    return KR


class fogad_Stream:
    def __init__(자신, végpont):
        자신.végpont = végpont
        자신.남은자료 = b""
        자신.Futtatás = operációs_rendszer.ticks_ms()

    def 정확히읽기(자신, hossz_ÉRTÉK):
        adat = bytearray()
        while len(adat) < hossz_ÉRTÉK:
            if operációs_rendszer.ticks_ms() - 자신.Futtatás > 90000:
                raise ValueError("köteg 중계 válasz IDŐ_ÉRTÉK 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operációs_rendszer.tcp_read(자신.végpont, 512)
                except OSError as HIBA:
                    if HIBA.args[0] != 11:
                        raise
                    operációs_rendszer.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("köteg 전송이 중간에 끝났습니다.")
            cikk_DARAB = min(hossz_ÉRTÉK - len(adat), len(자신.남은자료))
            adat.extend(자신.남은자료[:cikk_DARAB])
            자신.남은자료 = 자신.남은자료[cikk_DARAB:]
            operációs_rendszer.sleep_ms(0)
        return bytes(adat)


def letölt(kérés, portszám):
    if len(kérés) > 96 or any(karakter_ÉRTÉK not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karakter_ÉRTÉK in kérés):
        raise ValueError("사용법: pip install Név 또는 Név==버전")
    végpont = operációs_rendszer.tcp_open()
    try:
        Futtatás = operációs_rendszer.ticks_ms()
        while True:
            try:
                operációs_rendszer.tcp_connect(végpont, "10.0.2.2", portszám)
                break
            except OSError as HIBA:
                if HIBA.args[0] not in (11, 115) or operációs_rendszer.ticks_ms() - Futtatás > 5000:
                    raise ValueError("köteg 중계 Kapcsolódás hiba_ÉRTÉK: 호스트에서 --network --pip로 실행하십시오.")
                operációs_rendszer.sleep_ms(10)
        adat = (kérés + "\n").encode()
        while adat:
            try:
                cikk_DARAB = operációs_rendszer.tcp_write(végpont, adat)
                if not cikk_DARAB:
                    raise ValueError("köteg kérés átvisz_ÉRTÉK hiba_ÉRTÉK")
                adat = adat[cikk_DARAB:]
            except OSError as HIBA:
                if HIBA.args[0] != 11:
                    raise
                operációs_rendszer.sleep_ms(10)
                if operációs_rendszer.ticks_ms() - Futtatás > 10000:
                    raise ValueError("köteg kérés átvisz_ÉRTÉK IDŐ_ÉRTÉK 초과")
        Stream_ÉRTÉK = fogad_Stream(végpont)
        머리 = Stream_ÉRTÉK.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("köteg átvisz_ÉRTÉK szerződés_értéke 불일치")
        hossz_ÉRTÉK = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if hossz_ÉRTÉK > 8192:
            raise ValueError("köteg 명세가 너무 큽니다.")
        명세 = json.loads(Stream_ÉRTÉK.정확히읽기(hossz_ÉRTÉK).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 forrás_fa 파일은 1~16개여야 합니다.")
        if sum(bejegyzés_ÉRTÉK["size"] for bejegyzés_ÉRTÉK in 명세["files"]) > 65536:
            raise ValueError("köteg forrás_fa 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for bejegyzés_ÉRTÉK in 명세["files"]:
            ÚTVONAL = csekk_útvonal(bejegyzés_ÉRTÉK["path"])
            if ÚTVONAL in 파일들 or not 0 <= bejegyzés_ÉRTÉK["size"] <= 16384:
                raise ValueError("중복 ÚTVONAL 또는 Fájl Méret 초과")
            adat = Stream_ÉRTÉK.정확히읽기(bejegyzés_ÉRTÉK["size"])
            if 지문(adat) != bejegyzés_ÉRTÉK["sha256"]:
                raise ValueError("köteg Fájl SHA-256 불일치")
            # 실행하지 않고 aktuális_cikk MicroPython의 문법으로 먼저 검사한다.
            compile(adat.decode("utf-8"), ÚTVONAL, "exec")
            파일들[ÚTVONAL] = adat
            gc.collect()
        return 명세, 파일들
    finally:
        operációs_rendszer.udp_close(végpont)


def telepít_ÉRTÉK(kérés, portszám):
    print("köteg letölt:", kérés)
    명세, 파일들 = letölt(kérés, portszám)
    bejegyzés_Lista = 목록읽기()
    Név = 명세["name"]
    if Név in bejegyzés_Lista:
        if bejegyzés_Lista[Név]["version"] == 명세["version"]:
            for ÚTVONAL, 지문값 in bejegyzés_Lista[Név]["files"].items():
                if operációs_rendszer.path_kind(ÚTVONAL) != 1 or 지문(operációs_rendszer.read(ÚTVONAL)) != 지문값:
                    raise ValueError("설치된 köteg 파일이 달라졌습니다: " + ÚTVONAL)
            print("이미 설치됨:", Név, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_ÉRTÉK 설치하십시오.")
    for ÚTVONAL in 파일들:
        if operációs_rendszer.path_kind(ÚTVONAL):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ÚTVONAL)
    bejegyzés_Lista[Név] = {"version": 명세["version"], "files": {ÚTVONAL: 지문(adat) for ÚTVONAL, adat in 파일들.items()}}
    새목록 = json.dumps(bejegyzés_Lista).encode()
    if len(새목록) > 16384:
        raise ValueError("köteg bejegyzés_Lista Méret 초과")
    Előző_Lista = operációs_rendszer.read(Lista_útvonal) if operációs_rendszer.path_kind(Lista_útvonal) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ÚTVONAL, adat in 파일들.items():
            부분들 = ÚTVONAL.split("/")
            for szám in range(2, len(부분들)):
                címtár_ÉRTÉK = "/".join(부분들[:szám])
                Altípus_ÉRTÉK = operációs_rendszer.path_kind(címtár_ÉRTÉK)
                if Altípus_ÉRTÉK == 0:
                    operációs_rendszer.mkdir(címtár_ÉRTÉK)
                    만든폴더.append(címtár_ÉRTÉK)
                elif Altípus_ÉRTÉK != 2:
                    raise ValueError("címtár_ÉRTÉK 경로에 파일이 있습니다: " + címtár_ÉRTÉK)
            만든파일.append(ÚTVONAL)
            ír_LOG(ÚTVONAL, adat)
        ír_LOG(Lista_útvonal, 새목록)
    except Exception:
        for ÚTVONAL in 만든파일:
            if operációs_rendszer.path_kind(ÚTVONAL):
                operációs_rendszer.remove(ÚTVONAL)
        for címtár_ÉRTÉK in reversed(만든폴더):
            operációs_rendszer.rmdir(címtár_ÉRTÉK)
        if Előző_Lista is not None:
            ír_LOG(Lista_útvonal, Előző_Lista)
        elif operációs_rendszer.path_kind(Lista_útvonal):
            operációs_rendszer.remove(Lista_útvonal)
        raise
    print("telepít_ÉRTÉK 완료:", Név, 명세["version"], "→ /lib (RAM)")


def eltávolít_bejegyzés(Név):
    bejegyzés_Lista = 목록읽기()
    if Név not in bejegyzés_Lista:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Név)
    for ÚTVONAL, 지문값 in bejegyzés_Lista[Név]["files"].items():
        if operációs_rendszer.path_kind(ÚTVONAL) != 1 or 지문(operációs_rendszer.read(ÚTVONAL)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ÚTVONAL)
    for ÚTVONAL in bejegyzés_Lista[Név]["files"]:
        operációs_rendszer.remove(ÚTVONAL)
    del bejegyzés_Lista[Név]
    ír_LOG(Lista_útvonal, json.dumps(bejegyzés_Lista).encode())
    print("eltávolít_bejegyzés 완료:", Név)


def Futtatás(Argumentumok):
    portszám = 8027
    if len(Argumentumok) >= 2 and Argumentumok[-2] == "--port":
        portszám = int(Argumentumok[-1])
        Argumentumok = Argumentumok[:-2]
    if Argumentumok == ["list"]:
        for Név, msinfo32_exe in 목록읽기().items():
            print(Név, msinfo32_exe["version"])
    elif len(Argumentumok) == 2 and Argumentumok[0] == "install":
        telepít_ÉRTÉK(Argumentumok[1], portszám)
    elif len(Argumentumok) == 2 and Argumentumok[0] == "uninstall":
        eltávolít_bejegyzés(Argumentumok[1])
    elif not Argumentumok or Argumentumok in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython forrás_fa 설치기 (PyPA pip 전체가 아님)")
        print("pip install Név[==버전] [--port 8027] | pip list | pip uninstall Név")
        print("gazda: Eszközök/végrehajt_parancs.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Futtatás(sys.argv[1:])
    except Exception as HIBA:
        print("köteg HIBA:", HIBA)
        sys.exit(1)
