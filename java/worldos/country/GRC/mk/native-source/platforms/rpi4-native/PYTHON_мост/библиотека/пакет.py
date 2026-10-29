"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 вдоми 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as оперативен_систем

Список_патека = "/lib/.pip.json"


def 지문(податоци):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(податоци).digest())


def 목록읽기():
    if оперативен_систем.path_kind(Список_патека) == 0:
        return {}
    return json.loads(оперативен_систем.read(Список_патека).decode("utf-8"))


def запиши_LOG(ПАТЕКА, податоци):
    if оперативен_систем.write(ПАТЕКА, податоци) != len(податоци):
        raise OSError(28)


def провери_патека(ПАТЕКА):
    if not isinstance(ПАТЕКА, str) or not ПАТЕКА.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ПАТЕКА.split("/")):
        raise ValueError("허용하지 않는 пакет ПАТЕКА")
    if "\\" in ПАТЕКА or any(ord(знак_VALUE) < 32 or ord(знак_VALUE) == 127 for знак_VALUE in ПАТЕКА):
        raise ValueError("잘못된 ПАТЕКА 문자")
    мерка = "/lib/" + ПАТЕКА
    if len(мерка.encode("utf-8")) > 63 or ПАТЕКА in ("Македонски.py", "пакет.py"):
        raise ValueError("пакет 경로가 너무 길거나 стандардна_вредност 라이브러리와 겹칩니다.")
    return мерка


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Изврши_2 = оперативен_систем.ticks_ms()

    def 정확히읽기(자신, должина_VALUE):
        податоци = bytearray()
        while len(податоци) < должина_VALUE:
            if оперативен_систем.ticks_ms() - 자신.Изврши_2 > 90000:
                raise ValueError("пакет 중계 одговори TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = оперативен_систем.tcp_read(자신.종단, 512)
                except OSError as ГРЕШКА:
                    if ГРЕШКА.args[0] != 11:
                        raise
                    оперативен_систем.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("пакет 전송이 중간에 끝났습니다.")
            ставка_COUNT = min(должина_VALUE - len(податоци), len(자신.남은자료))
            податоци.extend(자신.남은자료[:ставка_COUNT])
            자신.남은자료 = 자신.남은자료[ставка_COUNT:]
            оперативен_систем.sleep_ms(0)
        return bytes(податоци)


def преземи(Барање_на_HTTP, број_на_порта):
    if len(Барање_на_HTTP) > 96 or any(знак_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for знак_VALUE in Барање_на_HTTP):
        raise ValueError("사용법: pip install Име 또는 Име==버전")
    종단 = оперативен_систем.tcp_open()
    try:
        Изврши_2 = оперативен_систем.ticks_ms()
        while True:
            try:
                оперативен_систем.tcp_connect(종단, "10.0.2.2", број_на_порта)
                break
            except OSError as ГРЕШКА:
                if ГРЕШКА.args[0] not in (11, 115) or оперативен_систем.ticks_ms() - Изврши_2 > 5000:
                    raise ValueError("пакет 중계 Врзи_се неуспех_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                оперативен_систем.sleep_ms(10)
        податоци = (Барање_на_HTTP + "\n").encode()
        while податоци:
            try:
                ставка_COUNT = оперативен_систем.tcp_write(종단, податоци)
                if not ставка_COUNT:
                    raise ValueError("пакет Барање_на_HTTP пренос_VALUE неуспех_VALUE")
                податоци = податоци[ставка_COUNT:]
            except OSError as ГРЕШКА:
                if ГРЕШКА.args[0] != 11:
                    raise
                оперативен_систем.sleep_ms(10)
                if оперативен_систем.ticks_ms() - Изврши_2 > 10000:
                    raise ValueError("пакет Барање_на_HTTP пренос_VALUE TIME_VALUE 초과")
        Stream_VALUE = 수신흐름(종단)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("пакет пренос_VALUE задача_VALUE_102996da 불일치")
        должина_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if должина_VALUE > 8192:
            raise ValueError("пакет 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(должина_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 извор_дрво 파일은 1~16개여야 합니다.")
        if sum(внес_VALUE["size"] for внес_VALUE in 명세["files"]) > 65536:
            raise ValueError("пакет извор_дрво 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for внес_VALUE in 명세["files"]:
            ПАТЕКА = провери_патека(внес_VALUE["path"])
            if ПАТЕКА in 파일들 or not 0 <= внес_VALUE["size"] <= 16384:
                raise ValueError("중복 ПАТЕКА 또는 Датотека Големина 초과")
            податоци = Stream_VALUE.정확히읽기(внес_VALUE["size"])
            if 지문(податоци) != внес_VALUE["sha256"]:
                raise ValueError("пакет Датотека SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(податоци.decode("utf-8"), ПАТЕКА, "exec")
            파일들[ПАТЕКА] = податоци
            gc.collect()
        return 명세, 파일들
    finally:
        оперативен_систем.udp_close(종단)


def инсталирај_VALUE(Барање_на_HTTP, број_на_порта):
    print("пакет преземи:", Барање_на_HTTP)
    명세, 파일들 = преземи(Барање_на_HTTP, број_на_порта)
    внес_Список = 목록읽기()
    Име = 명세["name"]
    if Име in внес_Список:
        if внес_Список[Име]["version"] == 명세["version"]:
            for ПАТЕКА, 지문값 in внес_Список[Име]["files"].items():
                if оперативен_систем.path_kind(ПАТЕКА) != 1 or 지문(оперативен_систем.read(ПАТЕКА)) != 지문값:
                    raise ValueError("설치된 пакет 파일이 달라졌습니다: " + ПАТЕКА)
            print("이미 설치됨:", Име, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Назад_VALUE 설치하십시오.")
    for ПАТЕКА in 파일들:
        if оперативен_систем.path_kind(ПАТЕКА):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ПАТЕКА)
    внес_Список[Име] = {"version": 명세["version"], "files": {ПАТЕКА: 지문(податоци) for ПАТЕКА, податоци in 파일들.items()}}
    새목록 = json.dumps(внес_Список).encode()
    if len(새목록) > 16384:
        raise ValueError("пакет внес_Список Големина 초과")
    이전목록 = оперативен_систем.read(Список_патека) if оперативен_систем.path_kind(Список_патека) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ПАТЕКА, податоци in 파일들.items():
            부분들 = ПАТЕКА.split("/")
            for 수 in range(2, len(부분들)):
                Именик_VALUE = "/".join(부분들[:수])
                종류 = оперативен_систем.path_kind(Именик_VALUE)
                if 종류 == 0:
                    оперативен_систем.mkdir(Именик_VALUE)
                    만든폴더.append(Именик_VALUE)
                elif 종류 != 2:
                    raise ValueError("Именик_VALUE 경로에 파일이 있습니다: " + Именик_VALUE)
            만든파일.append(ПАТЕКА)
            запиши_LOG(ПАТЕКА, податоци)
        запиши_LOG(Список_патека, 새목록)
    except Exception:
        for ПАТЕКА in 만든파일:
            if оперативен_систем.path_kind(ПАТЕКА):
                оперативен_систем.remove(ПАТЕКА)
        for Именик_VALUE in reversed(만든폴더):
            оперативен_систем.rmdir(Именик_VALUE)
        if 이전목록 is not None:
            запиши_LOG(Список_патека, 이전목록)
        elif оперативен_систем.path_kind(Список_патека):
            оперативен_систем.remove(Список_патека)
        raise
    print("инсталирај_VALUE 완료:", Име, 명세["version"], "→ /lib (RAM)")


def отстрани_внес(Име):
    внес_Список = 목록읽기()
    if Име not in внес_Список:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Име)
    for ПАТЕКА, 지문값 in внес_Список[Име]["files"].items():
        if оперативен_систем.path_kind(ПАТЕКА) != 1 or 지문(оперативен_систем.read(ПАТЕКА)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ПАТЕКА)
    for ПАТЕКА in внес_Список[Име]["files"]:
        оперативен_систем.remove(ПАТЕКА)
    del внес_Список[Име]
    запиши_LOG(Список_патека, json.dumps(внес_Список).encode())
    print("отстрани_внес 완료:", Име)


def Изврши_2(Аргументи):
    број_на_порта = 8027
    if len(Аргументи) >= 2 and Аргументи[-2] == "--port":
        број_на_порта = int(Аргументи[-1])
        Аргументи = Аргументи[:-2]
    if Аргументи == ["list"]:
        for Име, msinfo32_exe in 목록읽기().items():
            print(Име, msinfo32_exe["version"])
    elif len(Аргументи) == 2 and Аргументи[0] == "install":
        инсталирај_VALUE(Аргументи[1], број_на_порта)
    elif len(Аргументи) == 2 and Аргументи[0] == "uninstall":
        отстрани_внес(Аргументи[1])
    elif not Аргументи or Аргументи in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython извор_дрво 설치기 (PyPA pip 전체가 아님)")
        print("pip install Име[==버전] [--port 8027] | pip list | pip uninstall Име")
        print("вдоми: Алатки/Изврши_наредба.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Изврши_2(sys.argv[1:])
    except Exception as ГРЕШКА:
        print("пакет ГРЕШКА:", ГРЕШКА)
        sys.exit(1)
