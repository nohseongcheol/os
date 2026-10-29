"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 հոստ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as գործավար_համակարգ

Ցուցակ_ուղի = "/lib/.pip.json"


def 지문(տվյալ):
    return "".join("%02x" % արժեք for արժեք in hashlib.sha256(տվյալ).digest())


def 목록읽기():
    if գործավար_համակարգ.path_kind(Ցուցակ_ուղի) == 0:
        return {}
    return json.loads(գործավար_համակարգ.read(Ցուցակ_ուղի).decode("utf-8"))


def գրել_մատյան(Ճանապարհ, տվյալ):
    if գործավար_համակարգ.write(Ճանապարհ, տվյալ) != len(տվյալ):
        raise OSError(28)


def կտրոն_ուղի(Ճանապարհ):
    if not isinstance(Ճանապարհ, str) or not Ճանապարհ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Ճանապարհ.split("/")):
        raise ValueError("허용하지 않는 փաթեթ Ճանապարհ")
    if "\\" in Ճանապարհ or any(ord(գրանշան_արժեք) < 32 or ord(գրանշան_արժեք) == 127 for գրանշան_արժեք in Ճանապարհ):
        raise ValueError("잘못된 Ճանապարհ 문자")
    չափ = "/lib/" + Ճանապարհ
    if len(չափ.encode("utf-8")) > 63 or Ճանապարհ in ("한국어.py", "փաթեթ.py"):
        raise ValueError("փաթեթ 경로가 너무 길거나 սկզբնադիր_արժեք 라이브러리와 겹칩니다.")
    return չափ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Գործարկել = գործավար_համակարգ.ticks_ms()

    def 정확히읽기(자신, տեւողություն_արժեք):
        տվյալ = bytearray()
        while len(տվյալ) < տեւողություն_արժեք:
            if գործավար_համակարգ.ticks_ms() - 자신.Գործարկել > 90000:
                raise ValueError("փաթեթ 중계 պատասխանել 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = գործավար_համակարգ.tcp_read(자신.종단, 512)
                except OSError as Սխալ:
                    if Սխալ.args[0] != 11:
                        raise
                    գործավար_համակարգ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("փաթեթ 전송이 중간에 끝났습니다.")
            개수 = min(տեւողություն_արժեք - len(տվյալ), len(자신.남은자료))
            տվյալ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            գործավար_համակարգ.sleep_ms(0)
        return bytes(տվյալ)


def ներբեռնել(요청, 접속번호):
    if len(요청) > 96 or any(գրանշան_արժեք not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for գրանշան_արժեք in 요청):
        raise ValueError("사용법: pip install Անուն 또는 Անուն==버전")
    종단 = գործավար_համակարգ.tcp_open()
    try:
        Գործարկել = գործավար_համակարգ.ticks_ms()
        while True:
            try:
                գործավար_համակարգ.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Սխալ:
                if Սխալ.args[0] not in (11, 115) or գործավար_համակարգ.ticks_ms() - Գործարկել > 5000:
                    raise ValueError("փաթեթ 중계 Միացնել ձախողում_արժեք: 호스트에서 --network --pip로 실행하십시오.")
                գործավար_համակարգ.sleep_ms(10)
        տվյալ = (요청 + "\n").encode()
        while տվյալ:
            try:
                개수 = գործավար_համակարգ.tcp_write(종단, տվյալ)
                if not 개수:
                    raise ValueError("փաթեթ 요청 փոխանցել_արժեք ձախողում_արժեք")
                տվյալ = տվյալ[개수:]
            except OSError as Սխալ:
                if Սխալ.args[0] != 11:
                    raise
                գործավար_համակարգ.sleep_ms(10)
                if գործավար_համակարգ.ticks_ms() - Գործարկել > 10000:
                    raise ValueError("փաթեթ 요청 փոխանցել_արժեք 시간 초과")
        հոսք_արժեք = 수신흐름(종단)
        머리 = հոսք_արժեք.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("փաթեթ փոխանցել_արժեք գործ_արժեք 불일치")
        տեւողություն_արժեք = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if տեւողություն_արժեք > 8192:
            raise ValueError("փաթեթ 명세가 너무 큽니다.")
        명세 = json.loads(հոսք_արժեք.정확히읽기(տեւողություն_արժեք).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 աղբյուր_ծառ 파일은 1~16개여야 합니다.")
        if sum(մուտքագրում_արժեք["size"] for մուտքագրում_արժեք in 명세["files"]) > 65536:
            raise ValueError("փաթեթ աղբյուր_ծառ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for մուտքագրում_արժեք in 명세["files"]:
            Ճանապարհ = կտրոն_ուղի(մուտքագրում_արժեք["path"])
            if Ճանապարհ in 파일들 or not 0 <= մուտքագրում_արժեք["size"] <= 16384:
                raise ValueError("중복 Ճանապարհ 또는 Ֆայլ Չափս 초과")
            տվյալ = հոսք_արժեք.정확히읽기(մուտքագրում_արժեք["size"])
            if 지문(տվյալ) != մուտքագրում_արժեք["sha256"]:
                raise ValueError("փաթեթ Ֆայլ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(տվյալ.decode("utf-8"), Ճանապարհ, "exec")
            파일들[Ճանապարհ] = տվյալ
            gc.collect()
        return 명세, 파일들
    finally:
        գործավար_համակարգ.udp_close(종단)


def տեղադրել_արժեք(요청, 접속번호):
    print("փաթեթ ներբեռնել:", 요청)
    명세, 파일들 = ներբեռնել(요청, 접속번호)
    մուտքագրում_Ցուցակ = 목록읽기()
    Անուն = 명세["name"]
    if Անուն in մուտքագրում_Ցուցակ:
        if մուտքագրում_Ցուցակ[Անուն]["version"] == 명세["version"]:
            for Ճանապարհ, 지문값 in մուտքագրում_Ցուցակ[Անուն]["files"].items():
                if գործավար_համակարգ.path_kind(Ճանապարհ) != 1 or 지문(գործավար_համակարգ.read(Ճանապարհ)) != 지문값:
                    raise ValueError("설치된 փաթեթ 파일이 달라졌습니다: " + Ճանապարհ)
            print("이미 설치됨:", Անուն, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Հետ_արժեք 설치하십시오.")
    for Ճանապարհ in 파일들:
        if գործավար_համակարգ.path_kind(Ճանապարհ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Ճանապարհ)
    մուտքագրում_Ցուցակ[Անուն] = {"version": 명세["version"], "files": {Ճանապարհ: 지문(տվյալ) for Ճանապարհ, տվյալ in 파일들.items()}}
    새목록 = json.dumps(մուտքագրում_Ցուցակ).encode()
    if len(새목록) > 16384:
        raise ValueError("փաթեթ մուտքագրում_Ցուցակ Չափս 초과")
    이전목록 = գործավար_համակարգ.read(Ցուցակ_ուղի) if գործավար_համակարգ.path_kind(Ցուցակ_ուղի) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Ճանապարհ, տվյալ in 파일들.items():
            부분들 = Ճանապարհ.split("/")
            for 수 in range(2, len(부분들)):
                գրացուցակ_արժեք = "/".join(부분들[:수])
                종류 = գործավար_համակարգ.path_kind(գրացուցակ_արժեք)
                if 종류 == 0:
                    գործավար_համակարգ.mkdir(գրացուցակ_արժեք)
                    만든폴더.append(գրացուցակ_արժեք)
                elif 종류 != 2:
                    raise ValueError("գրացուցակ_արժեք 경로에 파일이 있습니다: " + գրացուցակ_արժեք)
            만든파일.append(Ճանապարհ)
            գրել_մատյան(Ճանապարհ, տվյալ)
        գրել_մատյան(Ցուցակ_ուղի, 새목록)
    except Exception:
        for Ճանապարհ in 만든파일:
            if գործավար_համակարգ.path_kind(Ճանապարհ):
                գործավար_համակարգ.remove(Ճանապարհ)
        for գրացուցակ_արժեք in reversed(만든폴더):
            գործավար_համակարգ.rmdir(գրացուցակ_արժեք)
        if 이전목록 is not None:
            գրել_մատյան(Ցուցակ_ուղի, 이전목록)
        elif գործավար_համակարգ.path_kind(Ցուցակ_ուղի):
            գործավար_համակարգ.remove(Ցուցակ_ուղի)
        raise
    print("տեղադրել_արժեք 완료:", Անուն, 명세["version"], "→ /lib (RAM)")


def հեռացնել_մուտքագրում(Անուն):
    մուտքագրում_Ցուցակ = 목록읽기()
    if Անուն not in մուտքագրում_Ցուցակ:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Անուն)
    for Ճանապարհ, 지문값 in մուտքագրում_Ցուցակ[Անուն]["files"].items():
        if գործավար_համակարգ.path_kind(Ճանապարհ) != 1 or 지문(գործավար_համակարգ.read(Ճանապարհ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Ճանապարհ)
    for Ճանապարհ in մուտքագրում_Ցուցակ[Անուն]["files"]:
        գործավար_համակարգ.remove(Ճանապարհ)
    del մուտքագրում_Ցուցակ[Անուն]
    գրել_մատյան(Ցուցակ_ուղի, json.dumps(մուտքագրում_Ցուցակ).encode())
    print("հեռացնել_մուտքագրում 완료:", Անուն)


def Գործարկել(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Անուն, Համակարգի_տեղեկություն in 목록읽기().items():
            print(Անուն, Համակարգի_տեղեկություն["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        տեղադրել_արժեք(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        հեռացնել_մուտքագրում(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython աղբյուր_ծառ 설치기 (PyPA pip 전체가 아님)")
        print("pip install Անուն[==버전] [--port 8027] | pip list | pip uninstall Անուն")
        print("հոստ: Գործիքներ/կատարել_հրաման.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Գործարկել(sys.argv[1:])
    except Exception as Սխալ:
        print("փաթեթ Սխալ:", Սխալ)
        sys.exit(1)
