"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ධාරකය 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as මෙහෙයුම්_පද්ධතිය

ලැයිස්තුව_පෙත = "/lib/.pip.json"


def 지문(දත්ත):
    return "".join("%02x" % අගය for අගය in hashlib.sha256(දත්ත).digest())


def 목록읽기():
    if මෙහෙයුම්_පද්ධතිය.path_kind(ලැයිස්තුව_පෙත) == 0:
        return {}
    return json.loads(මෙහෙයුම්_පද්ධතිය.read(ලැයිස්තුව_පෙත).decode("utf-8"))


def ලියන්න_ලොගය(මාර්_ගය, දත්ත):
    if මෙහෙයුම්_පද්ධතිය.write(මාර්_ගය, දත්ත) != len(දත්ත):
        raise OSError(28)


def චෙක්පත_පෙත(මාර්_ගය):
    if not isinstance(මාර්_ගය, str) or not මාර්_ගය.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in මාර්_ගය.split("/")):
        raise ValueError("허용하지 않는 පොදිය මාර්_ගය")
    if "\\" in මාර්_ගය or any(ord(අනුලකුණ_අගය) < 32 or ord(අනුලකුණ_අගය) == 127 for අනුලකුණ_අගය in මාර්_ගය):
        raise ValueError("잘못된 මාර්_ගය 문자")
    결과 = "/lib/" + මාර්_ගය
    if len(결과.encode("utf-8")) > 63 or මාර්_ගය in ("한국어.py", "පොදිය.py"):
        raise ValueError("පොදිය 경로가 너무 길거나 පෙරනිමි_අගය 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ක්_රියාත්මක_කරන්න_2 = මෙහෙයුම්_පද්ධතිය.ticks_ms()

    def 정확히읽기(자신, දිග_අගය):
        දත්ත = bytearray()
        while len(දත්ත) < දිග_අගය:
            if මෙහෙයුම්_පද්ධතිය.ticks_ms() - 자신.ක්_රියාත්මක_කරන්න_2 > 90000:
                raise ValueError("පොදිය 중계 පිළිතුරු_දෙන්න 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = මෙහෙයුම්_පද්ධතිය.tcp_read(자신.종단, 512)
                except OSError as දෝෂය:
                    if දෝෂය.args[0] != 11:
                        raise
                    මෙහෙයුම්_පද්ධතිය.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("පොදිය 전송이 중간에 끝났습니다.")
            개수 = min(දිග_අගය - len(දත්ත), len(자신.남은자료))
            දත්ත.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            මෙහෙයුම්_පද්ධතිය.sleep_ms(0)
        return bytes(දත්ත)


def බාගන්න(요청, 접속번호):
    if len(요청) > 96 or any(අනුලකුණ_අගය not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for අනුලකුණ_අගය in 요청):
        raise ValueError("사용법: pip install නම 또는 නම==버전")
    종단 = මෙහෙයුම්_පද්ධතිය.tcp_open()
    try:
        ක්_රියාත්මක_කරන්න_2 = මෙහෙයුම්_පද්ධතිය.ticks_ms()
        while True:
            try:
                මෙහෙයුම්_පද්ධතිය.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as දෝෂය:
                if දෝෂය.args[0] not in (11, 115) or මෙහෙයුම්_පද්ධතිය.ticks_ms() - ක්_රියාත්මක_කරන්න_2 > 5000:
                    raise ValueError("පොදිය 중계 සම්බන්ද_වන්න අසමත්වීම_අගය: 호스트에서 --network --pip로 실행하십시오.")
                මෙහෙයුම්_පද්ධතිය.sleep_ms(10)
        දත්ත = (요청 + "\n").encode()
        while දත්ත:
            try:
                개수 = මෙහෙයුම්_පද්ධතිය.tcp_write(종단, දත්ත)
                if not 개수:
                    raise ValueError("පොදිය 요청 මාරුව_අගය අසමත්වීම_අගය")
                දත්ත = දත්ත[개수:]
            except OSError as දෝෂය:
                if දෝෂය.args[0] != 11:
                    raise
                මෙහෙයුම්_පද්ධතිය.sleep_ms(10)
                if මෙහෙයුම්_පද්ධතිය.ticks_ms() - ක්_රියාත්මක_කරන්න_2 > 10000:
                    raise ValueError("පොදිය 요청 මාරුව_අගය 시간 초과")
        දහර_අගය = 수신흐름(종단)
        머리 = දහර_අගය.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("පොදිය මාරුව_අගය කාරණය_අගය 불일치")
        දිග_අගය = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if දිග_අගය > 8192:
            raise ValueError("පොදිය 명세가 너무 큽니다.")
        명세 = json.loads(දහර_අගය.정확히읽기(දිග_අගය).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 මූලය_රුක 파일은 1~16개여야 합니다.")
        if sum(පිවිසුම_අගය["size"] for පිවිසුම_අගය in 명세["files"]) > 65536:
            raise ValueError("පොදිය මූලය_රුක 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for පිවිසුම_අගය in 명세["files"]:
            මාර්_ගය = චෙක්පත_පෙත(පිවිසුම_අගය["path"])
            if මාර්_ගය in 파일들 or not 0 <= පිවිසුම_අගය["size"] <= 16384:
                raise ValueError("중복 මාර්_ගය 또는 ගොනු ප්_රමාණය 초과")
            දත්ත = දහර_අගය.정확히읽기(පිවිසුම_අගය["size"])
            if 지문(දත්ත) != පිවිසුම_අගය["sha256"]:
                raise ValueError("පොදිය ගොනු SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(දත්ත.decode("utf-8"), මාර්_ගය, "exec")
            파일들[මාර්_ගය] = දත්ත
            gc.collect()
        return 명세, 파일들
    finally:
        මෙහෙයුම්_පද්ධතිය.udp_close(종단)


def ස්ථාපනය_කරන්න_අගය(요청, 접속번호):
    print("පොදිය බාගන්න:", 요청)
    명세, 파일들 = බාගන්න(요청, 접속번호)
    පිවිසුම_ලැයිස්තුව = 목록읽기()
    නම = 명세["name"]
    if නම in පිවිසුම_ලැයිස්තුව:
        if පිවිසුම_ලැයිස්තුව[නම]["version"] == 명세["version"]:
            for මාර්_ගය, 지문값 in පිවිසුම_ලැයිස්තුව[නම]["files"].items():
                if මෙහෙයුම්_පද්ධතිය.path_kind(මාර්_ගය) != 1 or 지문(මෙහෙයුම්_පද්ධතිය.read(මාර්_ගය)) != 지문값:
                    raise ValueError("설치된 පොදිය 파일이 달라졌습니다: " + මාර්_ගය)
            print("이미 설치됨:", නම, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ආපසු_අගය 설치하십시오.")
    for මාර්_ගය in 파일들:
        if මෙහෙයුම්_පද්ධතිය.path_kind(මාර්_ගය):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + මාර්_ගය)
    පිවිසුම_ලැයිස්තුව[නම] = {"version": 명세["version"], "files": {මාර්_ගය: 지문(දත්ත) for මාර්_ගය, දත්ත in 파일들.items()}}
    새목록 = json.dumps(පිවිසුම_ලැයිස්තුව).encode()
    if len(새목록) > 16384:
        raise ValueError("පොදිය පිවිසුම_ලැයිස්තුව ප්_රමාණය 초과")
    이전목록 = මෙහෙයුම්_පද්ධතිය.read(ලැයිස්තුව_පෙත) if මෙහෙයුම්_පද්ධතිය.path_kind(ලැයිස්තුව_පෙත) else None
    만든파일 = []
    만든폴더 = []
    try:
        for මාර්_ගය, දත්ත in 파일들.items():
            부분들 = මාර්_ගය.split("/")
            for 수 in range(2, len(부분들)):
                නාමාවලිය_අගය = "/".join(부분들[:수])
                종류 = මෙහෙයුම්_පද්ධතිය.path_kind(නාමාවලිය_අගය)
                if 종류 == 0:
                    මෙහෙයුම්_පද්ධතිය.mkdir(නාමාවලිය_අගය)
                    만든폴더.append(නාමාවලිය_අගය)
                elif 종류 != 2:
                    raise ValueError("නාමාවලිය_අගය 경로에 파일이 있습니다: " + නාමාවලිය_අගය)
            만든파일.append(මාර්_ගය)
            ලියන්න_ලොගය(මාර්_ගය, දත්ත)
        ලියන්න_ලොගය(ලැයිස්තුව_පෙත, 새목록)
    except Exception:
        for මාර්_ගය in 만든파일:
            if මෙහෙයුම්_පද්ධතිය.path_kind(මාර්_ගය):
                මෙහෙයුම්_පද්ධතිය.remove(මාර්_ගය)
        for නාමාවලිය_අගය in reversed(만든폴더):
            මෙහෙයුම්_පද්ධතිය.rmdir(නාමාවලිය_අගය)
        if 이전목록 is not None:
            ලියන්න_ලොගය(ලැයිස්තුව_පෙත, 이전목록)
        elif මෙහෙයුම්_පද්ධතිය.path_kind(ලැයිස්තුව_පෙත):
            මෙහෙයුම්_පද්ධතිය.remove(ලැයිස්තුව_පෙත)
        raise
    print("ස්ථාපනය_කරන්න_අගය 완료:", නම, 명세["version"], "→ /lib (RAM)")


def ඉවත්_කරන්න_පිවිසුම(නම):
    පිවිසුම_ලැයිස්තුව = 목록읽기()
    if නම not in පිවිසුම_ලැයිස්තුව:
        raise ValueError("설치되지 않은 꾸러미입니다: " + නම)
    for මාර්_ගය, 지문값 in පිවිසුම_ලැයිස්තුව[නම]["files"].items():
        if මෙහෙයුම්_පද්ධතිය.path_kind(මාර්_ගය) != 1 or 지문(මෙහෙයුම්_පද්ධතිය.read(මාර්_ගය)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + මාර්_ගය)
    for මාර්_ගය in පිවිසුම_ලැයිස්තුව[නම]["files"]:
        මෙහෙයුම්_පද්ධතිය.remove(මාර්_ගය)
    del පිවිසුම_ලැයිස්තුව[නම]
    ලියන්න_ලොගය(ලැයිස්තුව_පෙත, json.dumps(පිවිසුම_ලැයිස්තුව).encode())
    print("ඉවත්_කරන්න_පිවිසුම 완료:", නම)


def ක්_රියාත්මක_කරන්න_2(විස්තාරක):
    접속번호 = 8027
    if len(විස්තාරක) >= 2 and විස්තාරක[-2] == "--port":
        접속번호 = int(විස්තාරක[-1])
        විස්තාරක = විස්තාරක[:-2]
    if විස්තාරක == ["list"]:
        for නම, පද්ධති_තොරතුරු in 목록읽기().items():
            print(නම, පද්ධති_තොරතුරු["version"])
    elif len(විස්තාරක) == 2 and විස්තාරක[0] == "install":
        ස්ථාපනය_කරන්න_අගය(විස්තාරක[1], 접속번호)
    elif len(විස්තාරක) == 2 and විස්තාරක[0] == "uninstall":
        ඉවත්_කරන්න_පිවිසුම(විස්තාරක[1])
    elif not විස්තාරක or විස්තාරක in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython මූලය_රුක 설치기 (PyPA pip 전체가 아님)")
        print("pip install නම[==버전] [--port 8027] | pip list | pip uninstall නම")
        print("ධාරකය: මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ක්_රියාත්මක_කරන්න_2(sys.argv[1:])
    except Exception as දෝෂය:
        print("පොදිය දෝෂය:", දෝෂය)
        sys.exit(1)
