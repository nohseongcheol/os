"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 አዐንግድ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ስርዓት_ስርሒት

ዝርዝር_መገዲ = "/lib/.pip.json"


def 지문(ሓበሬታ):
    return "".join("%02x" % ዋጋ for ዋጋ in hashlib.sha256(ሓበሬታ).digest())


def 목록읽기():
    if ስርዓት_ስርሒት.path_kind(ዝርዝር_መገዲ) == 0:
        return {}
    return json.loads(ስርዓት_ስርሒት.read(ዝርዝር_መገዲ).decode("utf-8"))


def ጸሓፍ_ምዝጉብ(መገዲ, ሓበሬታ):
    if ስርዓት_ስርሒት.write(መገዲ, ሓበሬታ) != len(ሓበሬታ):
        raise OSError(28)


def ፈትሽ_መገዲ(መገዲ):
    if not isinstance(መገዲ, str) or not መገዲ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in መገዲ.split("/")):
        raise ValueError("허용하지 않는 ጥማር መገዲ")
    if "\\" in መገዲ or any(ord(ፊደል_ዋጋ) < 32 or ord(ፊደል_ዋጋ) == 127 for ፊደል_ዋጋ in መገዲ):
        raise ValueError("잘못된 መገዲ 문자")
    결과 = "/lib/" + መገዲ
    if len(결과.encode("utf-8")) > 63 or መገዲ in ("ትግርኛ.py", "ጥማር.py"):
        raise ValueError("ጥማር 경로가 너무 길거나 ንቡር_ዋጋ 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ኣኺድ = ስርዓት_ስርሒት.ticks_ms()

    def 정확히읽기(자신, ንውሓት_ዋጋ):
        ሓበሬታ = bytearray()
        while len(ሓበሬታ) < ንውሓት_ዋጋ:
            if ስርዓት_ስርሒት.ticks_ms() - 자신.ኣኺድ > 90000:
                raise ValueError("ጥማር 중계 መልስ 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ስርዓት_ስርሒት.tcp_read(자신.종단, 512)
                except OSError as ጌጋ:
                    if ጌጋ.args[0] != 11:
                        raise
                    ስርዓት_ስርሒት.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ጥማር 전송이 중간에 끝났습니다.")
            개수 = min(ንውሓት_ዋጋ - len(ሓበሬታ), len(자신.남은자료))
            ሓበሬታ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ስርዓት_ስርሒት.sleep_ms(0)
        return bytes(ሓበሬታ)


def ምውራድ(요청, 접속번호):
    if len(요청) > 96 or any(ፊደል_ዋጋ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ፊደል_ዋጋ in 요청):
        raise ValueError("사용법: pip install ሽም 또는 ሽም==버전")
    종단 = ስርዓት_ስርሒት.tcp_open()
    try:
        ኣኺድ = ስርዓት_ስርሒት.ticks_ms()
        while True:
            try:
                ስርዓት_ስርሒት.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as ጌጋ:
                if ጌጋ.args[0] not in (11, 115) or ስርዓት_ስርሒት.ticks_ms() - ኣኺድ > 5000:
                    raise ValueError("ጥማር 중계 ኣላግብ ፍሽለት_ዋጋ: 호스트에서 --network --pip로 실행하십시오.")
                ስርዓት_ስርሒት.sleep_ms(10)
        ሓበሬታ = (요청 + "\n").encode()
        while ሓበሬታ:
            try:
                개수 = ስርዓት_ስርሒት.tcp_write(종단, ሓበሬታ)
                if not 개수:
                    raise ValueError("ጥማር 요청 ምስጋር_ዋጋ ፍሽለት_ዋጋ")
                ሓበሬታ = ሓበሬታ[개수:]
            except OSError as ጌጋ:
                if ጌጋ.args[0] != 11:
                    raise
                ስርዓት_ስርሒት.sleep_ms(10)
                if ስርዓት_ስርሒት.ticks_ms() - ኣኺድ > 10000:
                    raise ValueError("ጥማር 요청 ምስጋር_ዋጋ 시간 초과")
        ወሓዚ_ዋጋ = 수신흐름(종단)
        머리 = ወሓዚ_ዋጋ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ጥማር ምስጋር_ዋጋ ዕዮ_ዋጋ_102996da 불일치")
        ንውሓት_ዋጋ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ንውሓት_ዋጋ > 8192:
            raise ValueError("ጥማር 명세가 너무 큽니다.")
        명세 = json.loads(ወሓዚ_ዋጋ.정확히읽기(ንውሓት_ዋጋ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ምንጪ_ገረብ 파일은 1~16개여야 합니다.")
        if sum(ምእታው_ዋጋ["size"] for ምእታው_ዋጋ in 명세["files"]) > 65536:
            raise ValueError("ጥማር ምንጪ_ገረብ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ምእታው_ዋጋ in 명세["files"]:
            መገዲ = ፈትሽ_መገዲ(ምእታው_ዋጋ["path"])
            if መገዲ in 파일들 or not 0 <= ምእታው_ዋጋ["size"] <= 16384:
                raise ValueError("중복 መገዲ 또는 ፋይል መጠን 초과")
            ሓበሬታ = ወሓዚ_ዋጋ.정확히읽기(ምእታው_ዋጋ["size"])
            if 지문(ሓበሬታ) != ምእታው_ዋጋ["sha256"]:
                raise ValueError("ጥማር ፋይል SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ሓበሬታ.decode("utf-8"), መገዲ, "exec")
            파일들[መገዲ] = ሓበሬታ
            gc.collect()
        return 명세, 파일들
    finally:
        ስርዓት_ስርሒት.udp_close(종단)


def ጸዓን_ዋጋ(요청, 접속번호):
    print("ጥማር ምውራድ:", 요청)
    명세, 파일들 = ምውራድ(요청, 접속번호)
    ምእታው_ዝርዝር = 목록읽기()
    ሽም = 명세["name"]
    if ሽም in ምእታው_ዝርዝር:
        if ምእታው_ዝርዝር[ሽም]["version"] == 명세["version"]:
            for መገዲ, 지문값 in ምእታው_ዝርዝር[ሽም]["files"].items():
                if ስርዓት_ስርሒት.path_kind(መገዲ) != 1 or 지문(ስርዓት_ስርሒት.read(መገዲ)) != 지문값:
                    raise ValueError("설치된 ጥማር 파일이 달라졌습니다: " + መገዲ)
            print("이미 설치됨:", ሽም, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ድሕሪት_ዋጋ 설치하십시오.")
    for መገዲ in 파일들:
        if ስርዓት_ስርሒት.path_kind(መገዲ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + መገዲ)
    ምእታው_ዝርዝር[ሽም] = {"version": 명세["version"], "files": {መገዲ: 지문(ሓበሬታ) for መገዲ, ሓበሬታ in 파일들.items()}}
    새목록 = json.dumps(ምእታው_ዝርዝር).encode()
    if len(새목록) > 16384:
        raise ValueError("ጥማር ምእታው_ዝርዝር መጠን 초과")
    이전목록 = ስርዓት_ስርሒት.read(ዝርዝር_መገዲ) if ስርዓት_ስርሒት.path_kind(ዝርዝር_መገዲ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for መገዲ, ሓበሬታ in 파일들.items():
            부분들 = መገዲ.split("/")
            for 수 in range(2, len(부분들)):
                ሓባሪ_ማህደር_ዋጋ = "/".join(부분들[:수])
                종류 = ስርዓት_ስርሒት.path_kind(ሓባሪ_ማህደር_ዋጋ)
                if 종류 == 0:
                    ስርዓት_ስርሒት.mkdir(ሓባሪ_ማህደር_ዋጋ)
                    만든폴더.append(ሓባሪ_ማህደር_ዋጋ)
                elif 종류 != 2:
                    raise ValueError("ሓባሪ_ማህደር_ዋጋ 경로에 파일이 있습니다: " + ሓባሪ_ማህደር_ዋጋ)
            만든파일.append(መገዲ)
            ጸሓፍ_ምዝጉብ(መገዲ, ሓበሬታ)
        ጸሓፍ_ምዝጉብ(ዝርዝር_መገዲ, 새목록)
    except Exception:
        for መገዲ in 만든파일:
            if ስርዓት_ስርሒት.path_kind(መገዲ):
                ስርዓት_ስርሒት.remove(መገዲ)
        for ሓባሪ_ማህደር_ዋጋ in reversed(만든폴더):
            ስርዓት_ስርሒት.rmdir(ሓባሪ_ማህደር_ዋጋ)
        if 이전목록 is not None:
            ጸሓፍ_ምዝጉብ(ዝርዝር_መገዲ, 이전목록)
        elif ስርዓት_ስርሒት.path_kind(ዝርዝር_መገዲ):
            ስርዓት_ስርሒት.remove(ዝርዝር_መገዲ)
        raise
    print("ጸዓን_ዋጋ 완료:", ሽም, 명세["version"], "→ /lib (RAM)")


def ኣልግስ_ምእታው(ሽም):
    ምእታው_ዝርዝር = 목록읽기()
    if ሽም not in ምእታው_ዝርዝር:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ሽም)
    for መገዲ, 지문값 in ምእታው_ዝርዝር[ሽም]["files"].items():
        if ስርዓት_ስርሒት.path_kind(መገዲ) != 1 or 지문(ስርዓት_ስርሒት.read(መገዲ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + መገዲ)
    for መገዲ in ምእታው_ዝርዝር[ሽም]["files"]:
        ስርዓት_ስርሒት.remove(መገዲ)
    del ምእታው_ዝርዝር[ሽም]
    ጸሓፍ_ምዝጉብ(ዝርዝር_መገዲ, json.dumps(ምእታው_ዝርዝር).encode())
    print("ኣልግስ_ምእታው 완료:", ሽም)


def ኣኺድ(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ሽም, ናይ_ስርዓት_ሓበሬታ in 목록읽기().items():
            print(ሽም, ናይ_ስርዓት_ሓበሬታ["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ጸዓን_ዋጋ(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ኣልግስ_ምእታው(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ምንጪ_ገረብ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ሽም[==버전] [--port 8027] | pip list | pip uninstall ሽም")
        print("አዐንግድ: መሳርሒታት/ተግብር_ትእዛዝ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ኣኺድ(sys.argv[1:])
    except Exception as ጌጋ:
        print("ጥማር ጌጋ:", ጌጋ)
        sys.exit(1)
