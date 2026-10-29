"""eget 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 vert 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operativsystem

Liste_bane = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VERDI for VERDI in hashlib.sha256(data).digest())


def 목록읽기():
    if operativsystem.path_kind(Liste_bane) == 0:
        return {}
    return json.loads(operativsystem.read(Liste_bane).decode("utf-8"))


def skrive_LOG(Sti, data):
    if operativsystem.write(Sti, data) != len(data):
        raise OSError(28)


def sjekk_bane(Sti):
    if not isinstance(Sti, str) or not Sti.endswith(".py"):
        raise ValueError("Python 소스만 설치할 nummer 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Sti.split("/")):
        raise ValueError("허용하지 않는 bunt Sti")
    if "\\" in Sti or any(ord(tegn_VERDI) < 32 or ord(tegn_VERDI) == 127 for tegn_VERDI in Sti):
        raise ValueError("잘못된 Sti 문자")
    KR = "/lib/" + Sti
    if len(KR.encode("utf-8")) > 63 or Sti in ("norsk.py", "bunt.py"):
        raise ValueError("bunt 경로가 너무 길거나 standardverdi 라이브러리와 겹칩니다.")
    return KR


class motta_strøm:
    def __init__(자신, deltaker):
        자신.deltaker = deltaker
        자신.남은자료 = b""
        자신.Kjør_2 = operativsystem.ticks_ms()

    def 정확히읽기(자신, lengde_VERDI):
        data = bytearray()
        while len(data) < lengde_VERDI:
            if operativsystem.ticks_ms() - 자신.Kjør_2 > 90000:
                raise ValueError("bunt 중계 svar TID_VERDI 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operativsystem.tcp_read(자신.deltaker, 512)
                except OSError as feil:
                    if feil.args[0] != 11:
                        raise
                    operativsystem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bunt 전송이 중간에 끝났습니다.")
            vare_ANTALL = min(lengde_VERDI - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:vare_ANTALL])
            자신.남은자료 = 자신.남은자료[vare_ANTALL:]
            operativsystem.sleep_ms(0)
        return bytes(data)


def last_ned(forespørsel, portnummer):
    if len(forespørsel) > 96 or any(tegn_VERDI not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for tegn_VERDI in forespørsel):
        raise ValueError("사용법: pip install Navn 또는 Navn==버전")
    deltaker = operativsystem.tcp_open()
    try:
        Kjør_2 = operativsystem.ticks_ms()
        while True:
            try:
                operativsystem.tcp_connect(deltaker, "10.0.2.2", portnummer)
                break
            except OSError as feil:
                if feil.args[0] not in (11, 115) or operativsystem.ticks_ms() - Kjør_2 > 5000:
                    raise ValueError("bunt 중계 Koble_til feil_VERDI: 호스트에서 --network --pip로 실행하십시오.")
                operativsystem.sleep_ms(10)
        data = (forespørsel + "\n").encode()
        while data:
            try:
                vare_ANTALL = operativsystem.tcp_write(deltaker, data)
                if not vare_ANTALL:
                    raise ValueError("bunt forespørsel overføre_VERDI feil_VERDI")
                data = data[vare_ANTALL:]
            except OSError as feil:
                if feil.args[0] != 11:
                    raise
                operativsystem.sleep_ms(10)
                if operativsystem.ticks_ms() - Kjør_2 > 10000:
                    raise ValueError("bunt forespørsel overføre_VERDI TID_VERDI 초과")
        strøm_VERDI = motta_strøm(deltaker)
        머리 = strøm_VERDI.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bunt overføre_VERDI kontraktverdi 불일치")
        lengde_VERDI = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if lengde_VERDI > 8192:
            raise ValueError("bunt 명세가 너무 큽니다.")
        명세 = json.loads(strøm_VERDI.정확히읽기(lengde_VERDI).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 kilde_tre 파일은 1~16개여야 합니다.")
        if sum(oppføring_VERDI["size"] for oppføring_VERDI in 명세["files"]) > 65536:
            raise ValueError("bunt kilde_tre 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for oppføring_VERDI in 명세["files"]:
            Sti = sjekk_bane(oppføring_VERDI["path"])
            if Sti in 파일들 or not 0 <= oppføring_VERDI["size"] <= 16384:
                raise ValueError("중복 Sti 또는 Fil Størrelse 초과")
            data = strøm_VERDI.정확히읽기(oppføring_VERDI["size"])
            if 지문(data) != oppføring_VERDI["sha256"]:
                raise ValueError("bunt Fil SHA-256 불일치")
            # 실행하지 않고 betalt_vare MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), Sti, "exec")
            파일들[Sti] = data
            gc.collect()
        return 명세, 파일들
    finally:
        operativsystem.udp_close(deltaker)


def installer_VERDI(forespørsel, portnummer):
    print("bunt last_ned:", forespørsel)
    명세, 파일들 = last_ned(forespørsel, portnummer)
    oppføring_Liste = 목록읽기()
    Navn = 명세["name"]
    if Navn in oppføring_Liste:
        if oppføring_Liste[Navn]["version"] == 명세["version"]:
            for Sti, 지문값 in oppføring_Liste[Navn]["files"].items():
                if operativsystem.path_kind(Sti) != 1 or 지문(operativsystem.read(Sti)) != 지문값:
                    raise ValueError("설치된 bunt 파일이 달라졌습니다: " + Sti)
            print("이미 설치됨:", Navn, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 TILBAKE_VERDI 설치하십시오.")
    for Sti in 파일들:
        if operativsystem.path_kind(Sti):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Sti)
    oppføring_Liste[Navn] = {"version": 명세["version"], "files": {Sti: 지문(data) for Sti, data in 파일들.items()}}
    새목록 = json.dumps(oppføring_Liste).encode()
    if len(새목록) > 16384:
        raise ValueError("bunt oppføring_Liste Størrelse 초과")
    Forrige_Liste = operativsystem.read(Liste_bane) if operativsystem.path_kind(Liste_bane) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Sti, data in 파일들.items():
            부분들 = Sti.split("/")
            for nummer in range(2, len(부분들)):
                katalog_VERDI = "/".join(부분들[:nummer])
                종류 = operativsystem.path_kind(katalog_VERDI)
                if 종류 == 0:
                    operativsystem.mkdir(katalog_VERDI)
                    만든폴더.append(katalog_VERDI)
                elif 종류 != 2:
                    raise ValueError("katalog_VERDI 경로에 파일이 있습니다: " + katalog_VERDI)
            만든파일.append(Sti)
            skrive_LOG(Sti, data)
        skrive_LOG(Liste_bane, 새목록)
    except Exception:
        for Sti in 만든파일:
            if operativsystem.path_kind(Sti):
                operativsystem.remove(Sti)
        for katalog_VERDI in reversed(만든폴더):
            operativsystem.rmdir(katalog_VERDI)
        if Forrige_Liste is not None:
            skrive_LOG(Liste_bane, Forrige_Liste)
        elif operativsystem.path_kind(Liste_bane):
            operativsystem.remove(Liste_bane)
        raise
    print("installer_VERDI 완료:", Navn, 명세["version"], "→ /lib (RAM)")


def fjerne_oppføring(Navn):
    oppføring_Liste = 목록읽기()
    if Navn not in oppføring_Liste:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Navn)
    for Sti, 지문값 in oppføring_Liste[Navn]["files"].items():
        if operativsystem.path_kind(Sti) != 1 or 지문(operativsystem.read(Sti)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Sti)
    for Sti in oppføring_Liste[Navn]["files"]:
        operativsystem.remove(Sti)
    del oppføring_Liste[Navn]
    skrive_LOG(Liste_bane, json.dumps(oppføring_Liste).encode())
    print("fjerne_oppføring 완료:", Navn)


def Kjør_2(Argumenter):
    portnummer = 8027
    if len(Argumenter) >= 2 and Argumenter[-2] == "--port":
        portnummer = int(Argumenter[-1])
        Argumenter = Argumenter[:-2]
    if Argumenter == ["list"]:
        for Navn, msinfo32_exe in 목록읽기().items():
            print(Navn, msinfo32_exe["version"])
    elif len(Argumenter) == 2 and Argumenter[0] == "install":
        installer_VERDI(Argumenter[1], portnummer)
    elif len(Argumenter) == 2 and Argumenter[0] == "uninstall":
        fjerne_oppføring(Argumenter[1])
    elif not Argumenter or Argumenter in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython kilde_tre 설치기 (PyPA pip 전체가 아님)")
        print("pip install Navn[==버전] [--port 8027] | pip list | pip uninstall Navn")
        print("vert: Verktøy/Utfør_kommando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Kjør_2(sys.argv[1:])
    except Exception as feil:
        print("bunt feil:", feil)
        sys.exit(1)
