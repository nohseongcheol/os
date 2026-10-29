"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 dalal 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as doxalukaay

lim_Yoonu_jëmale = "/lib/.pip.json"


def 지문(mbir):
    return "".join("%02x" % xëyma for xëyma in hashlib.sha256(mbir).digest())


def 목록읽기():
    if doxalukaay.path_kind(lim_Yoonu_jëmale) == 0:
        return {}
    return json.loads(doxalukaay.read(lim_Yoonu_jëmale).decode("utf-8"))


def biir_làq(Yoonu_jëmale, mbir):
    if doxalukaay.write(Yoonu_jëmale, mbir) != len(mbir):
        raise OSError(28)


def sek_Yoonu_jëmale(Yoonu_jëmale):
    if not isinstance(Yoonu_jëmale, str) or not Yoonu_jëmale.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Yoonu_jëmale.split("/")):
        raise ValueError("허용하지 않는 takku_xéewël Yoonu_jëmale")
    if "\\" in Yoonu_jëmale or any(ord(Araf_xëyma) < 32 or ord(Araf_xëyma) == 127 for Araf_xëyma in Yoonu_jëmale):
        raise ValueError("잘못된 Yoonu_jëmale 문자")
    결과 = "/lib/" + Yoonu_jëmale
    if len(결과.encode("utf-8")) > 63 or Yoonu_jëmale in ("한국어.py", "takku_xéewël.py"):
        raise ValueError("takku_xéewël 경로가 너무 길거나 xayma_bi_teew 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.daw = doxalukaay.ticks_ms()

    def 정확히읽기(자신, diir_xëyma):
        mbir = bytearray()
        while len(mbir) < diir_xëyma:
            if doxalukaay.ticks_ms() - 자신.daw > 90000:
                raise ValueError("takku_xéewël 중계 tontu 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = doxalukaay.tcp_read(자신.종단, 512)
                except OSError as njumte:
                    if njumte.args[0] != 11:
                        raise
                    doxalukaay.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("takku_xéewël 전송이 중간에 끝났습니다.")
            개수 = min(diir_xëyma - len(mbir), len(자신.남은자료))
            mbir.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            doxalukaay.sleep_ms(0)
        return bytes(mbir)


def yebbi(요청, 접속번호):
    if len(요청) > 96 or any(Araf_xëyma not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for Araf_xëyma in 요청):
        raise ValueError("사용법: pip install tur_253d1510 또는 tur_253d1510==버전")
    종단 = doxalukaay.tcp_open()
    try:
        daw = doxalukaay.ticks_ms()
        while True:
            try:
                doxalukaay.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as njumte:
                if njumte.args[0] not in (11, 115) or doxalukaay.ticks_ms() - daw > 5000:
                    raise ValueError("takku_xéewël 중계 JOKKOO foo_xëyma: 호스트에서 --network --pip로 실행하십시오.")
                doxalukaay.sleep_ms(10)
        mbir = (요청 + "\n").encode()
        while mbir:
            try:
                개수 = doxalukaay.tcp_write(종단, mbir)
                if not 개수:
                    raise ValueError("takku_xéewël 요청 toxal_xëyma_630ba093 foo_xëyma")
                mbir = mbir[개수:]
            except OSError as njumte:
                if njumte.args[0] != 11:
                    raise
                doxalukaay.sleep_ms(10)
                if doxalukaay.ticks_ms() - daw > 10000:
                    raise ValueError("takku_xéewël 요청 toxal_xëyma_630ba093 시간 초과")
        dawal_xëyma = 수신흐름(종단)
        머리 = dawal_xëyma.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("takku_xéewël toxal_xëyma_630ba093 ay_xëyma 불일치")
        diir_xëyma = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if diir_xëyma > 8192:
            raise ValueError("takku_xéewël 명세가 너무 큽니다.")
        명세 = json.loads(dawal_xëyma.정확히읽기(diir_xëyma).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 Cosaan_tëralinuy_pàcc 파일은 1~16개여야 합니다.")
        if sum(dugal_xabaar_xëyma["size"] for dugal_xabaar_xëyma in 명세["files"]) > 65536:
            raise ValueError("takku_xéewël Cosaan_tëralinuy_pàcc 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for dugal_xabaar_xëyma in 명세["files"]:
            Yoonu_jëmale = sek_Yoonu_jëmale(dugal_xabaar_xëyma["path"])
            if Yoonu_jëmale in 파일들 or not 0 <= dugal_xabaar_xëyma["size"] <= 16384:
                raise ValueError("중복 Yoonu_jëmale 또는 bara_denc tolluwaay 초과")
            mbir = dawal_xëyma.정확히읽기(dugal_xabaar_xëyma["size"])
            if 지문(mbir) != dugal_xabaar_xëyma["sha256"]:
                raise ValueError("takku_xéewël bara_denc SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(mbir.decode("utf-8"), Yoonu_jëmale, "exec")
            파일들[Yoonu_jëmale] = mbir
            gc.collect()
        return 명세, 파일들
    finally:
        doxalukaay.udp_close(종단)


def samp_xëyma(요청, 접속번호):
    print("takku_xéewël yebbi:", 요청)
    명세, 파일들 = yebbi(요청, 접속번호)
    dugal_xabaar_lim = 목록읽기()
    tur_253d1510 = 명세["name"]
    if tur_253d1510 in dugal_xabaar_lim:
        if dugal_xabaar_lim[tur_253d1510]["version"] == 명세["version"]:
            for Yoonu_jëmale, 지문값 in dugal_xabaar_lim[tur_253d1510]["files"].items():
                if doxalukaay.path_kind(Yoonu_jëmale) != 1 or 지문(doxalukaay.read(Yoonu_jëmale)) != 지문값:
                    raise ValueError("설치된 takku_xéewël 파일이 달라졌습니다: " + Yoonu_jëmale)
            print("이미 설치됨:", tur_253d1510, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 woñeeku_xëyma 설치하십시오.")
    for Yoonu_jëmale in 파일들:
        if doxalukaay.path_kind(Yoonu_jëmale):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Yoonu_jëmale)
    dugal_xabaar_lim[tur_253d1510] = {"version": 명세["version"], "files": {Yoonu_jëmale: 지문(mbir) for Yoonu_jëmale, mbir in 파일들.items()}}
    새목록 = json.dumps(dugal_xabaar_lim).encode()
    if len(새목록) > 16384:
        raise ValueError("takku_xéewël dugal_xabaar_lim tolluwaay 초과")
    이전목록 = doxalukaay.read(lim_Yoonu_jëmale) if doxalukaay.path_kind(lim_Yoonu_jëmale) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Yoonu_jëmale, mbir in 파일들.items():
            부분들 = Yoonu_jëmale.split("/")
            for 수 in range(2, len(부분들)):
                dàmb_xëyma = "/".join(부분들[:수])
                종류 = doxalukaay.path_kind(dàmb_xëyma)
                if 종류 == 0:
                    doxalukaay.mkdir(dàmb_xëyma)
                    만든폴더.append(dàmb_xëyma)
                elif 종류 != 2:
                    raise ValueError("dàmb_xëyma 경로에 파일이 있습니다: " + dàmb_xëyma)
            만든파일.append(Yoonu_jëmale)
            biir_làq(Yoonu_jëmale, mbir)
        biir_làq(lim_Yoonu_jëmale, 새목록)
    except Exception:
        for Yoonu_jëmale in 만든파일:
            if doxalukaay.path_kind(Yoonu_jëmale):
                doxalukaay.remove(Yoonu_jëmale)
        for dàmb_xëyma in reversed(만든폴더):
            doxalukaay.rmdir(dàmb_xëyma)
        if 이전목록 is not None:
            biir_làq(lim_Yoonu_jëmale, 이전목록)
        elif doxalukaay.path_kind(lim_Yoonu_jëmale):
            doxalukaay.remove(lim_Yoonu_jëmale)
        raise
    print("samp_xëyma 완료:", tur_253d1510, 명세["version"], "→ /lib (RAM)")


def dandal_dugal_xabaar(tur_253d1510):
    dugal_xabaar_lim = 목록읽기()
    if tur_253d1510 not in dugal_xabaar_lim:
        raise ValueError("설치되지 않은 꾸러미입니다: " + tur_253d1510)
    for Yoonu_jëmale, 지문값 in dugal_xabaar_lim[tur_253d1510]["files"].items():
        if doxalukaay.path_kind(Yoonu_jëmale) != 1 or 지문(doxalukaay.read(Yoonu_jëmale)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Yoonu_jëmale)
    for Yoonu_jëmale in dugal_xabaar_lim[tur_253d1510]["files"]:
        doxalukaay.remove(Yoonu_jëmale)
    del dugal_xabaar_lim[tur_253d1510]
    biir_làq(lim_Yoonu_jëmale, json.dumps(dugal_xabaar_lim).encode())
    print("dandal_dugal_xabaar 완료:", tur_253d1510)


def daw(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for tur_253d1510, msinfo32_exe in 목록읽기().items():
            print(tur_253d1510, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        samp_xëyma(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        dandal_dugal_xabaar(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython Cosaan_tëralinuy_pàcc 설치기 (PyPA pip 전체가 아님)")
        print("pip install tur_253d1510[==버전] [--port 8027] | pip list | pip uninstall tur_253d1510")
        print("dalal: Jumtukaay_yi/def_ndigel.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        daw(sys.argv[1:])
    except Exception as njumte:
        print("takku_xéewël njumte:", njumte)
        sys.exit(1)
