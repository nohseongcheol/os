"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 òstair 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as siostam_obrachaidh

Liosta_slighe = "/lib/.pip.json"


def 지문(dàta):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(dàta).digest())


def 목록읽기():
    if siostam_obrachaidh.path_kind(Liosta_slighe) == 0:
        return {}
    return json.loads(siostam_obrachaidh.read(Liosta_slighe).decode("utf-8"))


def sgrìobh_LOG(Slighe, dàta):
    if siostam_obrachaidh.write(Slighe, dàta) != len(dàta):
        raise OSError(28)


def seic_slighe(Slighe):
    if not isinstance(Slighe, str) or not Slighe.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Slighe.split("/")):
        raise ValueError("허용하지 않는 trusgan Slighe")
    if "\\" in Slighe or any(ord(caractar_VALUE) < 32 or ord(caractar_VALUE) == 127 for caractar_VALUE in Slighe):
        raise ValueError("잘못된 Slighe 문자")
    tomhas = "/lib/" + Slighe
    if len(tomhas.encode("utf-8")) > 63 or Slighe in ("한국어.py", "trusgan.py"):
        raise ValueError("trusgan 경로가 너무 길거나 luach_bunaiteach 라이브러리와 겹칩니다.")
    return tomhas


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ruith = siostam_obrachaidh.ticks_ms()

    def 정확히읽기(자신, faid_VALUE):
        dàta = bytearray()
        while len(dàta) < faid_VALUE:
            if siostam_obrachaidh.ticks_ms() - 자신.ruith > 90000:
                raise ValueError("trusgan 중계 freagair TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = siostam_obrachaidh.tcp_read(자신.종단, 512)
                except OSError as Mearachd:
                    if Mearachd.args[0] != 11:
                        raise
                    siostam_obrachaidh.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("trusgan 전송이 중간에 끝났습니다.")
            nì_COUNT = min(faid_VALUE - len(dàta), len(자신.남은자료))
            dàta.extend(자신.남은자료[:nì_COUNT])
            자신.남은자료 = 자신.남은자료[nì_COUNT:]
            siostam_obrachaidh.sleep_ms(0)
        return bytes(dàta)


def luchdadh_a_nuas(요청, 접속번호):
    if len(요청) > 96 or any(caractar_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for caractar_VALUE in 요청):
        raise ValueError("사용법: pip install Ainm 또는 Ainm==버전")
    종단 = siostam_obrachaidh.tcp_open()
    try:
        ruith = siostam_obrachaidh.ticks_ms()
        while True:
            try:
                siostam_obrachaidh.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Mearachd:
                if Mearachd.args[0] not in (11, 115) or siostam_obrachaidh.ticks_ms() - ruith > 5000:
                    raise ValueError("trusgan 중계 CONNECT fàilligeadh_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                siostam_obrachaidh.sleep_ms(10)
        dàta = (요청 + "\n").encode()
        while dàta:
            try:
                nì_COUNT = siostam_obrachaidh.tcp_write(종단, dàta)
                if not nì_COUNT:
                    raise ValueError("trusgan 요청 tar_chur_VALUE fàilligeadh_VALUE")
                dàta = dàta[nì_COUNT:]
            except OSError as Mearachd:
                if Mearachd.args[0] != 11:
                    raise
                siostam_obrachaidh.sleep_ms(10)
                if siostam_obrachaidh.ticks_ms() - ruith > 10000:
                    raise ValueError("trusgan 요청 tar_chur_VALUE TIME_VALUE 초과")
        sruth_VALUE = 수신흐름(종단)
        머리 = sruth_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("trusgan tar_chur_VALUE cùis_VALUE 불일치")
        faid_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if faid_VALUE > 8192:
            raise ValueError("trusgan 명세가 너무 큽니다.")
        명세 = json.loads(sruth_VALUE.정확히읽기(faid_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 tùs_craobh 파일은 1~16개여야 합니다.")
        if sum(cur_a_steach_VALUE["size"] for cur_a_steach_VALUE in 명세["files"]) > 65536:
            raise ValueError("trusgan tùs_craobh 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for cur_a_steach_VALUE in 명세["files"]:
            Slighe = seic_slighe(cur_a_steach_VALUE["path"])
            if Slighe in 파일들 or not 0 <= cur_a_steach_VALUE["size"] <= 16384:
                raise ValueError("중복 Slighe 또는 faidhle atharraich_am_meud 초과")
            dàta = sruth_VALUE.정확히읽기(cur_a_steach_VALUE["size"])
            if 지문(dàta) != cur_a_steach_VALUE["sha256"]:
                raise ValueError("trusgan faidhle SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(dàta.decode("utf-8"), Slighe, "exec")
            파일들[Slighe] = dàta
            gc.collect()
        return 명세, 파일들
    finally:
        siostam_obrachaidh.udp_close(종단)


def stàlaich_VALUE(요청, 접속번호):
    print("trusgan luchdadh_a_nuas:", 요청)
    명세, 파일들 = luchdadh_a_nuas(요청, 접속번호)
    cur_a_steach_Liosta = 목록읽기()
    Ainm = 명세["name"]
    if Ainm in cur_a_steach_Liosta:
        if cur_a_steach_Liosta[Ainm]["version"] == 명세["version"]:
            for Slighe, 지문값 in cur_a_steach_Liosta[Ainm]["files"].items():
                if siostam_obrachaidh.path_kind(Slighe) != 1 or 지문(siostam_obrachaidh.read(Slighe)) != 지문값:
                    raise ValueError("설치된 trusgan 파일이 달라졌습니다: " + Slighe)
            print("이미 설치됨:", Ainm, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Air_ais_VALUE 설치하십시오.")
    for Slighe in 파일들:
        if siostam_obrachaidh.path_kind(Slighe):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Slighe)
    cur_a_steach_Liosta[Ainm] = {"version": 명세["version"], "files": {Slighe: 지문(dàta) for Slighe, dàta in 파일들.items()}}
    새목록 = json.dumps(cur_a_steach_Liosta).encode()
    if len(새목록) > 16384:
        raise ValueError("trusgan cur_a_steach_Liosta atharraich_am_meud 초과")
    이전목록 = siostam_obrachaidh.read(Liosta_slighe) if siostam_obrachaidh.path_kind(Liosta_slighe) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Slighe, dàta in 파일들.items():
            부분들 = Slighe.split("/")
            for 수 in range(2, len(부분들)):
                eòlaire_VALUE = "/".join(부분들[:수])
                종류 = siostam_obrachaidh.path_kind(eòlaire_VALUE)
                if 종류 == 0:
                    siostam_obrachaidh.mkdir(eòlaire_VALUE)
                    만든폴더.append(eòlaire_VALUE)
                elif 종류 != 2:
                    raise ValueError("eòlaire_VALUE 경로에 파일이 있습니다: " + eòlaire_VALUE)
            만든파일.append(Slighe)
            sgrìobh_LOG(Slighe, dàta)
        sgrìobh_LOG(Liosta_slighe, 새목록)
    except Exception:
        for Slighe in 만든파일:
            if siostam_obrachaidh.path_kind(Slighe):
                siostam_obrachaidh.remove(Slighe)
        for eòlaire_VALUE in reversed(만든폴더):
            siostam_obrachaidh.rmdir(eòlaire_VALUE)
        if 이전목록 is not None:
            sgrìobh_LOG(Liosta_slighe, 이전목록)
        elif siostam_obrachaidh.path_kind(Liosta_slighe):
            siostam_obrachaidh.remove(Liosta_slighe)
        raise
    print("stàlaich_VALUE 완료:", Ainm, 명세["version"], "→ /lib (RAM)")


def thoir_air_falbh_cur_a_steach(Ainm):
    cur_a_steach_Liosta = 목록읽기()
    if Ainm not in cur_a_steach_Liosta:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ainm)
    for Slighe, 지문값 in cur_a_steach_Liosta[Ainm]["files"].items():
        if siostam_obrachaidh.path_kind(Slighe) != 1 or 지문(siostam_obrachaidh.read(Slighe)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Slighe)
    for Slighe in cur_a_steach_Liosta[Ainm]["files"]:
        siostam_obrachaidh.remove(Slighe)
    del cur_a_steach_Liosta[Ainm]
    sgrìobh_LOG(Liosta_slighe, json.dumps(cur_a_steach_Liosta).encode())
    print("thoir_air_falbh_cur_a_steach 완료:", Ainm)


def ruith(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Ainm, msinfo32_exe in 목록읽기().items():
            print(Ainm, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        stàlaich_VALUE(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        thoir_air_falbh_cur_a_steach(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython tùs_craobh 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ainm[==버전] [--port 8027] | pip list | pip uninstall Ainm")
        print("òstair: innealan/gnìomhaich_àithne.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ruith(sys.argv[1:])
    except Exception as Mearachd:
        print("trusgan Mearachd:", Mearachd)
        sys.exit(1)
