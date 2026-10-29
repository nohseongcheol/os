"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 organizator 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operativni_sistem

spisak_put = "/lib/.pip.json"


def 지문(podaci):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(podaci).digest())


def 목록읽기():
    if operativni_sistem.path_kind(spisak_put) == 0:
        return {}
    return json.loads(operativni_sistem.read(spisak_put).decode("utf-8"))


def pisati_LOG(Putanja, podaci):
    if operativni_sistem.write(Putanja, podaci) != len(podaci):
        raise OSError(28)


def ček_put(Putanja):
    if not isinstance(Putanja, str) or not Putanja.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Putanja.split("/")):
        raise ValueError("허용하지 않는 paket Putanja")
    if "\\" in Putanja or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in Putanja):
        raise ValueError("잘못된 Putanja 문자")
    mjera = "/lib/" + Putanja
    if len(mjera.encode("utf-8")) > 63 or Putanja in ("한국어.py", "paket.py"):
        raise ValueError("paket 경로가 너무 길거나 zadana_vrijednost 라이브러리와 겹칩니다.")
    return mjera


class 수신흐름:
    def __init__(자신, završna_tačka):
        자신.završna_tačka = završna_tačka
        자신.남은자료 = b""
        자신.Pokreni = operativni_sistem.ticks_ms()

    def 정확히읽기(자신, dužina_VALUE):
        podaci = bytearray()
        while len(podaci) < dužina_VALUE:
            if operativni_sistem.ticks_ms() - 자신.Pokreni > 90000:
                raise ValueError("paket 중계 odgovoriti TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operativni_sistem.tcp_read(자신.završna_tačka, 512)
                except OSError as GRESKA:
                    if GRESKA.args[0] != 11:
                        raise
                    operativni_sistem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paket 전송이 중간에 끝났습니다.")
            stavka_COUNT = min(dužina_VALUE - len(podaci), len(자신.남은자료))
            podaci.extend(자신.남은자료[:stavka_COUNT])
            자신.남은자료 = 자신.남은자료[stavka_COUNT:]
            operativni_sistem.sleep_ms(0)
        return bytes(podaci)


def preuzeti(HTTP_zahtjev, broj_priključka):
    if len(HTTP_zahtjev) > 96 or any(znak_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_VALUE in HTTP_zahtjev):
        raise ValueError("사용법: pip install Naziv 또는 Naziv==버전")
    završna_tačka = operativni_sistem.tcp_open()
    try:
        Pokreni = operativni_sistem.ticks_ms()
        while True:
            try:
                operativni_sistem.tcp_connect(završna_tačka, "10.0.2.2", broj_priključka)
                break
            except OSError as GRESKA:
                if GRESKA.args[0] not in (11, 115) or operativni_sistem.ticks_ms() - Pokreni > 5000:
                    raise ValueError("paket 중계 Spoji_se neuspjeh_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operativni_sistem.sleep_ms(10)
        podaci = (HTTP_zahtjev + "\n").encode()
        while podaci:
            try:
                stavka_COUNT = operativni_sistem.tcp_write(završna_tačka, podaci)
                if not stavka_COUNT:
                    raise ValueError("paket HTTP_zahtjev prijenos_VALUE neuspjeh_VALUE")
                podaci = podaci[stavka_COUNT:]
            except OSError as GRESKA:
                if GRESKA.args[0] != 11:
                    raise
                operativni_sistem.sleep_ms(10)
                if operativni_sistem.ticks_ms() - Pokreni > 10000:
                    raise ValueError("paket HTTP_zahtjev prijenos_VALUE TIME_VALUE 초과")
        tok_VALUE = 수신흐름(završna_tačka)
        머리 = tok_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("paket prijenos_VALUE slučaj_VALUE 불일치")
        dužina_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if dužina_VALUE > 8192:
            raise ValueError("paket 명세가 너무 큽니다.")
        명세 = json.loads(tok_VALUE.정확히읽기(dužina_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 izvor_stablo 파일은 1~16개여야 합니다.")
        if sum(unos_VALUE["size"] for unos_VALUE in 명세["files"]) > 65536:
            raise ValueError("paket izvor_stablo 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for unos_VALUE in 명세["files"]:
            Putanja = ček_put(unos_VALUE["path"])
            if Putanja in 파일들 or not 0 <= unos_VALUE["size"] <= 16384:
                raise ValueError("중복 Putanja 또는 Fajl Veličina 초과")
            podaci = tok_VALUE.정확히읽기(unos_VALUE["size"])
            if 지문(podaci) != unos_VALUE["sha256"]:
                raise ValueError("paket Fajl SHA-256 불일치")
            # 실행하지 않고 trenutno_stavka MicroPython의 문법으로 먼저 검사한다.
            compile(podaci.decode("utf-8"), Putanja, "exec")
            파일들[Putanja] = podaci
            gc.collect()
        return 명세, 파일들
    finally:
        operativni_sistem.udp_close(završna_tačka)


def instalirati_VALUE(HTTP_zahtjev, broj_priključka):
    print("paket preuzeti:", HTTP_zahtjev)
    명세, 파일들 = preuzeti(HTTP_zahtjev, broj_priključka)
    unos_spisak = 목록읽기()
    Naziv = 명세["name"]
    if Naziv in unos_spisak:
        if unos_spisak[Naziv]["version"] == 명세["version"]:
            for Putanja, 지문값 in unos_spisak[Naziv]["files"].items():
                if operativni_sistem.path_kind(Putanja) != 1 or 지문(operativni_sistem.read(Putanja)) != 지문값:
                    raise ValueError("설치된 paket 파일이 달라졌습니다: " + Putanja)
            print("이미 설치됨:", Naziv, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ZAD_VALUE 설치하십시오.")
    for Putanja in 파일들:
        if operativni_sistem.path_kind(Putanja):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Putanja)
    unos_spisak[Naziv] = {"version": 명세["version"], "files": {Putanja: 지문(podaci) for Putanja, podaci in 파일들.items()}}
    새목록 = json.dumps(unos_spisak).encode()
    if len(새목록) > 16384:
        raise ValueError("paket unos_spisak Veličina 초과")
    이전목록 = operativni_sistem.read(spisak_put) if operativni_sistem.path_kind(spisak_put) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Putanja, podaci in 파일들.items():
            부분들 = Putanja.split("/")
            for 수 in range(2, len(부분들)):
                Direktorij_VALUE = "/".join(부분들[:수])
                종류 = operativni_sistem.path_kind(Direktorij_VALUE)
                if 종류 == 0:
                    operativni_sistem.mkdir(Direktorij_VALUE)
                    만든폴더.append(Direktorij_VALUE)
                elif 종류 != 2:
                    raise ValueError("Direktorij_VALUE 경로에 파일이 있습니다: " + Direktorij_VALUE)
            만든파일.append(Putanja)
            pisati_LOG(Putanja, podaci)
        pisati_LOG(spisak_put, 새목록)
    except Exception:
        for Putanja in 만든파일:
            if operativni_sistem.path_kind(Putanja):
                operativni_sistem.remove(Putanja)
        for Direktorij_VALUE in reversed(만든폴더):
            operativni_sistem.rmdir(Direktorij_VALUE)
        if 이전목록 is not None:
            pisati_LOG(spisak_put, 이전목록)
        elif operativni_sistem.path_kind(spisak_put):
            operativni_sistem.remove(spisak_put)
        raise
    print("instalirati_VALUE 완료:", Naziv, 명세["version"], "→ /lib (RAM)")


def ukloniti_unos(Naziv):
    unos_spisak = 목록읽기()
    if Naziv not in unos_spisak:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Naziv)
    for Putanja, 지문값 in unos_spisak[Naziv]["files"].items():
        if operativni_sistem.path_kind(Putanja) != 1 or 지문(operativni_sistem.read(Putanja)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Putanja)
    for Putanja in unos_spisak[Naziv]["files"]:
        operativni_sistem.remove(Putanja)
    del unos_spisak[Naziv]
    pisati_LOG(spisak_put, json.dumps(unos_spisak).encode())
    print("ukloniti_unos 완료:", Naziv)


def Pokreni(Argumenti):
    broj_priključka = 8027
    if len(Argumenti) >= 2 and Argumenti[-2] == "--port":
        broj_priključka = int(Argumenti[-1])
        Argumenti = Argumenti[:-2]
    if Argumenti == ["list"]:
        for Naziv, msinfo32_exe in 목록읽기().items():
            print(Naziv, msinfo32_exe["version"])
    elif len(Argumenti) == 2 and Argumenti[0] == "install":
        instalirati_VALUE(Argumenti[1], broj_priključka)
    elif len(Argumenti) == 2 and Argumenti[0] == "uninstall":
        ukloniti_unos(Argumenti[1])
    elif not Argumenti or Argumenti in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython izvor_stablo 설치기 (PyPA pip 전체가 아님)")
        print("pip install Naziv[==버전] [--port 8027] | pip list | pip uninstall Naziv")
        print("organizator: Alati/Izvrši_komanda.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Pokreni(sys.argv[1:])
    except Exception as GRESKA:
        print("paket GRESKA:", GRESKA)
        sys.exit(1)
