"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 epiajatü 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as a_yatawajiraaya_a_laülaasü

목록경로 = "/lib/.pip.json"


def 지문(atijaaya):
    return "".join("%02x" % ajutuu for ajutuu in hashlib.sha256(atijaaya).digest())


def 목록읽기():
    if a_yatawajiraaya_a_laülaasü.path_kind(목록경로) == 0:
        return {}
    return json.loads(a_yatawajiraaya_a_laülaasü.read(목록경로).decode("utf-8"))


def ashajaa_aa_innachikimaajatü(wopu_a_ttaaleemüin, atijaaya):
    if a_yatawajiraaya_a_laülaasü.write(wopu_a_ttaaleemüin, atijaaya) != len(atijaaya):
        raise OSError(28)


def cheeke_wopu_a_ttaaleemüin(wopu_a_ttaaleemüin):
    if not isinstance(wopu_a_ttaaleemüin, str) or not wopu_a_ttaaleemüin.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in wopu_a_ttaaleemüin.split("/")):
        raise ValueError("허용하지 않는 꾸러미 wopu_a_ttaaleemüin")
    if "\\" in wopu_a_ttaaleemüin or any(ord(jeerü_ajutuu) < 32 or ord(jeerü_ajutuu) == 127 for jeerü_ajutuu in wopu_a_ttaaleemüin):
        raise ValueError("잘못된 wopu_a_ttaaleemüin 문자")
    결과 = "/lib/" + wopu_a_ttaaleemüin
    if len(결과.encode("utf-8")) > 63 or wopu_a_ttaaleemüin in ("한국어.py", "꾸러미.py"):
        raise ValueError("꾸러미 경로가 너무 길거나 ajutuu_aneekuushitüjülia 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.시작 = a_yatawajiraaya_a_laülaasü.ticks_ms()

    def 정확히읽기(자신, akaliaa_ajutuu):
        atijaaya = bytearray()
        while len(atijaaya) < akaliaa_ajutuu:
            if a_yatawajiraaya_a_laülaasü.ticks_ms() - 자신.시작 > 90000:
                raise ValueError("꾸러미 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = a_yatawajiraaya_a_laülaasü.tcp_read(자신.종단, 512)
                except OSError as ajachitia:
                    if ajachitia.args[0] != 11:
                        raise
                    a_yatawajiraaya_a_laülaasü.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("꾸러미 전송이 중간에 끝났습니다.")
            개수 = min(akaliaa_ajutuu - len(atijaaya), len(자신.남은자료))
            atijaaya.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            a_yatawajiraaya_a_laülaasü.sleep_ms(0)
        return bytes(atijaaya)


def ashakatiraa(요청, 접속번호):
    if len(요청) > 96 or any(jeerü_ajutuu not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for jeerü_ajutuu in 요청):
        raise ValueError("사용법: pip install 이름 또는 이름==버전")
    종단 = a_yatawajiraaya_a_laülaasü.tcp_open()
    try:
        시작 = a_yatawajiraaya_a_laülaasü.ticks_ms()
        while True:
            try:
                a_yatawajiraaya_a_laülaasü.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as ajachitia:
                if ajachitia.args[0] not in (11, 115) or a_yatawajiraaya_a_laülaasü.ticks_ms() - 시작 > 5000:
                    raise ValueError("꾸러미 중계 a_ataa ajachitia_ajutuu: 호스트에서 --network --pip로 실행하십시오.")
                a_yatawajiraaya_a_laülaasü.sleep_ms(10)
        atijaaya = (요청 + "\n").encode()
        while atijaaya:
            try:
                개수 = a_yatawajiraaya_a_laülaasü.tcp_write(종단, atijaaya)
                if not 개수:
                    raise ValueError("꾸러미 요청 alate_eraa_ajutuu ajachitia_ajutuu")
                atijaaya = atijaaya[개수:]
            except OSError as ajachitia:
                if ajachitia.args[0] != 11:
                    raise
                a_yatawajiraaya_a_laülaasü.sleep_ms(10)
                if a_yatawajiraaya_a_laülaasü.ticks_ms() - 시작 > 10000:
                    raise ValueError("꾸러미 요청 alate_eraa_ajutuu 시간 초과")
        palantüsü_ajutuu = 수신흐름(종단)
        머리 = palantüsü_ajutuu.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("꾸러미 alate_eraa_ajutuu achikii_ajutuu 불일치")
        akaliaa_ajutuu = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if akaliaa_ajutuu > 8192:
            raise ValueError("꾸러미 명세가 너무 큽니다.")
        명세 = json.loads(palantüsü_ajutuu.정확히읽기(akaliaa_ajutuu).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 eejeejetülein_wunu_ulia 파일은 1~16개여야 합니다.")
        if sum(ekeroliaa_ajutuu["size"] for ekeroliaa_ajutuu in 명세["files"]) > 65536:
            raise ValueError("꾸러미 eejeejetülein_wunu_ulia 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ekeroliaa_ajutuu in 명세["files"]:
            wopu_a_ttaaleemüin = cheeke_wopu_a_ttaaleemüin(ekeroliaa_ajutuu["path"])
            if wopu_a_ttaaleemüin in 파일들 or not 0 <= ekeroliaa_ajutuu["size"] <= 16384:
                raise ValueError("중복 wopu_a_ttaaleemüin 또는 anaajaalaa 크기 초과")
            atijaaya = palantüsü_ajutuu.정확히읽기(ekeroliaa_ajutuu["size"])
            if 지문(atijaaya) != ekeroliaa_ajutuu["sha256"]:
                raise ValueError("꾸러미 anaajaalaa SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(atijaaya.decode("utf-8"), wopu_a_ttaaleemüin, "exec")
            파일들[wopu_a_ttaaleemüin] = atijaaya
            gc.collect()
        return 명세, 파일들
    finally:
        a_yatawajiraaya_a_laülaasü.udp_close(종단)


def e_itawaa_ajutuu(요청, 접속번호):
    print("꾸러미 ashakatiraa:", 요청)
    명세, 파일들 = ashakatiraa(요청, 접속번호)
    목록 = 목록읽기()
    이름 = 명세["name"]
    if 이름 in 목록:
        if 목록[이름]["version"] == 명세["version"]:
            for wopu_a_ttaaleemüin, 지문값 in 목록[이름]["files"].items():
                if a_yatawajiraaya_a_laülaasü.path_kind(wopu_a_ttaaleemüin) != 1 or 지문(a_yatawajiraaya_a_laülaasü.read(wopu_a_ttaaleemüin)) != 지문값:
                    raise ValueError("설치된 꾸러미 파일이 달라졌습니다: " + wopu_a_ttaaleemüin)
            print("이미 설치됨:", 이름, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 뒤 설치하십시오.")
    for wopu_a_ttaaleemüin in 파일들:
        if a_yatawajiraaya_a_laülaasü.path_kind(wopu_a_ttaaleemüin):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + wopu_a_ttaaleemüin)
    목록[이름] = {"version": 명세["version"], "files": {wopu_a_ttaaleemüin: 지문(atijaaya) for wopu_a_ttaaleemüin, atijaaya in 파일들.items()}}
    새목록 = json.dumps(목록).encode()
    if len(새목록) > 16384:
        raise ValueError("꾸러미 목록 크기 초과")
    이전목록 = a_yatawajiraaya_a_laülaasü.read(목록경로) if a_yatawajiraaya_a_laülaasü.path_kind(목록경로) else None
    만든파일 = []
    만든폴더 = []
    try:
        for wopu_a_ttaaleemüin, atijaaya in 파일들.items():
            부분들 = wopu_a_ttaaleemüin.split("/")
            for 수 in range(2, len(부분들)):
                anaajaalee_ajutuu = "/".join(부분들[:수])
                종류 = a_yatawajiraaya_a_laülaasü.path_kind(anaajaalee_ajutuu)
                if 종류 == 0:
                    a_yatawajiraaya_a_laülaasü.mkdir(anaajaalee_ajutuu)
                    만든폴더.append(anaajaalee_ajutuu)
                elif 종류 != 2:
                    raise ValueError("anaajaalee_ajutuu 경로에 파일이 있습니다: " + anaajaalee_ajutuu)
            만든파일.append(wopu_a_ttaaleemüin)
            ashajaa_aa_innachikimaajatü(wopu_a_ttaaleemüin, atijaaya)
        ashajaa_aa_innachikimaajatü(목록경로, 새목록)
    except Exception:
        for wopu_a_ttaaleemüin in 만든파일:
            if a_yatawajiraaya_a_laülaasü.path_kind(wopu_a_ttaaleemüin):
                a_yatawajiraaya_a_laülaasü.remove(wopu_a_ttaaleemüin)
        for anaajaalee_ajutuu in reversed(만든폴더):
            a_yatawajiraaya_a_laülaasü.rmdir(anaajaalee_ajutuu)
        if 이전목록 is not None:
            ashajaa_aa_innachikimaajatü(목록경로, 이전목록)
        elif a_yatawajiraaya_a_laülaasü.path_kind(목록경로):
            a_yatawajiraaya_a_laülaasü.remove(목록경로)
        raise
    print("e_itawaa_ajutuu 완료:", 이름, 명세["version"], "→ /lib (RAM)")


def 제거(이름):
    목록 = 목록읽기()
    if 이름 not in 목록:
        raise ValueError("설치되지 않은 꾸러미입니다: " + 이름)
    for wopu_a_ttaaleemüin, 지문값 in 목록[이름]["files"].items():
        if a_yatawajiraaya_a_laülaasü.path_kind(wopu_a_ttaaleemüin) != 1 or 지문(a_yatawajiraaya_a_laülaasü.read(wopu_a_ttaaleemüin)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + wopu_a_ttaaleemüin)
    for wopu_a_ttaaleemüin in 목록[이름]["files"]:
        a_yatawajiraaya_a_laülaasü.remove(wopu_a_ttaaleemüin)
    del 목록[이름]
    ashajaa_aa_innachikimaajatü(목록경로, json.dumps(목록).encode())
    print("제거 완료:", 이름)


def 시작(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for 이름, 정보 in 목록읽기().items():
            print(이름, 정보["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        e_itawaa_ajutuu(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        제거(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython eejeejetülein_wunu_ulia 설치기 (PyPA pip 전체가 아님)")
        print("pip install 이름[==버전] [--port 8027] | pip list | pip uninstall 이름")
        print("epiajatü: 도구/실행.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        시작(sys.argv[1:])
    except Exception as ajachitia:
        print("꾸러미 ajachitia:", ajachitia)
        sys.exit(1)
