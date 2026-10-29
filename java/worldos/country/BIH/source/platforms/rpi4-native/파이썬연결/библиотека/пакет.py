"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 хост_рачунар 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as оперативни_систем

списак_пут = "/lib/.pip.json"


def 지문(подаци):
    return "".join("%02x" % вриједност for вриједност in hashlib.sha256(подаци).digest())


def 목록읽기():
    if оперативни_систем.path_kind(списак_пут) == 0:
        return {}
    return json.loads(оперативни_систем.read(списак_пут).decode("utf-8"))


def писати_дневник_рада(пут, подаци):
    if оперативни_систем.write(пут, подаци) != len(подаци):
        raise OSError(28)


def чек_пут(пут):
    if not isinstance(пут, str) or not пут.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in пут.split("/")):
        raise ValueError("허용하지 않는 пакет пут")
    if "\\" in пут or any(ord(знак_вриједност) < 32 or ord(знак_вриједност) == 127 for знак_вриједност in пут):
        raise ValueError("잘못된 пут 문자")
    결과 = "/lib/" + пут
    if len(결과.encode("utf-8")) > 63 or пут in ("한국어.py", "пакет.py"):
        raise ValueError("пакет 경로가 너무 길거나 задана_вриједност 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, крајња_тачка):
        자신.крајња_тачка = крајња_тачка
        자신.남은자료 = b""
        자신.시작 = оперативни_систем.ticks_ms()

    def 정확히읽기(자신, дужина_вриједност):
        подаци = bytearray()
        while len(подаци) < дужина_вриједност:
            if оперативни_систем.ticks_ms() - 자신.시작 > 90000:
                raise ValueError("пакет 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = оперативни_систем.tcp_read(자신.крајња_тачка, 512)
                except OSError as грешка:
                    if грешка.args[0] != 11:
                        raise
                    оперативни_систем.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("пакет 전송이 중간에 끝났습니다.")
            개수 = min(дужина_вриједност - len(подаци), len(자신.남은자료))
            подаци.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            оперативни_систем.sleep_ms(0)
        return bytes(подаци)


def преузети(요청, 접속번호):
    if len(요청) > 96 or any(знак_вриједност not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for знак_вриједност in 요청):
        raise ValueError("사용법: pip install назив 또는 назив==버전")
    крајња_тачка = оперативни_систем.tcp_open()
    try:
        시작 = оперативни_систем.ticks_ms()
        while True:
            try:
                оперативни_систем.tcp_connect(крајња_тачка, "10.0.2.2", 접속번호)
                break
            except OSError as грешка:
                if грешка.args[0] not in (11, 115) or оперативни_систем.ticks_ms() - 시작 > 5000:
                    raise ValueError("пакет 중계 повезати неуспјех_вриједност: 호스트에서 --network --pip로 실행하십시오.")
                оперативни_систем.sleep_ms(10)
        подаци = (요청 + "\n").encode()
        while подаци:
            try:
                개수 = оперативни_систем.tcp_write(крајња_тачка, подаци)
                if not 개수:
                    raise ValueError("пакет 요청 пријенос_вриједност неуспјех_вриједност")
                подаци = подаци[개수:]
            except OSError as грешка:
                if грешка.args[0] != 11:
                    raise
                оперативни_систем.sleep_ms(10)
                if оперативни_систем.ticks_ms() - 시작 > 10000:
                    raise ValueError("пакет 요청 пријенос_вриједност 시간 초과")
        ток_вриједност = 수신흐름(крајња_тачка)
        머리 = ток_вриједност.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("пакет пријенос_вриједност Уговор_вриједност 불일치")
        дужина_вриједност = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if дужина_вриједност > 8192:
            raise ValueError("пакет 명세가 너무 큽니다.")
        명세 = json.loads(ток_вриједност.정확히읽기(дужина_вриједност).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 извор_стабло 파일은 1~16개여야 합니다.")
        if sum(унос_вриједност["size"] for унос_вриједност in 명세["files"]) > 65536:
            raise ValueError("пакет извор_стабло 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for унос_вриједност in 명세["files"]:
            пут = чек_пут(унос_вриједност["path"])
            if пут in 파일들 or not 0 <= унос_вриједност["size"] <= 16384:
                raise ValueError("중복 пут 또는 фајл подесити_величину 초과")
            подаци = ток_вриједност.정확히읽기(унос_вриједност["size"])
            if 지문(подаци) != унос_вриједност["sha256"]:
                raise ValueError("пакет фајл SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(подаци.decode("utf-8"), пут, "exec")
            파일들[пут] = подаци
            gc.collect()
        return 명세, 파일들
    finally:
        оперативни_систем.udp_close(крајња_тачка)


def инсталирати_вриједност(요청, 접속번호):
    print("пакет преузети:", 요청)
    명세, 파일들 = преузети(요청, 접속번호)
    унос_списак = 목록읽기()
    назив = 명세["name"]
    if назив in унос_списак:
        if унос_списак[назив]["version"] == 명세["version"]:
            for пут, 지문값 in унос_списак[назив]["files"].items():
                if оперативни_систем.path_kind(пут) != 1 or 지문(оперативни_систем.read(пут)) != 지문값:
                    raise ValueError("설치된 пакет 파일이 달라졌습니다: " + пут)
            print("이미 설치됨:", назив, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Назад_вриједност 설치하십시오.")
    for пут in 파일들:
        if оперативни_систем.path_kind(пут):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + пут)
    унос_списак[назив] = {"version": 명세["version"], "files": {пут: 지문(подаци) for пут, подаци in 파일들.items()}}
    새목록 = json.dumps(унос_списак).encode()
    if len(새목록) > 16384:
        raise ValueError("пакет унос_списак подесити_величину 초과")
    이전목록 = оперативни_систем.read(списак_пут) if оперативни_систем.path_kind(списак_пут) else None
    만든파일 = []
    만든폴더 = []
    try:
        for пут, подаци in 파일들.items():
            부분들 = пут.split("/")
            for 수 in range(2, len(부분들)):
                директориј_вриједност = "/".join(부분들[:수])
                종류 = оперативни_систем.path_kind(директориј_вриједност)
                if 종류 == 0:
                    оперативни_систем.mkdir(директориј_вриједност)
                    만든폴더.append(директориј_вриједност)
                elif 종류 != 2:
                    raise ValueError("директориј_вриједност 경로에 파일이 있습니다: " + директориј_вриједност)
            만든파일.append(пут)
            писати_дневник_рада(пут, подаци)
        писати_дневник_рада(списак_пут, 새목록)
    except Exception:
        for пут in 만든파일:
            if оперативни_систем.path_kind(пут):
                оперативни_систем.remove(пут)
        for директориј_вриједност in reversed(만든폴더):
            оперативни_систем.rmdir(директориј_вриједност)
        if 이전목록 is not None:
            писати_дневник_рада(списак_пут, 이전목록)
        elif оперативни_систем.path_kind(списак_пут):
            оперативни_систем.remove(списак_пут)
        raise
    print("инсталирати_вриједност 완료:", назив, 명세["version"], "→ /lib (RAM)")


def уклонити_унос(назив):
    унос_списак = 목록읽기()
    if назив not in унос_списак:
        raise ValueError("설치되지 않은 꾸러미입니다: " + назив)
    for пут, 지문값 in унос_списак[назив]["files"].items():
        if оперативни_систем.path_kind(пут) != 1 or 지문(оперативни_систем.read(пут)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + пут)
    for пут in унос_списак[назив]["files"]:
        оперативни_систем.remove(пут)
    del унос_списак[назив]
    писати_дневник_рада(списак_пут, json.dumps(унос_списак).encode())
    print("уклонити_унос 완료:", назив)


def 시작(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for назив, систем_информација in 목록읽기().items():
            print(назив, систем_информација["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        инсталирати_вриједност(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        уклонити_унос(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython извор_стабло 설치기 (PyPA pip 전체가 아님)")
        print("pip install назив[==버전] [--port 8027] | pip list | pip uninstall назив")
        print("хост_рачунар: 도구/실행.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        시작(sys.argv[1:])
    except Exception as грешка:
        print("пакет грешка:", грешка)
        sys.exit(1)
