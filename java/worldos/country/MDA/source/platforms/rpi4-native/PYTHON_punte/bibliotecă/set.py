"""propriu 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 gazdă 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistem_de_operare

Listă_cale = "/lib/.pip.json"


def 지문(date):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(date).digest())


def 목록읽기():
    if sistem_de_operare.path_kind(Listă_cale) == 0:
        return {}
    return json.loads(sistem_de_operare.read(Listă_cale).decode("utf-8"))


def scriere_LOG(Cale, date):
    if sistem_de_operare.write(Cale, date) != len(date):
        raise OSError(28)


def verifica_cale(Cale):
    if not isinstance(Cale, str) or not Cale.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Cale.split("/")):
        raise ValueError("허용하지 않는 set Cale")
    if "\\" in Cale or any(ord(caracter_VALUE) < 32 or ord(caracter_VALUE) == 127 for caracter_VALUE in Cale):
        raise ValueError("잘못된 Cale 문자")
    KR = "/lib/" + Cale
    if len(KR.encode("utf-8")) > 63 or Cale in ("Română.py", "set.py"):
        raise ValueError("set 경로가 너무 길거나 valoare_implicită 라이브러리와 겹칩니다.")
    return KR


class primi_flux:
    def __init__(자신, participant):
        자신.participant = participant
        자신.남은자료 = b""
        자신.Pornește = sistem_de_operare.ticks_ms()

    def 정확히읽기(자신, lungime_VALUE):
        date = bytearray()
        while len(date) < lungime_VALUE:
            if sistem_de_operare.ticks_ms() - 자신.Pornește > 90000:
                raise ValueError("set 중계 replică oră_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistem_de_operare.tcp_read(자신.participant, 512)
                except OSError as eroare:
                    if eroare.args[0] != 11:
                        raise
                    sistem_de_operare.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("set 전송이 중간에 끝났습니다.")
            element_COUNT = min(lungime_VALUE - len(date), len(자신.남은자료))
            date.extend(자신.남은자료[:element_COUNT])
            자신.남은자료 = 자신.남은자료[element_COUNT:]
            sistem_de_operare.sleep_ms(0)
        return bytes(date)


def descărca(cerere, număr_port):
    if len(cerere) > 96 or any(caracter_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for caracter_VALUE in cerere):
        raise ValueError("사용법: pip install Nume 또는 Nume==버전")
    participant = sistem_de_operare.tcp_open()
    try:
        Pornește = sistem_de_operare.ticks_ms()
        while True:
            try:
                sistem_de_operare.tcp_connect(participant, "10.0.2.2", număr_port)
                break
            except OSError as eroare:
                if eroare.args[0] not in (11, 115) or sistem_de_operare.ticks_ms() - Pornește > 5000:
                    raise ValueError("set 중계 Conectează eroare_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                sistem_de_operare.sleep_ms(10)
        date = (cerere + "\n").encode()
        while date:
            try:
                element_COUNT = sistem_de_operare.tcp_write(participant, date)
                if not element_COUNT:
                    raise ValueError("set cerere Transfer_VALUE eroare_VALUE")
                date = date[element_COUNT:]
            except OSError as eroare:
                if eroare.args[0] != 11:
                    raise
                sistem_de_operare.sleep_ms(10)
                if sistem_de_operare.ticks_ms() - Pornește > 10000:
                    raise ValueError("set cerere Transfer_VALUE oră_VALUE 초과")
        flux_VALUE = primi_flux(participant)
        머리 = flux_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("set Transfer_VALUE caz_VALUE 불일치")
        lungime_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if lungime_VALUE > 8192:
            raise ValueError("set 명세가 너무 큽니다.")
        명세 = json.loads(flux_VALUE.정확히읽기(lungime_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 sursă_arborescență 파일은 1~16개여야 합니다.")
        if sum(intrare_VALUE["size"] for intrare_VALUE in 명세["files"]) > 65536:
            raise ValueError("set sursă_arborescență 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for intrare_VALUE in 명세["files"]:
            Cale = verifica_cale(intrare_VALUE["path"])
            if Cale in 파일들 or not 0 <= intrare_VALUE["size"] <= 16384:
                raise ValueError("중복 Cale 또는 Fișier Mărime 초과")
            date = flux_VALUE.정확히읽기(intrare_VALUE["size"])
            if 지문(date) != intrare_VALUE["sha256"]:
                raise ValueError("set Fișier SHA-256 불일치")
            # 실행하지 않고 curent_element MicroPython의 문법으로 먼저 검사한다.
            compile(date.decode("utf-8"), Cale, "exec")
            파일들[Cale] = date
            gc.collect()
        return 명세, 파일들
    finally:
        sistem_de_operare.udp_close(participant)


def instala_VALUE(cerere, număr_port):
    print("set descărca:", cerere)
    명세, 파일들 = descărca(cerere, număr_port)
    intrare_Listă = 목록읽기()
    Nume = 명세["name"]
    if Nume in intrare_Listă:
        if intrare_Listă[Nume]["version"] == 명세["version"]:
            for Cale, 지문값 in intrare_Listă[Nume]["files"].items():
                if sistem_de_operare.path_kind(Cale) != 1 or 지문(sistem_de_operare.read(Cale)) != 지문값:
                    raise ValueError("설치된 set 파일이 달라졌습니다: " + Cale)
            print("이미 설치됨:", Nume, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ÎNAPOI_VALUE 설치하십시오.")
    for Cale in 파일들:
        if sistem_de_operare.path_kind(Cale):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Cale)
    intrare_Listă[Nume] = {"version": 명세["version"], "files": {Cale: 지문(date) for Cale, date in 파일들.items()}}
    새목록 = json.dumps(intrare_Listă).encode()
    if len(새목록) > 16384:
        raise ValueError("set intrare_Listă Mărime 초과")
    Anteriorul_Listă = sistem_de_operare.read(Listă_cale) if sistem_de_operare.path_kind(Listă_cale) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Cale, date in 파일들.items():
            부분들 = Cale.split("/")
            for 수 in range(2, len(부분들)):
                Director_VALUE = "/".join(부분들[:수])
                종류 = sistem_de_operare.path_kind(Director_VALUE)
                if 종류 == 0:
                    sistem_de_operare.mkdir(Director_VALUE)
                    만든폴더.append(Director_VALUE)
                elif 종류 != 2:
                    raise ValueError("Director_VALUE 경로에 파일이 있습니다: " + Director_VALUE)
            만든파일.append(Cale)
            scriere_LOG(Cale, date)
        scriere_LOG(Listă_cale, 새목록)
    except Exception:
        for Cale in 만든파일:
            if sistem_de_operare.path_kind(Cale):
                sistem_de_operare.remove(Cale)
        for Director_VALUE in reversed(만든폴더):
            sistem_de_operare.rmdir(Director_VALUE)
        if Anteriorul_Listă is not None:
            scriere_LOG(Listă_cale, Anteriorul_Listă)
        elif sistem_de_operare.path_kind(Listă_cale):
            sistem_de_operare.remove(Listă_cale)
        raise
    print("instala_VALUE 완료:", Nume, 명세["version"], "→ /lib (RAM)")


def elimina_intrare(Nume):
    intrare_Listă = 목록읽기()
    if Nume not in intrare_Listă:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nume)
    for Cale, 지문값 in intrare_Listă[Nume]["files"].items():
        if sistem_de_operare.path_kind(Cale) != 1 or 지문(sistem_de_operare.read(Cale)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Cale)
    for Cale in intrare_Listă[Nume]["files"]:
        sistem_de_operare.remove(Cale)
    del intrare_Listă[Nume]
    scriere_LOG(Listă_cale, json.dumps(intrare_Listă).encode())
    print("elimina_intrare 완료:", Nume)


def Pornește(Argumente):
    număr_port = 8027
    if len(Argumente) >= 2 and Argumente[-2] == "--port":
        număr_port = int(Argumente[-1])
        Argumente = Argumente[:-2]
    if Argumente == ["list"]:
        for Nume, msinfo32_exe in 목록읽기().items():
            print(Nume, msinfo32_exe["version"])
    elif len(Argumente) == 2 and Argumente[0] == "install":
        instala_VALUE(Argumente[1], număr_port)
    elif len(Argumente) == 2 and Argumente[0] == "uninstall":
        elimina_intrare(Argumente[1])
    elif not Argumente or Argumente in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython sursă_arborescență 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nume[==버전] [--port 8027] | pip list | pip uninstall Nume")
        print("gazdă: Instrumente/executa_comandă.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Pornește(sys.argv[1:])
    except Exception as eroare:
        print("set eroare:", eroare)
        sys.exit(1)
