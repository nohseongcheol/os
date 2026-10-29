"""vlastní 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 hostit 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operační_systém

Seznam_cesta = "/lib/.pip.json"


def otisk_HODNOTA(data):
    return "".join("%02x" % HODNOTA for HODNOTA in hashlib.sha256(data).digest())


def 목록읽기():
    if operační_systém.path_kind(Seznam_cesta) == 0:
        return {}
    return json.loads(operační_systém.read(Seznam_cesta).decode("utf-8"))


def zápis_LOGZ(cesta_2, data):
    if operační_systém.write(cesta_2, data) != len(data):
        raise OSError(28)


def šek_cesta(cesta_2):
    if not isinstance(cesta_2, str) or not cesta_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 číslo 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in cesta_2.split("/")):
        raise ValueError("허용하지 않는 sada cesta_2")
    if "\\" in cesta_2 or any(ord(znak_HODNOTA) < 32 or ord(znak_HODNOTA) == 127 for znak_HODNOTA in cesta_2):
        raise ValueError("잘못된 cesta_2 문자")
    VÝSLEDEK = "/lib/" + cesta_2
    if len(VÝSLEDEK.encode("utf-8")) > 63 or cesta_2 in ("čeština.py", "sada.py"):
        raise ValueError("sada 경로가 너무 길거나 výchozí_hodnota 라이브러리와 겹칩니다.")
    return VÝSLEDEK


class dostat_tok:
    def __init__(자신, účastník):
        자신.účastník = účastník
        자신.남은자료 = b""
        자신.Spustit_2 = operační_systém.ticks_ms()

    def 정확히읽기(자신, délka_HODNOTA):
        data = bytearray()
        while len(data) < délka_HODNOTA:
            if operační_systém.ticks_ms() - 자신.Spustit_2 > 90000:
                raise ValueError("sada Přenos_HODNOTA odezva časová_hodnota 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operační_systém.tcp_read(자신.účastník, 512)
                except OSError as chyba:
                    if chyba.args[0] != 11:
                        raise
                    operační_systém.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("sada 전송이 중간에 끝났습니다.")
            zboží_POČET = min(délka_HODNOTA - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:zboží_POČET])
            자신.남은자료 = 자신.남은자료[zboží_POČET:]
            operační_systém.sleep_ms(0)
        return bytes(data)


def stažení(žádost, číslo_portu):
    if len(žádost) > 96 or any(znak_HODNOTA not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_HODNOTA in žádost):
        raise ValueError("사용법: pip install Název 또는 Název==버전")
    účastník = operační_systém.tcp_open()
    try:
        Spustit_2 = operační_systém.ticks_ms()
        while True:
            try:
                operační_systém.tcp_connect(účastník, "10.0.2.2", číslo_portu)
                break
            except OSError as chyba:
                if chyba.args[0] not in (11, 115) or operační_systém.ticks_ms() - Spustit_2 > 5000:
                    raise ValueError("sada Přenos_HODNOTA Připojit selhání_HODNOTA: 호스트에서 --network --pip로 실행하십시오.")
                operační_systém.sleep_ms(10)
        data = (žádost + "\n").encode()
        while data:
            try:
                zboží_POČET = operační_systém.tcp_write(účastník, data)
                if not zboží_POČET:
                    raise ValueError("sada žádost přenos_HODNOTA selhání_HODNOTA")
                data = data[zboží_POČET:]
            except OSError as chyba:
                if chyba.args[0] != 11:
                    raise
                operační_systém.sleep_ms(10)
                if operační_systém.ticks_ms() - Spustit_2 > 10000:
                    raise ValueError("sada žádost přenos_HODNOTA časová_hodnota 초과")
        tok_HODNOTA = dostat_tok(účastník)
        머리 = tok_HODNOTA.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("sada přenos_HODNOTA hodnota_smlouvy 불일치")
        délka_HODNOTA = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if délka_HODNOTA > 8192:
            raise ValueError("sada 명세가 너무 큽니다.")
        명세 = json.loads(tok_HODNOTA.정확히읽기(délka_HODNOTA).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 zdroj_strom 파일은 1~16개여야 합니다.")
        if sum(položka_HODNOTA["size"] for položka_HODNOTA in 명세["files"]) > 65536:
            raise ValueError("sada zdroj_strom 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for položka_HODNOTA in 명세["files"]:
            cesta_2 = šek_cesta(položka_HODNOTA["path"])
            if cesta_2 in 파일들 or not 0 <= položka_HODNOTA["size"] <= 16384:
                raise ValueError("중복 cesta_2 또는 název_souboru Velikost 초과")
            data = tok_HODNOTA.정확히읽기(položka_HODNOTA["size"])
            if otisk_HODNOTA(data) != položka_HODNOTA["sha256"]:
                raise ValueError("sada název_souboru SHA-256 불일치")
            # 실행하지 않고 dobrá_zboží MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), cesta_2, "exec")
            파일들[cesta_2] = data
            gc.collect()
        return 명세, 파일들
    finally:
        operační_systém.udp_close(účastník)


def instalovat_HODNOTA(žádost, číslo_portu):
    print("sada stažení:", žádost)
    명세, 파일들 = stažení(žádost, číslo_portu)
    položka_Seznam = 목록읽기()
    Název = 명세["name"]
    if Název in položka_Seznam:
        if položka_Seznam[Název]["version"] == 명세["version"]:
            for cesta_2, otisk_data in položka_Seznam[Název]["files"].items():
                if operační_systém.path_kind(cesta_2) != 1 or otisk_HODNOTA(operační_systém.read(cesta_2)) != otisk_data:
                    raise ValueError("설치된 sada 파일이 달라졌습니다: " + cesta_2)
            print("이미 설치됨:", Název, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_HODNOTA 설치하십시오.")
    for cesta_2 in 파일들:
        if operační_systém.path_kind(cesta_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + cesta_2)
    položka_Seznam[Název] = {"version": 명세["version"], "files": {cesta_2: otisk_HODNOTA(data) for cesta_2, data in 파일들.items()}}
    새목록 = json.dumps(položka_Seznam).encode()
    if len(새목록) > 16384:
        raise ValueError("sada položka_Seznam Velikost 초과")
    Předchozí_Seznam = operační_systém.read(Seznam_cesta) if operační_systém.path_kind(Seznam_cesta) else None
    만든파일 = []
    만든폴더 = []
    try:
        for cesta_2, data in 파일들.items():
            부분들 = cesta_2.split("/")
            for číslo in range(2, len(부분들)):
                Adresář_HODNOTA = "/".join(부분들[:číslo])
                Druh_HODNOTA = operační_systém.path_kind(Adresář_HODNOTA)
                if Druh_HODNOTA == 0:
                    operační_systém.mkdir(Adresář_HODNOTA)
                    만든폴더.append(Adresář_HODNOTA)
                elif Druh_HODNOTA != 2:
                    raise ValueError("Adresář_HODNOTA 경로에 파일이 있습니다: " + Adresář_HODNOTA)
            만든파일.append(cesta_2)
            zápis_LOGZ(cesta_2, data)
        zápis_LOGZ(Seznam_cesta, 새목록)
    except Exception:
        for cesta_2 in 만든파일:
            if operační_systém.path_kind(cesta_2):
                operační_systém.remove(cesta_2)
        for Adresář_HODNOTA in reversed(만든폴더):
            operační_systém.rmdir(Adresář_HODNOTA)
        if Předchozí_Seznam is not None:
            zápis_LOGZ(Seznam_cesta, Předchozí_Seznam)
        elif operační_systém.path_kind(Seznam_cesta):
            operační_systém.remove(Seznam_cesta)
        raise
    print("instalovat_HODNOTA 완료:", Název, 명세["version"], "→ /lib (RAM)")


def odebrat_položka(Název):
    položka_Seznam = 목록읽기()
    if Název not in položka_Seznam:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Název)
    for cesta_2, otisk_data in položka_Seznam[Název]["files"].items():
        if operační_systém.path_kind(cesta_2) != 1 or otisk_HODNOTA(operační_systém.read(cesta_2)) != otisk_data:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + cesta_2)
    for cesta_2 in položka_Seznam[Název]["files"]:
        operační_systém.remove(cesta_2)
    del položka_Seznam[Název]
    zápis_LOGZ(Seznam_cesta, json.dumps(položka_Seznam).encode())
    print("odebrat_položka 완료:", Název)


def Spustit_2(argumenty):
    číslo_portu = 8027
    if len(argumenty) >= 2 and argumenty[-2] == "--port":
        číslo_portu = int(argumenty[-1])
        argumenty = argumenty[:-2]
    if argumenty == ["list"]:
        for Název, Informace_o_systému in 목록읽기().items():
            print(Název, Informace_o_systému["version"])
    elif len(argumenty) == 2 and argumenty[0] == "install":
        instalovat_HODNOTA(argumenty[1], číslo_portu)
    elif len(argumenty) == 2 and argumenty[0] == "uninstall":
        odebrat_položka(argumenty[1])
    elif not argumenty or argumenty in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython zdroj_strom 설치기 (PyPA pip 전체가 아님)")
        print("pip install Název[==버전] [--port 8027] | pip list | pip uninstall Název")
        print("hostit: nástroje/Provést_příkaz.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Spustit_2(sys.argv[1:])
    except Exception as chyba:
        print("sada chyba:", chyba)
        sys.exit(1)
