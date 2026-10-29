"""własny 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as system_operacyjny

Lista_ścieżka = "/lib/.pip.json"


def odcisk_palca_WARTOŚĆ(dane):
    return "".join("%02x" % WARTOŚĆ for WARTOŚĆ in hashlib.sha256(dane).digest())


def 목록읽기():
    if system_operacyjny.path_kind(Lista_ścieżka) == 0:
        return {}
    return json.loads(system_operacyjny.read(Lista_ścieżka).decode("utf-8"))


def zapis_LOG(ścieżka_2, dane):
    if system_operacyjny.write(ścieżka_2, dane) != len(dane):
        raise OSError(28)


def czek_ścieżka(ścieżka_2):
    if not isinstance(ścieżka_2, str) or not ścieżka_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 identyfikator 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ścieżka_2.split("/")):
        raise ValueError("허용하지 않는 pakiet ścieżka_2")
    if "\\" in ścieżka_2 or any(ord(znak_WARTOŚĆ) < 32 or ord(znak_WARTOŚĆ) == 127 for znak_WARTOŚĆ in ścieżka_2):
        raise ValueError("잘못된 ścieżka_2 문자")
    WYNIK = "/lib/" + ścieżka_2
    if len(WYNIK.encode("utf-8")) > 63 or ścieżka_2 in ("polski.py", "pakiet.py"):
        raise ValueError("pakiet 경로가 너무 길거나 wartość_domyślna 라이브러리와 겹칩니다.")
    return WYNIK


class odbierać_Stream:
    def __init__(자신, uczestnik):
        자신.uczestnik = uczestnik
        자신.남은자료 = b""
        자신.Uruchom_2 = system_operacyjny.ticks_ms()

    def 정확히읽기(자신, długość_WARTOŚĆ):
        dane = bytearray()
        while len(dane) < długość_WARTOŚĆ:
            if system_operacyjny.ticks_ms() - 자신.Uruchom_2 > 90000:
                raise ValueError("pakiet Przekazywanie_WARTOŚĆ odpowiedź wartość_czasu 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = system_operacyjny.tcp_read(자신.uczestnik, 512)
                except OSError as błąd:
                    if błąd.args[0] != 11:
                        raise
                    system_operacyjny.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("pakiet 전송이 중간에 끝났습니다.")
            towar_ILE_LICZB = min(długość_WARTOŚĆ - len(dane), len(자신.남은자료))
            dane.extend(자신.남은자료[:towar_ILE_LICZB])
            자신.남은자료 = 자신.남은자료[towar_ILE_LICZB:]
            system_operacyjny.sleep_ms(0)
        return bytes(dane)


def pobrać(żądanie, numer_portu):
    if len(żądanie) > 96 or any(znak_WARTOŚĆ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_WARTOŚĆ in żądanie):
        raise ValueError("사용법: pip install Nazwa 또는 Nazwa==버전")
    uczestnik = system_operacyjny.tcp_open()
    try:
        Uruchom_2 = system_operacyjny.ticks_ms()
        while True:
            try:
                system_operacyjny.tcp_connect(uczestnik, "10.0.2.2", numer_portu)
                break
            except OSError as błąd:
                if błąd.args[0] not in (11, 115) or system_operacyjny.ticks_ms() - Uruchom_2 > 5000:
                    raise ValueError("pakiet Przekazywanie_WARTOŚĆ Połącz awaria_WARTOŚĆ: 호스트에서 --network --pip로 실행하십시오.")
                system_operacyjny.sleep_ms(10)
        dane = (żądanie + "\n").encode()
        while dane:
            try:
                towar_ILE_LICZB = system_operacyjny.tcp_write(uczestnik, dane)
                if not towar_ILE_LICZB:
                    raise ValueError("pakiet żądanie transfer_WARTOŚĆ awaria_WARTOŚĆ")
                dane = dane[towar_ILE_LICZB:]
            except OSError as błąd:
                if błąd.args[0] != 11:
                    raise
                system_operacyjny.sleep_ms(10)
                if system_operacyjny.ticks_ms() - Uruchom_2 > 10000:
                    raise ValueError("pakiet żądanie transfer_WARTOŚĆ wartość_czasu 초과")
        Stream_WARTOŚĆ = odbierać_Stream(uczestnik)
        머리 = Stream_WARTOŚĆ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("pakiet transfer_WARTOŚĆ wartość_kontraktu 불일치")
        długość_WARTOŚĆ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if długość_WARTOŚĆ > 8192:
            raise ValueError("pakiet 명세가 너무 큽니다.")
        명세 = json.loads(Stream_WARTOŚĆ.정확히읽기(długość_WARTOŚĆ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 źródło_drzewo 파일은 1~16개여야 합니다.")
        if sum(wpis_WARTOŚĆ["size"] for wpis_WARTOŚĆ in 명세["files"]) > 65536:
            raise ValueError("pakiet źródło_drzewo 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for wpis_WARTOŚĆ in 명세["files"]:
            ścieżka_2 = czek_ścieżka(wpis_WARTOŚĆ["path"])
            if ścieżka_2 in 파일들 or not 0 <= wpis_WARTOŚĆ["size"] <= 16384:
                raise ValueError("중복 ścieżka_2 또는 nazwa_pliku Rozmiar 초과")
            dane = Stream_WARTOŚĆ.정확히읽기(wpis_WARTOŚĆ["size"])
            if odcisk_palca_WARTOŚĆ(dane) != wpis_WARTOŚĆ["sha256"]:
                raise ValueError("pakiet nazwa_pliku SHA-256 불일치")
            # 실행하지 않고 bieżący_towar MicroPython의 문법으로 먼저 검사한다.
            compile(dane.decode("utf-8"), ścieżka_2, "exec")
            파일들[ścieżka_2] = dane
            gc.collect()
        return 명세, 파일들
    finally:
        system_operacyjny.udp_close(uczestnik)


def instalować_WARTOŚĆ(żądanie, numer_portu):
    print("pakiet pobrać:", żądanie)
    명세, 파일들 = pobrać(żądanie, numer_portu)
    wpis_Lista = 목록읽기()
    Nazwa = 명세["name"]
    if Nazwa in wpis_Lista:
        if wpis_Lista[Nazwa]["version"] == 명세["version"]:
            for ścieżka_2, odcisk_palca_dane in wpis_Lista[Nazwa]["files"].items():
                if system_operacyjny.path_kind(ścieżka_2) != 1 or odcisk_palca_WARTOŚĆ(system_operacyjny.read(ścieżka_2)) != odcisk_palca_dane:
                    raise ValueError("설치된 pakiet 파일이 달라졌습니다: " + ścieżka_2)
            print("이미 설치됨:", Nazwa, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_WARTOŚĆ 설치하십시오.")
    for ścieżka_2 in 파일들:
        if system_operacyjny.path_kind(ścieżka_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ścieżka_2)
    wpis_Lista[Nazwa] = {"version": 명세["version"], "files": {ścieżka_2: odcisk_palca_WARTOŚĆ(dane) for ścieżka_2, dane in 파일들.items()}}
    새목록 = json.dumps(wpis_Lista).encode()
    if len(새목록) > 16384:
        raise ValueError("pakiet wpis_Lista Rozmiar 초과")
    Wstecz_Lista = system_operacyjny.read(Lista_ścieżka) if system_operacyjny.path_kind(Lista_ścieżka) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ścieżka_2, dane in 파일들.items():
            부분들 = ścieżka_2.split("/")
            for identyfikator in range(2, len(부분들)):
                Katalog_WARTOŚĆ = "/".join(부분들[:identyfikator])
                Rodzaj_WARTOŚĆ = system_operacyjny.path_kind(Katalog_WARTOŚĆ)
                if Rodzaj_WARTOŚĆ == 0:
                    system_operacyjny.mkdir(Katalog_WARTOŚĆ)
                    만든폴더.append(Katalog_WARTOŚĆ)
                elif Rodzaj_WARTOŚĆ != 2:
                    raise ValueError("Katalog_WARTOŚĆ 경로에 파일이 있습니다: " + Katalog_WARTOŚĆ)
            만든파일.append(ścieżka_2)
            zapis_LOG(ścieżka_2, dane)
        zapis_LOG(Lista_ścieżka, 새목록)
    except Exception:
        for ścieżka_2 in 만든파일:
            if system_operacyjny.path_kind(ścieżka_2):
                system_operacyjny.remove(ścieżka_2)
        for Katalog_WARTOŚĆ in reversed(만든폴더):
            system_operacyjny.rmdir(Katalog_WARTOŚĆ)
        if Wstecz_Lista is not None:
            zapis_LOG(Lista_ścieżka, Wstecz_Lista)
        elif system_operacyjny.path_kind(Lista_ścieżka):
            system_operacyjny.remove(Lista_ścieżka)
        raise
    print("instalować_WARTOŚĆ 완료:", Nazwa, 명세["version"], "→ /lib (RAM)")


def usuń_wpis(Nazwa):
    wpis_Lista = 목록읽기()
    if Nazwa not in wpis_Lista:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nazwa)
    for ścieżka_2, odcisk_palca_dane in wpis_Lista[Nazwa]["files"].items():
        if system_operacyjny.path_kind(ścieżka_2) != 1 or odcisk_palca_WARTOŚĆ(system_operacyjny.read(ścieżka_2)) != odcisk_palca_dane:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ścieżka_2)
    for ścieżka_2 in wpis_Lista[Nazwa]["files"]:
        system_operacyjny.remove(ścieżka_2)
    del wpis_Lista[Nazwa]
    zapis_LOG(Lista_ścieżka, json.dumps(wpis_Lista).encode())
    print("usuń_wpis 완료:", Nazwa)


def Uruchom_2(argumenty):
    numer_portu = 8027
    if len(argumenty) >= 2 and argumenty[-2] == "--port":
        numer_portu = int(argumenty[-1])
        argumenty = argumenty[:-2]
    if argumenty == ["list"]:
        for Nazwa, msinfo32_exe in 목록읽기().items():
            print(Nazwa, msinfo32_exe["version"])
    elif len(argumenty) == 2 and argumenty[0] == "install":
        instalować_WARTOŚĆ(argumenty[1], numer_portu)
    elif len(argumenty) == 2 and argumenty[0] == "uninstall":
        usuń_wpis(argumenty[1])
    elif not argumenty or argumenty in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython źródło_drzewo 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nazwa[==버전] [--port 8027] | pip list | pip uninstall Nazwa")
        print("host: narzędzia/Wykonaj_polecenie.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Uruchom_2(sys.argv[1:])
    except Exception as błąd:
        print("pakiet błąd:", błąd)
        sys.exit(1)
