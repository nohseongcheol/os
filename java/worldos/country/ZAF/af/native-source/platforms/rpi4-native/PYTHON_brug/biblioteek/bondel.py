"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 hou 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as bedryfstelsel

Lys_pad = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if bedryfstelsel.path_kind(Lys_pad) == 0:
        return {}
    return json.loads(bedryfstelsel.read(Lys_pad).decode("utf-8"))


def skryf_LOG(Pad, data):
    if bedryfstelsel.write(Pad, data) != len(data):
        raise OSError(28)


def tjek_pad(Pad):
    if not isinstance(Pad, str) or not Pad.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Pad.split("/")):
        raise ValueError("허용하지 않는 bondel Pad")
    if "\\" in Pad or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in Pad):
        raise ValueError("잘못된 Pad 문자")
    maatreël = "/lib/" + Pad
    if len(maatreël.encode("utf-8")) > 63 or Pad in ("한국어.py", "bondel.py"):
        raise ValueError("bondel 경로가 너무 길거나 verstekwaarde 라이브러리와 겹칩니다.")
    return maatreël


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Loop = bedryfstelsel.ticks_ms()

    def 정확히읽기(자신, lengte_VALUE):
        data = bytearray()
        while len(data) < lengte_VALUE:
            if bedryfstelsel.ticks_ms() - 자신.Loop > 90000:
                raise ValueError("bondel 중계 antwoord tyd_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = bedryfstelsel.tcp_read(자신.종단, 512)
                except OSError as Fout:
                    if Fout.args[0] != 11:
                        raise
                    bedryfstelsel.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("bondel 전송이 중간에 끝났습니다.")
            item_COUNT = min(lengte_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:item_COUNT])
            자신.남은자료 = 자신.남은자료[item_COUNT:]
            bedryfstelsel.sleep_ms(0)
        return bytes(data)


def aflaai(요청, 접속번호):
    if len(요청) > 96 or any(karakter_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karakter_VALUE in 요청):
        raise ValueError("사용법: pip install Naam 또는 Naam==버전")
    종단 = bedryfstelsel.tcp_open()
    try:
        Loop = bedryfstelsel.ticks_ms()
        while True:
            try:
                bedryfstelsel.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Fout:
                if Fout.args[0] not in (11, 115) or bedryfstelsel.ticks_ms() - Loop > 5000:
                    raise ValueError("bondel 중계 Koppel faling_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                bedryfstelsel.sleep_ms(10)
        data = (요청 + "\n").encode()
        while data:
            try:
                item_COUNT = bedryfstelsel.tcp_write(종단, data)
                if not item_COUNT:
                    raise ValueError("bondel 요청 oordra_VALUE faling_VALUE")
                data = data[item_COUNT:]
            except OSError as Fout:
                if Fout.args[0] != 11:
                    raise
                bedryfstelsel.sleep_ms(10)
                if bedryfstelsel.ticks_ms() - Loop > 10000:
                    raise ValueError("bondel 요청 oordra_VALUE tyd_VALUE 초과")
        Stream_VALUE = 수신흐름(종단)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("bondel oordra_VALUE saak_VALUE 불일치")
        lengte_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if lengte_VALUE > 8192:
            raise ValueError("bondel 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(lengte_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 bron_boom 파일은 1~16개여야 합니다.")
        if sum(inskrywing_VALUE["size"] for inskrywing_VALUE in 명세["files"]) > 65536:
            raise ValueError("bondel bron_boom 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for inskrywing_VALUE in 명세["files"]:
            Pad = tjek_pad(inskrywing_VALUE["path"])
            if Pad in 파일들 or not 0 <= inskrywing_VALUE["size"] <= 16384:
                raise ValueError("중복 Pad 또는 Lêer Grootte 초과")
            data = Stream_VALUE.정확히읽기(inskrywing_VALUE["size"])
            if 지문(data) != inskrywing_VALUE["sha256"]:
                raise ValueError("bondel Lêer SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), Pad, "exec")
            파일들[Pad] = data
            gc.collect()
        return 명세, 파일들
    finally:
        bedryfstelsel.udp_close(종단)


def installeer_VALUE(요청, 접속번호):
    print("bondel aflaai:", 요청)
    명세, 파일들 = aflaai(요청, 접속번호)
    inskrywing_Lys = 목록읽기()
    Naam = 명세["name"]
    if Naam in inskrywing_Lys:
        if inskrywing_Lys[Naam]["version"] == 명세["version"]:
            for Pad, 지문값 in inskrywing_Lys[Naam]["files"].items():
                if bedryfstelsel.path_kind(Pad) != 1 or 지문(bedryfstelsel.read(Pad)) != 지문값:
                    raise ValueError("설치된 bondel 파일이 달라졌습니다: " + Pad)
            print("이미 설치됨:", Naam, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 TERUG_VALUE 설치하십시오.")
    for Pad in 파일들:
        if bedryfstelsel.path_kind(Pad):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Pad)
    inskrywing_Lys[Naam] = {"version": 명세["version"], "files": {Pad: 지문(data) for Pad, data in 파일들.items()}}
    새목록 = json.dumps(inskrywing_Lys).encode()
    if len(새목록) > 16384:
        raise ValueError("bondel inskrywing_Lys Grootte 초과")
    이전목록 = bedryfstelsel.read(Lys_pad) if bedryfstelsel.path_kind(Lys_pad) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Pad, data in 파일들.items():
            부분들 = Pad.split("/")
            for 수 in range(2, len(부분들)):
                gids_VALUE = "/".join(부분들[:수])
                종류 = bedryfstelsel.path_kind(gids_VALUE)
                if 종류 == 0:
                    bedryfstelsel.mkdir(gids_VALUE)
                    만든폴더.append(gids_VALUE)
                elif 종류 != 2:
                    raise ValueError("gids_VALUE 경로에 파일이 있습니다: " + gids_VALUE)
            만든파일.append(Pad)
            skryf_LOG(Pad, data)
        skryf_LOG(Lys_pad, 새목록)
    except Exception:
        for Pad in 만든파일:
            if bedryfstelsel.path_kind(Pad):
                bedryfstelsel.remove(Pad)
        for gids_VALUE in reversed(만든폴더):
            bedryfstelsel.rmdir(gids_VALUE)
        if 이전목록 is not None:
            skryf_LOG(Lys_pad, 이전목록)
        elif bedryfstelsel.path_kind(Lys_pad):
            bedryfstelsel.remove(Lys_pad)
        raise
    print("installeer_VALUE 완료:", Naam, 명세["version"], "→ /lib (RAM)")


def verwyder_inskrywing(Naam):
    inskrywing_Lys = 목록읽기()
    if Naam not in inskrywing_Lys:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Naam)
    for Pad, 지문값 in inskrywing_Lys[Naam]["files"].items():
        if bedryfstelsel.path_kind(Pad) != 1 or 지문(bedryfstelsel.read(Pad)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Pad)
    for Pad in inskrywing_Lys[Naam]["files"]:
        bedryfstelsel.remove(Pad)
    del inskrywing_Lys[Naam]
    skryf_LOG(Lys_pad, json.dumps(inskrywing_Lys).encode())
    print("verwyder_inskrywing 완료:", Naam)


def Loop(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Naam, Stelselinfo in 목록읽기().items():
            print(Naam, Stelselinfo["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        installeer_VALUE(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        verwyder_inskrywing(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython bron_boom 설치기 (PyPA pip 전체가 아님)")
        print("pip install Naam[==버전] [--port 8027] | pip list | pip uninstall Naam")
        print("hou: Nutsmiddels/uitvoer_bevel.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Loop(sys.argv[1:])
    except Exception as Fout:
        print("bondel Fout:", Fout)
        sys.exit(1)
