"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 кабылдоо 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as оперативдик_система

Тизме_жол = "/lib/.pip.json"


def 지문(берилмелер):
    return "".join("%02x" % маани for маани in hashlib.sha256(берилмелер).digest())


def 목록읽기():
    if оперативдик_система.path_kind(Тизме_жол) == 0:
        return {}
    return json.loads(оперативдик_система.read(Тизме_жол).decode("utf-8"))


def жазуу_жазуу(ЖОЛ, берилмелер):
    if оперативдик_система.write(ЖОЛ, берилмелер) != len(берилмелер):
        raise OSError(28)


def чек_жол(ЖОЛ):
    if not isinstance(ЖОЛ, str) or not ЖОЛ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ЖОЛ.split("/")):
        raise ValueError("허용하지 않는 пакет ЖОЛ")
    if "\\" in ЖОЛ or any(ord(символ_маани_068c2631) < 32 or ord(символ_маани_068c2631) == 127 for символ_маани_068c2631 in ЖОЛ):
        raise ValueError("잘못된 ЖОЛ 문자")
    결과 = "/lib/" + ЖОЛ
    if len(결과.encode("utf-8")) > 63 or ЖОЛ in ("한국어.py", "пакет.py"):
        raise ValueError("пакет 경로가 너무 길거나 жарыяланбаган_маани 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Жүргүзүү = оперативдик_система.ticks_ms()

    def 정확히읽기(자신, узундук_маани):
        берилмелер = bytearray()
        while len(берилмелер) < узундук_маани:
            if оперативдик_система.ticks_ms() - 자신.Жүргүзүү > 90000:
                raise ValueError("пакет 중계 жооп_берүү 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = оперативдик_система.tcp_read(자신.종단, 512)
                except OSError as Ката:
                    if Ката.args[0] != 11:
                        raise
                    оперативдик_система.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("пакет 전송이 중간에 끝났습니다.")
            개수 = min(узундук_маани - len(берилмелер), len(자신.남은자료))
            берилмелер.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            оперативдик_система.sleep_ms(0)
        return bytes(берилмелер)


def жүктөө(요청, 접속번호):
    if len(요청) > 96 or any(символ_маани_068c2631 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for символ_маани_068c2631 in 요청):
        raise ValueError("사용법: pip install Аты 또는 Аты==버전")
    종단 = оперативдик_система.tcp_open()
    try:
        Жүргүзүү = оперативдик_система.ticks_ms()
        while True:
            try:
                оперативдик_система.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Ката:
                if Ката.args[0] not in (11, 115) or оперативдик_система.ticks_ms() - Жүргүзүү > 5000:
                    raise ValueError("пакет 중계 Туташуу натыйжасыз_маани: 호스트에서 --network --pip로 실행하십시오.")
                оперативдик_система.sleep_ms(10)
        берилмелер = (요청 + "\n").encode()
        while берилмелер:
            try:
                개수 = оперативдик_система.tcp_write(종단, берилмелер)
                if not 개수:
                    raise ValueError("пакет 요청 ташүү_маани натыйжасыз_маани")
                берилмелер = берилмелер[개수:]
            except OSError as Ката:
                if Ката.args[0] != 11:
                    raise
                оперативдик_система.sleep_ms(10)
                if оперативдик_система.ticks_ms() - Жүргүзүү > 10000:
                    raise ValueError("пакет 요청 ташүү_маани 시간 초과")
        агым_маани = 수신흐름(종단)
        머리 = агым_маани.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("пакет ташүү_маани иш_маани 불일치")
        узундук_маани = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if узундук_маани > 8192:
            raise ValueError("пакет 명세가 너무 큽니다.")
        명세 = json.loads(агым_маани.정확히읽기(узундук_маани).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 башат_дарак 파일은 1~16개여야 합니다.")
        if sum(киргизме_жазуу_маани["size"] for киргизме_жазуу_маани in 명세["files"]) > 65536:
            raise ValueError("пакет башат_дарак 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for киргизме_жазуу_маани in 명세["files"]:
            ЖОЛ = чек_жол(киргизме_жазуу_маани["path"])
            if ЖОЛ in 파일들 or not 0 <= киргизме_жазуу_маани["size"] <= 16384:
                raise ValueError("중복 ЖОЛ 또는 Файл Өлчөмү 초과")
            берилмелер = агым_маани.정확히읽기(киргизме_жазуу_маани["size"])
            if 지문(берилмелер) != киргизме_жазуу_маани["sha256"]:
                raise ValueError("пакет Файл SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(берилмелер.decode("utf-8"), ЖОЛ, "exec")
            파일들[ЖОЛ] = берилмелер
            gc.collect()
        return 명세, 파일들
    finally:
        оперативдик_система.udp_close(종단)


def орнотуу_маани(요청, 접속번호):
    print("пакет жүктөө:", 요청)
    명세, 파일들 = жүктөө(요청, 접속번호)
    киргизме_жазуу_Тизме = 목록읽기()
    Аты = 명세["name"]
    if Аты in киргизме_жазуу_Тизме:
        if киргизме_жазуу_Тизме[Аты]["version"] == 명세["version"]:
            for ЖОЛ, 지문값 in киргизме_жазуу_Тизме[Аты]["files"].items():
                if оперативдик_система.path_kind(ЖОЛ) != 1 or 지문(оперативдик_система.read(ЖОЛ)) != 지문값:
                    raise ValueError("설치된 пакет 파일이 달라졌습니다: " + ЖОЛ)
            print("이미 설치됨:", Аты, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Артка_маани 설치하십시오.")
    for ЖОЛ in 파일들:
        if оперативдик_система.path_kind(ЖОЛ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ЖОЛ)
    киргизме_жазуу_Тизме[Аты] = {"version": 명세["version"], "files": {ЖОЛ: 지문(берилмелер) for ЖОЛ, берилмелер in 파일들.items()}}
    새목록 = json.dumps(киргизме_жазуу_Тизме).encode()
    if len(새목록) > 16384:
        raise ValueError("пакет киргизме_жазуу_Тизме Өлчөмү 초과")
    이전목록 = оперативдик_система.read(Тизме_жол) if оперативдик_система.path_kind(Тизме_жол) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ЖОЛ, берилмелер in 파일들.items():
            부분들 = ЖОЛ.split("/")
            for 수 in range(2, len(부분들)):
                каталог_маани = "/".join(부분들[:수])
                종류 = оперативдик_система.path_kind(каталог_маани)
                if 종류 == 0:
                    оперативдик_система.mkdir(каталог_маани)
                    만든폴더.append(каталог_маани)
                elif 종류 != 2:
                    raise ValueError("каталог_маани 경로에 파일이 있습니다: " + каталог_маани)
            만든파일.append(ЖОЛ)
            жазуу_жазуу(ЖОЛ, берилмелер)
        жазуу_жазуу(Тизме_жол, 새목록)
    except Exception:
        for ЖОЛ in 만든파일:
            if оперативдик_система.path_kind(ЖОЛ):
                оперативдик_система.remove(ЖОЛ)
        for каталог_маани in reversed(만든폴더):
            оперативдик_система.rmdir(каталог_маани)
        if 이전목록 is not None:
            жазуу_жазуу(Тизме_жол, 이전목록)
        elif оперативдик_система.path_kind(Тизме_жол):
            оперативдик_система.remove(Тизме_жол)
        raise
    print("орнотуу_маани 완료:", Аты, 명세["version"], "→ /lib (RAM)")


def алып_салуу_киргизме_жазуу(Аты):
    киргизме_жазуу_Тизме = 목록읽기()
    if Аты not in киргизме_жазуу_Тизме:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Аты)
    for ЖОЛ, 지문값 in киргизме_жазуу_Тизме[Аты]["files"].items():
        if оперативдик_система.path_kind(ЖОЛ) != 1 or 지문(оперативдик_система.read(ЖОЛ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ЖОЛ)
    for ЖОЛ in киргизме_жазуу_Тизме[Аты]["files"]:
        оперативдик_система.remove(ЖОЛ)
    del киргизме_жазуу_Тизме[Аты]
    жазуу_жазуу(Тизме_жол, json.dumps(киргизме_жазуу_Тизме).encode())
    print("алып_салуу_киргизме_жазуу 완료:", Аты)


def Жүргүзүү(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Аты, Система_маалыматы in 목록읽기().items():
            print(Аты, Система_маалыматы["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        орнотуу_маани(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        алып_салуу_киргизме_жазуу(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython башат_дарак 설치기 (PyPA pip 전체가 아님)")
        print("pip install Аты[==버전] [--port 8027] | pip list | pip uninstall Аты")
        print("кабылдоо: Куралдар/аткаруу_буйрук.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Жүргүзүү(sys.argv[1:])
    except Exception as Ката:
        print("пакет Ката:", Ката)
        sys.exit(1)
