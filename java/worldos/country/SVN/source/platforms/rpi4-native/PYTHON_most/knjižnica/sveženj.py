"""lastno 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 gostiti 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operacijski_sistem

Seznam_pot = "/lib/.pip.json"


def 지문(podatki):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(podatki).digest())


def 목록읽기():
    if operacijski_sistem.path_kind(Seznam_pot) == 0:
        return {}
    return json.loads(operacijski_sistem.read(Seznam_pot).decode("utf-8"))


def pisati_LOG(POT, podatki):
    if operacijski_sistem.write(POT, podatki) != len(podatki):
        raise OSError(28)


def preveriti_pot(POT):
    if not isinstance(POT, str) or not POT.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in POT.split("/")):
        raise ValueError("허용하지 않는 sveženj POT")
    if "\\" in POT or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in POT):
        raise ValueError("잘못된 POT 문자")
    REZULTAT = "/lib/" + POT
    if len(REZULTAT.encode("utf-8")) > 63 or POT in ("slovenščina.py", "sveženj.py"):
        raise ValueError("sveženj 경로가 너무 길거나 privzeta_vrednost 라이브러리와 겹칩니다.")
    return REZULTAT


class sprejeti_sprejemati_prejeti_prejemati_tok:
    def __init__(자신, končna_točka):
        자신.končna_točka = končna_točka
        자신.남은자료 = b""
        자신.Zaženi = operacijski_sistem.ticks_ms()

    def 정확히읽기(자신, 길이):
        podatki = bytearray()
        while len(podatki) < 길이:
            if operacijski_sistem.ticks_ms() - 자신.Zaženi > 90000:
                raise ValueError("sveženj 중계 odgovor čas_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operacijski_sistem.tcp_read(자신.končna_točka, 512)
                except OSError as NAPAKA:
                    if NAPAKA.args[0] != 11:
                        raise
                    operacijski_sistem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("sveženj 전송이 중간에 끝났습니다.")
            element_COUNT = min(길이 - len(podatki), len(자신.남은자료))
            podatki.extend(자신.남은자료[:element_COUNT])
            자신.남은자료 = 자신.남은자료[element_COUNT:]
            operacijski_sistem.sleep_ms(0)
        return bytes(podatki)


def prenos(zahteva, številka_vrat):
    if len(zahteva) > 96 or any(znak_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_VALUE in zahteva):
        raise ValueError("사용법: pip install Ime 또는 Ime==버전")
    končna_točka = operacijski_sistem.tcp_open()
    try:
        Zaženi = operacijski_sistem.ticks_ms()
        while True:
            try:
                operacijski_sistem.tcp_connect(končna_točka, "10.0.2.2", številka_vrat)
                break
            except OSError as NAPAKA:
                if NAPAKA.args[0] not in (11, 115) or operacijski_sistem.ticks_ms() - Zaženi > 5000:
                    raise ValueError("sveženj 중계 Poveži napaka_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operacijski_sistem.sleep_ms(10)
        podatki = (zahteva + "\n").encode()
        while podatki:
            try:
                element_COUNT = operacijski_sistem.tcp_write(končna_točka, podatki)
                if not element_COUNT:
                    raise ValueError("sveženj zahteva Prenos_VALUE napaka_VALUE")
                podatki = podatki[element_COUNT:]
            except OSError as NAPAKA:
                if NAPAKA.args[0] != 11:
                    raise
                operacijski_sistem.sleep_ms(10)
                if operacijski_sistem.ticks_ms() - Zaženi > 10000:
                    raise ValueError("sveženj zahteva Prenos_VALUE čas_VALUE 초과")
        tok_VALUE = sprejeti_sprejemati_prejeti_prejemati_tok(končna_točka)
        머리 = tok_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("sveženj Prenos_VALUE primer_VALUE 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("sveženj 명세가 너무 큽니다.")
        명세 = json.loads(tok_VALUE.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 vir_drevo 파일은 1~16개여야 합니다.")
        if sum(vnos_VALUE["size"] for vnos_VALUE in 명세["files"]) > 65536:
            raise ValueError("sveženj vir_drevo 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for vnos_VALUE in 명세["files"]:
            POT = preveriti_pot(vnos_VALUE["path"])
            if POT in 파일들 or not 0 <= vnos_VALUE["size"] <= 16384:
                raise ValueError("중복 POT 또는 Datoteka Velikost 초과")
            podatki = tok_VALUE.정확히읽기(vnos_VALUE["size"])
            if 지문(podatki) != vnos_VALUE["sha256"]:
                raise ValueError("sveženj Datoteka SHA-256 불일치")
            # 실행하지 않고 sprotno_element MicroPython의 문법으로 먼저 검사한다.
            compile(podatki.decode("utf-8"), POT, "exec")
            파일들[POT] = podatki
            gc.collect()
        return 명세, 파일들
    finally:
        operacijski_sistem.udp_close(končna_točka)


def namesti_VALUE(zahteva, številka_vrat):
    print("sveženj prenos:", zahteva)
    명세, 파일들 = prenos(zahteva, številka_vrat)
    vnos_Seznam = 목록읽기()
    Ime = 명세["name"]
    if Ime in vnos_Seznam:
        if vnos_Seznam[Ime]["version"] == 명세["version"]:
            for POT, 지문값 in vnos_Seznam[Ime]["files"].items():
                if operacijski_sistem.path_kind(POT) != 1 or 지문(operacijski_sistem.read(POT)) != 지문값:
                    raise ValueError("설치된 sveženj 파일이 달라졌습니다: " + POT)
            print("이미 설치됨:", Ime, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ZAJ_VALUE 설치하십시오.")
    for POT in 파일들:
        if operacijski_sistem.path_kind(POT):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + POT)
    vnos_Seznam[Ime] = {"version": 명세["version"], "files": {POT: 지문(podatki) for POT, podatki in 파일들.items()}}
    새목록 = json.dumps(vnos_Seznam).encode()
    if len(새목록) > 16384:
        raise ValueError("sveženj vnos_Seznam Velikost 초과")
    이전목록 = operacijski_sistem.read(Seznam_pot) if operacijski_sistem.path_kind(Seznam_pot) else None
    만든파일 = []
    만든폴더 = []
    try:
        for POT, podatki in 파일들.items():
            부분들 = POT.split("/")
            for 수 in range(2, len(부분들)):
                Imenik_VALUE = "/".join(부분들[:수])
                종류 = operacijski_sistem.path_kind(Imenik_VALUE)
                if 종류 == 0:
                    operacijski_sistem.mkdir(Imenik_VALUE)
                    만든폴더.append(Imenik_VALUE)
                elif 종류 != 2:
                    raise ValueError("Imenik_VALUE 경로에 파일이 있습니다: " + Imenik_VALUE)
            만든파일.append(POT)
            pisati_LOG(POT, podatki)
        pisati_LOG(Seznam_pot, 새목록)
    except Exception:
        for POT in 만든파일:
            if operacijski_sistem.path_kind(POT):
                operacijski_sistem.remove(POT)
        for Imenik_VALUE in reversed(만든폴더):
            operacijski_sistem.rmdir(Imenik_VALUE)
        if 이전목록 is not None:
            pisati_LOG(Seznam_pot, 이전목록)
        elif operacijski_sistem.path_kind(Seznam_pot):
            operacijski_sistem.remove(Seznam_pot)
        raise
    print("namesti_VALUE 완료:", Ime, 명세["version"], "→ /lib (RAM)")


def odstraniti_vnos(Ime):
    vnos_Seznam = 목록읽기()
    if Ime not in vnos_Seznam:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ime)
    for POT, 지문값 in vnos_Seznam[Ime]["files"].items():
        if operacijski_sistem.path_kind(POT) != 1 or 지문(operacijski_sistem.read(POT)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + POT)
    for POT in vnos_Seznam[Ime]["files"]:
        operacijski_sistem.remove(POT)
    del vnos_Seznam[Ime]
    pisati_LOG(Seznam_pot, json.dumps(vnos_Seznam).encode())
    print("odstraniti_vnos 완료:", Ime)


def Zaženi(Argumenti):
    številka_vrat = 8027
    if len(Argumenti) >= 2 and Argumenti[-2] == "--port":
        številka_vrat = int(Argumenti[-1])
        Argumenti = Argumenti[:-2]
    if Argumenti == ["list"]:
        for Ime, msinfo32_exe in 목록읽기().items():
            print(Ime, msinfo32_exe["version"])
    elif len(Argumenti) == 2 and Argumenti[0] == "install":
        namesti_VALUE(Argumenti[1], številka_vrat)
    elif len(Argumenti) == 2 and Argumenti[0] == "uninstall":
        odstraniti_vnos(Argumenti[1])
    elif not Argumenti or Argumenti in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython vir_drevo 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ime[==버전] [--port 8027] | pip list | pip uninstall Ime")
        print("gostiti: Orodja/Izvedi_ukaz.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Zaženi(sys.argv[1:])
    except Exception as NAPAKA:
        print("sveženj NAPAKA:", NAPAKA)
        sys.exit(1)
