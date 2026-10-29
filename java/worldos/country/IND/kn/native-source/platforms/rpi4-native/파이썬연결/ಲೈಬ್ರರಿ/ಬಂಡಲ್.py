"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ಹೋಸ್ಟ್ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ

ಪಟ್ಟಿ_ಹಾದಿ = "/lib/.pip.json"


def 지문(ಡೇಟಾ):
    return "".join("%02x" % ಮೌಲ್ಯ for ಮೌಲ್ಯ in hashlib.sha256(ಡೇಟಾ).digest())


def 목록읽기():
    if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಪಟ್ಟಿ_ಹಾದಿ) == 0:
        return {}
    return json.loads(ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.read(ಪಟ್ಟಿ_ಹಾದಿ).decode("utf-8"))


def ಬರೆ_ಲಾಗ್(ಮಾರ್ಗ, ಡೇಟಾ):
    if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.write(ಮಾರ್ಗ, ಡೇಟಾ) != len(ಡೇಟಾ):
        raise OSError(28)


def ಚೆಕ್_ಹಾದಿ(ಮಾರ್ಗ):
    if not isinstance(ಮಾರ್ಗ, str) or not ಮಾರ್ಗ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ಮಾರ್ಗ.split("/")):
        raise ValueError("허용하지 않는 ಬಂಡಲ್ ಮಾರ್ಗ")
    if "\\" in ಮಾರ್ಗ or any(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) < 32 or ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) == 127 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಮಾರ್ಗ):
        raise ValueError("잘못된 ಮಾರ್ಗ 문자")
    ಮಾಪನ = "/lib/" + ಮಾರ್ಗ
    if len(ಮಾಪನ.encode("utf-8")) > 63 or ಮಾರ್ಗ in ("ಕನ್ನಡ.py", "ಬಂಡಲ್.py"):
        raise ValueError("ಬಂಡಲ್ 경로가 너무 길거나 ಅಕ್ಷಮ_ಬೆಲೆ 라이브러리와 겹칩니다.")
    return ಮಾಪನ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ಚಲಾಯಿಸು_2 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.ticks_ms()

    def 정확히읽기(자신, ಉದ್ದ_ಮೌಲ್ಯ):
        ಡೇಟಾ = bytearray()
        while len(ಡೇಟಾ) < ಉದ್ದ_ಮೌಲ್ಯ:
            if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.ticks_ms() - 자신.ಚಲಾಯಿಸು_2 > 90000:
                raise ValueError("ಬಂಡಲ್ 중계 ಪ್ರತ್ಯುತ್ತರ ಸಮಯ_ಮೌಲ್ಯ 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.tcp_read(자신.종단, 512)
                except OSError as ದೋಷ:
                    if ದೋಷ.args[0] != 11:
                        raise
                    ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ಬಂಡಲ್ 전송이 중간에 끝났습니다.")
            개수 = min(ಉದ್ದ_ಮೌಲ್ಯ - len(ಡೇಟಾ), len(자신.남은자료))
            ಡೇಟಾ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.sleep_ms(0)
        return bytes(ಡೇಟಾ)


def ಡೌನ್_ಲೋಡ್(요청, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ):
    if len(요청) > 96 or any(ಅಕ್ಷರ_ಮೌಲ್ಯ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ಅಕ್ಷರ_ಮೌಲ್ಯ in 요청):
        raise ValueError("사용법: pip install ಹೆಸರು 또는 ಹೆಸರು==버전")
    종단 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.tcp_open()
    try:
        ಚಲಾಯಿಸು_2 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.ticks_ms()
        while True:
            try:
                ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.tcp_connect(종단, "10.0.2.2", ಪೋರ್ಟ್_ಸಂಖ್ಯೆ)
                break
            except OSError as ದೋಷ:
                if ದೋಷ.args[0] not in (11, 115) or ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.ticks_ms() - ಚಲಾಯಿಸು_2 > 5000:
                    raise ValueError("ಬಂಡಲ್ 중계 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು ವೈಫಲ್ಯ_ಮೌಲ್ಯ: 호스트에서 --network --pip로 실행하십시오.")
                ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.sleep_ms(10)
        ಡೇಟಾ = (요청 + "\n").encode()
        while ಡೇಟಾ:
            try:
                개수 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.tcp_write(종단, ಡೇಟಾ)
                if not 개수:
                    raise ValueError("ಬಂಡಲ್ 요청 ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ ವೈಫಲ್ಯ_ಮೌಲ್ಯ")
                ಡೇಟಾ = ಡೇಟಾ[개수:]
            except OSError as ದೋಷ:
                if ದೋಷ.args[0] != 11:
                    raise
                ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.sleep_ms(10)
                if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.ticks_ms() - ಚಲಾಯಿಸು_2 > 10000:
                    raise ValueError("ಬಂಡಲ್ 요청 ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ ಸಮಯ_ಮೌಲ್ಯ 초과")
        ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ = 수신흐름(종단)
        머리 = ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ಬಂಡಲ್ ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ ಕೆಲಸ_ಮೌಲ್ಯ 불일치")
        ಉದ್ದ_ಮೌಲ್ಯ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ಉದ್ದ_ಮೌಲ್ಯ > 8192:
            raise ValueError("ಬಂಡಲ್ 명세가 너무 큽니다.")
        명세 = json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.정확히읽기(ಉದ್ದ_ಮೌಲ್ಯ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ಮೂಲ_ವೃಕ್ಷ 파일은 1~16개여야 합니다.")
        if sum(ನಮೂದು_ಮೌಲ್ಯ["size"] for ನಮೂದು_ಮೌಲ್ಯ in 명세["files"]) > 65536:
            raise ValueError("ಬಂಡಲ್ ಮೂಲ_ವೃಕ್ಷ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ನಮೂದು_ಮೌಲ್ಯ in 명세["files"]:
            ಮಾರ್ಗ = ಚೆಕ್_ಹಾದಿ(ನಮೂದು_ಮೌಲ್ಯ["path"])
            if ಮಾರ್ಗ in 파일들 or not 0 <= ನಮೂದು_ಮೌಲ್ಯ["size"] <= 16384:
                raise ValueError("중복 ಮಾರ್ಗ 또는 ಕಡತ ಗಾತ್ರ 초과")
            ಡೇಟಾ = ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.정확히읽기(ನಮೂದು_ಮೌಲ್ಯ["size"])
            if 지문(ಡೇಟಾ) != ನಮೂದು_ಮೌಲ್ಯ["sha256"]:
                raise ValueError("ಬಂಡಲ್ ಕಡತ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ಡೇಟಾ.decode("utf-8"), ಮಾರ್ಗ, "exec")
            파일들[ಮಾರ್ಗ] = ಡೇಟಾ
            gc.collect()
        return 명세, 파일들
    finally:
        ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.udp_close(종단)


def ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ(요청, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ):
    print("ಬಂಡಲ್ ಡೌನ್_ಲೋಡ್:", 요청)
    명세, 파일들 = ಡೌನ್_ಲೋಡ್(요청, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ)
    ನಮೂದು_ಪಟ್ಟಿ = 목록읽기()
    ಹೆಸರು = 명세["name"]
    if ಹೆಸರು in ನಮೂದು_ಪಟ್ಟಿ:
        if ನಮೂದು_ಪಟ್ಟಿ[ಹೆಸರು]["version"] == 명세["version"]:
            for ಮಾರ್ಗ, 지문값 in ನಮೂದು_ಪಟ್ಟಿ[ಹೆಸರು]["files"].items():
                if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಮಾರ್ಗ) != 1 or 지문(ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.read(ಮಾರ್ಗ)) != 지문값:
                    raise ValueError("설치된 ಬಂಡಲ್ 파일이 달라졌습니다: " + ಮಾರ್ಗ)
            print("이미 설치됨:", ಹೆಸರು, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ಹಿಂದೆ_ಮೌಲ್ಯ 설치하십시오.")
    for ಮಾರ್ಗ in 파일들:
        if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಮಾರ್ಗ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ಮಾರ್ಗ)
    ನಮೂದು_ಪಟ್ಟಿ[ಹೆಸರು] = {"version": 명세["version"], "files": {ಮಾರ್ಗ: 지문(ಡೇಟಾ) for ಮಾರ್ಗ, ಡೇಟಾ in 파일들.items()}}
    새목록 = json.dumps(ನಮೂದು_ಪಟ್ಟಿ).encode()
    if len(새목록) > 16384:
        raise ValueError("ಬಂಡಲ್ ನಮೂದು_ಪಟ್ಟಿ ಗಾತ್ರ 초과")
    이전목록 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.read(ಪಟ್ಟಿ_ಹಾದಿ) if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಪಟ್ಟಿ_ಹಾದಿ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ಮಾರ್ಗ, ಡೇಟಾ in 파일들.items():
            부분들 = ಮಾರ್ಗ.split("/")
            for 수 in range(2, len(부분들)):
                ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ = "/".join(부분들[:수])
                종류 = ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)
                if 종류 == 0:
                    ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.mkdir(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)
                    만든폴더.append(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)
                elif 종류 != 2:
                    raise ValueError("ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ 경로에 파일이 있습니다: " + ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)
            만든파일.append(ಮಾರ್ಗ)
            ಬರೆ_ಲಾಗ್(ಮಾರ್ಗ, ಡೇಟಾ)
        ಬರೆ_ಲಾಗ್(ಪಟ್ಟಿ_ಹಾದಿ, 새목록)
    except Exception:
        for ಮಾರ್ಗ in 만든파일:
            if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಮಾರ್ಗ):
                ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.remove(ಮಾರ್ಗ)
        for ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ in reversed(만든폴더):
            ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.rmdir(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ)
        if 이전목록 is not None:
            ಬರೆ_ಲಾಗ್(ಪಟ್ಟಿ_ಹಾದಿ, 이전목록)
        elif ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಪಟ್ಟಿ_ಹಾದಿ):
            ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.remove(ಪಟ್ಟಿ_ಹಾದಿ)
        raise
    print("ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ 완료:", ಹೆಸರು, 명세["version"], "→ /lib (RAM)")


def ತೆಗೆ_ನಮೂದು(ಹೆಸರು):
    ನಮೂದು_ಪಟ್ಟಿ = 목록읽기()
    if ಹೆಸರು not in ನಮೂದು_ಪಟ್ಟಿ:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ಹೆಸರು)
    for ಮಾರ್ಗ, 지문값 in ನಮೂದು_ಪಟ್ಟಿ[ಹೆಸರು]["files"].items():
        if ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.path_kind(ಮಾರ್ಗ) != 1 or 지문(ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.read(ಮಾರ್ಗ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ಮಾರ್ಗ)
    for ಮಾರ್ಗ in ನಮೂದು_ಪಟ್ಟಿ[ಹೆಸರು]["files"]:
        ಆಪರೇಟಿಂಗ್_ಸಿಸ್ಟಂ.remove(ಮಾರ್ಗ)
    del ನಮೂದು_ಪಟ್ಟಿ[ಹೆಸರು]
    ಬರೆ_ಲಾಗ್(ಪಟ್ಟಿ_ಹಾದಿ, json.dumps(ನಮೂದು_ಪಟ್ಟಿ).encode())
    print("ತೆಗೆ_ನಮೂದು 완료:", ಹೆಸರು)


def ಚಲಾಯಿಸು_2(인수):
    ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ಹೆಸರು, ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ in 목록읽기().items():
            print(ಹೆಸರು, ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ(인수[1], ಪೋರ್ಟ್_ಸಂಖ್ಯೆ)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ತೆಗೆ_ನಮೂದು(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ಮೂಲ_ವೃಕ್ಷ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ಹೆಸರು[==버전] [--port 8027] | pip list | pip uninstall ಹೆಸರು")
        print("ಹೋಸ್ಟ್: ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ಚಲಾಯಿಸು_2(sys.argv[1:])
    except Exception as ದೋಷ:
        print("ಬಂಡಲ್ ದೋಷ:", ದೋಷ)
        sys.exit(1)
