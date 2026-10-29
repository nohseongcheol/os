"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 хост 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as операцион_система

Исемлек_юл = "/lib/.pip.json"


def 지문(мәгълүмат):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(мәгълүмат).digest())


def 목록읽기():
    if операцион_система.path_kind(Исемлек_юл) == 0:
        return {}
    return json.loads(операцион_система.read(Исемлек_юл).decode("utf-8"))


def язу_LOG(Yul, мәгълүмат):
    if операцион_система.write(Yul, мәгълүмат) != len(мәгълүмат):
        raise OSError(28)


def чек_юл(Yul):
    if not isinstance(Yul, str) or not Yul.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Yul.split("/")):
        raise ValueError("허용하지 않는 пакет Yul")
    if "\\" in Yul or any(ord(символ_VALUE_068c2631) < 32 or ord(символ_VALUE_068c2631) == 127 for символ_VALUE_068c2631 in Yul):
        raise ValueError("잘못된 Yul 문자")
    үлчәм = "/lib/" + Yul
    if len(үлчәм.encode("utf-8")) > 63 or Yul in ("Татарча.py", "пакет.py"):
        raise ValueError("пакет 경로가 너무 길거나 килешенгәнчә_кыйммәт 라이브러리와 겹칩니다.")
    return үлчәм


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.эшләтү = операцион_система.ticks_ms()

    def 정확히읽기(자신, озынлык_VALUE):
        мәгълүмат = bytearray()
        while len(мәгълүмат) < озынлык_VALUE:
            if операцион_система.ticks_ms() - 자신.эшләтү > 90000:
                raise ValueError("пакет 중계 җавап_бирү TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = операцион_система.tcp_read(자신.종단, 512)
                except OSError as Хата:
                    if Хата.args[0] != 11:
                        raise
                    операцион_система.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("пакет 전송이 중간에 끝났습니다.")
            элемент_COUNT = min(озынлык_VALUE - len(мәгълүмат), len(자신.남은자료))
            мәгълүмат.extend(자신.남은자료[:элемент_COUNT])
            자신.남은자료 = 자신.남은자료[элемент_COUNT:]
            операцион_система.sleep_ms(0)
        return bytes(мәгълүмат)


def йөкләү_496ddb99(요청, 접속번호):
    if len(요청) > 96 or any(символ_VALUE_068c2631 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for символ_VALUE_068c2631 in 요청):
        raise ValueError("사용법: pip install исем 또는 исем==버전")
    종단 = операцион_система.tcp_open()
    try:
        эшләтү = операцион_система.ticks_ms()
        while True:
            try:
                операцион_система.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Хата:
                if Хата.args[0] not in (11, 115) or операцион_система.ticks_ms() - эшләтү > 5000:
                    raise ValueError("пакет 중계 ялгау эштән_туктау_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                операцион_система.sleep_ms(10)
        мәгълүмат = (요청 + "\n").encode()
        while мәгълүмат:
            try:
                элемент_COUNT = операцион_система.tcp_write(종단, мәгълүмат)
                if not элемент_COUNT:
                    raise ValueError("пакет 요청 күчерү_VALUE_630ba093 эштән_туктау_VALUE")
                мәгълүмат = мәгълүмат[элемент_COUNT:]
            except OSError as Хата:
                if Хата.args[0] != 11:
                    raise
                операцион_система.sleep_ms(10)
                if операцион_система.ticks_ms() - эшләтү > 10000:
                    raise ValueError("пакет 요청 күчерү_VALUE_630ba093 TIME_VALUE 초과")
        агым_VALUE = 수신흐름(종단)
        머리 = агым_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("пакет күчерү_VALUE_630ba093 бирем_VALUE_102996da 불일치")
        озынлык_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if озынлык_VALUE > 8192:
            raise ValueError("пакет 명세가 너무 큽니다.")
        명세 = json.loads(агым_VALUE.정확히읽기(озынлык_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 чыганак_агач 파일은 1~16개여야 합니다.")
        if sum(кертү_VALUE["size"] for кертү_VALUE in 명세["files"]) > 65536:
            raise ValueError("пакет чыганак_агач 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for кертү_VALUE in 명세["files"]:
            Yul = чек_юл(кертү_VALUE["path"])
            if Yul in 파일들 or not 0 <= кертү_VALUE["size"] <= 16384:
                raise ValueError("중복 Yul 또는 Birem үлчәмен_үзгәртү 초과")
            мәгълүмат = агым_VALUE.정확히읽기(кертү_VALUE["size"])
            if 지문(мәгълүмат) != кертү_VALUE["sha256"]:
                raise ValueError("пакет Birem SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(мәгълүмат.decode("utf-8"), Yul, "exec")
            파일들[Yul] = мәгълүмат
            gc.collect()
        return 명세, 파일들
    finally:
        операцион_система.udp_close(종단)


def урнаштыру_VALUE_6a28baa5(요청, 접속번호):
    print("пакет йөкләү_496ddb99:", 요청)
    명세, 파일들 = йөкләү_496ddb99(요청, 접속번호)
    кертү_Исемлек = 목록읽기()
    исем = 명세["name"]
    if исем in кертү_Исемлек:
        if кертү_Исемлек[исем]["version"] == 명세["version"]:
            for Yul, 지문값 in кертү_Исемлек[исем]["files"].items():
                if операцион_система.path_kind(Yul) != 1 or 지문(операцион_система.read(Yul)) != 지문값:
                    raise ValueError("설치된 пакет 파일이 달라졌습니다: " + Yul)
            print("이미 설치됨:", исем, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Артка_VALUE 설치하십시오.")
    for Yul in 파일들:
        if операцион_система.path_kind(Yul):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Yul)
    кертү_Исемлек[исем] = {"version": 명세["version"], "files": {Yul: 지문(мәгълүмат) for Yul, мәгълүмат in 파일들.items()}}
    새목록 = json.dumps(кертү_Исемлек).encode()
    if len(새목록) > 16384:
        raise ValueError("пакет кертү_Исемлек үлчәмен_үзгәртү 초과")
    이전목록 = операцион_система.read(Исемлек_юл) if операцион_система.path_kind(Исемлек_юл) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Yul, мәгълүмат in 파일들.items():
            부분들 = Yul.split("/")
            for 수 in range(2, len(부분들)):
                каталог_VALUE = "/".join(부분들[:수])
                종류 = операцион_система.path_kind(каталог_VALUE)
                if 종류 == 0:
                    операцион_система.mkdir(каталог_VALUE)
                    만든폴더.append(каталог_VALUE)
                elif 종류 != 2:
                    raise ValueError("каталог_VALUE 경로에 파일이 있습니다: " + каталог_VALUE)
            만든파일.append(Yul)
            язу_LOG(Yul, мәгълүмат)
        язу_LOG(Исемлек_юл, 새목록)
    except Exception:
        for Yul in 만든파일:
            if операцион_система.path_kind(Yul):
                операцион_система.remove(Yul)
        for каталог_VALUE in reversed(만든폴더):
            операцион_система.rmdir(каталог_VALUE)
        if 이전목록 is not None:
            язу_LOG(Исемлек_юл, 이전목록)
        elif операцион_система.path_kind(Исемлек_юл):
            операцион_система.remove(Исемлек_юл)
        raise
    print("урнаштыру_VALUE_6a28baa5 완료:", исем, 명세["version"], "→ /lib (RAM)")


def бетерү_кертү(исем):
    кертү_Исемлек = 목록읽기()
    if исем not in кертү_Исемлек:
        raise ValueError("설치되지 않은 꾸러미입니다: " + исем)
    for Yul, 지문값 in кертү_Исемлек[исем]["files"].items():
        if операцион_система.path_kind(Yul) != 1 or 지문(операцион_система.read(Yul)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Yul)
    for Yul in кертү_Исемлек[исем]["files"]:
        операцион_система.remove(Yul)
    del кертү_Исемлек[исем]
    язу_LOG(Исемлек_юл, json.dumps(кертү_Исемлек).encode())
    print("бетерү_кертү 완료:", исем)


def эшләтү(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for исем, msinfo32_exe in 목록읽기().items():
            print(исем, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        урнаштыру_VALUE_6a28baa5(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        бетерү_кертү(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython чыганак_агач 설치기 (PyPA pip 전체가 아님)")
        print("pip install исем[==버전] [--port 8027] | pip list | pip uninstall исем")
        print("хост: Кораллар/үтәргә_команда.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        эшләтү(sys.argv[1:])
    except Exception as Хата:
        print("пакет Хата:", Хата)
        sys.exit(1)
