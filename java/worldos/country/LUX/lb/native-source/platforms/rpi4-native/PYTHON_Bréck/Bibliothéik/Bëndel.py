"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as Betribssystem

Lëscht_Wee = "/lib/.pip.json"


def 지문(Daten):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(Daten).digest())


def 목록읽기():
    if Betribssystem.path_kind(Lëscht_Wee) == 0:
        return {}
    return json.loads(Betribssystem.read(Lëscht_Wee).decode("utf-8"))


def schreiwen_LOG(Wee, Daten):
    if Betribssystem.write(Wee, Daten) != len(Daten):
        raise OSError(28)


def Scheck_Wee(Wee):
    if not isinstance(Wee, str) or not Wee.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Wee.split("/")):
        raise ValueError("허용하지 않는 Bëndel Wee")
    if "\\" in Wee or any(ord(Zeechen_VALUE) < 32 or ord(Zeechen_VALUE) == 127 for Zeechen_VALUE in Wee):
        raise ValueError("잘못된 Wee 문자")
    Mooss = "/lib/" + Wee
    if len(Mooss.encode("utf-8")) > 63 or Wee in ("한국어.py", "Bëndel.py"):
        raise ValueError("Bëndel 경로가 너무 길거나 Standardwäert 라이브러리와 겹칩니다.")
    return Mooss


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Laf = Betribssystem.ticks_ms()

    def 정확히읽기(자신, Längt_VALUE):
        Daten = bytearray()
        while len(Daten) < Längt_VALUE:
            if Betribssystem.ticks_ms() - 자신.Laf > 90000:
                raise ValueError("Bëndel 중계 äntweren TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = Betribssystem.tcp_read(자신.종단, 512)
                except OSError as Feeler:
                    if Feeler.args[0] != 11:
                        raise
                    Betribssystem.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("Bëndel 전송이 중간에 끝났습니다.")
            Element_COUNT = min(Längt_VALUE - len(Daten), len(자신.남은자료))
            Daten.extend(자신.남은자료[:Element_COUNT])
            자신.남은자료 = 자신.남은자료[Element_COUNT:]
            Betribssystem.sleep_ms(0)
        return bytes(Daten)


def Download(요청, 접속번호):
    if len(요청) > 96 or any(Zeechen_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for Zeechen_VALUE in 요청):
        raise ValueError("사용법: pip install Numm 또는 Numm==버전")
    종단 = Betribssystem.tcp_open()
    try:
        Laf = Betribssystem.ticks_ms()
        while True:
            try:
                Betribssystem.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Feeler:
                if Feeler.args[0] not in (11, 115) or Betribssystem.ticks_ms() - Laf > 5000:
                    raise ValueError("Bëndel 중계 Verbannen Feeler_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                Betribssystem.sleep_ms(10)
        Daten = (요청 + "\n").encode()
        while Daten:
            try:
                Element_COUNT = Betribssystem.tcp_write(종단, Daten)
                if not Element_COUNT:
                    raise ValueError("Bëndel 요청 Transfer_VALUE Feeler_VALUE")
                Daten = Daten[Element_COUNT:]
            except OSError as Feeler:
                if Feeler.args[0] != 11:
                    raise
                Betribssystem.sleep_ms(10)
                if Betribssystem.ticks_ms() - Laf > 10000:
                    raise ValueError("Bëndel 요청 Transfer_VALUE TIME_VALUE 초과")
        Stream_VALUE = 수신흐름(종단)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("Bëndel Transfer_VALUE Job_VALUE 불일치")
        Längt_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if Längt_VALUE > 8192:
            raise ValueError("Bëndel 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(Längt_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 Quell_Bamstruktur 파일은 1~16개여야 합니다.")
        if sum(Agab_VALUE["size"] for Agab_VALUE in 명세["files"]) > 65536:
            raise ValueError("Bëndel Quell_Bamstruktur 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for Agab_VALUE in 명세["files"]:
            Wee = Scheck_Wee(Agab_VALUE["path"])
            if Wee in 파일들 or not 0 <= Agab_VALUE["size"] <= 16384:
                raise ValueError("중복 Wee 또는 Fichier d_Gréisst_veränneren 초과")
            Daten = Stream_VALUE.정확히읽기(Agab_VALUE["size"])
            if 지문(Daten) != Agab_VALUE["sha256"]:
                raise ValueError("Bëndel Fichier SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(Daten.decode("utf-8"), Wee, "exec")
            파일들[Wee] = Daten
            gc.collect()
        return 명세, 파일들
    finally:
        Betribssystem.udp_close(종단)


def installéieren_VALUE(요청, 접속번호):
    print("Bëndel Download:", 요청)
    명세, 파일들 = Download(요청, 접속번호)
    Agab_Lëscht = 목록읽기()
    Numm = 명세["name"]
    if Numm in Agab_Lëscht:
        if Agab_Lëscht[Numm]["version"] == 명세["version"]:
            for Wee, 지문값 in Agab_Lëscht[Numm]["files"].items():
                if Betribssystem.path_kind(Wee) != 1 or 지문(Betribssystem.read(Wee)) != 지문값:
                    raise ValueError("설치된 Bëndel 파일이 달라졌습니다: " + Wee)
            print("이미 설치됨:", Numm, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Zeréck_VALUE 설치하십시오.")
    for Wee in 파일들:
        if Betribssystem.path_kind(Wee):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Wee)
    Agab_Lëscht[Numm] = {"version": 명세["version"], "files": {Wee: 지문(Daten) for Wee, Daten in 파일들.items()}}
    새목록 = json.dumps(Agab_Lëscht).encode()
    if len(새목록) > 16384:
        raise ValueError("Bëndel Agab_Lëscht d_Gréisst_veränneren 초과")
    이전목록 = Betribssystem.read(Lëscht_Wee) if Betribssystem.path_kind(Lëscht_Wee) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Wee, Daten in 파일들.items():
            부분들 = Wee.split("/")
            for 수 in range(2, len(부분들)):
                Verzeechnes_VALUE = "/".join(부분들[:수])
                종류 = Betribssystem.path_kind(Verzeechnes_VALUE)
                if 종류 == 0:
                    Betribssystem.mkdir(Verzeechnes_VALUE)
                    만든폴더.append(Verzeechnes_VALUE)
                elif 종류 != 2:
                    raise ValueError("Verzeechnes_VALUE 경로에 파일이 있습니다: " + Verzeechnes_VALUE)
            만든파일.append(Wee)
            schreiwen_LOG(Wee, Daten)
        schreiwen_LOG(Lëscht_Wee, 새목록)
    except Exception:
        for Wee in 만든파일:
            if Betribssystem.path_kind(Wee):
                Betribssystem.remove(Wee)
        for Verzeechnes_VALUE in reversed(만든폴더):
            Betribssystem.rmdir(Verzeechnes_VALUE)
        if 이전목록 is not None:
            schreiwen_LOG(Lëscht_Wee, 이전목록)
        elif Betribssystem.path_kind(Lëscht_Wee):
            Betribssystem.remove(Lëscht_Wee)
        raise
    print("installéieren_VALUE 완료:", Numm, 명세["version"], "→ /lib (RAM)")


def ewechhuelen_Agab(Numm):
    Agab_Lëscht = 목록읽기()
    if Numm not in Agab_Lëscht:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Numm)
    for Wee, 지문값 in Agab_Lëscht[Numm]["files"].items():
        if Betribssystem.path_kind(Wee) != 1 or 지문(Betribssystem.read(Wee)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Wee)
    for Wee in Agab_Lëscht[Numm]["files"]:
        Betribssystem.remove(Wee)
    del Agab_Lëscht[Numm]
    schreiwen_LOG(Lëscht_Wee, json.dumps(Agab_Lëscht).encode())
    print("ewechhuelen_Agab 완료:", Numm)


def Laf(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Numm, msinfo32_exe in 목록읽기().items():
            print(Numm, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        installéieren_VALUE(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ewechhuelen_Agab(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython Quell_Bamstruktur 설치기 (PyPA pip 전체가 아님)")
        print("pip install Numm[==버전] [--port 8027] | pip list | pip uninstall Numm")
        print("Host: Tools/ausféieren_Befeel.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Laf(sys.argv[1:])
    except Exception as Feeler:
        print("Bëndel Feeler:", Feeler)
        sys.exit(1)
