"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 usu 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as OS

ndepụta_ụzọ_ozi = "/lib/.pip.json"


def 지문(datà):
    return "".join("%02x" % valuu for valuu in hashlib.sha256(datà).digest())


def 목록읽기():
    if OS.path_kind(ndepụta_ụzọ_ozi) == 0:
        return {}
    return json.loads(OS.read(ndepụta_ụzọ_ozi).decode("utf-8"))


def dee_ndekọ(ụzọ_ozi, datà):
    if OS.write(ụzọ_ozi, datà) != len(datà):
        raise OSError(28)


def cheèk_ụzọ_ozi(ụzọ_ozi):
    if not isinstance(ụzọ_ozi, str) or not ụzọ_ozi.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ụzọ_ozi.split("/")):
        raise ValueError("허용하지 않는 ngwungwu ụzọ_ozi")
    if "\\" in ụzọ_ozi or any(ord(mkpụrụedemede_valuu) < 32 or ord(mkpụrụedemede_valuu) == 127 for mkpụrụedemede_valuu in ụzọ_ozi):
        raise ValueError("잘못된 ụzọ_ozi 문자")
    결과 = "/lib/" + ụzọ_ozi
    if len(결과.encode("utf-8")) > 63 or ụzọ_ozi in ("한국어.py", "ngwungwu.py"):
        raise ValueError("ngwungwu 경로가 너무 길거나 Ngwa_ihe_dịadị 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Bido = OS.ticks_ms()

    def 정확히읽기(자신, ogologo_valuu):
        datà = bytearray()
        while len(datà) < ogologo_valuu:
            if OS.ticks_ms() - 자신.Bido > 90000:
                raise ValueError("ngwungwu 중계 nzaghachi 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = OS.tcp_read(자신.종단, 512)
                except OSError as mmejọ:
                    if mmejọ.args[0] != 11:
                        raise
                    OS.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ngwungwu 전송이 중간에 끝났습니다.")
            개수 = min(ogologo_valuu - len(datà), len(자신.남은자료))
            datà.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            OS.sleep_ms(0)
        return bytes(datà)


def butùo(요청, 접속번호):
    if len(요청) > 96 or any(mkpụrụedemede_valuu not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for mkpụrụedemede_valuu in 요청):
        raise ValueError("사용법: pip install Aha 또는 Aha==버전")
    종단 = OS.tcp_open()
    try:
        Bido = OS.ticks_ms()
        while True:
            try:
                OS.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as mmejọ:
                if mmejọ.args[0] not in (11, 115) or OS.ticks_ms() - Bido > 5000:
                    raise ValueError("ngwungwu 중계 Banye ọdịdà_valuu: 호스트에서 --network --pip로 실행하십시오.")
                OS.sleep_ms(10)
        datà = (요청 + "\n").encode()
        while datà:
            try:
                개수 = OS.tcp_write(종단, datà)
                if not 개수:
                    raise ValueError("ngwungwu 요청 dògharịa_valuu ọdịdà_valuu")
                datà = datà[개수:]
            except OSError as mmejọ:
                if mmejọ.args[0] != 11:
                    raise
                OS.sleep_ms(10)
                if OS.ticks_ms() - Bido > 10000:
                    raise ValueError("ngwungwu 요청 dògharịa_valuu 시간 초과")
        agịrị_valuu = 수신흐름(종단)
        머리 = agịrị_valuu.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ngwungwu dògharịa_valuu ngō_valuu 불일치")
        ogologo_valuu = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ogologo_valuu > 8192:
            raise ValueError("ngwungwu 명세가 너무 큽니다.")
        명세 = json.loads(agịrị_valuu.정확히읽기(ogologo_valuu).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ebensìbịa_èsèrèsè_osisi 파일은 1~16개여야 합니다.")
        if sum(ndebà_valuu["size"] for ndebà_valuu in 명세["files"]) > 65536:
            raise ValueError("ngwungwu ebensìbịa_èsèrèsè_osisi 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ndebà_valuu in 명세["files"]:
            ụzọ_ozi = cheèk_ụzọ_ozi(ndebà_valuu["path"])
            if ụzọ_ozi in 파일들 or not 0 <= ndebà_valuu["size"] <= 16384:
                raise ValueError("중복 ụzọ_ozi 또는 Faịlụ Ụhara 초과")
            datà = agịrị_valuu.정확히읽기(ndebà_valuu["size"])
            if 지문(datà) != ndebà_valuu["sha256"]:
                raise ValueError("ngwungwu Faịlụ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(datà.decode("utf-8"), ụzọ_ozi, "exec")
            파일들[ụzọ_ozi] = datà
            gc.collect()
        return 명세, 파일들
    finally:
        OS.udp_close(종단)


def wùbe_valuu(요청, 접속번호):
    print("ngwungwu butùo:", 요청)
    명세, 파일들 = butùo(요청, 접속번호)
    ndebà_ndepụta = 목록읽기()
    Aha = 명세["name"]
    if Aha in ndebà_ndepụta:
        if ndebà_ndepụta[Aha]["version"] == 명세["version"]:
            for ụzọ_ozi, 지문값 in ndebà_ndepụta[Aha]["files"].items():
                if OS.path_kind(ụzọ_ozi) != 1 or 지문(OS.read(ụzọ_ozi)) != 지문값:
                    raise ValueError("설치된 ngwungwu 파일이 달라졌습니다: " + ụzọ_ozi)
            print("이미 설치됨:", Aha, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Àzụ_valuu 설치하십시오.")
    for ụzọ_ozi in 파일들:
        if OS.path_kind(ụzọ_ozi):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ụzọ_ozi)
    ndebà_ndepụta[Aha] = {"version": 명세["version"], "files": {ụzọ_ozi: 지문(datà) for ụzọ_ozi, datà in 파일들.items()}}
    새목록 = json.dumps(ndebà_ndepụta).encode()
    if len(새목록) > 16384:
        raise ValueError("ngwungwu ndebà_ndepụta Ụhara 초과")
    이전목록 = OS.read(ndepụta_ụzọ_ozi) if OS.path_kind(ndepụta_ụzọ_ozi) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ụzọ_ozi, datà in 파일들.items():
            부분들 = ụzọ_ozi.split("/")
            for 수 in range(2, len(부분들)):
                dàịrektrị_valuu = "/".join(부분들[:수])
                종류 = OS.path_kind(dàịrektrị_valuu)
                if 종류 == 0:
                    OS.mkdir(dàịrektrị_valuu)
                    만든폴더.append(dàịrektrị_valuu)
                elif 종류 != 2:
                    raise ValueError("dàịrektrị_valuu 경로에 파일이 있습니다: " + dàịrektrị_valuu)
            만든파일.append(ụzọ_ozi)
            dee_ndekọ(ụzọ_ozi, datà)
        dee_ndekọ(ndepụta_ụzọ_ozi, 새목록)
    except Exception:
        for ụzọ_ozi in 만든파일:
            if OS.path_kind(ụzọ_ozi):
                OS.remove(ụzọ_ozi)
        for dàịrektrị_valuu in reversed(만든폴더):
            OS.rmdir(dàịrektrị_valuu)
        if 이전목록 is not None:
            dee_ndekọ(ndepụta_ụzọ_ozi, 이전목록)
        elif OS.path_kind(ndepụta_ụzọ_ozi):
            OS.remove(ndepụta_ụzọ_ozi)
        raise
    print("wùbe_valuu 완료:", Aha, 명세["version"], "→ /lib (RAM)")


def wepụ_ndebà(Aha):
    ndebà_ndepụta = 목록읽기()
    if Aha not in ndebà_ndepụta:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Aha)
    for ụzọ_ozi, 지문값 in ndebà_ndepụta[Aha]["files"].items():
        if OS.path_kind(ụzọ_ozi) != 1 or 지문(OS.read(ụzọ_ozi)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ụzọ_ozi)
    for ụzọ_ozi in ndebà_ndepụta[Aha]["files"]:
        OS.remove(ụzọ_ozi)
    del ndebà_ndepụta[Aha]
    dee_ndekọ(ndepụta_ụzọ_ozi, json.dumps(ndebà_ndepụta).encode())
    print("wepụ_ndebà 완료:", Aha)


def Bido(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Aha, Ozi_Sistèm in 목록읽기().items():
            print(Aha, Ozi_Sistèm["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        wùbe_valuu(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        wepụ_ndebà(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ebensìbịa_èsèrèsè_osisi 설치기 (PyPA pip 전체가 아님)")
        print("pip install Aha[==버전] [--port 8027] | pip list | pip uninstall Aha")
        print("usu: Ngwaọrụ/mee_nnyemiwu.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Bido(sys.argv[1:])
    except Exception as mmejọ:
        print("ngwungwu mmejọ:", mmejọ)
        sys.exit(1)
