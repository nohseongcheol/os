"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 óstach 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as córas_oibriúcháin

Liosta_cosán = "/lib/.pip.json"


def 지문(sonraí):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(sonraí).digest())


def 목록읽기():
    if córas_oibriúcháin.path_kind(Liosta_cosán) == 0:
        return {}
    return json.loads(córas_oibriúcháin.read(Liosta_cosán).decode("utf-8"))


def scríobh_LOG(CONAIR, sonraí):
    if córas_oibriúcháin.write(CONAIR, sonraí) != len(sonraí):
        raise OSError(28)


def seic_cosán(CONAIR):
    if not isinstance(CONAIR, str) or not CONAIR.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in CONAIR.split("/")):
        raise ValueError("허용하지 않는 beart CONAIR")
    if "\\" in CONAIR or any(ord(carachtar_VALUE) < 32 or ord(carachtar_VALUE) == 127 for carachtar_VALUE in CONAIR):
        raise ValueError("잘못된 CONAIR 문자")
    tomhas = "/lib/" + CONAIR
    if len(tomhas.encode("utf-8")) > 63 or CONAIR in ("Gaeilge.py", "beart.py"):
        raise ValueError("beart 경로가 너무 길거나 luach_réamhshocraithe 라이브러리와 겹칩니다.")
    return tomhas


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Rith_2 = córas_oibriúcháin.ticks_ms()

    def 정확히읽기(자신, fad_VALUE):
        sonraí = bytearray()
        while len(sonraí) < fad_VALUE:
            if córas_oibriúcháin.ticks_ms() - 자신.Rith_2 > 90000:
                raise ValueError("beart 중계 freagair TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = córas_oibriúcháin.tcp_read(자신.종단, 512)
                except OSError as ERREÁID:
                    if ERREÁID.args[0] != 11:
                        raise
                    córas_oibriúcháin.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("beart 전송이 중간에 끝났습니다.")
            mír_COUNT = min(fad_VALUE - len(sonraí), len(자신.남은자료))
            sonraí.extend(자신.남은자료[:mír_COUNT])
            자신.남은자료 = 자신.남은자료[mír_COUNT:]
            córas_oibriúcháin.sleep_ms(0)
        return bytes(sonraí)


def íoslódáil(iarratas_HTTP, uimhir_phoirt):
    if len(iarratas_HTTP) > 96 or any(carachtar_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for carachtar_VALUE in iarratas_HTTP):
        raise ValueError("사용법: pip install Ainm 또는 Ainm==버전")
    종단 = córas_oibriúcháin.tcp_open()
    try:
        Rith_2 = córas_oibriúcháin.ticks_ms()
        while True:
            try:
                córas_oibriúcháin.tcp_connect(종단, "10.0.2.2", uimhir_phoirt)
                break
            except OSError as ERREÁID:
                if ERREÁID.args[0] not in (11, 115) or córas_oibriúcháin.ticks_ms() - Rith_2 > 5000:
                    raise ValueError("beart 중계 Nasc teip_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                córas_oibriúcháin.sleep_ms(10)
        sonraí = (iarratas_HTTP + "\n").encode()
        while sonraí:
            try:
                mír_COUNT = córas_oibriúcháin.tcp_write(종단, sonraí)
                if not mír_COUNT:
                    raise ValueError("beart iarratas_HTTP traschur_VALUE teip_VALUE")
                sonraí = sonraí[mír_COUNT:]
            except OSError as ERREÁID:
                if ERREÁID.args[0] != 11:
                    raise
                córas_oibriúcháin.sleep_ms(10)
                if córas_oibriúcháin.ticks_ms() - Rith_2 > 10000:
                    raise ValueError("beart iarratas_HTTP traschur_VALUE TIME_VALUE 초과")
        sruth_VALUE = 수신흐름(종단)
        머리 = sruth_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("beart traschur_VALUE cás_VALUE 불일치")
        fad_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if fad_VALUE > 8192:
            raise ValueError("beart 명세가 너무 큽니다.")
        명세 = json.loads(sruth_VALUE.정확히읽기(fad_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 foinse_crann 파일은 1~16개여야 합니다.")
        if sum(iontráil_VALUE["size"] for iontráil_VALUE in 명세["files"]) > 65536:
            raise ValueError("beart foinse_crann 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for iontráil_VALUE in 명세["files"]:
            CONAIR = seic_cosán(iontráil_VALUE["path"])
            if CONAIR in 파일들 or not 0 <= iontráil_VALUE["size"] <= 16384:
                raise ValueError("중복 CONAIR 또는 Comhad Méid 초과")
            sonraí = sruth_VALUE.정확히읽기(iontráil_VALUE["size"])
            if 지문(sonraí) != iontráil_VALUE["sha256"]:
                raise ValueError("beart Comhad SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(sonraí.decode("utf-8"), CONAIR, "exec")
            파일들[CONAIR] = sonraí
            gc.collect()
        return 명세, 파일들
    finally:
        córas_oibriúcháin.udp_close(종단)


def suiteáil_VALUE(iarratas_HTTP, uimhir_phoirt):
    print("beart íoslódáil:", iarratas_HTTP)
    명세, 파일들 = íoslódáil(iarratas_HTTP, uimhir_phoirt)
    iontráil_Liosta = 목록읽기()
    Ainm = 명세["name"]
    if Ainm in iontráil_Liosta:
        if iontráil_Liosta[Ainm]["version"] == 명세["version"]:
            for CONAIR, 지문값 in iontráil_Liosta[Ainm]["files"].items():
                if córas_oibriúcháin.path_kind(CONAIR) != 1 or 지문(córas_oibriúcháin.read(CONAIR)) != 지문값:
                    raise ValueError("설치된 beart 파일이 달라졌습니다: " + CONAIR)
            print("이미 설치됨:", Ainm, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Siar_VALUE 설치하십시오.")
    for CONAIR in 파일들:
        if córas_oibriúcháin.path_kind(CONAIR):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + CONAIR)
    iontráil_Liosta[Ainm] = {"version": 명세["version"], "files": {CONAIR: 지문(sonraí) for CONAIR, sonraí in 파일들.items()}}
    새목록 = json.dumps(iontráil_Liosta).encode()
    if len(새목록) > 16384:
        raise ValueError("beart iontráil_Liosta Méid 초과")
    이전목록 = córas_oibriúcháin.read(Liosta_cosán) if córas_oibriúcháin.path_kind(Liosta_cosán) else None
    만든파일 = []
    만든폴더 = []
    try:
        for CONAIR, sonraí in 파일들.items():
            부분들 = CONAIR.split("/")
            for 수 in range(2, len(부분들)):
                eolaire_VALUE = "/".join(부분들[:수])
                종류 = córas_oibriúcháin.path_kind(eolaire_VALUE)
                if 종류 == 0:
                    córas_oibriúcháin.mkdir(eolaire_VALUE)
                    만든폴더.append(eolaire_VALUE)
                elif 종류 != 2:
                    raise ValueError("eolaire_VALUE 경로에 파일이 있습니다: " + eolaire_VALUE)
            만든파일.append(CONAIR)
            scríobh_LOG(CONAIR, sonraí)
        scríobh_LOG(Liosta_cosán, 새목록)
    except Exception:
        for CONAIR in 만든파일:
            if córas_oibriúcháin.path_kind(CONAIR):
                córas_oibriúcháin.remove(CONAIR)
        for eolaire_VALUE in reversed(만든폴더):
            córas_oibriúcháin.rmdir(eolaire_VALUE)
        if 이전목록 is not None:
            scríobh_LOG(Liosta_cosán, 이전목록)
        elif córas_oibriúcháin.path_kind(Liosta_cosán):
            córas_oibriúcháin.remove(Liosta_cosán)
        raise
    print("suiteáil_VALUE 완료:", Ainm, 명세["version"], "→ /lib (RAM)")


def bain_iontráil(Ainm):
    iontráil_Liosta = 목록읽기()
    if Ainm not in iontráil_Liosta:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ainm)
    for CONAIR, 지문값 in iontráil_Liosta[Ainm]["files"].items():
        if córas_oibriúcháin.path_kind(CONAIR) != 1 or 지문(córas_oibriúcháin.read(CONAIR)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + CONAIR)
    for CONAIR in iontráil_Liosta[Ainm]["files"]:
        córas_oibriúcháin.remove(CONAIR)
    del iontráil_Liosta[Ainm]
    scríobh_LOG(Liosta_cosán, json.dumps(iontráil_Liosta).encode())
    print("bain_iontráil 완료:", Ainm)


def Rith_2(Argóintí):
    uimhir_phoirt = 8027
    if len(Argóintí) >= 2 and Argóintí[-2] == "--port":
        uimhir_phoirt = int(Argóintí[-1])
        Argóintí = Argóintí[:-2]
    if Argóintí == ["list"]:
        for Ainm, msinfo32_exe in 목록읽기().items():
            print(Ainm, msinfo32_exe["version"])
    elif len(Argóintí) == 2 and Argóintí[0] == "install":
        suiteáil_VALUE(Argóintí[1], uimhir_phoirt)
    elif len(Argóintí) == 2 and Argóintí[0] == "uninstall":
        bain_iontráil(Argóintí[1])
    elif not Argóintí or Argóintí in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython foinse_crann 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ainm[==버전] [--port 8027] | pip list | pip uninstall Ainm")
        print("óstach: Uirlisí/Rith_ordú.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Rith_2(sys.argv[1:])
    except Exception as ERREÁID:
        print("beart ERREÁID:", ERREÁID)
        sys.exit(1)
