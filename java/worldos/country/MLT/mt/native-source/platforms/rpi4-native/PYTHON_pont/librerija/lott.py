"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistema_operattiva

Lista_mogħdija = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if sistema_operattiva.path_kind(Lista_mogħdija) == 0:
        return {}
    return json.loads(sistema_operattiva.read(Lista_mogħdija).decode("utf-8"))


def kiteb_LOG(mogħdija, data):
    if sistema_operattiva.write(mogħdija, data) != len(data):
        raise OSError(28)


def ċekk_mogħdija(mogħdija):
    if not isinstance(mogħdija, str) or not mogħdija.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in mogħdija.split("/")):
        raise ValueError("허용하지 않는 lott mogħdija")
    if "\\" in mogħdija or any(ord(karattru_VALUE) < 32 or ord(karattru_VALUE) == 127 for karattru_VALUE in mogħdija):
        raise ValueError("잘못된 mogħdija 문자")
    miżura = "/lib/" + mogħdija
    if len(miżura.encode("utf-8")) > 63 or mogħdija in ("Malti.py", "lott.py"):
        raise ValueError("lott 경로가 너무 길거나 valur_default 라이브러리와 겹칩니다.")
    return miżura


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.serje = sistema_operattiva.ticks_ms()

    def 정확히읽기(자신, tul_VALUE):
        data = bytearray()
        while len(data) < tul_VALUE:
            if sistema_operattiva.ticks_ms() - 자신.serje > 90000:
                raise ValueError("lott 중계 wieġeb TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistema_operattiva.tcp_read(자신.종단, 512)
                except OSError as żball:
                    if żball.args[0] != 11:
                        raise
                    sistema_operattiva.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("lott 전송이 중간에 끝났습니다.")
            element_COUNT = min(tul_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:element_COUNT])
            자신.남은자료 = 자신.남은자료[element_COUNT:]
            sistema_operattiva.sleep_ms(0)
        return bytes(data)


def niżżel(요청, 접속번호):
    if len(요청) > 96 or any(karattru_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karattru_VALUE in 요청):
        raise ValueError("사용법: pip install isem 또는 isem==버전")
    종단 = sistema_operattiva.tcp_open()
    try:
        serje = sistema_operattiva.ticks_ms()
        while True:
            try:
                sistema_operattiva.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as żball:
                if żball.args[0] not in (11, 115) or sistema_operattiva.ticks_ms() - serje > 5000:
                    raise ValueError("lott 중계 AQBAD żball_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                sistema_operattiva.sleep_ms(10)
        data = (요청 + "\n").encode()
        while data:
            try:
                element_COUNT = sistema_operattiva.tcp_write(종단, data)
                if not element_COUNT:
                    raise ValueError("lott 요청 trasferiment_VALUE żball_VALUE")
                data = data[element_COUNT:]
            except OSError as żball:
                if żball.args[0] != 11:
                    raise
                sistema_operattiva.sleep_ms(10)
                if sistema_operattiva.ticks_ms() - serje > 10000:
                    raise ValueError("lott 요청 trasferiment_VALUE TIME_VALUE 초과")
        Stream_VALUE = 수신흐름(종단)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("lott trasferiment_VALUE każ_VALUE 불일치")
        tul_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if tul_VALUE > 8192:
            raise ValueError("lott 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(tul_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 sors_siġra 파일은 1~16개여야 합니다.")
        if sum(entrata_VALUE["size"] for entrata_VALUE in 명세["files"]) > 65536:
            raise ValueError("lott sors_siġra 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for entrata_VALUE in 명세["files"]:
            mogħdija = ċekk_mogħdija(entrata_VALUE["path"])
            if mogħdija in 파일들 or not 0 <= entrata_VALUE["size"] <= 16384:
                raise ValueError("중복 mogħdija 또는 fajl daqqas 초과")
            data = Stream_VALUE.정확히읽기(entrata_VALUE["size"])
            if 지문(data) != entrata_VALUE["sha256"]:
                raise ValueError("lott fajl SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), mogħdija, "exec")
            파일들[mogħdija] = data
            gc.collect()
        return 명세, 파일들
    finally:
        sistema_operattiva.udp_close(종단)


def installa_VALUE(요청, 접속번호):
    print("lott niżżel:", 요청)
    명세, 파일들 = niżżel(요청, 접속번호)
    entrata_Lista = 목록읽기()
    isem = 명세["name"]
    if isem in entrata_Lista:
        if entrata_Lista[isem]["version"] == 명세["version"]:
            for mogħdija, 지문값 in entrata_Lista[isem]["files"].items():
                if sistema_operattiva.path_kind(mogħdija) != 1 or 지문(sistema_operattiva.read(mogħdija)) != 지문값:
                    raise ValueError("설치된 lott 파일이 달라졌습니다: " + mogħdija)
            print("이미 설치됨:", isem, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Lura_VALUE 설치하십시오.")
    for mogħdija in 파일들:
        if sistema_operattiva.path_kind(mogħdija):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + mogħdija)
    entrata_Lista[isem] = {"version": 명세["version"], "files": {mogħdija: 지문(data) for mogħdija, data in 파일들.items()}}
    새목록 = json.dumps(entrata_Lista).encode()
    if len(새목록) > 16384:
        raise ValueError("lott entrata_Lista daqqas 초과")
    이전목록 = sistema_operattiva.read(Lista_mogħdija) if sistema_operattiva.path_kind(Lista_mogħdija) else None
    만든파일 = []
    만든폴더 = []
    try:
        for mogħdija, data in 파일들.items():
            부분들 = mogħdija.split("/")
            for 수 in range(2, len(부분들)):
                direttorju_VALUE = "/".join(부분들[:수])
                종류 = sistema_operattiva.path_kind(direttorju_VALUE)
                if 종류 == 0:
                    sistema_operattiva.mkdir(direttorju_VALUE)
                    만든폴더.append(direttorju_VALUE)
                elif 종류 != 2:
                    raise ValueError("direttorju_VALUE 경로에 파일이 있습니다: " + direttorju_VALUE)
            만든파일.append(mogħdija)
            kiteb_LOG(mogħdija, data)
        kiteb_LOG(Lista_mogħdija, 새목록)
    except Exception:
        for mogħdija in 만든파일:
            if sistema_operattiva.path_kind(mogħdija):
                sistema_operattiva.remove(mogħdija)
        for direttorju_VALUE in reversed(만든폴더):
            sistema_operattiva.rmdir(direttorju_VALUE)
        if 이전목록 is not None:
            kiteb_LOG(Lista_mogħdija, 이전목록)
        elif sistema_operattiva.path_kind(Lista_mogħdija):
            sistema_operattiva.remove(Lista_mogħdija)
        raise
    print("installa_VALUE 완료:", isem, 명세["version"], "→ /lib (RAM)")


def neħħa_entrata(isem):
    entrata_Lista = 목록읽기()
    if isem not in entrata_Lista:
        raise ValueError("설치되지 않은 꾸러미입니다: " + isem)
    for mogħdija, 지문값 in entrata_Lista[isem]["files"].items():
        if sistema_operattiva.path_kind(mogħdija) != 1 or 지문(sistema_operattiva.read(mogħdija)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + mogħdija)
    for mogħdija in entrata_Lista[isem]["files"]:
        sistema_operattiva.remove(mogħdija)
    del entrata_Lista[isem]
    kiteb_LOG(Lista_mogħdija, json.dumps(entrata_Lista).encode())
    print("neħħa_entrata 완료:", isem)


def serje(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for isem, msinfo32_exe in 목록읽기().items():
            print(isem, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        installa_VALUE(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        neħħa_entrata(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython sors_siġra 설치기 (PyPA pip 전체가 아님)")
        print("pip install isem[==버전] [--port 8027] | pip list | pip uninstall isem")
        print("host: Għodod/eżegwixxa_kmand.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        serje(sys.argv[1:])
    except Exception as żball:
        print("lott żball:", żball)
        sys.exit(1)
