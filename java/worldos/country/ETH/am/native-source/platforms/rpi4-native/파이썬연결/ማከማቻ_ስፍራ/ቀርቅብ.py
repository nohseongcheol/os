"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 አዘጋጅ_b78e430d 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ስርዓተ_ክወና

ዝርዝር_ዱካ = "/lib/.pip.json"


def 지문(ውሂብ):
    return "".join("%02x" % እሴት for እሴት in hashlib.sha256(ውሂብ).digest())


def 목록읽기():
    if ስርዓተ_ክወና.path_kind(ዝርዝር_ዱካ) == 0:
        return {}
    return json.loads(ስርዓተ_ክወና.read(ዝርዝር_ዱካ).decode("utf-8"))


def ጻፍ_መዝግብ(መተላለፊያ, ውሂብ):
    if ስርዓተ_ክወና.write(መተላለፊያ, ውሂብ) != len(ውሂብ):
        raise OSError(28)


def ቼክ_ዱካ(መተላለፊያ):
    if not isinstance(መተላለፊያ, str) or not መተላለፊያ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in መተላለፊያ.split("/")):
        raise ValueError("허용하지 않는 ቀርቅብ መተላለፊያ")
    if "\\" in መተላለፊያ or any(ord(ቁምፊ_እሴት) < 32 or ord(ቁምፊ_እሴት) == 127 for ቁምፊ_እሴት in መተላለፊያ):
        raise ValueError("잘못된 መተላለፊያ 문자")
    ልኬት = "/lib/" + መተላለፊያ
    if len(ልኬት.encode("utf-8")) > 63 or መተላለፊያ in ("አማርኛ.py", "ቀርቅብ.py"):
        raise ValueError("ቀርቅብ 경로가 너무 길거나 ነባሪ_እሴት 라이브러리와 겹칩니다.")
    return ልኬት


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ማስኬጃ = ስርዓተ_ክወና.ticks_ms()

    def 정확히읽기(자신, ርዝመት_እሴት):
        ውሂብ = bytearray()
        while len(ውሂብ) < ርዝመት_እሴት:
            if ስርዓተ_ክወና.ticks_ms() - 자신.ማስኬጃ > 90000:
                raise ValueError("ቀርቅብ 중계 መልስ ጊዜ_እሴት 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ስርዓተ_ክወና.tcp_read(자신.종단, 512)
                except OSError as ስህተት:
                    if ስህተት.args[0] != 11:
                        raise
                    ስርዓተ_ክወና.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ቀርቅብ 전송이 중간에 끝났습니다.")
            개수 = min(ርዝመት_እሴት - len(ውሂብ), len(자신.남은자료))
            ውሂብ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ስርዓተ_ክወና.sleep_ms(0)
        return bytes(ውሂብ)


def ወራጅ(요청, የወደብ_ቁጥር):
    if len(요청) > 96 or any(ቁምፊ_እሴት not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ቁምፊ_እሴት in 요청):
        raise ValueError("사용법: pip install ስም 또는 ስም==버전")
    종단 = ስርዓተ_ክወና.tcp_open()
    try:
        ማስኬጃ = ስርዓተ_ክወና.ticks_ms()
        while True:
            try:
                ስርዓተ_ክወና.tcp_connect(종단, "10.0.2.2", የወደብ_ቁጥር)
                break
            except OSError as ስህተት:
                if ስህተት.args[0] not in (11, 115) or ስርዓተ_ክወና.ticks_ms() - ማስኬጃ > 5000:
                    raise ValueError("ቀርቅብ 중계 መገናኛ ተስኖት_እሴት: 호스트에서 --network --pip로 실행하십시오.")
                ስርዓተ_ክወና.sleep_ms(10)
        ውሂብ = (요청 + "\n").encode()
        while ውሂብ:
            try:
                개수 = ስርዓተ_ክወና.tcp_write(종단, ውሂብ)
                if not 개수:
                    raise ValueError("ቀርቅብ 요청 ትልልፍ_እሴት ተስኖት_እሴት")
                ውሂብ = ውሂብ[개수:]
            except OSError as ስህተት:
                if ስህተት.args[0] != 11:
                    raise
                ስርዓተ_ክወና.sleep_ms(10)
                if ስርዓተ_ክወና.ticks_ms() - ማስኬጃ > 10000:
                    raise ValueError("ቀርቅብ 요청 ትልልፍ_እሴት ጊዜ_እሴት 초과")
        ልቀቅ_እሴት = 수신흐름(종단)
        머리 = ልቀቅ_እሴት.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ቀርቅብ ትልልፍ_እሴት ስራ_እሴት_102996da 불일치")
        ርዝመት_እሴት = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ርዝመት_እሴት > 8192:
            raise ValueError("ቀርቅብ 명세가 너무 큽니다.")
        명세 = json.loads(ልቀቅ_እሴት.정확히읽기(ርዝመት_እሴት).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ምንጭ_ዛፍ 파일은 1~16개여야 합니다.")
        if sum(ምዝግብ_እሴት["size"] for ምዝግብ_እሴት in 명세["files"]) > 65536:
            raise ValueError("ቀርቅብ ምንጭ_ዛፍ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ምዝግብ_እሴት in 명세["files"]:
            መተላለፊያ = ቼክ_ዱካ(ምዝግብ_እሴት["path"])
            if መተላለፊያ in 파일들 or not 0 <= ምዝግብ_እሴት["size"] <= 16384:
                raise ValueError("중복 መተላለፊያ 또는 ፋይል መጠን 초과")
            ውሂብ = ልቀቅ_እሴት.정확히읽기(ምዝግብ_እሴት["size"])
            if 지문(ውሂብ) != ምዝግብ_እሴት["sha256"]:
                raise ValueError("ቀርቅብ ፋይል SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ውሂብ.decode("utf-8"), መተላለፊያ, "exec")
            파일들[መተላለፊያ] = ውሂብ
            gc.collect()
        return 명세, 파일들
    finally:
        ስርዓተ_ክወና.udp_close(종단)


def ጫን_እሴት(요청, የወደብ_ቁጥር):
    print("ቀርቅብ ወራጅ:", 요청)
    명세, 파일들 = ወራጅ(요청, የወደብ_ቁጥር)
    ምዝግብ_ዝርዝር = 목록읽기()
    ስም = 명세["name"]
    if ስም in ምዝግብ_ዝርዝር:
        if ምዝግብ_ዝርዝር[ስም]["version"] == 명세["version"]:
            for መተላለፊያ, 지문값 in ምዝግብ_ዝርዝር[ስም]["files"].items():
                if ስርዓተ_ክወና.path_kind(መተላለፊያ) != 1 or 지문(ስርዓተ_ክወና.read(መተላለፊያ)) != 지문값:
                    raise ValueError("설치된 ቀርቅብ 파일이 달라졌습니다: " + መተላለፊያ)
            print("이미 설치됨:", ስም, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ተመለስ_እሴት 설치하십시오.")
    for መተላለፊያ in 파일들:
        if ስርዓተ_ክወና.path_kind(መተላለፊያ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + መተላለፊያ)
    ምዝግብ_ዝርዝር[ስም] = {"version": 명세["version"], "files": {መተላለፊያ: 지문(ውሂብ) for መተላለፊያ, ውሂብ in 파일들.items()}}
    새목록 = json.dumps(ምዝግብ_ዝርዝር).encode()
    if len(새목록) > 16384:
        raise ValueError("ቀርቅብ ምዝግብ_ዝርዝር መጠን 초과")
    이전목록 = ስርዓተ_ክወና.read(ዝርዝር_ዱካ) if ስርዓተ_ክወና.path_kind(ዝርዝር_ዱካ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for መተላለፊያ, ውሂብ in 파일들.items():
            부분들 = መተላለፊያ.split("/")
            for 수 in range(2, len(부분들)):
                ማውጫ_እሴት = "/".join(부분들[:수])
                종류 = ስርዓተ_ክወና.path_kind(ማውጫ_እሴት)
                if 종류 == 0:
                    ስርዓተ_ክወና.mkdir(ማውጫ_እሴት)
                    만든폴더.append(ማውጫ_እሴት)
                elif 종류 != 2:
                    raise ValueError("ማውጫ_እሴት 경로에 파일이 있습니다: " + ማውጫ_እሴት)
            만든파일.append(መተላለፊያ)
            ጻፍ_መዝግብ(መተላለፊያ, ውሂብ)
        ጻፍ_መዝግብ(ዝርዝር_ዱካ, 새목록)
    except Exception:
        for መተላለፊያ in 만든파일:
            if ስርዓተ_ክወና.path_kind(መተላለፊያ):
                ስርዓተ_ክወና.remove(መተላለፊያ)
        for ማውጫ_እሴት in reversed(만든폴더):
            ስርዓተ_ክወና.rmdir(ማውጫ_እሴት)
        if 이전목록 is not None:
            ጻፍ_መዝግብ(ዝርዝር_ዱካ, 이전목록)
        elif ስርዓተ_ክወና.path_kind(ዝርዝር_ዱካ):
            ስርዓተ_ክወና.remove(ዝርዝር_ዱካ)
        raise
    print("ጫን_እሴት 완료:", ስም, 명세["version"], "→ /lib (RAM)")


def አስወግድ_ምዝግብ(ስም):
    ምዝግብ_ዝርዝር = 목록읽기()
    if ስም not in ምዝግብ_ዝርዝር:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ስም)
    for መተላለፊያ, 지문값 in ምዝግብ_ዝርዝር[ስም]["files"].items():
        if ስርዓተ_ክወና.path_kind(መተላለፊያ) != 1 or 지문(ስርዓተ_ክወና.read(መተላለፊያ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + መተላለፊያ)
    for መተላለፊያ in ምዝግብ_ዝርዝር[ስም]["files"]:
        ስርዓተ_ክወና.remove(መተላለፊያ)
    del ምዝግብ_ዝርዝር[ስም]
    ጻፍ_መዝግብ(ዝርዝር_ዱካ, json.dumps(ምዝግብ_ዝርዝር).encode())
    print("አስወግድ_ምዝግብ 완료:", ስም)


def ማስኬጃ(인수):
    የወደብ_ቁጥር = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        የወደብ_ቁጥር = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ስም, የስርዓት_መረጃ in 목록읽기().items():
            print(ስም, የስርዓት_መረጃ["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ጫን_እሴት(인수[1], የወደብ_ቁጥር)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        አስወግድ_ምዝግብ(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ምንጭ_ዛፍ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ስም[==버전] [--port 8027] | pip list | pip uninstall ስም")
        print("አዘጋጅ_b78e430d: መሳሪያዎች/ፈጽም_ትእዛዝ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ማስኬጃ(sys.argv[1:])
    except Exception as ስህተት:
        print("ቀርቅብ ስህተት:", ስህተት)
        sys.exit(1)
