"""eget 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 värd 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operativsystem

ange_väg = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % värde for värde in hashlib.sha256(data).digest())


def läsa_ange():
    if operativsystem.path_kind(ange_väg) == 0:
        return {}
    return json.loads(operativsystem.read(ange_väg).decode("utf-8"))


def skriva_LOG(sökväg_2, data):
    if operativsystem.write(sökväg_2, data) != len(data):
        raise OSError(28)


def check_väg(sökväg_2):
    if not isinstance(sökväg_2, str) or not sökväg_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 nummer 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in sökväg_2.split("/")):
        raise ValueError("허용하지 않는 bunt sökväg_2")
    if "\\" in sökväg_2 or any(ord(tecken_värde) < 32 or ord(tecken_värde) == 127 for tecken_värde in sökväg_2):
        raise ValueError("잘못된 sökväg_2 문자")
    RESULTAT = "/lib/" + sökväg_2
    if len(RESULTAT.encode("utf-8")) > 63 or sökväg_2 in ("Svenska.py", "bunt.py"):
        raise ValueError("bunt 경로가 너무 길거나 standardvärde 라이브러리와 겹칩니다.")
    return RESULTAT


class få_flöde:
    def __init__(자신, deltagare):
        자신.deltagare = deltagare
        자신.남은자료 = b""
        자신.Kör = operativsystem.ticks_ms()

    def 정확히읽기(자신, längd_värde):
        data = bytearray()
        while len(data) < längd_värde:
            if operativsystem.ticks_ms() - 자신.Kör > 90000:
                raise ValueError("bunt 중계 svara tid_värde 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operativsystem.tcp_read(자신.deltagare, 512)
                except OSError as fel:
                    if fel.args[0] != 11:
                        raise
                    operativsystem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bunt 전송이 중간에 끝났습니다.")
            objekt_ANTAL = min(längd_värde - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:objekt_ANTAL])
            자신.남은자료 = 자신.남은자료[objekt_ANTAL:]
            operativsystem.sleep_ms(0)
        return bytes(data)


def hämtning(begäran, portnummer):
    if len(begäran) > 96 or any(tecken_värde not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for tecken_värde in begäran):
        raise ValueError("사용법: pip install Namn 또는 Namn==버전")
    deltagare = operativsystem.tcp_open()
    try:
        Kör = operativsystem.ticks_ms()
        while True:
            try:
                operativsystem.tcp_connect(deltagare, "10.0.2.2", portnummer)
                break
            except OSError as fel:
                if fel.args[0] not in (11, 115) or operativsystem.ticks_ms() - Kör > 5000:
                    raise ValueError("bunt 중계 Anslut fel_värde: 호스트에서 --network --pip로 실행하십시오.")
                operativsystem.sleep_ms(10)
        data = (begäran + "\n").encode()
        while data:
            try:
                objekt_ANTAL = operativsystem.tcp_write(deltagare, data)
                if not objekt_ANTAL:
                    raise ValueError("bunt begäran Överför_värde fel_värde")
                data = data[objekt_ANTAL:]
            except OSError as fel:
                if fel.args[0] != 11:
                    raise
                operativsystem.sleep_ms(10)
                if operativsystem.ticks_ms() - Kör > 10000:
                    raise ValueError("bunt begäran Överför_värde tid_värde 초과")
        flöde_värde = få_flöde(deltagare)
        머리 = flöde_värde.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bunt Överför_värde kontraktsvärde 불일치")
        längd_värde = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if längd_värde > 8192:
            raise ValueError("bunt 명세가 너무 큽니다.")
        명세 = json.loads(flöde_värde.정확히읽기(längd_värde).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 källa_träd 파일은 1~16개여야 합니다.")
        if sum(post_värde["size"] for post_värde in 명세["files"]) > 65536:
            raise ValueError("bunt källa_träd 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for post_värde in 명세["files"]:
            sökväg_2 = check_väg(post_värde["path"])
            if sökväg_2 in 파일들 or not 0 <= post_värde["size"] <= 16384:
                raise ValueError("중복 sökväg_2 또는 filnamn Storlek 초과")
            data = flöde_värde.정확히읽기(post_värde["size"])
            if 지문(data) != post_värde["sha256"]:
                raise ValueError("bunt filnamn SHA-256 불일치")
            # 실행하지 않고 aktuellt_objekt MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), sökväg_2, "exec")
            파일들[sökväg_2] = data
            gc.collect()
        return 명세, 파일들
    finally:
        operativsystem.udp_close(deltagare)


def installera_värde(begäran, portnummer):
    print("bunt hämtning:", begäran)
    명세, 파일들 = hämtning(begäran, portnummer)
    post_ange = läsa_ange()
    Namn = 명세["name"]
    if Namn in post_ange:
        if post_ange[Namn]["version"] == 명세["version"]:
            for sökväg_2, 지문값 in post_ange[Namn]["files"].items():
                if operativsystem.path_kind(sökväg_2) != 1 or 지문(operativsystem.read(sökväg_2)) != 지문값:
                    raise ValueError("설치된 bunt 파일이 달라졌습니다: " + sökväg_2)
            print("이미 설치됨:", Namn, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_värde 설치하십시오.")
    for sökväg_2 in 파일들:
        if operativsystem.path_kind(sökväg_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + sökväg_2)
    post_ange[Namn] = {"version": 명세["version"], "files": {sökväg_2: 지문(data) for sökväg_2, data in 파일들.items()}}
    새목록 = json.dumps(post_ange).encode()
    if len(새목록) > 16384:
        raise ValueError("bunt post_ange Storlek 초과")
    Föregående_ange = operativsystem.read(ange_väg) if operativsystem.path_kind(ange_väg) else None
    만든파일 = []
    만든폴더 = []
    try:
        for sökväg_2, data in 파일들.items():
            부분들 = sökväg_2.split("/")
            for nummer in range(2, len(부분들)):
                Katalog_värde = "/".join(부분들[:nummer])
                variant_värde = operativsystem.path_kind(Katalog_värde)
                if variant_värde == 0:
                    operativsystem.mkdir(Katalog_värde)
                    만든폴더.append(Katalog_värde)
                elif variant_värde != 2:
                    raise ValueError("Katalog_värde 경로에 파일이 있습니다: " + Katalog_värde)
            만든파일.append(sökväg_2)
            skriva_LOG(sökväg_2, data)
        skriva_LOG(ange_väg, 새목록)
    except Exception:
        for sökväg_2 in 만든파일:
            if operativsystem.path_kind(sökväg_2):
                operativsystem.remove(sökväg_2)
        for Katalog_värde in reversed(만든폴더):
            operativsystem.rmdir(Katalog_värde)
        if Föregående_ange is not None:
            skriva_LOG(ange_väg, Föregående_ange)
        elif operativsystem.path_kind(ange_väg):
            operativsystem.remove(ange_väg)
        raise
    print("installera_värde 완료:", Namn, 명세["version"], "→ /lib (RAM)")


def ta_bort_post(Namn):
    post_ange = läsa_ange()
    if Namn not in post_ange:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Namn)
    for sökväg_2, 지문값 in post_ange[Namn]["files"].items():
        if operativsystem.path_kind(sökväg_2) != 1 or 지문(operativsystem.read(sökväg_2)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + sökväg_2)
    for sökväg_2 in post_ange[Namn]["files"]:
        operativsystem.remove(sökväg_2)
    del post_ange[Namn]
    skriva_LOG(ange_väg, json.dumps(post_ange).encode())
    print("ta_bort_post 완료:", Namn)


def Kör(argument):
    portnummer = 8027
    if len(argument) >= 2 and argument[-2] == "--port":
        portnummer = int(argument[-1])
        argument = argument[:-2]
    if argument == ["list"]:
        for Namn, msinfo32_exe in läsa_ange().items():
            print(Namn, msinfo32_exe["version"])
    elif len(argument) == 2 and argument[0] == "install":
        installera_värde(argument[1], portnummer)
    elif len(argument) == 2 and argument[0] == "uninstall":
        ta_bort_post(argument[1])
    elif not argument or argument in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython källa_träd 설치기 (PyPA pip 전체가 아님)")
        print("pip install Namn[==버전] [--port 8027] | pip list | pip uninstall Namn")
        print("värd: verktyg/köra_kommando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Kör(sys.argv[1:])
    except Exception as fel:
        print("bunt fel:", fel)
        sys.exit(1)
