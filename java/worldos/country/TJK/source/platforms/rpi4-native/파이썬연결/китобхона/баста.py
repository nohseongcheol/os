"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 мизбон 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as системаи_омил

Рӯйхат_масир = "/lib/.pip.json"


def 지문(иттилоот):
    return "".join("%02x" % қимат for қимат in hashlib.sha256(иттилоот).digest())


def 목록읽기():
    if системаи_омил.path_kind(Рӯйхат_масир) == 0:
        return {}
    return json.loads(системаи_омил.read(Рӯйхат_масир).decode("utf-8"))


def навиштан_сабт_кардан(масир, иттилоот):
    if системаи_омил.write(масир, иттилоот) != len(иттилоот):
        raise OSError(28)


def санҷиш_масир(масир):
    if not isinstance(масир, str) or not масир.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in масир.split("/")):
        raise ValueError("허용하지 않는 баста масир")
    if "\\" in масир or any(ord(аломат_қимат_068c2631) < 32 or ord(аломат_қимат_068c2631) == 127 for аломат_қимат_068c2631 in масир):
        raise ValueError("잘못된 масир 문자")
    결과 = "/lib/" + масир
    if len(결과.encode("utf-8")) > 63 or масир in ("한국어.py", "баста.py"):
        raise ValueError("баста 경로가 너무 길거나 қимати_пешфарз 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.порча = системаи_омил.ticks_ms()

    def 정확히읽기(자신, дарозӣ_қимат):
        иттилоот = bytearray()
        while len(иттилоот) < дарозӣ_қимат:
            if системаи_омил.ticks_ms() - 자신.порча > 90000:
                raise ValueError("баста 중계 ҷавоб_додан 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = системаи_омил.tcp_read(자신.종단, 512)
                except OSError as Хато:
                    if Хато.args[0] != 11:
                        raise
                    системаи_омил.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("баста 전송이 중간에 끝났습니다.")
            개수 = min(дарозӣ_қимат - len(иттилоот), len(자신.남은자료))
            иттилоот.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            системаи_омил.sleep_ms(0)
        return bytes(иттилоот)


def боргирӣ(요청, 접속번호):
    if len(요청) > 96 or any(аломат_қимат_068c2631 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for аломат_қимат_068c2631 in 요청):
        raise ValueError("사용법: pip install Ном 또는 Ном==버전")
    종단 = системаи_омил.tcp_open()
    try:
        порча = системаи_омил.ticks_ms()
        while True:
            try:
                системаи_омил.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Хато:
                if Хато.args[0] not in (11, 115) or системаи_омил.ticks_ms() - порча > 5000:
                    raise ValueError("баста 중계 ПАЙВАСТ нокомӣ_қимат: 호스트에서 --network --pip로 실행하십시오.")
                системаи_омил.sleep_ms(10)
        иттилоот = (요청 + "\n").encode()
        while иттилоот:
            try:
                개수 = системаи_омил.tcp_write(종단, иттилоот)
                if not 개수:
                    raise ValueError("баста 요청 интиқол_қимат нокомӣ_қимат")
                иттилоот = иттилоот[개수:]
            except OSError as Хато:
                if Хато.args[0] != 11:
                    raise
                системаи_омил.sleep_ms(10)
                if системаи_омил.ticks_ms() - порча > 10000:
                    raise ValueError("баста 요청 интиқол_қимат 시간 초과")
        ҷараён_қимат = 수신흐름(종단)
        머리 = ҷараён_қимат.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("баста интиқол_қимат кор_қимат 불일치")
        дарозӣ_қимат = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if дарозӣ_қимат > 8192:
            raise ValueError("баста 명세가 너무 큽니다.")
        명세 = json.loads(ҷараён_қимат.정확히읽기(дарозӣ_қимат).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 манбаъ_дарахт 파일은 1~16개여야 합니다.")
        if sum(ворида_қимат["size"] for ворида_қимат in 명세["files"]) > 65536:
            raise ValueError("баста манбаъ_дарахт 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ворида_қимат in 명세["files"]:
            масир = санҷиш_масир(ворида_қимат["path"])
            if масир in 파일들 or not 0 <= ворида_қимат["size"] <= 16384:
                raise ValueError("중복 масир 또는 Файл андоза_кардан 초과")
            иттилоот = ҷараён_қимат.정확히읽기(ворида_қимат["size"])
            if 지문(иттилоот) != ворида_қимат["sha256"]:
                raise ValueError("баста Файл SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(иттилоот.decode("utf-8"), масир, "exec")
            파일들[масир] = иттилоот
            gc.collect()
        return 명세, 파일들
    finally:
        системаи_омил.udp_close(종단)


def насб_кардан_қимат(요청, 접속번호):
    print("баста боргирӣ:", 요청)
    명세, 파일들 = боргирӣ(요청, 접속번호)
    ворида_Рӯйхат = 목록읽기()
    Ном = 명세["name"]
    if Ном in ворида_Рӯйхат:
        if ворида_Рӯйхат[Ном]["version"] == 명세["version"]:
            for масир, 지문값 in ворида_Рӯйхат[Ном]["files"].items():
                if системаи_омил.path_kind(масир) != 1 or 지문(системаи_омил.read(масир)) != 지문값:
                    raise ValueError("설치된 баста 파일이 달라졌습니다: " + масир)
            print("이미 설치됨:", Ном, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Бозгашт_қимат 설치하십시오.")
    for масир in 파일들:
        if системаи_омил.path_kind(масир):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + масир)
    ворида_Рӯйхат[Ном] = {"version": 명세["version"], "files": {масир: 지문(иттилоот) for масир, иттилоот in 파일들.items()}}
    새목록 = json.dumps(ворида_Рӯйхат).encode()
    if len(새목록) > 16384:
        raise ValueError("баста ворида_Рӯйхат андоза_кардан 초과")
    이전목록 = системаи_омил.read(Рӯйхат_масир) if системаи_омил.path_kind(Рӯйхат_масир) else None
    만든파일 = []
    만든폴더 = []
    try:
        for масир, иттилоот in 파일들.items():
            부분들 = масир.split("/")
            for 수 in range(2, len(부분들)):
                директория_қимат = "/".join(부분들[:수])
                종류 = системаи_омил.path_kind(директория_қимат)
                if 종류 == 0:
                    системаи_омил.mkdir(директория_қимат)
                    만든폴더.append(директория_қимат)
                elif 종류 != 2:
                    raise ValueError("директория_қимат 경로에 파일이 있습니다: " + директория_қимат)
            만든파일.append(масир)
            навиштан_сабт_кардан(масир, иттилоот)
        навиштан_сабт_кардан(Рӯйхат_масир, 새목록)
    except Exception:
        for масир in 만든파일:
            if системаи_омил.path_kind(масир):
                системаи_омил.remove(масир)
        for директория_қимат in reversed(만든폴더):
            системаи_омил.rmdir(директория_қимат)
        if 이전목록 is not None:
            навиштан_сабт_кардан(Рӯйхат_масир, 이전목록)
        elif системаи_омил.path_kind(Рӯйхат_масир):
            системаи_омил.remove(Рӯйхат_масир)
        raise
    print("насб_кардан_қимат 완료:", Ном, 명세["version"], "→ /lib (RAM)")


def тоза_кардан_ворида(Ном):
    ворида_Рӯйхат = 목록읽기()
    if Ном not in ворида_Рӯйхат:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ном)
    for масир, 지문값 in ворида_Рӯйхат[Ном]["files"].items():
        if системаи_омил.path_kind(масир) != 1 or 지문(системаи_омил.read(масир)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + масир)
    for масир in ворида_Рӯйхат[Ном]["files"]:
        системаи_омил.remove(масир)
    del ворида_Рӯйхат[Ном]
    навиштан_сабт_кардан(Рӯйхат_масир, json.dumps(ворида_Рӯйхат).encode())
    print("тоза_кардан_ворида 완료:", Ном)


def порча(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Ном, Маълумоти_система in 목록읽기().items():
            print(Ном, Маълумоти_система["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        насб_кардан_қимат(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        тоза_кардан_ворида(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython манбаъ_дарахт 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ном[==버전] [--port 8027] | pip list | pip uninstall Ном")
        print("мизбон: Абзорҳо/иҷро_кардан_фармон.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        порча(sys.argv[1:])
    except Exception as Хато:
        print("баста Хато:", Хато)
        sys.exit(1)
