"""निज 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 आयोजक 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ऑपरेटिंग_सिस्टम

सूची_पथ = "/lib/.pip.json"


def 지문(आँकड़े):
    return "".join("%02x" % मान for मान in hashlib.sha256(आँकड़े).digest())


def पढें_सूची():
    if ऑपरेटिंग_सिस्टम.path_kind(सूची_पथ) == 0:
        return {}
    return json.loads(ऑपरेटिंग_सिस्टम.read(सूची_पथ).decode("utf-8"))


def लिखना_लॉग(पथ, आँकड़े):
    if ऑपरेटिंग_सिस्टम.write(पथ, आँकड़े) != len(आँकड़े):
        raise OSError(28)


def जाँचें_पथ(पथ):
    if not isinstance(पथ, str) or not पथ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in पथ.split("/")):
        raise ValueError("허용하지 않는 बंडल पथ")
    if "\\" in पथ or any(ord(कैरेक्टर_मान) < 32 or ord(कैरेक्टर_मान) == 127 for कैरेक्टर_मान in पथ):
        raise ValueError("잘못된 पथ 문자")
    परिणाम = "/lib/" + पथ
    if len(परिणाम.encode("utf-8")) > 63 or पथ in ("हिंदी.py", "बंडल.py"):
        raise ValueError("बंडल 경로가 너무 길거나 डिफ़ॉल्ट_मान 라이브러리와 겹칩니다.")
    return परिणाम


class 수신흐름:
    def __init__(자신, एंडपॉइंट):
        자신.एंडपॉइंट = एंडपॉइंट
        자신.남은자료 = b""
        자신.चलाएँ = ऑपरेटिंग_सिस्टम.ticks_ms()

    def 정확히읽기(자신, 길이):
        आँकड़े = bytearray()
        while len(आँकड़े) < 길이:
            if ऑपरेटिंग_सिस्टम.ticks_ms() - 자신.चलाएँ > 90000:
                raise ValueError("बंडल 중계 उत्तर समय_उपयोगिता 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ऑपरेटिंग_सिस्टम.tcp_read(자신.एंडपॉइंट, 512)
                except OSError as त्रुटि:
                    if त्रुटि.args[0] != 11:
                        raise
                    ऑपरेटिंग_सिस्टम.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("बंडल 전송이 중간에 끝났습니다.")
            개수 = min(길이 - len(आँकड़े), len(자신.남은자료))
            आँकड़े.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ऑपरेटिंग_सिस्टम.sleep_ms(0)
        return bytes(आँकड़े)


def डाउनलोड(अनुरोध, पोर्ट_संख्या):
    if len(अनुरोध) > 96 or any(कैरेक्टर_मान not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for कैरेक्टर_मान in अनुरोध):
        raise ValueError("사용법: pip install नाम 또는 नाम==버전")
    एंडपॉइंट = ऑपरेटिंग_सिस्टम.tcp_open()
    try:
        चलाएँ = ऑपरेटिंग_सिस्टम.ticks_ms()
        while True:
            try:
                ऑपरेटिंग_सिस्टम.tcp_connect(एंडपॉइंट, "10.0.2.2", पोर्ट_संख्या)
                break
            except OSError as त्रुटि:
                if त्रुटि.args[0] not in (11, 115) or ऑपरेटिंग_सिस्टम.ticks_ms() - चलाएँ > 5000:
                    raise ValueError("बंडल 중계 जोड़ना विफलता_मान: 호스트에서 --network --pip로 실행하십시오.")
                ऑपरेटिंग_सिस्टम.sleep_ms(10)
        आँकड़े = (अनुरोध + "\n").encode()
        while आँकड़े:
            try:
                개수 = ऑपरेटिंग_सिस्टम.tcp_write(एंडपॉइंट, आँकड़े)
                if not 개수:
                    raise ValueError("बंडल अनुरोध हस्तांतरण_मान विफलता_मान")
                आँकड़े = आँकड़े[개수:]
            except OSError as त्रुटि:
                if त्रुटि.args[0] != 11:
                    raise
                ऑपरेटिंग_सिस्टम.sleep_ms(10)
                if ऑपरेटिंग_सिस्टम.ticks_ms() - चलाएँ > 10000:
                    raise ValueError("बंडल अनुरोध हस्तांतरण_मान समय_उपयोगिता 초과")
        स्ट्रीम_मान = 수신흐름(एंडपॉइंट)
        머리 = स्ट्रीम_मान.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("बंडल हस्तांतरण_मान मामला_मान 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("बंडल 명세가 너무 큽니다.")
        명세 = json.loads(स्ट्रीम_मान.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 स्रोत_ट्री 파일은 1~16개여야 합니다.")
        if sum(एन्ट्री_मान["size"] for एन्ट्री_मान in 명세["files"]) > 65536:
            raise ValueError("बंडल स्रोत_ट्री 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for एन्ट्री_मान in 명세["files"]:
            पथ = जाँचें_पथ(एन्ट्री_मान["path"])
            if पथ in 파일들 or not 0 <= एन्ट्री_मान["size"] <= 16384:
                raise ValueError("중복 पथ 또는 संचिका आकार 초과")
            आँकड़े = स्ट्रीम_मान.정확히읽기(एन्ट्री_मान["size"])
            if 지문(आँकड़े) != एन्ट्री_मान["sha256"]:
                raise ValueError("बंडल संचिका SHA-256 불일치")
            # 실행하지 않고 अद्यतित_आइटम MicroPython의 문법으로 먼저 검사한다.
            compile(आँकड़े.decode("utf-8"), पथ, "exec")
            파일들[पथ] = आँकड़े
            gc.collect()
        return 명세, 파일들
    finally:
        ऑपरेटिंग_सिस्टम.udp_close(एंडपॉइंट)


def इंस्टॉल_करें_मान(अनुरोध, पोर्ट_संख्या):
    print("बंडल डाउनलोड:", अनुरोध)
    명세, 파일들 = डाउनलोड(अनुरोध, पोर्ट_संख्या)
    एन्ट्री_सूची = पढें_सूची()
    नाम = 명세["name"]
    if नाम in एन्ट्री_सूची:
        if एन्ट्री_सूची[नाम]["version"] == 명세["version"]:
            for पथ, 지문값 in एन्ट्री_सूची[नाम]["files"].items():
                if ऑपरेटिंग_सिस्टम.path_kind(पथ) != 1 or 지문(ऑपरेटिंग_सिस्टम.read(पथ)) != 지문값:
                    raise ValueError("설치된 बंडल 파일이 달라졌습니다: " + पथ)
            print("이미 설치됨:", नाम, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 वापस_मान 설치하십시오.")
    for पथ in 파일들:
        if ऑपरेटिंग_सिस्टम.path_kind(पथ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + पथ)
    एन्ट्री_सूची[नाम] = {"version": 명세["version"], "files": {पथ: 지문(आँकड़े) for पथ, आँकड़े in 파일들.items()}}
    새목록 = json.dumps(एन्ट्री_सूची).encode()
    if len(새목록) > 16384:
        raise ValueError("बंडल एन्ट्री_सूची आकार 초과")
    이전목록 = ऑपरेटिंग_सिस्टम.read(सूची_पथ) if ऑपरेटिंग_सिस्टम.path_kind(सूची_पथ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for पथ, आँकड़े in 파일들.items():
            부분들 = पथ.split("/")
            for 수 in range(2, len(부분들)):
                डायरेक्टरी_मान = "/".join(부분들[:수])
                종류 = ऑपरेटिंग_सिस्टम.path_kind(डायरेक्टरी_मान)
                if 종류 == 0:
                    ऑपरेटिंग_सिस्टम.mkdir(डायरेक्टरी_मान)
                    만든폴더.append(डायरेक्टरी_मान)
                elif 종류 != 2:
                    raise ValueError("डायरेक्टरी_मान 경로에 파일이 있습니다: " + डायरेक्टरी_मान)
            만든파일.append(पथ)
            लिखना_लॉग(पथ, आँकड़े)
        लिखना_लॉग(सूची_पथ, 새목록)
    except Exception:
        for पथ in 만든파일:
            if ऑपरेटिंग_सिस्टम.path_kind(पथ):
                ऑपरेटिंग_सिस्टम.remove(पथ)
        for डायरेक्टरी_मान in reversed(만든폴더):
            ऑपरेटिंग_सिस्टम.rmdir(डायरेक्टरी_मान)
        if 이전목록 is not None:
            लिखना_लॉग(सूची_पथ, 이전목록)
        elif ऑपरेटिंग_सिस्टम.path_kind(सूची_पथ):
            ऑपरेटिंग_सिस्टम.remove(सूची_पथ)
        raise
    print("इंस्टॉल_करें_मान 완료:", नाम, 명세["version"], "→ /lib (RAM)")


def निकालें_एन्ट्री(नाम):
    एन्ट्री_सूची = पढें_सूची()
    if नाम not in एन्ट्री_सूची:
        raise ValueError("설치되지 않은 꾸러미입니다: " + नाम)
    for पथ, 지문값 in एन्ट्री_सूची[नाम]["files"].items():
        if ऑपरेटिंग_सिस्टम.path_kind(पथ) != 1 or 지문(ऑपरेटिंग_सिस्टम.read(पथ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + पथ)
    for पथ in एन्ट्री_सूची[नाम]["files"]:
        ऑपरेटिंग_सिस्टम.remove(पथ)
    del एन्ट्री_सूची[नाम]
    लिखना_लॉग(सूची_पथ, json.dumps(एन्ट्री_सूची).encode())
    print("निकालें_एन्ट्री 완료:", नाम)


def चलाएँ(तर्क):
    पोर्ट_संख्या = 8027
    if len(तर्क) >= 2 and तर्क[-2] == "--port":
        पोर्ट_संख्या = int(तर्क[-1])
        तर्क = तर्क[:-2]
    if तर्क == ["list"]:
        for नाम, सिस्टम_जानकारी in पढें_सूची().items():
            print(नाम, सिस्टम_जानकारी["version"])
    elif len(तर्क) == 2 and तर्क[0] == "install":
        इंस्टॉल_करें_मान(तर्क[1], पोर्ट_संख्या)
    elif len(तर्क) == 2 and तर्क[0] == "uninstall":
        निकालें_एन्ट्री(तर्क[1])
    elif not तर्क or तर्क in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython स्रोत_ट्री 설치기 (PyPA pip 전체가 아님)")
        print("pip install नाम[==버전] [--port 8027] | pip list | pip uninstall नाम")
        print("आयोजक: उपकरण/निष्पादित_करें_आदेश.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        चलाएँ(sys.argv[1:])
    except Exception as त्रुटि:
        print("बंडल त्रुटि:", त्रुटि)
        sys.exit(1)
