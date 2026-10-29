"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 njaatigi 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as yuɓɓo_kurdinɗo

Doggol_laawol = "/lib/.pip.json"


def 지문(keɓe):
    return "".join("%02x" % njaru for njaru in hashlib.sha256(keɓe).digest())


def 목록읽기():
    if yuɓɓo_kurdinɗo.path_kind(Doggol_laawol) == 0:
        return {}
    return json.loads(yuɓɓo_kurdinɗo.read(Doggol_laawol).decode("utf-8"))


def winndude_suurnal(laawol, keɓe):
    if yuɓɓo_kurdinɗo.write(laawol, keɓe) != len(keɓe):
        raise OSError(28)


def sek_laawol(laawol):
    if not isinstance(laawol, str) or not laawol.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in laawol.split("/")):
        raise ValueError("허용하지 않는 꾸러미 laawol")
    if "\\" in laawol or any(ord(alkulal_njaru) < 32 or ord(alkulal_njaru) == 127 for alkulal_njaru in laawol):
        raise ValueError("잘못된 laawol 문자")
    결과 = "/lib/" + laawol
    if len(결과.encode("utf-8")) > 63 or laawol in ("한국어.py", "꾸러미.py"):
        raise ValueError("꾸러미 경로가 너무 길거나 lasli_njaru 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.huutoraade = yuɓɓo_kurdinɗo.ticks_ms()

    def 정확히읽기(자신, njuuteendi_njaru):
        keɓe = bytearray()
        while len(keɓe) < njuuteendi_njaru:
            if yuɓɓo_kurdinɗo.ticks_ms() - 자신.huutoraade > 90000:
                raise ValueError("꾸러미 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = yuɓɓo_kurdinɗo.tcp_read(자신.종단, 512)
                except OSError as juumre:
                    if juumre.args[0] != 11:
                        raise
                    yuɓɓo_kurdinɗo.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("꾸러미 전송이 중간에 끝났습니다.")
            개수 = min(njuuteendi_njaru - len(keɓe), len(자신.남은자료))
            keɓe.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            yuɓɓo_kurdinɗo.sleep_ms(0)
        return bytes(keɓe)


def loowtude(요청, 접속번호):
    if len(요청) > 96 or any(alkulal_njaru not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for alkulal_njaru in 요청):
        raise ValueError("사용법: pip install innde 또는 innde==버전")
    종단 = yuɓɓo_kurdinɗo.tcp_open()
    try:
        huutoraade = yuɓɓo_kurdinɗo.ticks_ms()
        while True:
            try:
                yuɓɓo_kurdinɗo.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as juumre:
                if juumre.args[0] not in (11, 115) or yuɓɓo_kurdinɗo.ticks_ms() - huutoraade > 5000:
                    raise ValueError("꾸러미 중계 seŋaade ella_njaru: 호스트에서 --network --pip로 실행하십시오.")
                yuɓɓo_kurdinɗo.sleep_ms(10)
        keɓe = (요청 + "\n").encode()
        while keɓe:
            try:
                개수 = yuɓɓo_kurdinɗo.tcp_write(종단, keɓe)
                if not 개수:
                    raise ValueError("꾸러미 요청 egginde_njaru ella_njaru")
                keɓe = keɓe[개수:]
            except OSError as juumre:
                if juumre.args[0] != 11:
                    raise
                yuɓɓo_kurdinɗo.sleep_ms(10)
                if yuɓɓo_kurdinɗo.ticks_ms() - huutoraade > 10000:
                    raise ValueError("꾸러미 요청 egginde_njaru 시간 초과")
        waraango_njaru = 수신흐름(종단)
        머리 = waraango_njaru.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("꾸러미 egginde_njaru haaju_njaru 불일치")
        njuuteendi_njaru = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if njuuteendi_njaru > 8192:
            raise ValueError("꾸러미 명세가 너무 큽니다.")
        명세 = json.loads(waraango_njaru.정확히읽기(njuuteendi_njaru).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 sewnde_lekki 파일은 1~16개여야 합니다.")
        if sum(naatnugol_njaru["size"] for naatnugol_njaru in 명세["files"]) > 65536:
            raise ValueError("꾸러미 sewnde_lekki 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for naatnugol_njaru in 명세["files"]:
            laawol = sek_laawol(naatnugol_njaru["path"])
            if laawol in 파일들 or not 0 <= naatnugol_njaru["size"] <= 16384:
                raise ValueError("중복 laawol 또는 fiilde waylude_etannde 초과")
            keɓe = waraango_njaru.정확히읽기(naatnugol_njaru["size"])
            if 지문(keɓe) != naatnugol_njaru["sha256"]:
                raise ValueError("꾸러미 fiilde SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(keɓe.decode("utf-8"), laawol, "exec")
            파일들[laawol] = keɓe
            gc.collect()
        return 명세, 파일들
    finally:
        yuɓɓo_kurdinɗo.udp_close(종단)


def diiñde_njaru(요청, 접속번호):
    print("꾸러미 loowtude:", 요청)
    명세, 파일들 = loowtude(요청, 접속번호)
    naatnugol_Doggol = 목록읽기()
    innde = 명세["name"]
    if innde in naatnugol_Doggol:
        if naatnugol_Doggol[innde]["version"] == 명세["version"]:
            for laawol, 지문값 in naatnugol_Doggol[innde]["files"].items():
                if yuɓɓo_kurdinɗo.path_kind(laawol) != 1 or 지문(yuɓɓo_kurdinɗo.read(laawol)) != 지문값:
                    raise ValueError("설치된 꾸러미 파일이 달라졌습니다: " + laawol)
            print("이미 설치됨:", innde, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Caggal_njaru 설치하십시오.")
    for laawol in 파일들:
        if yuɓɓo_kurdinɗo.path_kind(laawol):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + laawol)
    naatnugol_Doggol[innde] = {"version": 명세["version"], "files": {laawol: 지문(keɓe) for laawol, keɓe in 파일들.items()}}
    새목록 = json.dumps(naatnugol_Doggol).encode()
    if len(새목록) > 16384:
        raise ValueError("꾸러미 naatnugol_Doggol waylude_etannde 초과")
    이전목록 = yuɓɓo_kurdinɗo.read(Doggol_laawol) if yuɓɓo_kurdinɗo.path_kind(Doggol_laawol) else None
    만든파일 = []
    만든폴더 = []
    try:
        for laawol, keɓe in 파일들.items():
            부분들 = laawol.split("/")
            for 수 in range(2, len(부분들)):
                mooftordu_njaru = "/".join(부분들[:수])
                종류 = yuɓɓo_kurdinɗo.path_kind(mooftordu_njaru)
                if 종류 == 0:
                    yuɓɓo_kurdinɗo.mkdir(mooftordu_njaru)
                    만든폴더.append(mooftordu_njaru)
                elif 종류 != 2:
                    raise ValueError("mooftordu_njaru 경로에 파일이 있습니다: " + mooftordu_njaru)
            만든파일.append(laawol)
            winndude_suurnal(laawol, keɓe)
        winndude_suurnal(Doggol_laawol, 새목록)
    except Exception:
        for laawol in 만든파일:
            if yuɓɓo_kurdinɗo.path_kind(laawol):
                yuɓɓo_kurdinɗo.remove(laawol)
        for mooftordu_njaru in reversed(만든폴더):
            yuɓɓo_kurdinɗo.rmdir(mooftordu_njaru)
        if 이전목록 is not None:
            winndude_suurnal(Doggol_laawol, 이전목록)
        elif yuɓɓo_kurdinɗo.path_kind(Doggol_laawol):
            yuɓɓo_kurdinɗo.remove(Doggol_laawol)
        raise
    print("diiñde_njaru 완료:", innde, 명세["version"], "→ /lib (RAM)")


def ittude_naatnugol(innde):
    naatnugol_Doggol = 목록읽기()
    if innde not in naatnugol_Doggol:
        raise ValueError("설치되지 않은 꾸러미입니다: " + innde)
    for laawol, 지문값 in naatnugol_Doggol[innde]["files"].items():
        if yuɓɓo_kurdinɗo.path_kind(laawol) != 1 or 지문(yuɓɓo_kurdinɗo.read(laawol)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + laawol)
    for laawol in naatnugol_Doggol[innde]["files"]:
        yuɓɓo_kurdinɗo.remove(laawol)
    del naatnugol_Doggol[innde]
    winndude_suurnal(Doggol_laawol, json.dumps(naatnugol_Doggol).encode())
    print("ittude_naatnugol 완료:", innde)


def huutoraade(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for innde, msinfo32_exe in 목록읽기().items():
            print(innde, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        diiñde_njaru(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ittude_naatnugol(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython sewnde_lekki 설치기 (PyPA pip 전체가 아님)")
        print("pip install innde[==버전] [--port 8027] | pip list | pip uninstall innde")
        print("njaatigi: 도구/실행.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        huutoraade(sys.argv[1:])
    except Exception as juumre:
        print("꾸러미 juumre:", juumre)
        sys.exit(1)
