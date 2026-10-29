"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 હોસ્ટ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ઑપરેટિંગ_સિસ્ટમ

સૂચી_પાથ = "/lib/.pip.json"


def 지문(ડેટા):
    return "".join("%02x" % મૂલ્ય for મૂલ્ય in hashlib.sha256(ડેટા).digest())


def 목록읽기():
    if ઑપરેટિંગ_સિસ્ટમ.path_kind(સૂચી_પાથ) == 0:
        return {}
    return json.loads(ઑપરેટિંગ_સિસ્ટમ.read(સૂચી_પાથ).decode("utf-8"))


def લખો_લૉગ(પથ, ડેટા):
    if ઑપરેટિંગ_સિસ્ટમ.write(પથ, ડેટા) != len(ડેટા):
        raise OSError(28)


def તપાસો_પાથ(પથ):
    if not isinstance(પથ, str) or not પથ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in પથ.split("/")):
        raise ValueError("허용하지 않는 બન્ડલ પથ")
    if "\\" in પથ or any(ord(વર્ણ_મૂલ્ય) < 32 or ord(વર્ણ_મૂલ્ય) == 127 for વર્ણ_મૂલ્ય in પથ):
        raise ValueError("잘못된 પથ 문자")
    પરિમાણ = "/lib/" + પથ
    if len(પરિમાણ.encode("utf-8")) > 63 or પથ in ("ગુજરાતી.py", "બન્ડલ.py"):
        raise ValueError("બન્ડલ 경로가 너무 길거나 ડિફૉલ્ટ_મૂલ્ય 라이브러리와 겹칩니다.")
    return પરિમાણ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ચલાવો_2 = ઑપરેટિંગ_સિસ્ટમ.ticks_ms()

    def 정확히읽기(자신, લંબાઈ_મૂલ્ય):
        ડેટા = bytearray()
        while len(ડેટા) < લંબાઈ_મૂલ્ય:
            if ઑપરેટિંગ_સિસ્ટમ.ticks_ms() - 자신.ચલાવો_2 > 90000:
                raise ValueError("બન્ડલ 중계 જવાબ સમય_મૂલ્ય 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ઑપરેટિંગ_સિસ્ટમ.tcp_read(자신.종단, 512)
                except OSError as ભૂલ:
                    if ભૂલ.args[0] != 11:
                        raise
                    ઑપરેટિંગ_સિસ્ટમ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("બન્ડલ 전송이 중간에 끝났습니다.")
            개수 = min(લંબાઈ_મૂલ્ય - len(ડેટા), len(자신.남은자료))
            ડેટા.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ઑપરેટિંગ_સિસ્ટમ.sleep_ms(0)
        return bytes(ડેટા)


def ડાઉનલોડ(요청, પોર્ટ_નંબર):
    if len(요청) > 96 or any(વર્ણ_મૂલ્ય not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for વર્ણ_મૂલ્ય in 요청):
        raise ValueError("사용법: pip install નામ 또는 નામ==버전")
    종단 = ઑપરેટિંગ_સિસ્ટમ.tcp_open()
    try:
        ચલાવો_2 = ઑપરેટિંગ_સિસ્ટમ.ticks_ms()
        while True:
            try:
                ઑપરેટિંગ_સિસ્ટમ.tcp_connect(종단, "10.0.2.2", પોર્ટ_નંબર)
                break
            except OSError as ભૂલ:
                if ભૂલ.args[0] not in (11, 115) or ઑપરેટિંગ_સિસ્ટમ.ticks_ms() - ચલાવો_2 > 5000:
                    raise ValueError("બન્ડલ 중계 સંપર્ક_કરો નિષ્ફળતા_મૂલ્ય: 호스트에서 --network --pip로 실행하십시오.")
                ઑપરેટિંગ_સિસ્ટમ.sleep_ms(10)
        ડેટા = (요청 + "\n").encode()
        while ડેટા:
            try:
                개수 = ઑપરેટિંગ_સિસ્ટમ.tcp_write(종단, ડેટા)
                if not 개수:
                    raise ValueError("બન્ડલ 요청 સ્થાનાંતર_મૂલ્ય નિષ્ફળતા_મૂલ્ય")
                ડેટા = ડેટા[개수:]
            except OSError as ભૂલ:
                if ભૂલ.args[0] != 11:
                    raise
                ઑપરેટિંગ_સિસ્ટમ.sleep_ms(10)
                if ઑપરેટિંગ_સિસ્ટમ.ticks_ms() - ચલાવો_2 > 10000:
                    raise ValueError("બન્ડલ 요청 સ્થાનાંતર_મૂલ્ય સમય_મૂલ્ય 초과")
        સ્ટ્રીમ_મૂલ્ય = 수신흐름(종단)
        머리 = સ્ટ્રીમ_મૂલ્ય.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("બન્ડલ સ્થાનાંતર_મૂલ્ય કામ_મૂલ્ય 불일치")
        લંબાઈ_મૂલ્ય = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if લંબાઈ_મૂલ્ય > 8192:
            raise ValueError("બન્ડલ 명세가 너무 큽니다.")
        명세 = json.loads(સ્ટ્રીમ_મૂલ્ય.정확히읽기(લંબાઈ_મૂલ્ય).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 સ્રોત_ટ્રી 파일은 1~16개여야 합니다.")
        if sum(પ્રવેશ_મૂલ્ય["size"] for પ્રવેશ_મૂલ્ય in 명세["files"]) > 65536:
            raise ValueError("બન્ડલ સ્રોત_ટ્રી 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for પ્રવેશ_મૂલ્ય in 명세["files"]:
            પથ = તપાસો_પાથ(પ્રવેશ_મૂલ્ય["path"])
            if પથ in 파일들 or not 0 <= પ્રવેશ_મૂલ્ય["size"] <= 16384:
                raise ValueError("중복 પથ 또는 ફાઈલ માપ 초과")
            ડેટા = સ્ટ્રીમ_મૂલ્ય.정확히읽기(પ્રવેશ_મૂલ્ય["size"])
            if 지문(ડેટા) != પ્રવેશ_મૂલ્ય["sha256"]:
                raise ValueError("બન્ડલ ફાઈલ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ડેટા.decode("utf-8"), પથ, "exec")
            파일들[પથ] = ડેટા
            gc.collect()
        return 명세, 파일들
    finally:
        ઑપરેટિંગ_સિસ્ટમ.udp_close(종단)


def સ્થાપિત_કરો_મૂલ્ય(요청, પોર્ટ_નંબર):
    print("બન્ડલ ડાઉનલોડ:", 요청)
    명세, 파일들 = ડાઉનલોડ(요청, પોર્ટ_નંબર)
    પ્રવેશ_સૂચી = 목록읽기()
    નામ = 명세["name"]
    if નામ in પ્રવેશ_સૂચી:
        if પ્રવેશ_સૂચી[નામ]["version"] == 명세["version"]:
            for પથ, 지문값 in પ્રવેશ_સૂચી[નામ]["files"].items():
                if ઑપરેટિંગ_સિસ્ટમ.path_kind(પથ) != 1 or 지문(ઑપરેટિંગ_સિસ્ટમ.read(પથ)) != 지문값:
                    raise ValueError("설치된 બન્ડલ 파일이 달라졌습니다: " + પથ)
            print("이미 설치됨:", નામ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 બેક_મૂલ્ય 설치하십시오.")
    for પથ in 파일들:
        if ઑપરેટિંગ_સિસ્ટમ.path_kind(પથ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + પથ)
    પ્રવેશ_સૂચી[નામ] = {"version": 명세["version"], "files": {પથ: 지문(ડેટા) for પથ, ડેટા in 파일들.items()}}
    새목록 = json.dumps(પ્રવેશ_સૂચી).encode()
    if len(새목록) > 16384:
        raise ValueError("બન્ડલ પ્રવેશ_સૂચી માપ 초과")
    이전목록 = ઑપરેટિંગ_સિસ્ટમ.read(સૂચી_પાથ) if ઑપરેટિંગ_સિસ્ટમ.path_kind(સૂચી_પાથ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for પથ, ડેટા in 파일들.items():
            부분들 = પથ.split("/")
            for 수 in range(2, len(부분들)):
                નિર્દેશિકા_મૂલ્ય = "/".join(부분들[:수])
                종류 = ઑપરેટિંગ_સિસ્ટમ.path_kind(નિર્દેશિકા_મૂલ્ય)
                if 종류 == 0:
                    ઑપરેટિંગ_સિસ્ટમ.mkdir(નિર્દેશિકા_મૂલ્ય)
                    만든폴더.append(નિર્દેશિકા_મૂલ્ય)
                elif 종류 != 2:
                    raise ValueError("નિર્દેશિકા_મૂલ્ય 경로에 파일이 있습니다: " + નિર્દેશિકા_મૂલ્ય)
            만든파일.append(પથ)
            લખો_લૉગ(પથ, ડેટા)
        લખો_લૉગ(સૂચી_પાથ, 새목록)
    except Exception:
        for પથ in 만든파일:
            if ઑપરેટિંગ_સિસ્ટમ.path_kind(પથ):
                ઑપરેટિંગ_સિસ્ટમ.remove(પથ)
        for નિર્દેશિકા_મૂલ્ય in reversed(만든폴더):
            ઑપરેટિંગ_સિસ્ટમ.rmdir(નિર્દેશિકા_મૂલ્ય)
        if 이전목록 is not None:
            લખો_લૉગ(સૂચી_પાથ, 이전목록)
        elif ઑપરેટિંગ_સિસ્ટમ.path_kind(સૂચી_પાથ):
            ઑપરેટિંગ_સિસ્ટમ.remove(સૂચી_પાથ)
        raise
    print("સ્થાપિત_કરો_મૂલ્ય 완료:", નામ, 명세["version"], "→ /lib (RAM)")


def કાઢી_નાંખો_પ્રવેશ(નામ):
    પ્રવેશ_સૂચી = 목록읽기()
    if નામ not in પ્રવેશ_સૂચી:
        raise ValueError("설치되지 않은 꾸러미입니다: " + નામ)
    for પથ, 지문값 in પ્રવેશ_સૂચી[નામ]["files"].items():
        if ઑપરેટિંગ_સિસ્ટમ.path_kind(પથ) != 1 or 지문(ઑપરેટિંગ_સિસ્ટમ.read(પથ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + પથ)
    for પથ in પ્રવેશ_સૂચી[નામ]["files"]:
        ઑપરેટિંગ_સિસ્ટમ.remove(પથ)
    del પ્રવેશ_સૂચી[નામ]
    લખો_લૉગ(સૂચી_પાથ, json.dumps(પ્રવેશ_સૂચી).encode())
    print("કાઢી_નાંખો_પ્રવેશ 완료:", નામ)


def ચલાવો_2(દલીલો):
    પોર્ટ_નંબર = 8027
    if len(દલીલો) >= 2 and દલીલો[-2] == "--port":
        પોર્ટ_નંબર = int(દલીલો[-1])
        દલીલો = દલીલો[:-2]
    if દલીલો == ["list"]:
        for નામ, સિસ્ટમ_માહિતી in 목록읽기().items():
            print(નામ, સિસ્ટમ_માહિતી["version"])
    elif len(દલીલો) == 2 and દલીલો[0] == "install":
        સ્થાપિત_કરો_મૂલ્ય(દલીલો[1], પોર્ટ_નંબર)
    elif len(દલીલો) == 2 and દલીલો[0] == "uninstall":
        કાઢી_નાંખો_પ્રવેશ(દલીલો[1])
    elif not દલીલો or દલીલો in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython સ્રોત_ટ્રી 설치기 (PyPA pip 전체가 아님)")
        print("pip install નામ[==버전] [--port 8027] | pip list | pip uninstall નામ")
        print("હોસ્ટ: ઉપકરણો/અમલ_કરો_આદેશ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ચલાવો_2(sys.argv[1:])
    except Exception as ભૂલ:
        print("બન્ડલ ભૂલ:", ભૂલ)
        sys.exit(1)
