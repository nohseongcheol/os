"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 호스트 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as 운영체제

목록경로 = "/lib/.pip.json"


def 지문(자료):
    return "".join("%02x" % 값 for 값 in hashlib.sha256(자료).digest())


def 목록읽기():
    if 운영체제.path_kind(목록경로) == 0:
        return {}
    return json.loads(운영체제.read(목록경로).decode("utf-8"))


def 기록쓰기(Yolçıq, 자료):
    if 운영체제.write(Yolçıq, 자료) != len(자료):
        raise OSError(28)


def 경로검사(Yolçıq):
    if not isinstance(Yolçıq, str) or not Yolçıq.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Yolçıq.split("/")):
        raise ValueError("허용하지 않는 꾸러미 Yolçıq")
    if "\\" in Yolçıq or any(ord(글자) < 32 or ord(글자) == 127 for 글자 in Yolçıq):
        raise ValueError("잘못된 Yolçıq 문자")
    결과 = "/lib/" + Yolçıq
    if len(결과.encode("utf-8")) > 63 or Yolçıq in ("한국어.py", "꾸러미.py"):
        raise ValueError("꾸러미 경로가 너무 길거나 기본 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Çaptır = 운영체제.ticks_ms()

    def 정확히읽기(자신, 길이):
        자료 = bytearray()
        while len(자료) < 길이:
            if 운영체제.ticks_ms() - 자신.Çaptır > 90000:
                raise ValueError("꾸러미 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = 운영체제.tcp_read(자신.종단, 512)
                except OSError as Hata:
                    if Hata.args[0] != 11:
                        raise
                    운영체제.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("꾸러미 전송이 중간에 끝났습니다.")
            개수 = min(길이 - len(자료), len(자신.남은자료))
            자료.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            운영체제.sleep_ms(0)
        return bytes(자료)


def 내려받기(요청, 접속번호):
    if len(요청) > 96 or any(글자 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for 글자 in 요청):
        raise ValueError("사용법: pip install İsim 또는 İsim==버전")
    종단 = 운영체제.tcp_open()
    try:
        Çaptır = 운영체제.ticks_ms()
        while True:
            try:
                운영체제.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Hata:
                if Hata.args[0] not in (11, 115) or 운영체제.ticks_ms() - Çaptır > 5000:
                    raise ValueError("꾸러미 중계 Bağlan 실패: 호스트에서 --network --pip로 실행하십시오.")
                운영체제.sleep_ms(10)
        자료 = (요청 + "\n").encode()
        while 자료:
            try:
                개수 = 운영체제.tcp_write(종단, 자료)
                if not 개수:
                    raise ValueError("꾸러미 요청 전송 실패")
                자료 = 자료[개수:]
            except OSError as Hata:
                if Hata.args[0] != 11:
                    raise
                운영체제.sleep_ms(10)
                if 운영체제.ticks_ms() - Çaptır > 10000:
                    raise ValueError("꾸러미 요청 전송 시간 초과")
        흐름 = 수신흐름(종단)
        머리 = 흐름.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("꾸러미 전송 규약 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("꾸러미 명세가 너무 큽니다.")
        명세 = json.loads(흐름.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 소스 파일은 1~16개여야 합니다.")
        if sum(항목["size"] for 항목 in 명세["files"]) > 65536:
            raise ValueError("꾸러미 소스 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for 항목 in 명세["files"]:
            Yolçıq = 경로검사(항목["path"])
            if Yolçıq in 파일들 or not 0 <= 항목["size"] <= 16384:
                raise ValueError("중복 Yolçıq 또는 Dosya Boyut 초과")
            자료 = 흐름.정확히읽기(항목["size"])
            if 지문(자료) != 항목["sha256"]:
                raise ValueError("꾸러미 Dosya SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(자료.decode("utf-8"), Yolçıq, "exec")
            파일들[Yolçıq] = 자료
            gc.collect()
        return 명세, 파일들
    finally:
        운영체제.udp_close(종단)


def 설치(요청, 접속번호):
    print("꾸러미 내려받기:", 요청)
    명세, 파일들 = 내려받기(요청, 접속번호)
    목록 = 목록읽기()
    İsim = 명세["name"]
    if İsim in 목록:
        if 목록[İsim]["version"] == 명세["version"]:
            for Yolçıq, 지문값 in 목록[İsim]["files"].items():
                if 운영체제.path_kind(Yolçıq) != 1 or 지문(운영체제.read(Yolçıq)) != 지문값:
                    raise ValueError("설치된 꾸러미 파일이 달라졌습니다: " + Yolçıq)
            print("이미 설치됨:", İsim, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 뒤 설치하십시오.")
    for Yolçıq in 파일들:
        if 운영체제.path_kind(Yolçıq):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Yolçıq)
    목록[İsim] = {"version": 명세["version"], "files": {Yolçıq: 지문(자료) for Yolçıq, 자료 in 파일들.items()}}
    새목록 = json.dumps(목록).encode()
    if len(새목록) > 16384:
        raise ValueError("꾸러미 목록 Boyut 초과")
    이전목록 = 운영체제.read(목록경로) if 운영체제.path_kind(목록경로) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Yolçıq, 자료 in 파일들.items():
            부분들 = Yolçıq.split("/")
            for 수 in range(2, len(부분들)):
                폴더 = "/".join(부분들[:수])
                종류 = 운영체제.path_kind(폴더)
                if 종류 == 0:
                    운영체제.mkdir(폴더)
                    만든폴더.append(폴더)
                elif 종류 != 2:
                    raise ValueError("폴더 경로에 파일이 있습니다: " + 폴더)
            만든파일.append(Yolçıq)
            기록쓰기(Yolçıq, 자료)
        기록쓰기(목록경로, 새목록)
    except Exception:
        for Yolçıq in 만든파일:
            if 운영체제.path_kind(Yolçıq):
                운영체제.remove(Yolçıq)
        for 폴더 in reversed(만든폴더):
            운영체제.rmdir(폴더)
        if 이전목록 is not None:
            기록쓰기(목록경로, 이전목록)
        elif 운영체제.path_kind(목록경로):
            운영체제.remove(목록경로)
        raise
    print("설치 완료:", İsim, 명세["version"], "→ /lib (RAM)")


def 제거(İsim):
    목록 = 목록읽기()
    if İsim not in 목록:
        raise ValueError("설치되지 않은 꾸러미입니다: " + İsim)
    for Yolçıq, 지문값 in 목록[İsim]["files"].items():
        if 운영체제.path_kind(Yolçıq) != 1 or 지문(운영체제.read(Yolçıq)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Yolçıq)
    for Yolçıq in 목록[İsim]["files"]:
        운영체제.remove(Yolçıq)
    del 목록[İsim]
    기록쓰기(목록경로, json.dumps(목록).encode())
    print("제거 완료:", İsim)


def Çaptır(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for İsim, 정보 in 목록읽기().items():
            print(İsim, 정보["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        설치(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        제거(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython 소스 설치기 (PyPA pip 전체가 아님)")
        print("pip install İsim[==버전] [--port 8027] | pip list | pip uninstall İsim")
        print("호스트: 도구/실행.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Çaptır(sys.argv[1:])
    except Exception as Hata:
        print("꾸러미 Hata:", Hata)
        sys.exit(1)
