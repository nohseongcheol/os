"""eget 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 vært 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operativsystem

Liste_sti = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VÆRDI for VÆRDI in hashlib.sha256(data).digest())


def 목록읽기():
    if operativsystem.path_kind(Liste_sti) == 0:
        return {}
    return json.loads(operativsystem.read(Liste_sti).decode("utf-8"))


def skrive_LOG(Sti, data):
    if operativsystem.write(Sti, data) != len(data):
        raise OSError(28)


def check_sti(Sti):
    if not isinstance(Sti, str) or not Sti.endswith(".py"):
        raise ValueError("Python 소스만 설치할 tal 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Sti.split("/")):
        raise ValueError("허용하지 않는 bundt Sti")
    if "\\" in Sti or any(ord(tegn_VÆRDI) < 32 or ord(tegn_VÆRDI) == 127 for tegn_VÆRDI in Sti):
        raise ValueError("잘못된 Sti 문자")
    KR = "/lib/" + Sti
    if len(KR.encode("utf-8")) > 63 or Sti in ("Dansk.py", "bundt.py"):
        raise ValueError("bundt 경로가 너무 길거나 standardværdi 라이브러리와 겹칩니다.")
    return KR


class modtage_strøm:
    def __init__(자신, slutpunkt):
        자신.slutpunkt = slutpunkt
        자신.남은자료 = b""
        자신.Kør_2 = operativsystem.ticks_ms()

    def 정확히읽기(자신, varighed_VÆRDI):
        data = bytearray()
        while len(data) < varighed_VÆRDI:
            if operativsystem.ticks_ms() - 자신.Kør_2 > 90000:
                raise ValueError("bundt 중계 svar TID_VÆRDI 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operativsystem.tcp_read(자신.slutpunkt, 512)
                except OSError as fejl:
                    if fejl.args[0] != 11:
                        raise
                    operativsystem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bundt 전송이 중간에 끝났습니다.")
            vare_TÆL = min(varighed_VÆRDI - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:vare_TÆL])
            자신.남은자료 = 자신.남은자료[vare_TÆL:]
            operativsystem.sleep_ms(0)
        return bytes(data)


def hente(anmodning, portnummer):
    if len(anmodning) > 96 or any(tegn_VÆRDI not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for tegn_VÆRDI in anmodning):
        raise ValueError("사용법: pip install Navn 또는 Navn==버전")
    slutpunkt = operativsystem.tcp_open()
    try:
        Kør_2 = operativsystem.ticks_ms()
        while True:
            try:
                operativsystem.tcp_connect(slutpunkt, "10.0.2.2", portnummer)
                break
            except OSError as fejl:
                if fejl.args[0] not in (11, 115) or operativsystem.ticks_ms() - Kør_2 > 5000:
                    raise ValueError("bundt 중계 Tilslut fejl_VÆRDI: 호스트에서 --network --pip로 실행하십시오.")
                operativsystem.sleep_ms(10)
        data = (anmodning + "\n").encode()
        while data:
            try:
                vare_TÆL = operativsystem.tcp_write(slutpunkt, data)
                if not vare_TÆL:
                    raise ValueError("bundt anmodning overføre_VÆRDI fejl_VÆRDI")
                data = data[vare_TÆL:]
            except OSError as fejl:
                if fejl.args[0] != 11:
                    raise
                operativsystem.sleep_ms(10)
                if operativsystem.ticks_ms() - Kør_2 > 10000:
                    raise ValueError("bundt anmodning overføre_VÆRDI TID_VÆRDI 초과")
        strøm_VÆRDI = modtage_strøm(slutpunkt)
        머리 = strøm_VÆRDI.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bundt overføre_VÆRDI kontraktværdi 불일치")
        varighed_VÆRDI = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if varighed_VÆRDI > 8192:
            raise ValueError("bundt 명세가 너무 큽니다.")
        명세 = json.loads(strøm_VÆRDI.정확히읽기(varighed_VÆRDI).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 kilde_træ 파일은 1~16개여야 합니다.")
        if sum(post_VÆRDI_962f286b["size"] for post_VÆRDI_962f286b in 명세["files"]) > 65536:
            raise ValueError("bundt kilde_træ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for post_VÆRDI_962f286b in 명세["files"]:
            Sti = check_sti(post_VÆRDI_962f286b["path"])
            if Sti in 파일들 or not 0 <= post_VÆRDI_962f286b["size"] <= 16384:
                raise ValueError("중복 Sti 또는 Fil Størrelse 초과")
            data = strøm_VÆRDI.정확히읽기(post_VÆRDI_962f286b["size"])
            if 지문(data) != post_VÆRDI_962f286b["sha256"]:
                raise ValueError("bundt Fil SHA-256 불일치")
            # 실행하지 않고 aktuel_vare MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), Sti, "exec")
            파일들[Sti] = data
            gc.collect()
        return 명세, 파일들
    finally:
        operativsystem.udp_close(slutpunkt)


def installér_VÆRDI(anmodning, portnummer):
    print("bundt hente:", anmodning)
    명세, 파일들 = hente(anmodning, portnummer)
    post_Liste = 목록읽기()
    Navn = 명세["name"]
    if Navn in post_Liste:
        if post_Liste[Navn]["version"] == 명세["version"]:
            for Sti, 지문값 in post_Liste[Navn]["files"].items():
                if operativsystem.path_kind(Sti) != 1 or 지문(operativsystem.read(Sti)) != 지문값:
                    raise ValueError("설치된 bundt 파일이 달라졌습니다: " + Sti)
            print("이미 설치됨:", Navn, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VÆRDI 설치하십시오.")
    for Sti in 파일들:
        if operativsystem.path_kind(Sti):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Sti)
    post_Liste[Navn] = {"version": 명세["version"], "files": {Sti: 지문(data) for Sti, data in 파일들.items()}}
    새목록 = json.dumps(post_Liste).encode()
    if len(새목록) > 16384:
        raise ValueError("bundt post_Liste Størrelse 초과")
    Forrige_Liste = operativsystem.read(Liste_sti) if operativsystem.path_kind(Liste_sti) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Sti, data in 파일들.items():
            부분들 = Sti.split("/")
            for tal in range(2, len(부분들)):
                mappe_VÆRDI = "/".join(부분들[:tal])
                종류 = operativsystem.path_kind(mappe_VÆRDI)
                if 종류 == 0:
                    operativsystem.mkdir(mappe_VÆRDI)
                    만든폴더.append(mappe_VÆRDI)
                elif 종류 != 2:
                    raise ValueError("mappe_VÆRDI 경로에 파일이 있습니다: " + mappe_VÆRDI)
            만든파일.append(Sti)
            skrive_LOG(Sti, data)
        skrive_LOG(Liste_sti, 새목록)
    except Exception:
        for Sti in 만든파일:
            if operativsystem.path_kind(Sti):
                operativsystem.remove(Sti)
        for mappe_VÆRDI in reversed(만든폴더):
            operativsystem.rmdir(mappe_VÆRDI)
        if Forrige_Liste is not None:
            skrive_LOG(Liste_sti, Forrige_Liste)
        elif operativsystem.path_kind(Liste_sti):
            operativsystem.remove(Liste_sti)
        raise
    print("installér_VÆRDI 완료:", Navn, 명세["version"], "→ /lib (RAM)")


def fjerne_post(Navn):
    post_Liste = 목록읽기()
    if Navn not in post_Liste:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Navn)
    for Sti, 지문값 in post_Liste[Navn]["files"].items():
        if operativsystem.path_kind(Sti) != 1 or 지문(operativsystem.read(Sti)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Sti)
    for Sti in post_Liste[Navn]["files"]:
        operativsystem.remove(Sti)
    del post_Liste[Navn]
    skrive_LOG(Liste_sti, json.dumps(post_Liste).encode())
    print("fjerne_post 완료:", Navn)


def Kør_2(Argumenter):
    portnummer = 8027
    if len(Argumenter) >= 2 and Argumenter[-2] == "--port":
        portnummer = int(Argumenter[-1])
        Argumenter = Argumenter[:-2]
    if Argumenter == ["list"]:
        for Navn, msinfo32_exe in 목록읽기().items():
            print(Navn, msinfo32_exe["version"])
    elif len(Argumenter) == 2 and Argumenter[0] == "install":
        installér_VÆRDI(Argumenter[1], portnummer)
    elif len(Argumenter) == 2 and Argumenter[0] == "uninstall":
        fjerne_post(Argumenter[1])
    elif not Argumenter or Argumenter in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython kilde_træ 설치기 (PyPA pip 전체가 아님)")
        print("pip install Navn[==버전] [--port 8027] | pip list | pip uninstall Navn")
        print("vært: Værktøjer/Udfør_kommando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Kør_2(sys.argv[1:])
    except Exception as fejl:
        print("bundt fejl:", fejl)
        sys.exit(1)
