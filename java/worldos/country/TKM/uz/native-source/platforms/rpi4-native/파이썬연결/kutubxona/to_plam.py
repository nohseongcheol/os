"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 tashkilotchi 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operatsion_tizim

Ro_yxat_yo_l = "/lib/.pip.json"


def 지문(ma_lumotlar):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(ma_lumotlar).digest())


def 목록읽기():
    if operatsion_tizim.path_kind(Ro_yxat_yo_l) == 0:
        return {}
    return json.loads(operatsion_tizim.read(Ro_yxat_yo_l).decode("utf-8"))


def yozmoq_LOG(yo_l, ma_lumotlar):
    if operatsion_tizim.write(yo_l, ma_lumotlar) != len(ma_lumotlar):
        raise OSError(28)


def chek_yo_l(yo_l):
    if not isinstance(yo_l, str) or not yo_l.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in yo_l.split("/")):
        raise ValueError("허용하지 않는 to_plam yo_l")
    if "\\" in yo_l or any(ord(belgi_VALUE) < 32 or ord(belgi_VALUE) == 127 for belgi_VALUE in yo_l):
        raise ValueError("잘못된 yo_l 문자")
    o_lchov = "/lib/" + yo_l
    if len(o_lchov.encode("utf-8")) > 63 or yo_l in ("한국어.py", "to_plam.py"):
        raise ValueError("to_plam 경로가 너무 길거나 sukut_bo_yicha_qiymat 라이브러리와 겹칩니다.")
    return o_lchov


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Bajarish = operatsion_tizim.ticks_ms()

    def 정확히읽기(자신, uzunlik_VALUE):
        ma_lumotlar = bytearray()
        while len(ma_lumotlar) < uzunlik_VALUE:
            if operatsion_tizim.ticks_ms() - 자신.Bajarish > 90000:
                raise ValueError("to_plam 중계 javob_berish TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operatsion_tizim.tcp_read(자신.종단, 512)
                except OSError as Xato:
                    if Xato.args[0] != 11:
                        raise
                    operatsion_tizim.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("to_plam 전송이 중간에 끝났습니다.")
            element_COUNT = min(uzunlik_VALUE - len(ma_lumotlar), len(자신.남은자료))
            ma_lumotlar.extend(자신.남은자료[:element_COUNT])
            자신.남은자료 = 자신.남은자료[element_COUNT:]
            operatsion_tizim.sleep_ms(0)
        return bytes(ma_lumotlar)


def yuklamoq(요청, 접속번호):
    if len(요청) > 96 or any(belgi_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for belgi_VALUE in 요청):
        raise ValueError("사용법: pip install Nomi 또는 Nomi==버전")
    종단 = operatsion_tizim.tcp_open()
    try:
        Bajarish = operatsion_tizim.ticks_ms()
        while True:
            try:
                operatsion_tizim.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Xato:
                if Xato.args[0] not in (11, 115) or operatsion_tizim.ticks_ms() - Bajarish > 5000:
                    raise ValueError("to_plam 중계 Ulanish to_xtab_qolish_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operatsion_tizim.sleep_ms(10)
        ma_lumotlar = (요청 + "\n").encode()
        while ma_lumotlar:
            try:
                element_COUNT = operatsion_tizim.tcp_write(종단, ma_lumotlar)
                if not element_COUNT:
                    raise ValueError("to_plam 요청 uzatish_VALUE to_xtab_qolish_VALUE")
                ma_lumotlar = ma_lumotlar[element_COUNT:]
            except OSError as Xato:
                if Xato.args[0] != 11:
                    raise
                operatsion_tizim.sleep_ms(10)
                if operatsion_tizim.ticks_ms() - Bajarish > 10000:
                    raise ValueError("to_plam 요청 uzatish_VALUE TIME_VALUE 초과")
        oqim_VALUE = 수신흐름(종단)
        머리 = oqim_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("to_plam uzatish_VALUE murojaat_VALUE 불일치")
        uzunlik_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if uzunlik_VALUE > 8192:
            raise ValueError("to_plam 명세가 너무 큽니다.")
        명세 = json.loads(oqim_VALUE.정확히읽기(uzunlik_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 manba_daraxt 파일은 1~16개여야 합니다.")
        if sum(kiritish_VALUE["size"] for kiritish_VALUE in 명세["files"]) > 65536:
            raise ValueError("to_plam manba_daraxt 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for kiritish_VALUE in 명세["files"]:
            yo_l = chek_yo_l(kiritish_VALUE["path"])
            if yo_l in 파일들 or not 0 <= kiritish_VALUE["size"] <= 16384:
                raise ValueError("중복 yo_l 또는 Fayl Hajmi 초과")
            ma_lumotlar = oqim_VALUE.정확히읽기(kiritish_VALUE["size"])
            if 지문(ma_lumotlar) != kiritish_VALUE["sha256"]:
                raise ValueError("to_plam Fayl SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ma_lumotlar.decode("utf-8"), yo_l, "exec")
            파일들[yo_l] = ma_lumotlar
            gc.collect()
        return 명세, 파일들
    finally:
        operatsion_tizim.udp_close(종단)


def o_rnatish_VALUE(요청, 접속번호):
    print("to_plam yuklamoq:", 요청)
    명세, 파일들 = yuklamoq(요청, 접속번호)
    kiritish_Ro_yxat = 목록읽기()
    Nomi = 명세["name"]
    if Nomi in kiritish_Ro_yxat:
        if kiritish_Ro_yxat[Nomi]["version"] == 명세["version"]:
            for yo_l, 지문값 in kiritish_Ro_yxat[Nomi]["files"].items():
                if operatsion_tizim.path_kind(yo_l) != 1 or 지문(operatsion_tizim.read(yo_l)) != 지문값:
                    raise ValueError("설치된 to_plam 파일이 달라졌습니다: " + yo_l)
            print("이미 설치됨:", Nomi, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Orqaga_VALUE 설치하십시오.")
    for yo_l in 파일들:
        if operatsion_tizim.path_kind(yo_l):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + yo_l)
    kiritish_Ro_yxat[Nomi] = {"version": 명세["version"], "files": {yo_l: 지문(ma_lumotlar) for yo_l, ma_lumotlar in 파일들.items()}}
    새목록 = json.dumps(kiritish_Ro_yxat).encode()
    if len(새목록) > 16384:
        raise ValueError("to_plam kiritish_Ro_yxat Hajmi 초과")
    이전목록 = operatsion_tizim.read(Ro_yxat_yo_l) if operatsion_tizim.path_kind(Ro_yxat_yo_l) else None
    만든파일 = []
    만든폴더 = []
    try:
        for yo_l, ma_lumotlar in 파일들.items():
            부분들 = yo_l.split("/")
            for 수 in range(2, len(부분들)):
                katalog_VALUE = "/".join(부분들[:수])
                종류 = operatsion_tizim.path_kind(katalog_VALUE)
                if 종류 == 0:
                    operatsion_tizim.mkdir(katalog_VALUE)
                    만든폴더.append(katalog_VALUE)
                elif 종류 != 2:
                    raise ValueError("katalog_VALUE 경로에 파일이 있습니다: " + katalog_VALUE)
            만든파일.append(yo_l)
            yozmoq_LOG(yo_l, ma_lumotlar)
        yozmoq_LOG(Ro_yxat_yo_l, 새목록)
    except Exception:
        for yo_l in 만든파일:
            if operatsion_tizim.path_kind(yo_l):
                operatsion_tizim.remove(yo_l)
        for katalog_VALUE in reversed(만든폴더):
            operatsion_tizim.rmdir(katalog_VALUE)
        if 이전목록 is not None:
            yozmoq_LOG(Ro_yxat_yo_l, 이전목록)
        elif operatsion_tizim.path_kind(Ro_yxat_yo_l):
            operatsion_tizim.remove(Ro_yxat_yo_l)
        raise
    print("o_rnatish_VALUE 완료:", Nomi, 명세["version"], "→ /lib (RAM)")


def olib_tashlamoq_kiritish(Nomi):
    kiritish_Ro_yxat = 목록읽기()
    if Nomi not in kiritish_Ro_yxat:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nomi)
    for yo_l, 지문값 in kiritish_Ro_yxat[Nomi]["files"].items():
        if operatsion_tizim.path_kind(yo_l) != 1 or 지문(operatsion_tizim.read(yo_l)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + yo_l)
    for yo_l in kiritish_Ro_yxat[Nomi]["files"]:
        operatsion_tizim.remove(yo_l)
    del kiritish_Ro_yxat[Nomi]
    yozmoq_LOG(Ro_yxat_yo_l, json.dumps(kiritish_Ro_yxat).encode())
    print("olib_tashlamoq_kiritish 완료:", Nomi)


def Bajarish(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Nomi, msinfo32_exe in 목록읽기().items():
            print(Nomi, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        o_rnatish_VALUE(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        olib_tashlamoq_kiritish(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython manba_daraxt 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nomi[==버전] [--port 8027] | pip list | pip uninstall Nomi")
        print("tashkilotchi: Vositalar/bajarmoq_buyruq.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Bajarish(sys.argv[1:])
    except Exception as Xato:
        print("to_plam Xato:", Xato)
        sys.exit(1)
