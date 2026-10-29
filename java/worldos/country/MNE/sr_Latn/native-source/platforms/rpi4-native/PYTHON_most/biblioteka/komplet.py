"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operativni_sistem

Lista_putanja = "/lib/.pip.json"


def 지문(podaci):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(podaci).digest())


def 목록읽기():
    if operativni_sistem.path_kind(Lista_putanja) == 0:
        return {}
    return json.loads(operativni_sistem.read(Lista_putanja).decode("utf-8"))


def 기록쓰기(putanja, podaci):
    if operativni_sistem.write(putanja, podaci) != len(podaci):
        raise OSError(28)


def proveriti_putanja(putanja):
    if not isinstance(putanja, str) or not putanja.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in putanja.split("/")):
        raise ValueError("허용하지 않는 komplet putanja")
    if "\\" in putanja or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in putanja):
        raise ValueError("잘못된 putanja 문자")
    KR = "/lib/" + putanja
    if len(KR.encode("utf-8")) > 63 or putanja in ("한국어.py", "komplet.py"):
        raise ValueError("komplet 경로가 너무 길거나 podrazumevana_vrednost 라이브러리와 겹칩니다.")
    return KR


class primiti_tok:
    def __init__(자신, učesnik):
        자신.učesnik = učesnik
        자신.남은자료 = b""
        자신.koristiti = operativni_sistem.ticks_ms()

    def 정확히읽기(자신, 길이):
        podaci = bytearray()
        while len(podaci) < 길이:
            if operativni_sistem.ticks_ms() - 자신.koristiti > 90000:
                raise ValueError("komplet 중계 odgovor TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operativni_sistem.tcp_read(자신.učesnik, 512)
                except OSError as greška:
                    if greška.args[0] != 11:
                        raise
                    operativni_sistem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("komplet 전송이 중간에 끝났습니다.")
            stavka_COUNT = min(길이 - len(podaci), len(자신.남은자료))
            podaci.extend(자신.남은자료[:stavka_COUNT])
            자신.남은자료 = 자신.남은자료[stavka_COUNT:]
            operativni_sistem.sleep_ms(0)
        return bytes(podaci)


def preuzmi(zahtev, broj_porta):
    if len(zahtev) > 96 or any(znak_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for znak_VALUE in zahtev):
        raise ValueError("사용법: pip install ime 또는 ime==버전")
    učesnik = operativni_sistem.tcp_open()
    try:
        koristiti = operativni_sistem.ticks_ms()
        while True:
            try:
                operativni_sistem.tcp_connect(učesnik, "10.0.2.2", broj_porta)
                break
            except OSError as greška:
                if greška.args[0] not in (11, 115) or operativni_sistem.ticks_ms() - koristiti > 5000:
                    raise ValueError("komplet 중계 veze otkazivanje_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operativni_sistem.sleep_ms(10)
        podaci = (zahtev + "\n").encode()
        while podaci:
            try:
                stavka_COUNT = operativni_sistem.tcp_write(učesnik, podaci)
                if not stavka_COUNT:
                    raise ValueError("komplet zahtev prenos_VALUE otkazivanje_VALUE")
                podaci = podaci[stavka_COUNT:]
            except OSError as greška:
                if greška.args[0] != 11:
                    raise
                operativni_sistem.sleep_ms(10)
                if operativni_sistem.ticks_ms() - koristiti > 10000:
                    raise ValueError("komplet zahtev prenos_VALUE TIME_VALUE 초과")
        tok_VALUE = primiti_tok(učesnik)
        머리 = tok_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("komplet prenos_VALUE ugovor_VALUE 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("komplet 명세가 너무 큽니다.")
        명세 = json.loads(tok_VALUE.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 izvor_stablo 파일은 1~16개여야 합니다.")
        if sum(stavka_VALUE["size"] for stavka_VALUE in 명세["files"]) > 65536:
            raise ValueError("komplet izvor_stablo 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for stavka_VALUE in 명세["files"]:
            putanja = proveriti_putanja(stavka_VALUE["path"])
            if putanja in 파일들 or not 0 <= stavka_VALUE["size"] <= 16384:
                raise ValueError("중복 putanja 또는 Datoteka promeniti_veličinu 초과")
            podaci = tok_VALUE.정확히읽기(stavka_VALUE["size"])
            if 지문(podaci) != stavka_VALUE["sha256"]:
                raise ValueError("komplet Datoteka SHA-256 불일치")
            # 실행하지 않고 aktuelno_stavka MicroPython의 문법으로 먼저 검사한다.
            compile(podaci.decode("utf-8"), putanja, "exec")
            파일들[putanja] = podaci
            gc.collect()
        return 명세, 파일들
    finally:
        operativni_sistem.udp_close(učesnik)


def instaliraj_VALUE(zahtev, broj_porta):
    print("komplet preuzmi:", zahtev)
    명세, 파일들 = preuzmi(zahtev, broj_porta)
    stavka_Lista = 목록읽기()
    ime = 명세["name"]
    if ime in stavka_Lista:
        if stavka_Lista[ime]["version"] == 명세["version"]:
            for putanja, 지문값 in stavka_Lista[ime]["files"].items():
                if operativni_sistem.path_kind(putanja) != 1 or 지문(operativni_sistem.read(putanja)) != 지문값:
                    raise ValueError("설치된 komplet 파일이 달라졌습니다: " + putanja)
            print("이미 설치됨:", ime, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 NAZAD_VALUE 설치하십시오.")
    for putanja in 파일들:
        if operativni_sistem.path_kind(putanja):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + putanja)
    stavka_Lista[ime] = {"version": 명세["version"], "files": {putanja: 지문(podaci) for putanja, podaci in 파일들.items()}}
    새목록 = json.dumps(stavka_Lista).encode()
    if len(새목록) > 16384:
        raise ValueError("komplet stavka_Lista promeniti_veličinu 초과")
    이전목록 = operativni_sistem.read(Lista_putanja) if operativni_sistem.path_kind(Lista_putanja) else None
    만든파일 = []
    만든폴더 = []
    try:
        for putanja, podaci in 파일들.items():
            부분들 = putanja.split("/")
            for 수 in range(2, len(부분들)):
                Imenik_VALUE = "/".join(부분들[:수])
                종류 = operativni_sistem.path_kind(Imenik_VALUE)
                if 종류 == 0:
                    operativni_sistem.mkdir(Imenik_VALUE)
                    만든폴더.append(Imenik_VALUE)
                elif 종류 != 2:
                    raise ValueError("Imenik_VALUE 경로에 파일이 있습니다: " + Imenik_VALUE)
            만든파일.append(putanja)
            기록쓰기(putanja, podaci)
        기록쓰기(Lista_putanja, 새목록)
    except Exception:
        for putanja in 만든파일:
            if operativni_sistem.path_kind(putanja):
                operativni_sistem.remove(putanja)
        for Imenik_VALUE in reversed(만든폴더):
            operativni_sistem.rmdir(Imenik_VALUE)
        if 이전목록 is not None:
            기록쓰기(Lista_putanja, 이전목록)
        elif operativni_sistem.path_kind(Lista_putanja):
            operativni_sistem.remove(Lista_putanja)
        raise
    print("instaliraj_VALUE 완료:", ime, 명세["version"], "→ /lib (RAM)")


def ukloniti_stavka(ime):
    stavka_Lista = 목록읽기()
    if ime not in stavka_Lista:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ime)
    for putanja, 지문값 in stavka_Lista[ime]["files"].items():
        if operativni_sistem.path_kind(putanja) != 1 or 지문(operativni_sistem.read(putanja)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + putanja)
    for putanja in stavka_Lista[ime]["files"]:
        operativni_sistem.remove(putanja)
    del stavka_Lista[ime]
    기록쓰기(Lista_putanja, json.dumps(stavka_Lista).encode())
    print("ukloniti_stavka 완료:", ime)


def koristiti(인수):
    broj_porta = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        broj_porta = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ime, msinfo32_exe in 목록읽기().items():
            print(ime, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        instaliraj_VALUE(인수[1], broj_porta)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ukloniti_stavka(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython izvor_stablo 설치기 (PyPA pip 전체가 아님)")
        print("pip install ime[==버전] [--port 8027] | pip list | pip uninstall ime")
        print("host: Alatke/Izvrši_komanda.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        koristiti(sys.argv[1:])
    except Exception as greška:
        print("komplet greška:", greška)
        sys.exit(1)
