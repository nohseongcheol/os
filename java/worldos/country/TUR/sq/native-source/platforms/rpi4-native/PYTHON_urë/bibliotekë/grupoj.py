"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 pritës 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistem_operativ

Listë_shteg = "/lib/.pip.json"


def 지문(të_dhëna):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(të_dhëna).digest())


def 목록읽기():
    if sistem_operativ.path_kind(Listë_shteg) == 0:
        return {}
    return json.loads(sistem_operativ.read(Listë_shteg).decode("utf-8"))


def shkruaj_LOG(POZICIONI, të_dhëna):
    if sistem_operativ.write(POZICIONI, të_dhëna) != len(të_dhëna):
        raise OSError(28)


def çek_shteg(POZICIONI):
    if not isinstance(POZICIONI, str) or not POZICIONI.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in POZICIONI.split("/")):
        raise ValueError("허용하지 않는 grupoj POZICIONI")
    if "\\" in POZICIONI or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in POZICIONI):
        raise ValueError("잘못된 POZICIONI 문자")
    llogaritje = "/lib/" + POZICIONI
    if len(llogaritje.encode("utf-8")) > 63 or POZICIONI in ("한국어.py", "grupoj.py"):
        raise ValueError("grupoj 경로가 너무 길거나 vlerë_e_parazgjedhur 라이브러리와 겹칩니다.")
    return llogaritje


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Ekzekuto = sistem_operativ.ticks_ms()

    def 정확히읽기(자신, gjatësi_VALUE):
        të_dhëna = bytearray()
        while len(të_dhëna) < gjatësi_VALUE:
            if sistem_operativ.ticks_ms() - 자신.Ekzekuto > 90000:
                raise ValueError("grupoj 중계 replikë Ora_VALUE_4692cef5 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistem_operativ.tcp_read(자신.종단, 512)
                except OSError as GABIM:
                    if GABIM.args[0] != 11:
                        raise
                    sistem_operativ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("grupoj 전송이 중간에 끝났습니다.")
            njësi_COUNT = min(gjatësi_VALUE - len(të_dhëna), len(자신.남은자료))
            të_dhëna.extend(자신.남은자료[:njësi_COUNT])
            자신.남은자료 = 자신.남은자료[njësi_COUNT:]
            sistem_operativ.sleep_ms(0)
        return bytes(të_dhëna)


def shkarkim(요청, numri_i_portës):
    if len(요청) > 96 or any(karakter_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karakter_VALUE in 요청):
        raise ValueError("사용법: pip install Emër 또는 Emër==버전")
    종단 = sistem_operativ.tcp_open()
    try:
        Ekzekuto = sistem_operativ.ticks_ms()
        while True:
            try:
                sistem_operativ.tcp_connect(종단, "10.0.2.2", numri_i_portës)
                break
            except OSError as GABIM:
                if GABIM.args[0] not in (11, 115) or sistem_operativ.ticks_ms() - Ekzekuto > 5000:
                    raise ValueError("grupoj 중계 Lidhu dështim_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                sistem_operativ.sleep_ms(10)
        të_dhëna = (요청 + "\n").encode()
        while të_dhëna:
            try:
                njësi_COUNT = sistem_operativ.tcp_write(종단, të_dhëna)
                if not njësi_COUNT:
                    raise ValueError("grupoj 요청 transferim_VALUE dështim_VALUE")
                të_dhëna = të_dhëna[njësi_COUNT:]
            except OSError as GABIM:
                if GABIM.args[0] != 11:
                    raise
                sistem_operativ.sleep_ms(10)
                if sistem_operativ.ticks_ms() - Ekzekuto > 10000:
                    raise ValueError("grupoj 요청 transferim_VALUE Ora_VALUE_4692cef5 초과")
        Stream_VALUE = 수신흐름(종단)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("grupoj transferim_VALUE punë_VALUE 불일치")
        gjatësi_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if gjatësi_VALUE > 8192:
            raise ValueError("grupoj 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(gjatësi_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 burim_degëzim 파일은 1~16개여야 합니다.")
        if sum(futje_VALUE["size"] for futje_VALUE in 명세["files"]) > 65536:
            raise ValueError("grupoj burim_degëzim 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for futje_VALUE in 명세["files"]:
            POZICIONI = çek_shteg(futje_VALUE["path"])
            if POZICIONI in 파일들 or not 0 <= futje_VALUE["size"] <= 16384:
                raise ValueError("중복 POZICIONI 또는 Kartelë Madhësi 초과")
            të_dhëna = Stream_VALUE.정확히읽기(futje_VALUE["size"])
            if 지문(të_dhëna) != futje_VALUE["sha256"]:
                raise ValueError("grupoj Kartelë SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(të_dhëna.decode("utf-8"), POZICIONI, "exec")
            파일들[POZICIONI] = të_dhëna
            gc.collect()
        return 명세, 파일들
    finally:
        sistem_operativ.udp_close(종단)


def instaloj_VALUE(요청, numri_i_portës):
    print("grupoj shkarkim:", 요청)
    명세, 파일들 = shkarkim(요청, numri_i_portës)
    futje_Listë = 목록읽기()
    Emër = 명세["name"]
    if Emër in futje_Listë:
        if futje_Listë[Emër]["version"] == 명세["version"]:
            for POZICIONI, 지문값 in futje_Listë[Emër]["files"].items():
                if sistem_operativ.path_kind(POZICIONI) != 1 or 지문(sistem_operativ.read(POZICIONI)) != 지문값:
                    raise ValueError("설치된 grupoj 파일이 달라졌습니다: " + POZICIONI)
            print("이미 설치됨:", Emër, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 PAS_VALUE 설치하십시오.")
    for POZICIONI in 파일들:
        if sistem_operativ.path_kind(POZICIONI):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + POZICIONI)
    futje_Listë[Emër] = {"version": 명세["version"], "files": {POZICIONI: 지문(të_dhëna) for POZICIONI, të_dhëna in 파일들.items()}}
    새목록 = json.dumps(futje_Listë).encode()
    if len(새목록) > 16384:
        raise ValueError("grupoj futje_Listë Madhësi 초과")
    이전목록 = sistem_operativ.read(Listë_shteg) if sistem_operativ.path_kind(Listë_shteg) else None
    만든파일 = []
    만든폴더 = []
    try:
        for POZICIONI, të_dhëna in 파일들.items():
            부분들 = POZICIONI.split("/")
            for 수 in range(2, len(부분들)):
                direktori_VALUE = "/".join(부분들[:수])
                종류 = sistem_operativ.path_kind(direktori_VALUE)
                if 종류 == 0:
                    sistem_operativ.mkdir(direktori_VALUE)
                    만든폴더.append(direktori_VALUE)
                elif 종류 != 2:
                    raise ValueError("direktori_VALUE 경로에 파일이 있습니다: " + direktori_VALUE)
            만든파일.append(POZICIONI)
            shkruaj_LOG(POZICIONI, të_dhëna)
        shkruaj_LOG(Listë_shteg, 새목록)
    except Exception:
        for POZICIONI in 만든파일:
            if sistem_operativ.path_kind(POZICIONI):
                sistem_operativ.remove(POZICIONI)
        for direktori_VALUE in reversed(만든폴더):
            sistem_operativ.rmdir(direktori_VALUE)
        if 이전목록 is not None:
            shkruaj_LOG(Listë_shteg, 이전목록)
        elif sistem_operativ.path_kind(Listë_shteg):
            sistem_operativ.remove(Listë_shteg)
        raise
    print("instaloj_VALUE 완료:", Emër, 명세["version"], "→ /lib (RAM)")


def heq_futje(Emër):
    futje_Listë = 목록읽기()
    if Emër not in futje_Listë:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Emër)
    for POZICIONI, 지문값 in futje_Listë[Emër]["files"].items():
        if sistem_operativ.path_kind(POZICIONI) != 1 or 지문(sistem_operativ.read(POZICIONI)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + POZICIONI)
    for POZICIONI in futje_Listë[Emër]["files"]:
        sistem_operativ.remove(POZICIONI)
    del futje_Listë[Emër]
    shkruaj_LOG(Listë_shteg, json.dumps(futje_Listë).encode())
    print("heq_futje 완료:", Emër)


def Ekzekuto(Argumente):
    numri_i_portës = 8027
    if len(Argumente) >= 2 and Argumente[-2] == "--port":
        numri_i_portës = int(Argumente[-1])
        Argumente = Argumente[:-2]
    if Argumente == ["list"]:
        for Emër, msinfo32_exe in 목록읽기().items():
            print(Emër, msinfo32_exe["version"])
    elif len(Argumente) == 2 and Argumente[0] == "install":
        instaloj_VALUE(Argumente[1], numri_i_portës)
    elif len(Argumente) == 2 and Argumente[0] == "uninstall":
        heq_futje(Argumente[1])
    elif not Argumente or Argumente in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython burim_degëzim 설치기 (PyPA pip 전체가 아님)")
        print("pip install Emër[==버전] [--port 8027] | pip list | pip uninstall Emër")
        print("pritës: Mjete/zbatoj_komandë.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Ekzekuto(sys.argv[1:])
    except Exception as GABIM:
        print("grupoj GABIM:", GABIM)
        sys.exit(1)
