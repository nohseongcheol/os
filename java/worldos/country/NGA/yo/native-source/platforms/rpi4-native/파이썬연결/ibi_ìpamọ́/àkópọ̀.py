"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 olùpèsè 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as OS

Àtòkọ_ọ̀nà = "/lib/.pip.json"


def 지문(détà):
    return "".join("%02x" % iye for iye in hashlib.sha256(détà).digest())


def 목록읽기():
    if OS.path_kind(Àtòkọ_ọ̀nà) == 0:
        return {}
    return json.loads(OS.read(Àtòkọ_ọ̀nà).decode("utf-8"))


def kọ_àkọsílẹ̀_ìṣe(ọ̀nà, détà):
    if OS.write(ọ̀nà, détà) != len(détà):
        raise OSError(28)


def ṣàyẹ̀wò_ọ̀nà(ọ̀nà):
    if not isinstance(ọ̀nà, str) or not ọ̀nà.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ọ̀nà.split("/")):
        raise ValueError("허용하지 않는 àkópọ̀ ọ̀nà")
    if "\\" in ọ̀nà or any(ord(ẹyọ_ọ̀rọ̀_iye) < 32 or ord(ẹyọ_ọ̀rọ̀_iye) == 127 for ẹyọ_ọ̀rọ̀_iye in ọ̀nà):
        raise ValueError("잘못된 ọ̀nà 문자")
    결과 = "/lib/" + ọ̀nà
    if len(결과.encode("utf-8")) > 63 or ọ̀nà in ("한국어.py", "àkópọ̀.py"):
        raise ValueError("àkópọ̀ 경로가 너무 길거나 àdáwọ̀ 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Rọ́ọ̀nù = OS.ticks_ms()

    def 정확히읽기(자신, gígùn_iye):
        détà = bytearray()
        while len(détà) < gígùn_iye:
            if OS.ticks_ms() - 자신.Rọ́ọ̀nù > 90000:
                raise ValueError("àkópọ̀ 중계 Fèsì 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = OS.tcp_read(자신.종단, 512)
                except OSError as àṣìṣe:
                    if àṣìṣe.args[0] != 11:
                        raise
                    OS.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("àkópọ̀ 전송이 중간에 끝났습니다.")
            개수 = min(gígùn_iye - len(détà), len(자신.남은자료))
            détà.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            OS.sleep_ms(0)
        return bytes(détà)


def gbígbà_ẹ̀dà_fáìlì(요청, 접속번호):
    if len(요청) > 96 or any(ẹyọ_ọ̀rọ̀_iye not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ẹyọ_ọ̀rọ̀_iye in 요청):
        raise ValueError("사용법: pip install Orúkọ 또는 Orúkọ==버전")
    종단 = OS.tcp_open()
    try:
        Rọ́ọ̀nù = OS.ticks_ms()
        while True:
            try:
                OS.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as àṣìṣe:
                if àṣìṣe.args[0] not in (11, 115) or OS.ticks_ms() - Rọ́ọ̀nù > 5000:
                    raise ValueError("àkópọ̀ 중계 Darapọ̀ ìkùnà_iye: 호스트에서 --network --pip로 실행하십시오.")
                OS.sleep_ms(10)
        détà = (요청 + "\n").encode()
        while détà:
            try:
                개수 = OS.tcp_write(종단, détà)
                if not 개수:
                    raise ValueError("àkópọ̀ 요청 ṣàgbélọ_iye ìkùnà_iye")
                détà = détà[개수:]
            except OSError as àṣìṣe:
                if àṣìṣe.args[0] != 11:
                    raise
                OS.sleep_ms(10)
                if OS.ticks_ms() - Rọ́ọ̀nù > 10000:
                    raise ValueError("àkópọ̀ 요청 ṣàgbélọ_iye 시간 초과")
        Stream_iye = 수신흐름(종단)
        머리 = Stream_iye.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("àkópọ̀ ṣàgbélọ_iye iṣẹ́_iye 불일치")
        gígùn_iye = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if gígùn_iye > 8192:
            raise ValueError("àkópọ̀ 명세가 너무 큽니다.")
        명세 = json.loads(Stream_iye.정확히읽기(gígùn_iye).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 orísun_ètò_afigijúwe 파일은 1~16개여야 합니다.")
        if sum(ìgbéwọlé_iye["size"] for ìgbéwọlé_iye in 명세["files"]) > 65536:
            raise ValueError("àkópọ̀ orísun_ètò_afigijúwe 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ìgbéwọlé_iye in 명세["files"]:
            ọ̀nà = ṣàyẹ̀wò_ọ̀nà(ìgbéwọlé_iye["path"])
            if ọ̀nà in 파일들 or not 0 <= ìgbéwọlé_iye["size"] <= 16384:
                raise ValueError("중복 ọ̀nà 또는 Fáìlì Ìwọ̀n 초과")
            détà = Stream_iye.정확히읽기(ìgbéwọlé_iye["size"])
            if 지문(détà) != ìgbéwọlé_iye["sha256"]:
                raise ValueError("àkópọ̀ Fáìlì SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(détà.decode("utf-8"), ọ̀nà, "exec")
            파일들[ọ̀nà] = détà
            gc.collect()
        return 명세, 파일들
    finally:
        OS.udp_close(종단)


def ṣàgbékalẹ̀_iye(요청, 접속번호):
    print("àkópọ̀ gbígbà_ẹ̀dà_fáìlì:", 요청)
    명세, 파일들 = gbígbà_ẹ̀dà_fáìlì(요청, 접속번호)
    ìgbéwọlé_Àtòkọ = 목록읽기()
    Orúkọ = 명세["name"]
    if Orúkọ in ìgbéwọlé_Àtòkọ:
        if ìgbéwọlé_Àtòkọ[Orúkọ]["version"] == 명세["version"]:
            for ọ̀nà, 지문값 in ìgbéwọlé_Àtòkọ[Orúkọ]["files"].items():
                if OS.path_kind(ọ̀nà) != 1 or 지문(OS.read(ọ̀nà)) != 지문값:
                    raise ValueError("설치된 àkópọ̀ 파일이 달라졌습니다: " + ọ̀nà)
            print("이미 설치됨:", Orúkọ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Padà_sẹ́yìn_iye 설치하십시오.")
    for ọ̀nà in 파일들:
        if OS.path_kind(ọ̀nà):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ọ̀nà)
    ìgbéwọlé_Àtòkọ[Orúkọ] = {"version": 명세["version"], "files": {ọ̀nà: 지문(détà) for ọ̀nà, détà in 파일들.items()}}
    새목록 = json.dumps(ìgbéwọlé_Àtòkọ).encode()
    if len(새목록) > 16384:
        raise ValueError("àkópọ̀ ìgbéwọlé_Àtòkọ Ìwọ̀n 초과")
    이전목록 = OS.read(Àtòkọ_ọ̀nà) if OS.path_kind(Àtòkọ_ọ̀nà) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ọ̀nà, détà in 파일들.items():
            부분들 = ọ̀nà.split("/")
            for 수 in range(2, len(부분들)):
                àkójọpọ̀_fáìlì_iye = "/".join(부분들[:수])
                종류 = OS.path_kind(àkójọpọ̀_fáìlì_iye)
                if 종류 == 0:
                    OS.mkdir(àkójọpọ̀_fáìlì_iye)
                    만든폴더.append(àkójọpọ̀_fáìlì_iye)
                elif 종류 != 2:
                    raise ValueError("àkójọpọ̀_fáìlì_iye 경로에 파일이 있습니다: " + àkójọpọ̀_fáìlì_iye)
            만든파일.append(ọ̀nà)
            kọ_àkọsílẹ̀_ìṣe(ọ̀nà, détà)
        kọ_àkọsílẹ̀_ìṣe(Àtòkọ_ọ̀nà, 새목록)
    except Exception:
        for ọ̀nà in 만든파일:
            if OS.path_kind(ọ̀nà):
                OS.remove(ọ̀nà)
        for àkójọpọ̀_fáìlì_iye in reversed(만든폴더):
            OS.rmdir(àkójọpọ̀_fáìlì_iye)
        if 이전목록 is not None:
            kọ_àkọsílẹ̀_ìṣe(Àtòkọ_ọ̀nà, 이전목록)
        elif OS.path_kind(Àtòkọ_ọ̀nà):
            OS.remove(Àtòkọ_ọ̀nà)
        raise
    print("ṣàgbékalẹ̀_iye 완료:", Orúkọ, 명세["version"], "→ /lib (RAM)")


def ṣèmúkúro_ìgbéwọlé(Orúkọ):
    ìgbéwọlé_Àtòkọ = 목록읽기()
    if Orúkọ not in ìgbéwọlé_Àtòkọ:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Orúkọ)
    for ọ̀nà, 지문값 in ìgbéwọlé_Àtòkọ[Orúkọ]["files"].items():
        if OS.path_kind(ọ̀nà) != 1 or 지문(OS.read(ọ̀nà)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ọ̀nà)
    for ọ̀nà in ìgbéwọlé_Àtòkọ[Orúkọ]["files"]:
        OS.remove(ọ̀nà)
    del ìgbéwọlé_Àtòkọ[Orúkọ]
    kọ_àkọsílẹ̀_ìṣe(Àtòkọ_ọ̀nà, json.dumps(ìgbéwọlé_Àtòkọ).encode())
    print("ṣèmúkúro_ìgbéwọlé 완료:", Orúkọ)


def Rọ́ọ̀nù(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Orúkọ, msinfo32_exe in 목록읽기().items():
            print(Orúkọ, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ṣàgbékalẹ̀_iye(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ṣèmúkúro_ìgbéwọlé(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython orísun_ètò_afigijúwe 설치기 (PyPA pip 전체가 아님)")
        print("pip install Orúkọ[==버전] [--port 8027] | pip list | pip uninstall Orúkọ")
        print("olùpèsè: Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Rọ́ọ̀nù(sys.argv[1:])
    except Exception as àṣìṣe:
        print("àkópọ̀ àṣìṣe:", àṣìṣe)
        sys.exit(1)
