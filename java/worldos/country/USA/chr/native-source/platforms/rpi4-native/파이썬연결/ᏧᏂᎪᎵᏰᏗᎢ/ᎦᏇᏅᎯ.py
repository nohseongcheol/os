"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ᎠᏁᏢᏍᎩ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ

ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ = "/lib/.pip.json"


def 지문(ᎦᏟᏌᏅᎯ):
    return "".join("%02x" % ᏧᎬᏩᎶᏗᏯ for ᏧᎬᏩᎶᏗᏯ in hashlib.sha256(ᎦᏟᏌᏅᎯ).digest())


def 목록읽기():
    if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ) == 0:
        return {}
    return json.loads(ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.read(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ).decode("utf-8"))


def ᎪᏪᎶᏗ_ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ):
    if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.write(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ) != len(ᎦᏟᏌᏅᎯ):
        raise OSError(28)


def ᎪᎯᏳᏔᏅ_ᎠᏍᏓᏩᏛᏍᏗ(ᎠᏍᏓᏩᏛᏍᏗ):
    if not isinstance(ᎠᏍᏓᏩᏛᏍᏗ, str) or not ᎠᏍᏓᏩᏛᏍᏗ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ᎠᏍᏓᏩᏛᏍᏗ.split("/")):
        raise ValueError("허용하지 않는 ᎦᏇᏅᎯ ᎠᏍᏓᏩᏛᏍᏗ")
    if "\\" in ᎠᏍᏓᏩᏛᏍᏗ or any(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) < 32 or ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) == 127 for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in ᎠᏍᏓᏩᏛᏍᏗ):
        raise ValueError("잘못된 ᎠᏍᏓᏩᏛᏍᏗ 문자")
    결과 = "/lib/" + ᎠᏍᏓᏩᏛᏍᏗ
    if len(결과.encode("utf-8")) > 63 or ᎠᏍᏓᏩᏛᏍᏗ in ("한국어.py", "ᎦᏇᏅᎯ.py"):
        raise ValueError("ᎦᏇᏅᎯ 경로가 너무 길거나 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ᎠᎢᏎᏍᏗ = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.ticks_ms()

    def 정확히읽기(자신, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ):
        ᎦᏟᏌᏅᎯ = bytearray()
        while len(ᎦᏟᏌᏅᎯ) < ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ:
            if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.ticks_ms() - 자신.ᎠᎢᏎᏍᏗ > 90000:
                raise ValueError("ᎦᏇᏅᎯ 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.tcp_read(자신.종단, 512)
                except OSError as ᎦᎵᏓᏍᏔᏅ:
                    if ᎦᎵᏓᏍᏔᏅ.args[0] != 11:
                        raise
                    ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ᎦᏇᏅᎯ 전송이 중간에 끝났습니다.")
            개수 = min(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ - len(ᎦᏟᏌᏅᎯ), len(자신.남은자료))
            ᎦᏟᏌᏅᎯ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.sleep_ms(0)
        return bytes(ᎦᏟᏌᏅᎯ)


def ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ(요청, 접속번호):
    if len(요청) > 96 or any(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 요청):
        raise ValueError("사용법: pip install ᏚᏙᎥᎢ 또는 ᏚᏙᎥᎢ==버전")
    종단 = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.tcp_open()
    try:
        ᎠᎢᏎᏍᏗ = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.ticks_ms()
        while True:
            try:
                ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as ᎦᎵᏓᏍᏔᏅ:
                if ᎦᎵᏓᏍᏔᏅ.args[0] not in (11, 115) or ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.ticks_ms() - ᎠᎢᏎᏍᏗ > 5000:
                    raise ValueError("ᎦᏇᏅᎯ 중계 ᎫᏓᎳ ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ: 호스트에서 --network --pip로 실행하십시오.")
                ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.sleep_ms(10)
        ᎦᏟᏌᏅᎯ = (요청 + "\n").encode()
        while ᎦᏟᏌᏅᎯ:
            try:
                개수 = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.tcp_write(종단, ᎦᏟᏌᏅᎯ)
                if not 개수:
                    raise ValueError("ᎦᏇᏅᎯ 요청 ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ")
                ᎦᏟᏌᏅᎯ = ᎦᏟᏌᏅᎯ[개수:]
            except OSError as ᎦᎵᏓᏍᏔᏅ:
                if ᎦᎵᏓᏍᏔᏅ.args[0] != 11:
                    raise
                ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.sleep_ms(10)
                if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.ticks_ms() - ᎠᎢᏎᏍᏗ > 10000:
                    raise ValueError("ᎦᏇᏅᎯ 요청 ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ 시간 초과")
        ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ = 수신흐름(종단)
        머리 = ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ᎦᏇᏅᎯ ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ 불일치")
        ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ > 8192:
            raise ValueError("ᎦᏇᏅᎯ 명세가 너무 큽니다.")
        명세 = json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.정확히읽기(ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ᎦᏟᏌᏅᎯ_ᏡᎬ 파일은 1~16개여야 합니다.")
        if sum(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ["size"] for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 명세["files"]) > 65536:
            raise ValueError("ᎦᏇᏅᎯ ᎦᏟᏌᏅᎯ_ᏡᎬ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 명세["files"]:
            ᎠᏍᏓᏩᏛᏍᏗ = ᎪᎯᏳᏔᏅ_ᎠᏍᏓᏩᏛᏍᏗ(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ["path"])
            if ᎠᏍᏓᏩᏛᏍᏗ in 파일들 or not 0 <= Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ["size"] <= 16384:
                raise ValueError("중복 ᎠᏍᏓᏩᏛᏍᏗ 또는 ᎠᏍᏆᏂᎪᏙᏗ ᎢᎩᏓ 초과")
            ᎦᏟᏌᏅᎯ = ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.정확히읽기(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ["size"])
            if 지문(ᎦᏟᏌᏅᎯ) != Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ["sha256"]:
                raise ValueError("ᎦᏇᏅᎯ ᎠᏍᏆᏂᎪᏙᏗ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ᎦᏟᏌᏅᎯ.decode("utf-8"), ᎠᏍᏓᏩᏛᏍᏗ, "exec")
            파일들[ᎠᏍᏓᏩᏛᏍᏗ] = ᎦᏟᏌᏅᎯ
            gc.collect()
        return 명세, 파일들
    finally:
        ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.udp_close(종단)


def ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ(요청, 접속번호):
    print("ᎦᏇᏅᎯ ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ:", 요청)
    명세, 파일들 = ᎡᎳᏓᎪᏘ_ᎦᏢᏍᎬᎢ(요청, 접속번호)
    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ = 목록읽기()
    ᏚᏙᎥᎢ = 명세["name"]
    if ᏚᏙᎥᎢ in Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ:
        if Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ[ᏚᏙᎥᎢ]["version"] == 명세["version"]:
            for ᎠᏍᏓᏩᏛᏍᏗ, 지문값 in Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ[ᏚᏙᎥᎢ]["files"].items():
                if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᎠᏍᏓᏩᏛᏍᏗ) != 1 or 지문(ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.read(ᎠᏍᏓᏩᏛᏍᏗ)) != 지문값:
                    raise ValueError("설치된 ᎦᏇᏅᎯ 파일이 달라졌습니다: " + ᎠᏍᏓᏩᏛᏍᏗ)
            print("이미 설치됨:", ᏚᏙᎥᎢ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ 설치하십시오.")
    for ᎠᏍᏓᏩᏛᏍᏗ in 파일들:
        if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᎠᏍᏓᏩᏛᏍᏗ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ᎠᏍᏓᏩᏛᏍᏗ)
    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ[ᏚᏙᎥᎢ] = {"version": 명세["version"], "files": {ᎠᏍᏓᏩᏛᏍᏗ: 지문(ᎦᏟᏌᏅᎯ) for ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ in 파일들.items()}}
    새목록 = json.dumps(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ).encode()
    if len(새목록) > 16384:
        raise ValueError("ᎦᏇᏅᎯ Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ ᎢᎩᏓ 초과")
    이전목록 = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.read(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ) if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ in 파일들.items():
            부분들 = ᎠᏍᏓᏩᏛᏍᏗ.split("/")
            for 수 in range(2, len(부분들)):
                ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ = "/".join(부분들[:수])
                종류 = ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)
                if 종류 == 0:
                    ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.mkdir(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)
                    만든폴더.append(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)
                elif 종류 != 2:
                    raise ValueError("ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ 경로에 파일이 있습니다: " + ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)
            만든파일.append(ᎠᏍᏓᏩᏛᏍᏗ)
            ᎪᏪᎶᏗ_ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ)
        ᎪᏪᎶᏗ_ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ, 새목록)
    except Exception:
        for ᎠᏍᏓᏩᏛᏍᏗ in 만든파일:
            if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᎠᏍᏓᏩᏛᏍᏗ):
                ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.remove(ᎠᏍᏓᏩᏛᏍᏗ)
        for ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ in reversed(만든폴더):
            ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.rmdir(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)
        if 이전목록 is not None:
            ᎪᏪᎶᏗ_ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ, 이전목록)
        elif ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ):
            ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.remove(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ)
        raise
    print("ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ 완료:", ᏚᏙᎥᎢ, 명세["version"], "→ /lib (RAM)")


def ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(ᏚᏙᎥᎢ):
    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ = 목록읽기()
    if ᏚᏙᎥᎢ not in Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ᏚᏙᎥᎢ)
    for ᎠᏍᏓᏩᏛᏍᏗ, 지문값 in Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ[ᏚᏙᎥᎢ]["files"].items():
        if ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.path_kind(ᎠᏍᏓᏩᏛᏍᏗ) != 1 or 지문(ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.read(ᎠᏍᏓᏩᏛᏍᏗ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ᎠᏍᏓᏩᏛᏍᏗ)
    for ᎠᏍᏓᏩᏛᏍᏗ in Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ[ᏚᏙᎥᎢ]["files"]:
        ᎢᏯᏛᏁᏗ_ᏄᏍᏗᏓᏅᎢ.remove(ᎠᏍᏓᏩᏛᏍᏗ)
    del Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ[ᏚᏙᎥᎢ]
    ᎪᏪᎶᏗ_ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ(ᏕᎦᏅᏅᏛ_ᎠᏍᏓᏩᏛᏍᏗ, json.dumps(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ).encode())
    print("ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ 완료:", ᏚᏙᎥᎢ)


def ᎠᎢᏎᏍᏗ(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ᏚᏙᎥᎢ, msinfo32_exe in 목록읽기().items():
            print(ᏚᏙᎥᎢ, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ᎯᎲᎾ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ᎦᏟᏌᏅᎯ_ᏡᎬ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ᏚᏙᎥᎢ[==버전] [--port 8027] | pip list | pip uninstall ᏚᏙᎥᎢ")
        print("ᎠᏁᏢᏍᎩ: 도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ᎠᎢᏎᏍᏗ(sys.argv[1:])
    except Exception as ᎦᎵᏓᏍᏔᏅ:
        print("ᎦᏇᏅᎯ ᎦᎵᏓᏍᏔᏅ:", ᎦᎵᏓᏍᏔᏅ)
        sys.exit(1)
