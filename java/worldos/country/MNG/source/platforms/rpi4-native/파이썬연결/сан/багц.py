"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 хост 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as үйлдлийн_систем

Жагсаалт_зам = "/lib/.pip.json"


def 지문(өгөгдөл):
    return "".join("%02x" % утга for утга in hashlib.sha256(өгөгдөл).digest())


def 목록읽기():
    if үйлдлийн_систем.path_kind(Жагсаалт_зам) == 0:
        return {}
    return json.loads(үйлдлийн_систем.read(Жагсаалт_зам).decode("utf-8"))


def бичих_бичих(ЗАМ, өгөгдөл):
    if үйлдлийн_систем.write(ЗАМ, өгөгдөл) != len(өгөгдөл):
        raise OSError(28)


def чек_зам(ЗАМ):
    if not isinstance(ЗАМ, str) or not ЗАМ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ЗАМ.split("/")):
        raise ValueError("허용하지 않는 багц ЗАМ")
    if "\\" in ЗАМ or any(ord(тэмдэгт_утга) < 32 or ord(тэмдэгт_утга) == 127 for тэмдэгт_утга in ЗАМ):
        raise ValueError("잘못된 ЗАМ 문자")
    결과 = "/lib/" + ЗАМ
    if len(결과.encode("utf-8")) > 63 or ЗАМ in ("한국어.py", "багц.py"):
        raise ValueError("багц 경로가 너무 길거나 өгөгдмөл_утга 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Ажиллуулах = үйлдлийн_систем.ticks_ms()

    def 정확히읽기(자신, урт_утга):
        өгөгдөл = bytearray()
        while len(өгөгдөл) < урт_утга:
            if үйлдлийн_систем.ticks_ms() - 자신.Ажиллуулах > 90000:
                raise ValueError("багц 중계 хариулах 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = үйлдлийн_систем.tcp_read(자신.종단, 512)
                except OSError as Алдаа:
                    if Алдаа.args[0] != 11:
                        raise
                    үйлдлийн_систем.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("багц 전송이 중간에 끝났습니다.")
            개수 = min(урт_утга - len(өгөгдөл), len(자신.남은자료))
            өгөгдөл.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            үйлдлийн_систем.sleep_ms(0)
        return bytes(өгөгдөл)


def татаж_авах(요청, 접속번호):
    if len(요청) > 96 or any(тэмдэгт_утга not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for тэмдэгт_утга in 요청):
        raise ValueError("사용법: pip install Нэр 또는 Нэр==버전")
    종단 = үйлдлийн_систем.tcp_open()
    try:
        Ажиллуулах = үйлдлийн_систем.ticks_ms()
        while True:
            try:
                үйлдлийн_систем.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Алдаа:
                if Алдаа.args[0] not in (11, 115) or үйлдлийн_систем.ticks_ms() - Ажиллуулах > 5000:
                    raise ValueError("багц 중계 Холбох гэмтэл_утга: 호스트에서 --network --pip로 실행하십시오.")
                үйлдлийн_систем.sleep_ms(10)
        өгөгдөл = (요청 + "\n").encode()
        while өгөгдөл:
            try:
                개수 = үйлдлийн_систем.tcp_write(종단, өгөгдөл)
                if not 개수:
                    raise ValueError("багц 요청 дамжуулах_утга гэмтэл_утга")
                өгөгдөл = өгөгдөл[개수:]
            except OSError as Алдаа:
                if Алдаа.args[0] != 11:
                    raise
                үйлдлийн_систем.sleep_ms(10)
                if үйлдлийн_систем.ticks_ms() - Ажиллуулах > 10000:
                    raise ValueError("багц 요청 дамжуулах_утга 시간 초과")
        урсгал_утга = 수신흐름(종단)
        머리 = урсгал_утга.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("багц дамжуулах_утга нөхцөл_байдал_утга 불일치")
        урт_утга = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if урт_утга > 8192:
            raise ValueError("багц 명세가 너무 큽니다.")
        명세 = json.loads(урсгал_утга.정확히읽기(урт_утга).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 эх_мод 파일은 1~16개여야 합니다.")
        if sum(оролт_утга["size"] for оролт_утга in 명세["files"]) > 65536:
            raise ValueError("багц эх_мод 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for оролт_утга in 명세["files"]:
            ЗАМ = чек_зам(оролт_утга["path"])
            if ЗАМ in 파일들 or not 0 <= оролт_утга["size"] <= 16384:
                raise ValueError("중복 ЗАМ 또는 Файл Хэмжээ 초과")
            өгөгдөл = урсгал_утга.정확히읽기(оролт_утга["size"])
            if 지문(өгөгдөл) != оролт_утга["sha256"]:
                raise ValueError("багц Файл SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(өгөгдөл.decode("utf-8"), ЗАМ, "exec")
            파일들[ЗАМ] = өгөгдөл
            gc.collect()
        return 명세, 파일들
    finally:
        үйлдлийн_систем.udp_close(종단)


def суулгах_утга(요청, 접속번호):
    print("багц татаж_авах:", 요청)
    명세, 파일들 = татаж_авах(요청, 접속번호)
    оролт_Жагсаалт = 목록읽기()
    Нэр = 명세["name"]
    if Нэр in оролт_Жагсаалт:
        if оролт_Жагсаалт[Нэр]["version"] == 명세["version"]:
            for ЗАМ, 지문값 in оролт_Жагсаалт[Нэр]["files"].items():
                if үйлдлийн_систем.path_kind(ЗАМ) != 1 or 지문(үйлдлийн_систем.read(ЗАМ)) != 지문값:
                    raise ValueError("설치된 багц 파일이 달라졌습니다: " + ЗАМ)
            print("이미 설치됨:", Нэр, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Буцах_утга 설치하십시오.")
    for ЗАМ in 파일들:
        if үйлдлийн_систем.path_kind(ЗАМ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ЗАМ)
    оролт_Жагсаалт[Нэр] = {"version": 명세["version"], "files": {ЗАМ: 지문(өгөгдөл) for ЗАМ, өгөгдөл in 파일들.items()}}
    새목록 = json.dumps(оролт_Жагсаалт).encode()
    if len(새목록) > 16384:
        raise ValueError("багц оролт_Жагсаалт Хэмжээ 초과")
    이전목록 = үйлдлийн_систем.read(Жагсаалт_зам) if үйлдлийн_систем.path_kind(Жагсаалт_зам) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ЗАМ, өгөгдөл in 파일들.items():
            부분들 = ЗАМ.split("/")
            for 수 in range(2, len(부분들)):
                лавлах_утга = "/".join(부분들[:수])
                종류 = үйлдлийн_систем.path_kind(лавлах_утга)
                if 종류 == 0:
                    үйлдлийн_систем.mkdir(лавлах_утга)
                    만든폴더.append(лавлах_утга)
                elif 종류 != 2:
                    raise ValueError("лавлах_утга 경로에 파일이 있습니다: " + лавлах_утга)
            만든파일.append(ЗАМ)
            бичих_бичих(ЗАМ, өгөгдөл)
        бичих_бичих(Жагсаалт_зам, 새목록)
    except Exception:
        for ЗАМ in 만든파일:
            if үйлдлийн_систем.path_kind(ЗАМ):
                үйлдлийн_систем.remove(ЗАМ)
        for лавлах_утга in reversed(만든폴더):
            үйлдлийн_систем.rmdir(лавлах_утга)
        if 이전목록 is not None:
            бичих_бичих(Жагсаалт_зам, 이전목록)
        elif үйлдлийн_систем.path_kind(Жагсаалт_зам):
            үйлдлийн_систем.remove(Жагсаалт_зам)
        raise
    print("суулгах_утга 완료:", Нэр, 명세["version"], "→ /lib (RAM)")


def арилгах_оролт(Нэр):
    оролт_Жагсаалт = 목록읽기()
    if Нэр not in оролт_Жагсаалт:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Нэр)
    for ЗАМ, 지문값 in оролт_Жагсаалт[Нэр]["files"].items():
        if үйлдлийн_систем.path_kind(ЗАМ) != 1 or 지문(үйлдлийн_систем.read(ЗАМ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ЗАМ)
    for ЗАМ in оролт_Жагсаалт[Нэр]["files"]:
        үйлдлийн_систем.remove(ЗАМ)
    del оролт_Жагсаалт[Нэр]
    бичих_бичих(Жагсаалт_зам, json.dumps(оролт_Жагсаалт).encode())
    print("арилгах_оролт 완료:", Нэр)


def Ажиллуулах(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Нэр, системийн_мэдээлэл in 목록읽기().items():
            print(Нэр, системийн_мэдээлэл["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        суулгах_утга(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        арилгах_оролт(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython эх_мод 설치기 (PyPA pip 전체가 아님)")
        print("pip install Нэр[==버전] [--port 8027] | pip list | pip uninstall Нэр")
        print("хост: Хэрэгслүүд/Гүйцэтгэх_команд.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Ажиллуулах(sys.argv[1:])
    except Exception as Алдаа:
        print("багц Алдаа:", Алдаа)
        sys.exit(1)
