"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 esasy 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operasiýa_ulgamy

Sanaw_ýol = "/lib/.pip.json"


def 지문(maglumat):
    return "".join("%02x" % baha for baha in hashlib.sha256(maglumat).digest())


def 목록읽기():
    if operasiýa_ulgamy.path_kind(Sanaw_ýol) == 0:
        return {}
    return json.loads(operasiýa_ulgamy.read(Sanaw_ýol).decode("utf-8"))


def ýaz_hasaba_alyş(Ýol, maglumat):
    if operasiýa_ulgamy.write(Ýol, maglumat) != len(maglumat):
        raise OSError(28)


def derňe_ýol(Ýol):
    if not isinstance(Ýol, str) or not Ýol.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Ýol.split("/")):
        raise ValueError("허용하지 않는 toplum Ýol")
    if "\\" in Ýol or any(ord(nyşan_baha_068c2631) < 32 or ord(nyşan_baha_068c2631) == 127 for nyşan_baha_068c2631 in Ýol):
        raise ValueError("잘못된 Ýol 문자")
    결과 = "/lib/" + Ýol
    if len(결과.encode("utf-8")) > 63 or Ýol in ("한국어.py", "toplum.py"):
        raise ValueError("toplum 경로가 너무 길거나 öňünden_kabul_edilen_baha 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Bitir = operasiýa_ulgamy.ticks_ms()

    def 정확히읽기(자신, dowamlylyk_baha):
        maglumat = bytearray()
        while len(maglumat) < dowamlylyk_baha:
            if operasiýa_ulgamy.ticks_ms() - 자신.Bitir > 90000:
                raise ValueError("toplum 중계 jogap_bermek 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operasiýa_ulgamy.tcp_read(자신.종단, 512)
                except OSError as Hata:
                    if Hata.args[0] != 11:
                        raise
                    operasiýa_ulgamy.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("toplum 전송이 중간에 끝났습니다.")
            개수 = min(dowamlylyk_baha - len(maglumat), len(자신.남은자료))
            maglumat.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            operasiýa_ulgamy.sleep_ms(0)
        return bytes(maglumat)


def göçürim(요청, 접속번호):
    if len(요청) > 96 or any(nyşan_baha_068c2631 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for nyşan_baha_068c2631 in 요청):
        raise ValueError("사용법: pip install Ad 또는 Ad==버전")
    종단 = operasiýa_ulgamy.tcp_open()
    try:
        Bitir = operasiýa_ulgamy.ticks_ms()
        while True:
            try:
                operasiýa_ulgamy.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Hata:
                if Hata.args[0] not in (11, 115) or operasiýa_ulgamy.ticks_ms() - Bitir > 5000:
                    raise ValueError("toplum 중계 Birikme näsazlyk_baha: 호스트에서 --network --pip로 실행하십시오.")
                operasiýa_ulgamy.sleep_ms(10)
        maglumat = (요청 + "\n").encode()
        while maglumat:
            try:
                개수 = operasiýa_ulgamy.tcp_write(종단, maglumat)
                if not 개수:
                    raise ValueError("toplum 요청 geçir_baha näsazlyk_baha")
                maglumat = maglumat[개수:]
            except OSError as Hata:
                if Hata.args[0] != 11:
                    raise
                operasiýa_ulgamy.sleep_ms(10)
                if operasiýa_ulgamy.ticks_ms() - Bitir > 10000:
                    raise ValueError("toplum 요청 geçir_baha 시간 초과")
        Stream_baha = 수신흐름(종단)
        머리 = Stream_baha.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("toplum geçir_baha ýumuş_baha_102996da 불일치")
        dowamlylyk_baha = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if dowamlylyk_baha > 8192:
            raise ValueError("toplum 명세가 너무 큽니다.")
        명세 = json.loads(Stream_baha.정확히읽기(dowamlylyk_baha).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 gor_agaç 파일은 1~16개여야 합니다.")
        if sum(girizmeklik_baha["size"] for girizmeklik_baha in 명세["files"]) > 65536:
            raise ValueError("toplum gor_agaç 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for girizmeklik_baha in 명세["files"]:
            Ýol = derňe_ýol(girizmeklik_baha["path"])
            if Ýol in 파일들 or not 0 <= girizmeklik_baha["size"] <= 16384:
                raise ValueError("중복 Ýol 또는 Faýl Ululyk 초과")
            maglumat = Stream_baha.정확히읽기(girizmeklik_baha["size"])
            if 지문(maglumat) != girizmeklik_baha["sha256"]:
                raise ValueError("toplum Faýl SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(maglumat.decode("utf-8"), Ýol, "exec")
            파일들[Ýol] = maglumat
            gc.collect()
        return 명세, 파일들
    finally:
        operasiýa_ulgamy.udp_close(종단)


def gurna_baha(요청, 접속번호):
    print("toplum göçürim:", 요청)
    명세, 파일들 = göçürim(요청, 접속번호)
    girizmeklik_Sanaw = 목록읽기()
    Ad = 명세["name"]
    if Ad in girizmeklik_Sanaw:
        if girizmeklik_Sanaw[Ad]["version"] == 명세["version"]:
            for Ýol, 지문값 in girizmeklik_Sanaw[Ad]["files"].items():
                if operasiýa_ulgamy.path_kind(Ýol) != 1 or 지문(operasiýa_ulgamy.read(Ýol)) != 지문값:
                    raise ValueError("설치된 toplum 파일이 달라졌습니다: " + Ýol)
            print("이미 설치됨:", Ad, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Yza_baha 설치하십시오.")
    for Ýol in 파일들:
        if operasiýa_ulgamy.path_kind(Ýol):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Ýol)
    girizmeklik_Sanaw[Ad] = {"version": 명세["version"], "files": {Ýol: 지문(maglumat) for Ýol, maglumat in 파일들.items()}}
    새목록 = json.dumps(girizmeklik_Sanaw).encode()
    if len(새목록) > 16384:
        raise ValueError("toplum girizmeklik_Sanaw Ululyk 초과")
    이전목록 = operasiýa_ulgamy.read(Sanaw_ýol) if operasiýa_ulgamy.path_kind(Sanaw_ýol) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Ýol, maglumat in 파일들.items():
            부분들 = Ýol.split("/")
            for 수 in range(2, len(부분들)):
                katalog_baha = "/".join(부분들[:수])
                종류 = operasiýa_ulgamy.path_kind(katalog_baha)
                if 종류 == 0:
                    operasiýa_ulgamy.mkdir(katalog_baha)
                    만든폴더.append(katalog_baha)
                elif 종류 != 2:
                    raise ValueError("katalog_baha 경로에 파일이 있습니다: " + katalog_baha)
            만든파일.append(Ýol)
            ýaz_hasaba_alyş(Ýol, maglumat)
        ýaz_hasaba_alyş(Sanaw_ýol, 새목록)
    except Exception:
        for Ýol in 만든파일:
            if operasiýa_ulgamy.path_kind(Ýol):
                operasiýa_ulgamy.remove(Ýol)
        for katalog_baha in reversed(만든폴더):
            operasiýa_ulgamy.rmdir(katalog_baha)
        if 이전목록 is not None:
            ýaz_hasaba_alyş(Sanaw_ýol, 이전목록)
        elif operasiýa_ulgamy.path_kind(Sanaw_ýol):
            operasiýa_ulgamy.remove(Sanaw_ýol)
        raise
    print("gurna_baha 완료:", Ad, 명세["version"], "→ /lib (RAM)")


def aýyr_girizmeklik(Ad):
    girizmeklik_Sanaw = 목록읽기()
    if Ad not in girizmeklik_Sanaw:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ad)
    for Ýol, 지문값 in girizmeklik_Sanaw[Ad]["files"].items():
        if operasiýa_ulgamy.path_kind(Ýol) != 1 or 지문(operasiýa_ulgamy.read(Ýol)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Ýol)
    for Ýol in girizmeklik_Sanaw[Ad]["files"]:
        operasiýa_ulgamy.remove(Ýol)
    del girizmeklik_Sanaw[Ad]
    ýaz_hasaba_alyş(Sanaw_ýol, json.dumps(girizmeklik_Sanaw).encode())
    print("aýyr_girizmeklik 완료:", Ad)


def Bitir(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Ad, msinfo32_exe in 목록읽기().items():
            print(Ad, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        gurna_baha(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        aýyr_girizmeklik(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython gor_agaç 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ad[==버전] [--port 8027] | pip list | pip uninstall Ad")
        print("esasy: Gurallar/ýerine_ýetir_buýruk.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Bitir(sys.argv[1:])
    except Exception as Hata:
        print("toplum Hata:", Hata)
        sys.exit(1)
