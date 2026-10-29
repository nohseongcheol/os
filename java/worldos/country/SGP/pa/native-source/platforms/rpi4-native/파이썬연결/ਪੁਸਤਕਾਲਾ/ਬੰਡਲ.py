"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ਹੋਸਟ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ਸਿਸਟਮ_ਚਲਾਉਣਾ

ਸੂਚੀ_ਰਸਤਾ = "/lib/.pip.json"


def 지문(ਸਮੱਗਰੀ):
    return "".join("%02x" % ਕੀਮਤ for ਕੀਮਤ in hashlib.sha256(ਸਮੱਗਰੀ).digest())


def 목록읽기():
    if ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਸੂਚੀ_ਰਸਤਾ) == 0:
        return {}
    return json.loads(ਸਿਸਟਮ_ਚਲਾਉਣਾ.read(ਸੂਚੀ_ਰਸਤਾ).decode("utf-8"))


def ਲਿੱਖੋ_ਲੌਗ(ਮਾਰਗ, ਸਮੱਗਰੀ):
    if ਸਿਸਟਮ_ਚਲਾਉਣਾ.write(ਮਾਰਗ, ਸਮੱਗਰੀ) != len(ਸਮੱਗਰੀ):
        raise OSError(28)


def ਚੈਕ_ਕਰੋ_ਰਸਤਾ(ਮਾਰਗ):
    if not isinstance(ਮਾਰਗ, str) or not ਮਾਰਗ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ਮਾਰਗ.split("/")):
        raise ValueError("허용하지 않는 ਬੰਡਲ ਮਾਰਗ")
    if "\\" in ਮਾਰਗ or any(ord(ਵਰਣ_ਕੀਮਤ) < 32 or ord(ਵਰਣ_ਕੀਮਤ) == 127 for ਵਰਣ_ਕੀਮਤ in ਮਾਰਗ):
        raise ValueError("잘못된 ਮਾਰਗ 문자")
    ਮਾਪ = "/lib/" + ਮਾਰਗ
    if len(ਮਾਪ.encode("utf-8")) > 63 or ਮਾਰਗ in ("ਪੰਜਾਬੀ.py", "ਬੰਡਲ.py"):
        raise ValueError("ਬੰਡਲ 경로가 너무 길거나 ਡਿਫੌਲਟ_ਵੈਲਯੂ 라이브러리와 겹칩니다.")
    return ਮਾਪ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ਚਲਾਓ_2 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.ticks_ms()

    def 정확히읽기(자신, ਲੰਬਾਈ_ਕੀਮਤ):
        ਸਮੱਗਰੀ = bytearray()
        while len(ਸਮੱਗਰੀ) < ਲੰਬਾਈ_ਕੀਮਤ:
            if ਸਿਸਟਮ_ਚਲਾਉਣਾ.ticks_ms() - 자신.ਚਲਾਓ_2 > 90000:
                raise ValueError("ਬੰਡਲ 중계 ਜਵਾਬ_ਦਿਓ 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.tcp_read(자신.종단, 512)
                except OSError as ਗਲਤੀ:
                    if ਗਲਤੀ.args[0] != 11:
                        raise
                    ਸਿਸਟਮ_ਚਲਾਉਣਾ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ਬੰਡਲ 전송이 중간에 끝났습니다.")
            개수 = min(ਲੰਬਾਈ_ਕੀਮਤ - len(ਸਮੱਗਰੀ), len(자신.남은자료))
            ਸਮੱਗਰੀ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ਸਿਸਟਮ_ਚਲਾਉਣਾ.sleep_ms(0)
        return bytes(ਸਮੱਗਰੀ)


def ਡਾਉਨਲਡ(요청, 접속번호):
    if len(요청) > 96 or any(ਵਰਣ_ਕੀਮਤ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ਵਰਣ_ਕੀਮਤ in 요청):
        raise ValueError("사용법: pip install ਨਾਂ 또는 ਨਾਂ==버전")
    종단 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.tcp_open()
    try:
        ਚਲਾਓ_2 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.ticks_ms()
        while True:
            try:
                ਸਿਸਟਮ_ਚਲਾਉਣਾ.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as ਗਲਤੀ:
                if ਗਲਤੀ.args[0] not in (11, 115) or ਸਿਸਟਮ_ਚਲਾਉਣਾ.ticks_ms() - ਚਲਾਓ_2 > 5000:
                    raise ValueError("ਬੰਡਲ 중계 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ ਅਸਫਲ_ਕੀਮਤ: 호스트에서 --network --pip로 실행하십시오.")
                ਸਿਸਟਮ_ਚਲਾਉਣਾ.sleep_ms(10)
        ਸਮੱਗਰੀ = (요청 + "\n").encode()
        while ਸਮੱਗਰੀ:
            try:
                개수 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.tcp_write(종단, ਸਮੱਗਰੀ)
                if not 개수:
                    raise ValueError("ਬੰਡਲ 요청 ਸਥਾਂਨਤਰ_ਕੀਮਤ ਅਸਫਲ_ਕੀਮਤ")
                ਸਮੱਗਰੀ = ਸਮੱਗਰੀ[개수:]
            except OSError as ਗਲਤੀ:
                if ਗਲਤੀ.args[0] != 11:
                    raise
                ਸਿਸਟਮ_ਚਲਾਉਣਾ.sleep_ms(10)
                if ਸਿਸਟਮ_ਚਲਾਉਣਾ.ticks_ms() - ਚਲਾਓ_2 > 10000:
                    raise ValueError("ਬੰਡਲ 요청 ਸਥਾਂਨਤਰ_ਕੀਮਤ 시간 초과")
        ਸਟ੍ਰੀਮ_ਕੀਮਤ = 수신흐름(종단)
        머리 = ਸਟ੍ਰੀਮ_ਕੀਮਤ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ਬੰਡਲ ਸਥਾਂਨਤਰ_ਕੀਮਤ ਕੰਮ_ਕੀਮਤ 불일치")
        ਲੰਬਾਈ_ਕੀਮਤ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ਲੰਬਾਈ_ਕੀਮਤ > 8192:
            raise ValueError("ਬੰਡਲ 명세가 너무 큽니다.")
        명세 = json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.정확히읽기(ਲੰਬਾਈ_ਕੀਮਤ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ਸਰੋਤ_ਟ੍ਰੀ 파일은 1~16개여야 합니다.")
        if sum(ਦਾਖਲਾ_ਕੀਮਤ["size"] for ਦਾਖਲਾ_ਕੀਮਤ in 명세["files"]) > 65536:
            raise ValueError("ਬੰਡਲ ਸਰੋਤ_ਟ੍ਰੀ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ਦਾਖਲਾ_ਕੀਮਤ in 명세["files"]:
            ਮਾਰਗ = ਚੈਕ_ਕਰੋ_ਰਸਤਾ(ਦਾਖਲਾ_ਕੀਮਤ["path"])
            if ਮਾਰਗ in 파일들 or not 0 <= ਦਾਖਲਾ_ਕੀਮਤ["size"] <= 16384:
                raise ValueError("중복 ਮਾਰਗ 또는 ਫਾਇਲ ਆਕਾਰ 초과")
            ਸਮੱਗਰੀ = ਸਟ੍ਰੀਮ_ਕੀਮਤ.정확히읽기(ਦਾਖਲਾ_ਕੀਮਤ["size"])
            if 지문(ਸਮੱਗਰੀ) != ਦਾਖਲਾ_ਕੀਮਤ["sha256"]:
                raise ValueError("ਬੰਡਲ ਫਾਇਲ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ਸਮੱਗਰੀ.decode("utf-8"), ਮਾਰਗ, "exec")
            파일들[ਮਾਰਗ] = ਸਮੱਗਰੀ
            gc.collect()
        return 명세, 파일들
    finally:
        ਸਿਸਟਮ_ਚਲਾਉਣਾ.udp_close(종단)


def ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ(요청, 접속번호):
    print("ਬੰਡਲ ਡਾਉਨਲਡ:", 요청)
    명세, 파일들 = ਡਾਉਨਲਡ(요청, 접속번호)
    ਦਾਖਲਾ_ਸੂਚੀ = 목록읽기()
    ਨਾਂ = 명세["name"]
    if ਨਾਂ in ਦਾਖਲਾ_ਸੂਚੀ:
        if ਦਾਖਲਾ_ਸੂਚੀ[ਨਾਂ]["version"] == 명세["version"]:
            for ਮਾਰਗ, 지문값 in ਦਾਖਲਾ_ਸੂਚੀ[ਨਾਂ]["files"].items():
                if ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਮਾਰਗ) != 1 or 지문(ਸਿਸਟਮ_ਚਲਾਉਣਾ.read(ਮਾਰਗ)) != 지문값:
                    raise ValueError("설치된 ਬੰਡਲ 파일이 달라졌습니다: " + ਮਾਰਗ)
            print("이미 설치됨:", ਨਾਂ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ਪਿਛਲਾ_ਕੀਮਤ 설치하십시오.")
    for ਮਾਰਗ in 파일들:
        if ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਮਾਰਗ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ਮਾਰਗ)
    ਦਾਖਲਾ_ਸੂਚੀ[ਨਾਂ] = {"version": 명세["version"], "files": {ਮਾਰਗ: 지문(ਸਮੱਗਰੀ) for ਮਾਰਗ, ਸਮੱਗਰੀ in 파일들.items()}}
    새목록 = json.dumps(ਦਾਖਲਾ_ਸੂਚੀ).encode()
    if len(새목록) > 16384:
        raise ValueError("ਬੰਡਲ ਦਾਖਲਾ_ਸੂਚੀ ਆਕਾਰ 초과")
    이전목록 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.read(ਸੂਚੀ_ਰਸਤਾ) if ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਸੂਚੀ_ਰਸਤਾ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ਮਾਰਗ, ਸਮੱਗਰੀ in 파일들.items():
            부분들 = ਮਾਰਗ.split("/")
            for 수 in range(2, len(부분들)):
                ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ = "/".join(부분들[:수])
                종류 = ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)
                if 종류 == 0:
                    ਸਿਸਟਮ_ਚਲਾਉਣਾ.mkdir(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)
                    만든폴더.append(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)
                elif 종류 != 2:
                    raise ValueError("ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ 경로에 파일이 있습니다: " + ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)
            만든파일.append(ਮਾਰਗ)
            ਲਿੱਖੋ_ਲੌਗ(ਮਾਰਗ, ਸਮੱਗਰੀ)
        ਲਿੱਖੋ_ਲੌਗ(ਸੂਚੀ_ਰਸਤਾ, 새목록)
    except Exception:
        for ਮਾਰਗ in 만든파일:
            if ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਮਾਰਗ):
                ਸਿਸਟਮ_ਚਲਾਉਣਾ.remove(ਮਾਰਗ)
        for ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ in reversed(만든폴더):
            ਸਿਸਟਮ_ਚਲਾਉਣਾ.rmdir(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ)
        if 이전목록 is not None:
            ਲਿੱਖੋ_ਲੌਗ(ਸੂਚੀ_ਰਸਤਾ, 이전목록)
        elif ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਸੂਚੀ_ਰਸਤਾ):
            ਸਿਸਟਮ_ਚਲਾਉਣਾ.remove(ਸੂਚੀ_ਰਸਤਾ)
        raise
    print("ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ 완료:", ਨਾਂ, 명세["version"], "→ /lib (RAM)")


def ਹਟਾਉਣਾ_ਦਾਖਲਾ(ਨਾਂ):
    ਦਾਖਲਾ_ਸੂਚੀ = 목록읽기()
    if ਨਾਂ not in ਦਾਖਲਾ_ਸੂਚੀ:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ਨਾਂ)
    for ਮਾਰਗ, 지문값 in ਦਾਖਲਾ_ਸੂਚੀ[ਨਾਂ]["files"].items():
        if ਸਿਸਟਮ_ਚਲਾਉਣਾ.path_kind(ਮਾਰਗ) != 1 or 지문(ਸਿਸਟਮ_ਚਲਾਉਣਾ.read(ਮਾਰਗ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ਮਾਰਗ)
    for ਮਾਰਗ in ਦਾਖਲਾ_ਸੂਚੀ[ਨਾਂ]["files"]:
        ਸਿਸਟਮ_ਚਲਾਉਣਾ.remove(ਮਾਰਗ)
    del ਦਾਖਲਾ_ਸੂਚੀ[ਨਾਂ]
    ਲਿੱਖੋ_ਲੌਗ(ਸੂਚੀ_ਰਸਤਾ, json.dumps(ਦਾਖਲਾ_ਸੂਚੀ).encode())
    print("ਹਟਾਉਣਾ_ਦਾਖਲਾ 완료:", ਨਾਂ)


def ਚਲਾਓ_2(ਆਰਗੂਮੈਂਟ):
    접속번호 = 8027
    if len(ਆਰਗੂਮੈਂਟ) >= 2 and ਆਰਗੂਮੈਂਟ[-2] == "--port":
        접속번호 = int(ਆਰਗੂਮੈਂਟ[-1])
        ਆਰਗੂਮੈਂਟ = ਆਰਗੂਮੈਂਟ[:-2]
    if ਆਰਗੂਮੈਂਟ == ["list"]:
        for ਨਾਂ, ਸਿਸਟਮ_ਜਾਣਕਾਰੀ in 목록읽기().items():
            print(ਨਾਂ, ਸਿਸਟਮ_ਜਾਣਕਾਰੀ["version"])
    elif len(ਆਰਗੂਮੈਂਟ) == 2 and ਆਰਗੂਮੈਂਟ[0] == "install":
        ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ(ਆਰਗੂਮੈਂਟ[1], 접속번호)
    elif len(ਆਰਗੂਮੈਂਟ) == 2 and ਆਰਗੂਮੈਂਟ[0] == "uninstall":
        ਹਟਾਉਣਾ_ਦਾਖਲਾ(ਆਰਗੂਮੈਂਟ[1])
    elif not ਆਰਗੂਮੈਂਟ or ਆਰਗੂਮੈਂਟ in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ਸਰੋਤ_ਟ੍ਰੀ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ਨਾਂ[==버전] [--port 8027] | pip list | pip uninstall ਨਾਂ")
        print("ਹੋਸਟ: ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ਚਲਾਓ_2(sys.argv[1:])
    except Exception as ਗਲਤੀ:
        print("ਬੰਡਲ ਗਲਤੀ:", ਗਲਤੀ)
        sys.exit(1)
