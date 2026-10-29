"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ଆୟୋଜକ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ଅପରେଟିଂ_ସିଷ୍ଟମ

ତାଲିକା_ପଥ = "/lib/.pip.json"


def 지문(ଡାଟା):
    return "".join("%02x" % ମୂଲ୍ୟ for ମୂଲ୍ୟ in hashlib.sha256(ଡାଟା).digest())


def 목록읽기():
    if ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ତାଲିକା_ପଥ) == 0:
        return {}
    return json.loads(ଅପରେଟିଂ_ସିଷ୍ଟମ.read(ତାଲିକା_ପଥ).decode("utf-8"))


def ଲିଖନ_ଲଗ୍(ପଥ, ଡାଟା):
    if ଅପରେଟିଂ_ସିଷ୍ଟମ.write(ପଥ, ଡାଟା) != len(ଡାଟା):
        raise OSError(28)


def ପରୀକ୍ଷିତ_ପଥ(ପଥ):
    if not isinstance(ପଥ, str) or not ପଥ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ପଥ.split("/")):
        raise ValueError("허용하지 않는 ବଣ୍ଡଲ୍ ପଥ")
    if "\\" in ପଥ or any(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) < 32 or ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) == 127 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ପଥ):
        raise ValueError("잘못된 ପଥ 문자")
    ମାପ = "/lib/" + ପଥ
    if len(ମାପ.encode("utf-8")) > 63 or ପଥ in ("한국어.py", "ବଣ୍ଡଲ୍.py"):
        raise ValueError("ବଣ୍ଡଲ୍ 경로가 너무 길거나 ଡିଫଲ୍ଟ_ମାନ 라이브러리와 겹칩니다.")
    return ମାପ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ଚଳାନ୍ତୁ = ଅପରେଟିଂ_ସିଷ୍ଟମ.ticks_ms()

    def 정확히읽기(자신, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ):
        ଡାଟା = bytearray()
        while len(ଡାଟା) < ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ:
            if ଅପରେଟିଂ_ସିଷ୍ଟମ.ticks_ms() - 자신.ଚଳାନ୍ତୁ > 90000:
                raise ValueError("ବଣ୍ଡଲ୍ 중계 ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ ସମୟ_ମୂଲ୍ୟ 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ଅପରେଟିଂ_ସିଷ୍ଟମ.tcp_read(자신.종단, 512)
                except OSError as ତ୍ରୁଟି:
                    if ତ୍ରୁଟି.args[0] != 11:
                        raise
                    ଅପରେଟିଂ_ସିଷ୍ଟମ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ବଣ୍ଡଲ୍ 전송이 중간에 끝났습니다.")
            개수 = min(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - len(ଡାଟା), len(자신.남은자료))
            ଡାଟା.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ଅପରେଟିଂ_ସିଷ୍ଟମ.sleep_ms(0)
        return bytes(ଡାଟା)


def ଡାଉନ୍_ଲୋଡ଼(요청, ପୋର୍ଟ୍_ନମ୍ଵର୍):
    if len(요청) > 96 or any(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 요청):
        raise ValueError("사용법: pip install ନାମ 또는 ନାମ==버전")
    종단 = ଅପରେଟିଂ_ସିଷ୍ଟମ.tcp_open()
    try:
        ଚଳାନ୍ତୁ = ଅପରେଟିଂ_ସିଷ୍ଟମ.ticks_ms()
        while True:
            try:
                ଅପରେଟିଂ_ସିଷ୍ଟମ.tcp_connect(종단, "10.0.2.2", ପୋର୍ଟ୍_ନମ୍ଵର୍)
                break
            except OSError as ତ୍ରୁଟି:
                if ତ୍ରୁଟି.args[0] not in (11, 115) or ଅପରେଟିଂ_ସିଷ୍ଟମ.ticks_ms() - ଚଳାନ୍ତୁ > 5000:
                    raise ValueError("ବଣ୍ଡଲ୍ 중계 ସଂଯୋଗ_କରନ୍ତୁ ବିଫଳତା_ମୂଲ୍ୟ: 호스트에서 --network --pip로 실행하십시오.")
                ଅପରେଟିଂ_ସିଷ୍ଟମ.sleep_ms(10)
        ଡାଟା = (요청 + "\n").encode()
        while ଡାଟା:
            try:
                개수 = ଅପରେଟିଂ_ସିଷ୍ଟମ.tcp_write(종단, ଡାଟା)
                if not 개수:
                    raise ValueError("ବଣ୍ଡଲ୍ 요청 ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ ବିଫଳତା_ମୂଲ୍ୟ")
                ଡାଟା = ଡାଟା[개수:]
            except OSError as ତ୍ରୁଟି:
                if ତ୍ରୁଟି.args[0] != 11:
                    raise
                ଅପରେଟିଂ_ସିଷ୍ଟମ.sleep_ms(10)
                if ଅପରେଟିଂ_ସିଷ୍ଟମ.ticks_ms() - ଚଳାନ୍ତୁ > 10000:
                    raise ValueError("ବଣ୍ଡଲ୍ 요청 ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ ସମୟ_ମୂଲ୍ୟ 초과")
        ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ = 수신흐름(종단)
        머리 = ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ବଣ୍ଡଲ୍ ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ କର୍ମ_ମୂଲ୍ୟ 불일치")
        ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ > 8192:
            raise ValueError("ବଣ୍ଡଲ୍ 명세가 너무 큽니다.")
        명세 = json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.정확히읽기(ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ଉତ୍ସ_ବୃକ୍ଷ 파일은 1~16개여야 합니다.")
        if sum(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ["size"] for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 명세["files"]) > 65536:
            raise ValueError("ବଣ୍ଡଲ୍ ଉତ୍ସ_ବୃକ୍ଷ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 명세["files"]:
            ପଥ = ପରୀକ୍ଷିତ_ପଥ(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ["path"])
            if ପଥ in 파일들 or not 0 <= ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ["size"] <= 16384:
                raise ValueError("중복 ପଥ 또는 ଫାଇଲ ଆକାର 초과")
            ଡାଟା = ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.정확히읽기(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ["size"])
            if 지문(ଡାଟା) != ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ["sha256"]:
                raise ValueError("ବଣ୍ଡଲ୍ ଫାଇଲ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ଡାଟା.decode("utf-8"), ପଥ, "exec")
            파일들[ପଥ] = ଡାଟା
            gc.collect()
        return 명세, 파일들
    finally:
        ଅପରେଟିଂ_ସିଷ୍ଟମ.udp_close(종단)


def ସଂସ୍ଥାପନ_ମୂଲ୍ୟ(요청, ପୋର୍ଟ୍_ନମ୍ଵର୍):
    print("ବଣ୍ଡଲ୍ ଡାଉନ୍_ଲୋଡ଼:", 요청)
    명세, 파일들 = ଡାଉନ୍_ଲୋଡ଼(요청, ପୋର୍ଟ୍_ନମ୍ଵର୍)
    ଏଣ୍ଟ୍ରି_ତାଲିକା = 목록읽기()
    ନାମ = 명세["name"]
    if ନାମ in ଏଣ୍ଟ୍ରି_ତାଲିକା:
        if ଏଣ୍ଟ୍ରି_ତାଲିକା[ନାମ]["version"] == 명세["version"]:
            for ପଥ, 지문값 in ଏଣ୍ଟ୍ରି_ତାଲିକା[ନାମ]["files"].items():
                if ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ପଥ) != 1 or 지문(ଅପରେଟିଂ_ସିଷ୍ଟମ.read(ପଥ)) != 지문값:
                    raise ValueError("설치된 ବଣ୍ଡଲ୍ 파일이 달라졌습니다: " + ପଥ)
            print("이미 설치됨:", ନାମ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ପଛ_ମୂଲ୍ୟ 설치하십시오.")
    for ପଥ in 파일들:
        if ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ପଥ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ପଥ)
    ଏଣ୍ଟ୍ରି_ତାଲିକା[ନାମ] = {"version": 명세["version"], "files": {ପଥ: 지문(ଡାଟା) for ପଥ, ଡାଟା in 파일들.items()}}
    새목록 = json.dumps(ଏଣ୍ଟ୍ରି_ତାଲିକା).encode()
    if len(새목록) > 16384:
        raise ValueError("ବଣ୍ଡଲ୍ ଏଣ୍ଟ୍ରି_ତାଲିକା ଆକାର 초과")
    이전목록 = ଅପରେଟିଂ_ସିଷ୍ଟମ.read(ତାଲିକା_ପଥ) if ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ତାଲିକା_ପଥ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ପଥ, ଡାଟା in 파일들.items():
            부분들 = ପଥ.split("/")
            for 수 in range(2, len(부분들)):
                ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ = "/".join(부분들[:수])
                종류 = ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)
                if 종류 == 0:
                    ଅପରେଟିଂ_ସିଷ୍ଟମ.mkdir(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)
                    만든폴더.append(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)
                elif 종류 != 2:
                    raise ValueError("ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ 경로에 파일이 있습니다: " + ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)
            만든파일.append(ପଥ)
            ଲିଖନ_ଲଗ୍(ପଥ, ଡାଟା)
        ଲିଖନ_ଲଗ୍(ତାଲିକା_ପଥ, 새목록)
    except Exception:
        for ପଥ in 만든파일:
            if ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ପଥ):
                ଅପରେଟିଂ_ସିଷ୍ଟମ.remove(ପଥ)
        for ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ in reversed(만든폴더):
            ଅପରେଟିଂ_ସିଷ୍ଟମ.rmdir(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ)
        if 이전목록 is not None:
            ଲିଖନ_ଲଗ୍(ତାଲିକା_ପଥ, 이전목록)
        elif ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ତାଲିକା_ପଥ):
            ଅପରେଟିଂ_ସିଷ୍ଟମ.remove(ତାଲିକା_ପଥ)
        raise
    print("ସଂସ୍ଥାପନ_ମୂଲ୍ୟ 완료:", ନାମ, 명세["version"], "→ /lib (RAM)")


def ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି(ନାମ):
    ଏଣ୍ଟ୍ରି_ତାଲିକା = 목록읽기()
    if ନାମ not in ଏଣ୍ଟ୍ରି_ତାଲିକା:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ନାମ)
    for ପଥ, 지문값 in ଏଣ୍ଟ୍ରି_ତାଲିକା[ନାମ]["files"].items():
        if ଅପରେଟିଂ_ସିଷ୍ଟମ.path_kind(ପଥ) != 1 or 지문(ଅପରେଟିଂ_ସିଷ୍ଟମ.read(ପଥ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ପଥ)
    for ପଥ in ଏଣ୍ଟ୍ରି_ତାଲିକା[ନାମ]["files"]:
        ଅପରେଟିଂ_ସିଷ୍ଟମ.remove(ପଥ)
    del ଏଣ୍ଟ୍ରି_ତାଲିକା[ନାମ]
    ଲିଖନ_ଲଗ୍(ତାଲିକା_ପଥ, json.dumps(ଏଣ୍ଟ୍ରି_ତାଲିକା).encode())
    print("ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି 완료:", ନାମ)


def ଚଳାନ୍ତୁ(인수):
    ପୋର୍ଟ୍_ନମ୍ଵର୍ = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        ପୋର୍ଟ୍_ନମ୍ଵର୍ = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ନାମ, ସିଷ୍ଟମ୍_ସୂଚନା in 목록읽기().items():
            print(ନାମ, ସିଷ୍ଟମ୍_ସୂଚନା["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ସଂସ୍ଥାପନ_ମୂଲ୍ୟ(인수[1], ପୋର୍ଟ୍_ନମ୍ଵର୍)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ଅପସାରଣ_କରିବା_ଏଣ୍ଟ୍ରି(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ଉତ୍ସ_ବୃକ୍ଷ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ନାମ[==버전] [--port 8027] | pip list | pip uninstall ନାମ")
        print("ଆୟୋଜକ: ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ଚଳାନ୍ତୁ(sys.argv[1:])
    except Exception as ତ୍ରୁଟି:
        print("ବଣ୍ଡଲ୍ ତ୍ରୁଟି:", ତ୍ରୁଟି)
        sys.exit(1)
