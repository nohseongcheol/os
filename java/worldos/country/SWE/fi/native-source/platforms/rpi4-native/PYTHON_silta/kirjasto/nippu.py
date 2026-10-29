"""oma 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 isäntä 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as käyttöjärjestelmä

luettelo_polku = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % ARVO for ARVO in hashlib.sha256(data).digest())


def lukea_luettelo():
    if käyttöjärjestelmä.path_kind(luettelo_polku) == 0:
        return {}
    return json.loads(käyttöjärjestelmä.read(luettelo_polku).decode("utf-8"))


def kirjoitus_LOG(polku_2, data):
    if käyttöjärjestelmä.write(polku_2, data) != len(data):
        raise OSError(28)


def sekki_polku(polku_2):
    if not isinstance(polku_2, str) or not polku_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 numero 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in polku_2.split("/")):
        raise ValueError("허용하지 않는 nippu polku_2")
    if "\\" in polku_2 or any(ord(merkki_ARVO) < 32 or ord(merkki_ARVO) == 127 for merkki_ARVO in polku_2):
        raise ValueError("잘못된 polku_2 문자")
    TULOS = "/lib/" + polku_2
    if len(TULOS.encode("utf-8")) > 63 or polku_2 in ("suomi.py", "nippu.py"):
        raise ValueError("nippu 경로가 너무 길거나 oletusarvo 라이브러리와 겹칩니다.")
    return TULOS


class saada_virta:
    def __init__(자신, päätepiste):
        자신.päätepiste = päätepiste
        자신.남은자료 = b""
        자신.Suorita_2 = käyttöjärjestelmä.ticks_ms()

    def 정확히읽기(자신, kesto_ARVO):
        data = bytearray()
        while len(data) < kesto_ARVO:
            if käyttöjärjestelmä.ticks_ms() - 자신.Suorita_2 > 90000:
                raise ValueError("nippu 중계 palaute AIKA_ARVO 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = käyttöjärjestelmä.tcp_read(자신.päätepiste, 512)
                except OSError as VIRHE:
                    if VIRHE.args[0] != 11:
                        raise
                    käyttöjärjestelmä.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("nippu 전송이 중간에 끝났습니다.")
            kohde_LASKE = min(kesto_ARVO - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:kohde_LASKE])
            자신.남은자료 = 자신.남은자료[kohde_LASKE:]
            käyttöjärjestelmä.sleep_ms(0)
        return bytes(data)


def ladata(pyyntö, portin_numero):
    if len(pyyntö) > 96 or any(merkki_ARVO not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for merkki_ARVO in pyyntö):
        raise ValueError("사용법: pip install Nimi 또는 Nimi==버전")
    päätepiste = käyttöjärjestelmä.tcp_open()
    try:
        Suorita_2 = käyttöjärjestelmä.ticks_ms()
        while True:
            try:
                käyttöjärjestelmä.tcp_connect(päätepiste, "10.0.2.2", portin_numero)
                break
            except OSError as VIRHE:
                if VIRHE.args[0] not in (11, 115) or käyttöjärjestelmä.ticks_ms() - Suorita_2 > 5000:
                    raise ValueError("nippu 중계 Yhdistä virhe_ARVO: 호스트에서 --network --pip로 실행하십시오.")
                käyttöjärjestelmä.sleep_ms(10)
        data = (pyyntö + "\n").encode()
        while data:
            try:
                kohde_LASKE = käyttöjärjestelmä.tcp_write(päätepiste, data)
                if not kohde_LASKE:
                    raise ValueError("nippu pyyntö Siirrä_ARVO virhe_ARVO")
                data = data[kohde_LASKE:]
            except OSError as VIRHE:
                if VIRHE.args[0] != 11:
                    raise
                käyttöjärjestelmä.sleep_ms(10)
                if käyttöjärjestelmä.ticks_ms() - Suorita_2 > 10000:
                    raise ValueError("nippu pyyntö Siirrä_ARVO AIKA_ARVO 초과")
        virta_ARVO = saada_virta(päätepiste)
        머리 = virta_ARVO.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("nippu Siirrä_ARVO sopimuksen_arvo 불일치")
        kesto_ARVO = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if kesto_ARVO > 8192:
            raise ValueError("nippu 명세가 너무 큽니다.")
        määritys = json.loads(virta_ARVO.정확히읽기(kesto_ARVO).decode())
        if "error" in määritys:
            raise ValueError(määritys["error"])
        if not 1 <= len(määritys["files"]) <= 16:
            raise ValueError("꾸러미당 lähde_puu 파일은 1~16개여야 합니다.")
        if sum(merkintä_ARVO_962f286b["size"] for merkintä_ARVO_962f286b in määritys["files"]) > 65536:
            raise ValueError("nippu lähde_puu 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for merkintä_ARVO_962f286b in määritys["files"]:
            polku_2 = sekki_polku(merkintä_ARVO_962f286b["path"])
            if polku_2 in 파일들 or not 0 <= merkintä_ARVO_962f286b["size"] <= 16384:
                raise ValueError("중복 polku_2 또는 tiedoston_nimi Koko 초과")
            data = virta_ARVO.정확히읽기(merkintä_ARVO_962f286b["size"])
            if 지문(data) != merkintä_ARVO_962f286b["sha256"]:
                raise ValueError("nippu tiedoston_nimi SHA-256 불일치")
            # 실행하지 않고 nykyinen_kohde MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), polku_2, "exec")
            파일들[polku_2] = data
            gc.collect()
        return määritys, 파일들
    finally:
        käyttöjärjestelmä.udp_close(päätepiste)


def asentaa_ARVO(pyyntö, portin_numero):
    print("nippu ladata:", pyyntö)
    määritys, 파일들 = ladata(pyyntö, portin_numero)
    merkintä_luettelo = lukea_luettelo()
    Nimi = määritys["name"]
    if Nimi in merkintä_luettelo:
        if merkintä_luettelo[Nimi]["version"] == määritys["version"]:
            for polku_2, 지문값 in merkintä_luettelo[Nimi]["files"].items():
                if käyttöjärjestelmä.path_kind(polku_2) != 1 or 지문(käyttöjärjestelmä.read(polku_2)) != 지문값:
                    raise ValueError("설치된 nippu 파일이 달라졌습니다: " + polku_2)
            print("이미 설치됨:", Nimi, määritys["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_ARVO 설치하십시오.")
    for polku_2 in 파일들:
        if käyttöjärjestelmä.path_kind(polku_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + polku_2)
    merkintä_luettelo[Nimi] = {"version": määritys["version"], "files": {polku_2: 지문(data) for polku_2, data in 파일들.items()}}
    새목록 = json.dumps(merkintä_luettelo).encode()
    if len(새목록) > 16384:
        raise ValueError("nippu merkintä_luettelo Koko 초과")
    Edellinen_luettelo = käyttöjärjestelmä.read(luettelo_polku) if käyttöjärjestelmä.path_kind(luettelo_polku) else None
    만든파일 = []
    만든폴더 = []
    try:
        for polku_2, data in 파일들.items():
            부분들 = polku_2.split("/")
            for numero in range(2, len(부분들)):
                Directory_ARVO = "/".join(부분들[:numero])
                종류 = käyttöjärjestelmä.path_kind(Directory_ARVO)
                if 종류 == 0:
                    käyttöjärjestelmä.mkdir(Directory_ARVO)
                    만든폴더.append(Directory_ARVO)
                elif 종류 != 2:
                    raise ValueError("Directory_ARVO 경로에 파일이 있습니다: " + Directory_ARVO)
            만든파일.append(polku_2)
            kirjoitus_LOG(polku_2, data)
        kirjoitus_LOG(luettelo_polku, 새목록)
    except Exception:
        for polku_2 in 만든파일:
            if käyttöjärjestelmä.path_kind(polku_2):
                käyttöjärjestelmä.remove(polku_2)
        for Directory_ARVO in reversed(만든폴더):
            käyttöjärjestelmä.rmdir(Directory_ARVO)
        if Edellinen_luettelo is not None:
            kirjoitus_LOG(luettelo_polku, Edellinen_luettelo)
        elif käyttöjärjestelmä.path_kind(luettelo_polku):
            käyttöjärjestelmä.remove(luettelo_polku)
        raise
    print("asentaa_ARVO 완료:", Nimi, määritys["version"], "→ /lib (RAM)")


def poistaa_merkintä(Nimi):
    merkintä_luettelo = lukea_luettelo()
    if Nimi not in merkintä_luettelo:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nimi)
    for polku_2, 지문값 in merkintä_luettelo[Nimi]["files"].items():
        if käyttöjärjestelmä.path_kind(polku_2) != 1 or 지문(käyttöjärjestelmä.read(polku_2)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + polku_2)
    for polku_2 in merkintä_luettelo[Nimi]["files"]:
        käyttöjärjestelmä.remove(polku_2)
    del merkintä_luettelo[Nimi]
    kirjoitus_LOG(luettelo_polku, json.dumps(merkintä_luettelo).encode())
    print("poistaa_merkintä 완료:", Nimi)


def Suorita_2(argumentit):
    portin_numero = 8027
    if len(argumentit) >= 2 and argumentit[-2] == "--port":
        portin_numero = int(argumentit[-1])
        argumentit = argumentit[:-2]
    if argumentit == ["list"]:
        for Nimi, msinfo32_exe in lukea_luettelo().items():
            print(Nimi, msinfo32_exe["version"])
    elif len(argumentit) == 2 and argumentit[0] == "install":
        asentaa_ARVO(argumentit[1], portin_numero)
    elif len(argumentit) == 2 and argumentit[0] == "uninstall":
        poistaa_merkintä(argumentit[1])
    elif not argumentit or argumentit in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython lähde_puu 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nimi[==버전] [--port 8027] | pip list | pip uninstall Nimi")
        print("isäntä: työkalut/Suorita_komento.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Suorita_2(sys.argv[1:])
    except Exception as VIRHE:
        print("nippu VIRHE:", VIRHE)
        sys.exit(1)
