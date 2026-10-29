"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Ostalari 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistema_eragile

Zerrenda_bide_izen = "/lib/.pip.json"


def 지문(datuak):
    return "".join("%02x" % balio for balio in hashlib.sha256(datuak).digest())


def 목록읽기():
    if sistema_eragile.path_kind(Zerrenda_bide_izen) == 0:
        return {}
    return json.loads(sistema_eragile.read(Zerrenda_bide_izen).decode("utf-8"))


def idatzi_LOG(Bide_izena, datuak):
    if sistema_eragile.write(Bide_izena, datuak) != len(datuak):
        raise OSError(28)


def txeke_bide_izen(Bide_izena):
    if not isinstance(Bide_izena, str) or not Bide_izena.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Bide_izena.split("/")):
        raise ValueError("허용하지 않는 multzo Bide_izena")
    if "\\" in Bide_izena or any(ord(karaktere_balio) < 32 or ord(karaktere_balio) == 127 for karaktere_balio in Bide_izena):
        raise ValueError("잘못된 Bide_izena 문자")
    EMAITZA = "/lib/" + Bide_izena
    if len(EMAITZA.encode("utf-8")) > 63 or Bide_izena in ("Euskara.py", "multzo.py"):
        raise ValueError("multzo 경로가 너무 길거나 balio_lehenetsi 라이브러리와 겹칩니다.")
    return EMAITZA


class 수신흐름:
    def __init__(자신, amaiera_puntu):
        자신.amaiera_puntu = amaiera_puntu
        자신.남은자료 = b""
        자신.Exekutatu_2 = sistema_eragile.ticks_ms()

    def 정확히읽기(자신, luzera_balio):
        datuak = bytearray()
        while len(datuak) < luzera_balio:
            if sistema_eragile.ticks_ms() - 자신.Exekutatu_2 > 90000:
                raise ValueError("multzo 중계 erantzun ordua_balio 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistema_eragile.tcp_read(자신.amaiera_puntu, 512)
                except OSError as errorea:
                    if errorea.args[0] != 11:
                        raise
                    sistema_eragile.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("multzo 전송이 중간에 끝났습니다.")
            elementu_ZENBATU = min(luzera_balio - len(datuak), len(자신.남은자료))
            datuak.extend(자신.남은자료[:elementu_ZENBATU])
            자신.남은자료 = 자신.남은자료[elementu_ZENBATU:]
            sistema_eragile.sleep_ms(0)
        return bytes(datuak)


def deskarga(eskaera, ataka_zenbaki):
    if len(eskaera) > 96 or any(karaktere_balio not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karaktere_balio in eskaera):
        raise ValueError("사용법: pip install Izena 또는 Izena==버전")
    amaiera_puntu = sistema_eragile.tcp_open()
    try:
        Exekutatu_2 = sistema_eragile.ticks_ms()
        while True:
            try:
                sistema_eragile.tcp_connect(amaiera_puntu, "10.0.2.2", ataka_zenbaki)
                break
            except OSError as errorea:
                if errorea.args[0] not in (11, 115) or sistema_eragile.ticks_ms() - Exekutatu_2 > 5000:
                    raise ValueError("multzo 중계 Konektatu hutsegite_balio: 호스트에서 --network --pip로 실행하십시오.")
                sistema_eragile.sleep_ms(10)
        datuak = (eskaera + "\n").encode()
        while datuak:
            try:
                elementu_ZENBATU = sistema_eragile.tcp_write(amaiera_puntu, datuak)
                if not elementu_ZENBATU:
                    raise ValueError("multzo eskaera transferitu_balio hutsegite_balio")
                datuak = datuak[elementu_ZENBATU:]
            except OSError as errorea:
                if errorea.args[0] != 11:
                    raise
                sistema_eragile.sleep_ms(10)
                if sistema_eragile.ticks_ms() - Exekutatu_2 > 10000:
                    raise ValueError("multzo eskaera transferitu_balio ordua_balio 초과")
        Stream_balio = 수신흐름(amaiera_puntu)
        머리 = Stream_balio.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("multzo transferitu_balio kasu_balio 불일치")
        luzera_balio = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if luzera_balio > 8192:
            raise ValueError("multzo 명세가 너무 큽니다.")
        명세 = json.loads(Stream_balio.정확히읽기(luzera_balio).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 iturburu_zuhaitz 파일은 1~16개여야 합니다.")
        if sum(sarrera_balio["size"] for sarrera_balio in 명세["files"]) > 65536:
            raise ValueError("multzo iturburu_zuhaitz 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for sarrera_balio in 명세["files"]:
            Bide_izena = txeke_bide_izen(sarrera_balio["path"])
            if Bide_izena in 파일들 or not 0 <= sarrera_balio["size"] <= 16384:
                raise ValueError("중복 Bide_izena 또는 Fitxategia Tamaina 초과")
            datuak = Stream_balio.정확히읽기(sarrera_balio["size"])
            if 지문(datuak) != sarrera_balio["sha256"]:
                raise ValueError("multzo Fitxategia SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(datuak.decode("utf-8"), Bide_izena, "exec")
            파일들[Bide_izena] = datuak
            gc.collect()
        return 명세, 파일들
    finally:
        sistema_eragile.udp_close(amaiera_puntu)


def instalatu_balio(eskaera, ataka_zenbaki):
    print("multzo deskarga:", eskaera)
    명세, 파일들 = deskarga(eskaera, ataka_zenbaki)
    sarrera_Zerrenda = 목록읽기()
    Izena = 명세["name"]
    if Izena in sarrera_Zerrenda:
        if sarrera_Zerrenda[Izena]["version"] == 명세["version"]:
            for Bide_izena, 지문값 in sarrera_Zerrenda[Izena]["files"].items():
                if sistema_eragile.path_kind(Bide_izena) != 1 or 지문(sistema_eragile.read(Bide_izena)) != 지문값:
                    raise ValueError("설치된 multzo 파일이 달라졌습니다: " + Bide_izena)
            print("이미 설치됨:", Izena, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ATZERA_balio 설치하십시오.")
    for Bide_izena in 파일들:
        if sistema_eragile.path_kind(Bide_izena):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Bide_izena)
    sarrera_Zerrenda[Izena] = {"version": 명세["version"], "files": {Bide_izena: 지문(datuak) for Bide_izena, datuak in 파일들.items()}}
    새목록 = json.dumps(sarrera_Zerrenda).encode()
    if len(새목록) > 16384:
        raise ValueError("multzo sarrera_Zerrenda Tamaina 초과")
    이전목록 = sistema_eragile.read(Zerrenda_bide_izen) if sistema_eragile.path_kind(Zerrenda_bide_izen) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Bide_izena, datuak in 파일들.items():
            부분들 = Bide_izena.split("/")
            for 수 in range(2, len(부분들)):
                direktorio_balio = "/".join(부분들[:수])
                종류 = sistema_eragile.path_kind(direktorio_balio)
                if 종류 == 0:
                    sistema_eragile.mkdir(direktorio_balio)
                    만든폴더.append(direktorio_balio)
                elif 종류 != 2:
                    raise ValueError("direktorio_balio 경로에 파일이 있습니다: " + direktorio_balio)
            만든파일.append(Bide_izena)
            idatzi_LOG(Bide_izena, datuak)
        idatzi_LOG(Zerrenda_bide_izen, 새목록)
    except Exception:
        for Bide_izena in 만든파일:
            if sistema_eragile.path_kind(Bide_izena):
                sistema_eragile.remove(Bide_izena)
        for direktorio_balio in reversed(만든폴더):
            sistema_eragile.rmdir(direktorio_balio)
        if 이전목록 is not None:
            idatzi_LOG(Zerrenda_bide_izen, 이전목록)
        elif sistema_eragile.path_kind(Zerrenda_bide_izen):
            sistema_eragile.remove(Zerrenda_bide_izen)
        raise
    print("instalatu_balio 완료:", Izena, 명세["version"], "→ /lib (RAM)")


def kendu_sarrera(Izena):
    sarrera_Zerrenda = 목록읽기()
    if Izena not in sarrera_Zerrenda:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Izena)
    for Bide_izena, 지문값 in sarrera_Zerrenda[Izena]["files"].items():
        if sistema_eragile.path_kind(Bide_izena) != 1 or 지문(sistema_eragile.read(Bide_izena)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Bide_izena)
    for Bide_izena in sarrera_Zerrenda[Izena]["files"]:
        sistema_eragile.remove(Bide_izena)
    del sarrera_Zerrenda[Izena]
    idatzi_LOG(Zerrenda_bide_izen, json.dumps(sarrera_Zerrenda).encode())
    print("kendu_sarrera 완료:", Izena)


def Exekutatu_2(Argumentuak):
    ataka_zenbaki = 8027
    if len(Argumentuak) >= 2 and Argumentuak[-2] == "--port":
        ataka_zenbaki = int(Argumentuak[-1])
        Argumentuak = Argumentuak[:-2]
    if Argumentuak == ["list"]:
        for Izena, msinfo32_exe in 목록읽기().items():
            print(Izena, msinfo32_exe["version"])
    elif len(Argumentuak) == 2 and Argumentuak[0] == "install":
        instalatu_balio(Argumentuak[1], ataka_zenbaki)
    elif len(Argumentuak) == 2 and Argumentuak[0] == "uninstall":
        kendu_sarrera(Argumentuak[1])
    elif not Argumentuak or Argumentuak in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython iturburu_zuhaitz 설치기 (PyPA pip 전체가 아님)")
        print("pip install Izena[==버전] [--port 8027] | pip list | pip uninstall Izena")
        print("Ostalari: Tresnak/exekutatu_komando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Exekutatu_2(sys.argv[1:])
    except Exception as errorea:
        print("multzo errorea:", errorea)
        sys.exit(1)
