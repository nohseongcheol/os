"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 орналастыру 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as операциялық_жүйе

Тізім_жол = "/lib/.pip.json"


def 지문(деректер):
    return "".join("%02x" % мән for мән in hashlib.sha256(деректер).digest())


def 목록읽기():
    if операциялық_жүйе.path_kind(Тізім_жол) == 0:
        return {}
    return json.loads(операциялық_жүйе.read(Тізім_жол).decode("utf-8"))


def жазу_журнал(Жол_2, деректер):
    if операциялық_жүйе.write(Жол_2, деректер) != len(деректер):
        raise OSError(28)


def чек_жол(Жол_2):
    if not isinstance(Жол_2, str) or not Жол_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Жол_2.split("/")):
        raise ValueError("허용하지 않는 жинау Жол_2")
    if "\\" in Жол_2 or any(ord(таңба_мән) < 32 or ord(таңба_мән) == 127 for таңба_мән in Жол_2):
        raise ValueError("잘못된 Жол_2 문자")
    НӘТИЖЕ = "/lib/" + Жол_2
    if len(НӘТИЖЕ.encode("utf-8")) > 63 or Жол_2 in ("한국어.py", "жинау.py"):
        raise ValueError("жинау 경로가 너무 길거나 әдепкі_мән 라이브러리와 겹칩니다.")
    return НӘТИЖЕ


class 수신흐름:
    def __init__(자신, қатысушы):
        자신.қатысушы = қатысушы
        자신.남은자료 = b""
        자신.Орындау_2 = операциялық_жүйе.ticks_ms()

    def 정확히읽기(자신, ұзындық_мән):
        деректер = bytearray()
        while len(деректер) < ұзындық_мән:
            if операциялық_жүйе.ticks_ms() - 자신.Орындау_2 > 90000:
                raise ValueError("жинау 중계 жауап уақыт_мән 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = операциялық_жүйе.tcp_read(자신.қатысушы, 512)
                except OSError as Қате:
                    if Қате.args[0] != 11:
                        raise
                    операциялық_жүйе.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("жинау 전송이 중간에 끝났습니다.")
            개수 = min(ұзындық_мән - len(деректер), len(자신.남은자료))
            деректер.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            операциялық_жүйе.sleep_ms(0)
        return bytes(деректер)


def жүктеме(요청, порт_нөмірі):
    if len(요청) > 96 or any(таңба_мән not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for таңба_мән in 요청):
        raise ValueError("사용법: pip install Аты 또는 Аты==버전")
    қатысушы = операциялық_жүйе.tcp_open()
    try:
        Орындау_2 = операциялық_жүйе.ticks_ms()
        while True:
            try:
                операциялық_жүйе.tcp_connect(қатысушы, "10.0.2.2", порт_нөмірі)
                break
            except OSError as Қате:
                if Қате.args[0] not in (11, 115) or операциялық_жүйе.ticks_ms() - Орындау_2 > 5000:
                    raise ValueError("жинау 중계 Байланысу қате_мән: 호스트에서 --network --pip로 실행하십시오.")
                операциялық_жүйе.sleep_ms(10)
        деректер = (요청 + "\n").encode()
        while деректер:
            try:
                개수 = операциялық_жүйе.tcp_write(қатысушы, деректер)
                if not 개수:
                    raise ValueError("жинау 요청 аудару_мән қате_мән")
                деректер = деректер[개수:]
            except OSError as Қате:
                if Қате.args[0] != 11:
                    raise
                операциялық_жүйе.sleep_ms(10)
                if операциялық_жүйе.ticks_ms() - Орындау_2 > 10000:
                    raise ValueError("жинау 요청 аудару_мән уақыт_мән 초과")
        ағым_мән = 수신흐름(қатысушы)
        머리 = ағым_мән.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("жинау аудару_мән іс_мән 불일치")
        ұзындық_мән = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ұзындық_мән > 8192:
            raise ValueError("жинау 명세가 너무 큽니다.")
        сипаттама = json.loads(ағым_мән.정확히읽기(ұзындық_мән).decode())
        if "error" in сипаттама:
            raise ValueError(сипаттама["error"])
        if not 1 <= len(сипаттама["files"]) <= 16:
            raise ValueError("꾸러미당 көз_дарақ 파일은 1~16개여야 합니다.")
        if sum(енгізу_мән["size"] for енгізу_мән in сипаттама["files"]) > 65536:
            raise ValueError("жинау көз_дарақ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for енгізу_мән in сипаттама["files"]:
            Жол_2 = чек_жол(енгізу_мән["path"])
            if Жол_2 in 파일들 or not 0 <= енгізу_мән["size"] <= 16384:
                raise ValueError("중복 Жол_2 또는 Файл Өлшемі 초과")
            деректер = ағым_мән.정확히읽기(енгізу_мән["size"])
            if 지문(деректер) != енгізу_мән["sha256"]:
                raise ValueError("жинау Файл SHA-256 불일치")
            # 실행하지 않고 ток_элемент MicroPython의 문법으로 먼저 검사한다.
            compile(деректер.decode("utf-8"), Жол_2, "exec")
            파일들[Жол_2] = деректер
            gc.collect()
        return сипаттама, 파일들
    finally:
        операциялық_жүйе.udp_close(қатысушы)


def орнату_мән(요청, порт_нөмірі):
    print("жинау жүктеме:", 요청)
    сипаттама, 파일들 = жүктеме(요청, порт_нөмірі)
    енгізу_Тізім = 목록읽기()
    Аты = сипаттама["name"]
    if Аты in енгізу_Тізім:
        if енгізу_Тізім[Аты]["version"] == сипаттама["version"]:
            for Жол_2, 지문값 in енгізу_Тізім[Аты]["files"].items():
                if операциялық_жүйе.path_kind(Жол_2) != 1 or 지문(операциялық_жүйе.read(Жол_2)) != 지문값:
                    raise ValueError("설치된 жинау 파일이 달라졌습니다: " + Жол_2)
            print("이미 설치됨:", Аты, сипаттама["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 АРТҚА_мән 설치하십시오.")
    for Жол_2 in 파일들:
        if операциялық_жүйе.path_kind(Жол_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Жол_2)
    енгізу_Тізім[Аты] = {"version": сипаттама["version"], "files": {Жол_2: 지문(деректер) for Жол_2, деректер in 파일들.items()}}
    새목록 = json.dumps(енгізу_Тізім).encode()
    if len(새목록) > 16384:
        raise ValueError("жинау енгізу_Тізім Өлшемі 초과")
    이전목록 = операциялық_жүйе.read(Тізім_жол) if операциялық_жүйе.path_kind(Тізім_жол) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Жол_2, деректер in 파일들.items():
            부분들 = Жол_2.split("/")
            for 수 in range(2, len(부분들)):
                каталог_мән = "/".join(부분들[:수])
                종류 = операциялық_жүйе.path_kind(каталог_мән)
                if 종류 == 0:
                    операциялық_жүйе.mkdir(каталог_мән)
                    만든폴더.append(каталог_мән)
                elif 종류 != 2:
                    raise ValueError("каталог_мән 경로에 파일이 있습니다: " + каталог_мән)
            만든파일.append(Жол_2)
            жазу_журнал(Жол_2, деректер)
        жазу_журнал(Тізім_жол, 새목록)
    except Exception:
        for Жол_2 in 만든파일:
            if операциялық_жүйе.path_kind(Жол_2):
                операциялық_жүйе.remove(Жол_2)
        for каталог_мән in reversed(만든폴더):
            операциялық_жүйе.rmdir(каталог_мән)
        if 이전목록 is not None:
            жазу_журнал(Тізім_жол, 이전목록)
        elif операциялық_жүйе.path_kind(Тізім_жол):
            операциялық_жүйе.remove(Тізім_жол)
        raise
    print("орнату_мән 완료:", Аты, сипаттама["version"], "→ /lib (RAM)")


def жою_енгізу(Аты):
    енгізу_Тізім = 목록읽기()
    if Аты not in енгізу_Тізім:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Аты)
    for Жол_2, 지문값 in енгізу_Тізім[Аты]["files"].items():
        if операциялық_жүйе.path_kind(Жол_2) != 1 or 지문(операциялық_жүйе.read(Жол_2)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Жол_2)
    for Жол_2 in енгізу_Тізім[Аты]["files"]:
        операциялық_жүйе.remove(Жол_2)
    del енгізу_Тізім[Аты]
    жазу_журнал(Тізім_жол, json.dumps(енгізу_Тізім).encode())
    print("жою_енгізу 완료:", Аты)


def Орындау_2(Аргументтер):
    порт_нөмірі = 8027
    if len(Аргументтер) >= 2 and Аргументтер[-2] == "--port":
        порт_нөмірі = int(Аргументтер[-1])
        Аргументтер = Аргументтер[:-2]
    if Аргументтер == ["list"]:
        for Аты, Жүйелік_ақпарат in 목록읽기().items():
            print(Аты, Жүйелік_ақпарат["version"])
    elif len(Аргументтер) == 2 and Аргументтер[0] == "install":
        орнату_мән(Аргументтер[1], порт_нөмірі)
    elif len(Аргументтер) == 2 and Аргументтер[0] == "uninstall":
        жою_енгізу(Аргументтер[1])
    elif not Аргументтер or Аргументтер in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython көз_дарақ 설치기 (PyPA pip 전체가 아님)")
        print("pip install Аты[==버전] [--port 8027] | pip list | pip uninstall Аты")
        print("орналастыру: Құралдар/орындау_пәрмен.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Орындау_2(sys.argv[1:])
    except Exception as Қате:
        print("жинау Қате:", Қате)
        sys.exit(1)
