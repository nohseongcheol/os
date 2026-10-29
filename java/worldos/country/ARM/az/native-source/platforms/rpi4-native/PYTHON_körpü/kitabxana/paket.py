"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as əməliyyat_sistemi

Siyahı_yol = "/lib/.pip.json"


def 지문(verilənlər):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(verilənlər).digest())


def 목록읽기():
    if əməliyyat_sistemi.path_kind(Siyahı_yol) == 0:
        return {}
    return json.loads(əməliyyat_sistemi.read(Siyahı_yol).decode("utf-8"))


def yazmaq_LOG(Cığır, verilənlər):
    if əməliyyat_sistemi.write(Cığır, verilənlər) != len(verilənlər):
        raise OSError(28)


def çek_yol(Cığır):
    if not isinstance(Cığır, str) or not Cığır.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Cığır.split("/")):
        raise ValueError("허용하지 않는 paket Cığır")
    if "\\" in Cığır or any(ord(simvol_VALUE_068c2631) < 32 or ord(simvol_VALUE_068c2631) == 127 for simvol_VALUE_068c2631 in Cığır):
        raise ValueError("잘못된 Cığır 문자")
    ölçü = "/lib/" + Cığır
    if len(ölçü.encode("utf-8")) > 63 or Cığır in ("한국어.py", "paket.py"):
        raise ValueError("paket 경로가 너무 길거나 standart_qiymət 라이브러리와 겹칩니다.")
    return ölçü


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.İcra_Et = əməliyyat_sistemi.ticks_ms()

    def 정확히읽기(자신, uzunluq_VALUE):
        verilənlər = bytearray()
        while len(verilənlər) < uzunluq_VALUE:
            if əməliyyat_sistemi.ticks_ms() - 자신.İcra_Et > 90000:
                raise ValueError("paket 중계 cavab TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = əməliyyat_sistemi.tcp_read(자신.종단, 512)
                except OSError as XƏTA:
                    if XƏTA.args[0] != 11:
                        raise
                    əməliyyat_sistemi.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paket 전송이 중간에 끝났습니다.")
            element_COUNT = min(uzunluq_VALUE - len(verilənlər), len(자신.남은자료))
            verilənlər.extend(자신.남은자료[:element_COUNT])
            자신.남은자료 = 자신.남은자료[element_COUNT:]
            əməliyyat_sistemi.sleep_ms(0)
        return bytes(verilənlər)


def yüklə(HTTP_sorğusu, 접속번호):
    if len(HTTP_sorğusu) > 96 or any(simvol_VALUE_068c2631 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for simvol_VALUE_068c2631 in HTTP_sorğusu):
        raise ValueError("사용법: pip install Ad 또는 Ad==버전")
    종단 = əməliyyat_sistemi.tcp_open()
    try:
        İcra_Et = əməliyyat_sistemi.ticks_ms()
        while True:
            try:
                əməliyyat_sistemi.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as XƏTA:
                if XƏTA.args[0] not in (11, 115) or əməliyyat_sistemi.ticks_ms() - İcra_Et > 5000:
                    raise ValueError("paket 중계 Bağlan xəta_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                əməliyyat_sistemi.sleep_ms(10)
        verilənlər = (HTTP_sorğusu + "\n").encode()
        while verilənlər:
            try:
                element_COUNT = əməliyyat_sistemi.tcp_write(종단, verilənlər)
                if not element_COUNT:
                    raise ValueError("paket HTTP_sorğusu ötürmə_VALUE xəta_VALUE")
                verilənlər = verilənlər[element_COUNT:]
            except OSError as XƏTA:
                if XƏTA.args[0] != 11:
                    raise
                əməliyyat_sistemi.sleep_ms(10)
                if əməliyyat_sistemi.ticks_ms() - İcra_Et > 10000:
                    raise ValueError("paket HTTP_sorğusu ötürmə_VALUE TIME_VALUE 초과")
        axın_VALUE = 수신흐름(종단)
        머리 = axın_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("paket ötürmə_VALUE müqavilə_VALUE 불일치")
        uzunluq_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if uzunluq_VALUE > 8192:
            raise ValueError("paket 명세가 너무 큽니다.")
        명세 = json.loads(axın_VALUE.정확히읽기(uzunluq_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 mənbə_ağac 파일은 1~16개여야 합니다.")
        if sum(daxiletmə_VALUE["size"] for daxiletmə_VALUE in 명세["files"]) > 65536:
            raise ValueError("paket mənbə_ağac 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for daxiletmə_VALUE in 명세["files"]:
            Cığır = çek_yol(daxiletmə_VALUE["path"])
            if Cığır in 파일들 or not 0 <= daxiletmə_VALUE["size"] <= 16384:
                raise ValueError("중복 Cığır 또는 FAYL Böyüklük 초과")
            verilənlər = axın_VALUE.정확히읽기(daxiletmə_VALUE["size"])
            if 지문(verilənlər) != daxiletmə_VALUE["sha256"]:
                raise ValueError("paket FAYL SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(verilənlər.decode("utf-8"), Cığır, "exec")
            파일들[Cığır] = verilənlər
            gc.collect()
        return 명세, 파일들
    finally:
        əməliyyat_sistemi.udp_close(종단)


def quraşdır_VALUE(HTTP_sorğusu, 접속번호):
    print("paket yüklə:", HTTP_sorğusu)
    명세, 파일들 = yüklə(HTTP_sorğusu, 접속번호)
    daxiletmə_Siyahı = 목록읽기()
    Ad = 명세["name"]
    if Ad in daxiletmə_Siyahı:
        if daxiletmə_Siyahı[Ad]["version"] == 명세["version"]:
            for Cığır, 지문값 in daxiletmə_Siyahı[Ad]["files"].items():
                if əməliyyat_sistemi.path_kind(Cığır) != 1 or 지문(əməliyyat_sistemi.read(Cığır)) != 지문값:
                    raise ValueError("설치된 paket 파일이 달라졌습니다: " + Cığır)
            print("이미 설치됨:", Ad, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 GERİ_VALUE 설치하십시오.")
    for Cığır in 파일들:
        if əməliyyat_sistemi.path_kind(Cığır):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Cığır)
    daxiletmə_Siyahı[Ad] = {"version": 명세["version"], "files": {Cığır: 지문(verilənlər) for Cığır, verilənlər in 파일들.items()}}
    새목록 = json.dumps(daxiletmə_Siyahı).encode()
    if len(새목록) > 16384:
        raise ValueError("paket daxiletmə_Siyahı Böyüklük 초과")
    이전목록 = əməliyyat_sistemi.read(Siyahı_yol) if əməliyyat_sistemi.path_kind(Siyahı_yol) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Cığır, verilənlər in 파일들.items():
            부분들 = Cığır.split("/")
            for 수 in range(2, len(부분들)):
                kataloq_VALUE = "/".join(부분들[:수])
                종류 = əməliyyat_sistemi.path_kind(kataloq_VALUE)
                if 종류 == 0:
                    əməliyyat_sistemi.mkdir(kataloq_VALUE)
                    만든폴더.append(kataloq_VALUE)
                elif 종류 != 2:
                    raise ValueError("kataloq_VALUE 경로에 파일이 있습니다: " + kataloq_VALUE)
            만든파일.append(Cığır)
            yazmaq_LOG(Cığır, verilənlər)
        yazmaq_LOG(Siyahı_yol, 새목록)
    except Exception:
        for Cığır in 만든파일:
            if əməliyyat_sistemi.path_kind(Cığır):
                əməliyyat_sistemi.remove(Cığır)
        for kataloq_VALUE in reversed(만든폴더):
            əməliyyat_sistemi.rmdir(kataloq_VALUE)
        if 이전목록 is not None:
            yazmaq_LOG(Siyahı_yol, 이전목록)
        elif əməliyyat_sistemi.path_kind(Siyahı_yol):
            əməliyyat_sistemi.remove(Siyahı_yol)
        raise
    print("quraşdır_VALUE 완료:", Ad, 명세["version"], "→ /lib (RAM)")


def silmək_daxiletmə(Ad):
    daxiletmə_Siyahı = 목록읽기()
    if Ad not in daxiletmə_Siyahı:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ad)
    for Cığır, 지문값 in daxiletmə_Siyahı[Ad]["files"].items():
        if əməliyyat_sistemi.path_kind(Cığır) != 1 or 지문(əməliyyat_sistemi.read(Cığır)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Cığır)
    for Cığır in daxiletmə_Siyahı[Ad]["files"]:
        əməliyyat_sistemi.remove(Cığır)
    del daxiletmə_Siyahı[Ad]
    yazmaq_LOG(Siyahı_yol, json.dumps(daxiletmə_Siyahı).encode())
    print("silmək_daxiletmə 완료:", Ad)


def İcra_Et(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Ad, msinfo32_exe in 목록읽기().items():
            print(Ad, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        quraşdır_VALUE(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        silmək_daxiletmə(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython mənbə_ağac 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ad[==버전] [--port 8027] | pip list | pip uninstall Ad")
        print("host: Alətlər/icra_etmək_əmr.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        İcra_Et(sys.argv[1:])
    except Exception as XƏTA:
        print("paket XƏTA:", XƏTA)
        sys.exit(1)
