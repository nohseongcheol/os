"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 کوربه 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as چليز_غونډال

목록경로 = "/lib/.pip.json"


def 지문(اومتوک):
    return "".join("%02x" % ارزښت for ارزښت in hashlib.sha256(اومتوک).digest())


def 목록읽기():
    if چليز_غونډال.path_kind(목록경로) == 0:
        return {}
    return json.loads(چليز_غونډال.read(목록경로).decode("utf-8"))


def ليکل_خبرال(يونلور, اومتوک):
    if چليز_غونډال.write(يونلور, اومتوک) != len(اومتوک):
        raise OSError(28)


def کتل_يونلور(يونلور):
    if not isinstance(يونلور, str) or not يونلور.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in يونلور.split("/")):
        raise ValueError("허용하지 않는 꾸러미 يونلور")
    if "\\" in يونلور or any(ord(لوښه_ارزښت) < 32 or ord(لوښه_ارزښت) == 127 for لوښه_ارزښت in يونلور):
        raise ValueError("잘못된 يونلور 문자")
    결과 = "/lib/" + يونلور
    if len(결과.encode("utf-8")) > 63 or يونلور in ("한국어.py", "꾸러미.py"):
        raise ValueError("꾸러미 경로가 너무 길거나 تلواله_ارزښت 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ځغلول = چليز_غونډال.ticks_ms()

    def 정확히읽기(자신, اوږدوالى_ارزښت):
        اومتوک = bytearray()
        while len(اومتوک) < اوږدوالى_ارزښت:
            if چليز_غونډال.ticks_ms() - 자신.ځغلول > 90000:
                raise ValueError("꾸러미 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = چليز_غونډال.tcp_read(자신.종단, 512)
                except OSError as تېروتنه:
                    if تېروتنه.args[0] != 11:
                        raise
                    چليز_غونډال.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("꾸러미 전송이 중간에 끝났습니다.")
            개수 = min(اوږدوالى_ارزښت - len(اومتوک), len(자신.남은자료))
            اومتوک.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            چليز_غونډال.sleep_ms(0)
        return bytes(اومتوک)


def رالېښل(요청, 접속번호):
    if len(요청) > 96 or any(لوښه_ارزښت not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for لوښه_ارزښت in 요청):
        raise ValueError("사용법: pip install نوم 또는 نوم==버전")
    종단 = چليز_غونډال.tcp_open()
    try:
        ځغلول = چليز_غونډال.ticks_ms()
        while True:
            try:
                چليز_غونډال.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as تېروتنه:
                if تېروتنه.args[0] not in (11, 115) or چليز_غونډال.ticks_ms() - ځغلول > 5000:
                    raise ValueError("꾸러미 중계 نښلېدل پاتېينه_ارزښت: 호스트에서 --network --pip로 실행하십시오.")
                چليز_غونډال.sleep_ms(10)
        اومتوک = (요청 + "\n").encode()
        while اومتوک:
            try:
                개수 = چليز_غونډال.tcp_write(종단, اومتوک)
                if not 개수:
                    raise ValueError("꾸러미 요청 لېږدول_ارزښت پاتېينه_ارزښت")
                اومتوک = اومتوک[개수:]
            except OSError as تېروتنه:
                if تېروتنه.args[0] != 11:
                    raise
                چليز_غونډال.sleep_ms(10)
                if چليز_غونډال.ticks_ms() - ځغلول > 10000:
                    raise ValueError("꾸러미 요청 لېږدول_ارزښت 시간 초과")
        بهنګ_ارزښت = 수신흐름(종단)
        머리 = بهنګ_ارزښت.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("꾸러미 لېږدول_ارزښت کیس_ارزښت 불일치")
        اوږدوالى_ارزښت = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if اوږدوالى_ارزښت > 8192:
            raise ValueError("꾸러미 명세가 너무 큽니다.")
        명세 = json.loads(بهنګ_ارزښت.정확히읽기(اوږدوالى_ارزښت).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 سرچینه_ونه 파일은 1~16개여야 합니다.")
        if sum(ننوت_ارزښت["size"] for ننوت_ارزښت in 명세["files"]) > 65536:
            raise ValueError("꾸러미 سرچینه_ونه 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ننوت_ارزښت in 명세["files"]:
            يونلور = کتل_يونلور(ننوت_ارزښت["path"])
            if يونلور in 파일들 or not 0 <= ننوت_ارزښت["size"] <= 16384:
                raise ValueError("중복 يونلور 또는 دوتنه کچ 초과")
            اومتوک = بهنګ_ارزښت.정확히읽기(ننوت_ارزښت["size"])
            if 지문(اومتوک) != ننوت_ارزښت["sha256"]:
                raise ValueError("꾸러미 دوتنه SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(اومتوک.decode("utf-8"), يونلور, "exec")
            파일들[يونلور] = اومتوک
            gc.collect()
        return 명세, 파일들
    finally:
        چليز_غونډال.udp_close(종단)


def لګول_ارزښت(요청, 접속번호):
    print("꾸러미 رالېښل:", 요청)
    명세, 파일들 = رالېښل(요청, 접속번호)
    목록 = 목록읽기()
    نوم = 명세["name"]
    if نوم in 목록:
        if 목록[نوم]["version"] == 명세["version"]:
            for يونلور, 지문값 in 목록[نوم]["files"].items():
                if چليز_غونډال.path_kind(يونلور) != 1 or 지문(چليز_غونډال.read(يونلور)) != 지문값:
                    raise ValueError("설치된 꾸러미 파일이 달라졌습니다: " + يونلور)
            print("이미 설치됨:", نوم, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 뒤 설치하십시오.")
    for يونلور in 파일들:
        if چليز_غونډال.path_kind(يونلور):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + يونلور)
    목록[نوم] = {"version": 명세["version"], "files": {يونلور: 지문(اومتوک) for يونلور, اومتوک in 파일들.items()}}
    새목록 = json.dumps(목록).encode()
    if len(새목록) > 16384:
        raise ValueError("꾸러미 목록 کچ 초과")
    이전목록 = چليز_غونډال.read(목록경로) if چليز_غونډال.path_kind(목록경로) else None
    만든파일 = []
    만든폴더 = []
    try:
        for يونلور, اومتوک in 파일들.items():
            부분들 = يونلور.split("/")
            for 수 in range(2, len(부분들)):
                نوملړ_ارزښت = "/".join(부분들[:수])
                종류 = چليز_غونډال.path_kind(نوملړ_ارزښت)
                if 종류 == 0:
                    چليز_غونډال.mkdir(نوملړ_ارزښت)
                    만든폴더.append(نوملړ_ارزښت)
                elif 종류 != 2:
                    raise ValueError("نوملړ_ارزښت 경로에 파일이 있습니다: " + نوملړ_ارزښت)
            만든파일.append(يونلور)
            ليکل_خبرال(يونلور, اومتوک)
        ليکل_خبرال(목록경로, 새목록)
    except Exception:
        for يونلور in 만든파일:
            if چليز_غونډال.path_kind(يونلور):
                چليز_غونډال.remove(يونلور)
        for نوملړ_ارزښت in reversed(만든폴더):
            چليز_غونډال.rmdir(نوملړ_ارزښت)
        if 이전목록 is not None:
            ليکل_خبرال(목록경로, 이전목록)
        elif چليز_غونډال.path_kind(목록경로):
            چليز_غونډال.remove(목록경로)
        raise
    print("لګول_ارزښت 완료:", نوم, 명세["version"], "→ /lib (RAM)")


def 제거(نوم):
    목록 = 목록읽기()
    if نوم not in 목록:
        raise ValueError("설치되지 않은 꾸러미입니다: " + نوم)
    for يونلور, 지문값 in 목록[نوم]["files"].items():
        if چليز_غونډال.path_kind(يونلور) != 1 or 지문(چليز_غونډال.read(يونلور)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + يونلور)
    for يونلور in 목록[نوم]["files"]:
        چليز_غونډال.remove(يونلور)
    del 목록[نوم]
    ليکل_خبرال(목록경로, json.dumps(목록).encode())
    print("제거 완료:", نوم)


def ځغلول(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for نوم, 정보 in 목록읽기().items():
            print(نوم, 정보["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        لګول_ارزښت(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        제거(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython سرچینه_ونه 설치기 (PyPA pip 전체가 아님)")
        print("pip install نوم[==버전] [--port 8027] | pip list | pip uninstall نوم")
        print("کوربه: 도구/실행.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ځغلول(sys.argv[1:])
    except Exception as تېروتنه:
        print("꾸러미 تېروتنه:", تېروتنه)
        sys.exit(1)
