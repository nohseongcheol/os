"""निज 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 होस्ट 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as सञ्चालनप्रणाली

सूची_बाटो = "/lib/.pip.json"


def 지문(लगत):
    return "".join("%02x" % मान for मान in hashlib.sha256(लगत).digest())


def 목록읽기():
    if सञ्चालनप्रणाली.path_kind(सूची_बाटो) == 0:
        return {}
    return json.loads(सञ्चालनप्रणाली.read(सूची_बाटो).decode("utf-8"))


def लेख्नुहोस्_लग(मार्ग, लगत):
    if सञ्चालनप्रणाली.write(मार्ग, लगत) != len(लगत):
        raise OSError(28)


def चेक_बाटो(मार्ग):
    if not isinstance(मार्ग, str) or not मार्ग.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in मार्ग.split("/")):
        raise ValueError("허용하지 않는 पोको मार्ग")
    if "\\" in मार्ग or any(ord(वर्ण_मान) < 32 or ord(वर्ण_मान) == 127 for वर्ण_मान in मार्ग):
        raise ValueError("잘못된 मार्ग 문자")
    मापन = "/lib/" + मार्ग
    if len(मापन.encode("utf-8")) > 63 or मार्ग in ("नेपाली.py", "पोको.py"):
        raise ValueError("पोको 경로가 너무 길거나 पूर्वनिर्धारित_मान 라이브러리와 겹칩니다.")
    return मापन


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.चलाउनुहोस् = सञ्चालनप्रणाली.ticks_ms()

    def 정확히읽기(자신, लम्बाइ_मान):
        लगत = bytearray()
        while len(लगत) < लम्बाइ_मान:
            if सञ्चालनप्रणाली.ticks_ms() - 자신.चलाउनुहोस् > 90000:
                raise ValueError("पोको 중계 जवाफ_दिनुहोस् 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = सञ्चालनप्रणाली.tcp_read(자신.종단, 512)
                except OSError as त्रुटि:
                    if त्रुटि.args[0] != 11:
                        raise
                    सञ्चालनप्रणाली.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("पोको 전송이 중간에 끝났습니다.")
            개수 = min(लम्बाइ_मान - len(लगत), len(자신.남은자료))
            लगत.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            सञ्चालनप्रणाली.sleep_ms(0)
        return bytes(लगत)


def डाउनलोड(요청, 접속번호):
    if len(요청) > 96 or any(वर्ण_मान not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for वर्ण_मान in 요청):
        raise ValueError("사용법: pip install नाम 또는 नाम==버전")
    종단 = सञ्चालनप्रणाली.tcp_open()
    try:
        चलाउनुहोस् = सञ्चालनप्रणाली.ticks_ms()
        while True:
            try:
                सञ्चालनप्रणाली.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as त्रुटि:
                if त्रुटि.args[0] not in (11, 115) or सञ्चालनप्रणाली.ticks_ms() - चलाउनुहोस् > 5000:
                    raise ValueError("पोको 중계 जडान विफल_मान: 호스트에서 --network --pip로 실행하십시오.")
                सञ्चालनप्रणाली.sleep_ms(10)
        लगत = (요청 + "\n").encode()
        while लगत:
            try:
                개수 = सञ्चालनप्रणाली.tcp_write(종단, लगत)
                if not 개수:
                    raise ValueError("पोको 요청 ट्रान्सफर_मान विफल_मान")
                लगत = लगत[개수:]
            except OSError as त्रुटि:
                if त्रुटि.args[0] != 11:
                    raise
                सञ्चालनप्रणाली.sleep_ms(10)
                if सञ्चालनप्रणाली.ticks_ms() - चलाउनुहोस् > 10000:
                    raise ValueError("पोको 요청 ट्रान्सफर_मान 시간 초과")
        प्रवाह_मान = 수신흐름(종단)
        머리 = प्रवाह_मान.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("पोको ट्रान्सफर_मान केस_मान 불일치")
        लम्बाइ_मान = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if लम्बाइ_मान > 8192:
            raise ValueError("पोको 명세가 너무 큽니다.")
        명세 = json.loads(प्रवाह_मान.정확히읽기(लम्बाइ_मान).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 स्रोत_वृक्ष 파일은 1~16개여야 합니다.")
        if sum(प्रविष्टि_मान["size"] for प्रविष्टि_मान in 명세["files"]) > 65536:
            raise ValueError("पोको स्रोत_वृक्ष 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for प्रविष्टि_मान in 명세["files"]:
            मार्ग = चेक_बाटो(प्रविष्टि_मान["path"])
            if मार्ग in 파일들 or not 0 <= प्रविष्टि_मान["size"] <= 16384:
                raise ValueError("중복 मार्ग 또는 फाइल आकार 초과")
            लगत = प्रवाह_मान.정확히읽기(प्रविष्टि_मान["size"])
            if 지문(लगत) != प्रविष्टि_मान["sha256"]:
                raise ValueError("पोको फाइल SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(लगत.decode("utf-8"), मार्ग, "exec")
            파일들[मार्ग] = लगत
            gc.collect()
        return 명세, 파일들
    finally:
        सञ्चालनप्रणाली.udp_close(종단)


def स्थापना_गर्नुहोस्_मान(요청, 접속번호):
    print("पोको डाउनलोड:", 요청)
    명세, 파일들 = डाउनलोड(요청, 접속번호)
    प्रविष्टि_सूची = 목록읽기()
    नाम = 명세["name"]
    if नाम in प्रविष्टि_सूची:
        if प्रविष्टि_सूची[नाम]["version"] == 명세["version"]:
            for मार्ग, 지문값 in प्रविष्टि_सूची[नाम]["files"].items():
                if सञ्चालनप्रणाली.path_kind(मार्ग) != 1 or 지문(सञ्चालनप्रणाली.read(मार्ग)) != 지문값:
                    raise ValueError("설치된 पोको 파일이 달라졌습니다: " + मार्ग)
            print("이미 설치됨:", नाम, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 पछाडि_मान 설치하십시오.")
    for मार्ग in 파일들:
        if सञ्चालनप्रणाली.path_kind(मार्ग):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + मार्ग)
    प्रविष्टि_सूची[नाम] = {"version": 명세["version"], "files": {मार्ग: 지문(लगत) for मार्ग, लगत in 파일들.items()}}
    새목록 = json.dumps(प्रविष्टि_सूची).encode()
    if len(새목록) > 16384:
        raise ValueError("पोको प्रविष्टि_सूची आकार 초과")
    이전목록 = सञ्चालनप्रणाली.read(सूची_बाटो) if सञ्चालनप्रणाली.path_kind(सूची_बाटो) else None
    만든파일 = []
    만든폴더 = []
    try:
        for मार्ग, लगत in 파일들.items():
            부분들 = मार्ग.split("/")
            for 수 in range(2, len(부분들)):
                डाइरेक्टरी_मान = "/".join(부분들[:수])
                종류 = सञ्चालनप्रणाली.path_kind(डाइरेक्टरी_मान)
                if 종류 == 0:
                    सञ्चालनप्रणाली.mkdir(डाइरेक्टरी_मान)
                    만든폴더.append(डाइरेक्टरी_मान)
                elif 종류 != 2:
                    raise ValueError("डाइरेक्टरी_मान 경로에 파일이 있습니다: " + डाइरेक्टरी_मान)
            만든파일.append(मार्ग)
            लेख्नुहोस्_लग(मार्ग, लगत)
        लेख्नुहोस्_लग(सूची_बाटो, 새목록)
    except Exception:
        for मार्ग in 만든파일:
            if सञ्चालनप्रणाली.path_kind(मार्ग):
                सञ्चालनप्रणाली.remove(मार्ग)
        for डाइरेक्टरी_मान in reversed(만든폴더):
            सञ्चालनप्रणाली.rmdir(डाइरेक्टरी_मान)
        if 이전목록 is not None:
            लेख्नुहोस्_लग(सूची_बाटो, 이전목록)
        elif सञ्चालनप्रणाली.path_kind(सूची_बाटो):
            सञ्चालनप्रणाली.remove(सूची_बाटो)
        raise
    print("स्थापना_गर्नुहोस्_मान 완료:", नाम, 명세["version"], "→ /lib (RAM)")


def हटाउनुहोस्_प्रविष्टि(नाम):
    प्रविष्टि_सूची = 목록읽기()
    if नाम not in प्रविष्टि_सूची:
        raise ValueError("설치되지 않은 꾸러미입니다: " + नाम)
    for मार्ग, 지문값 in प्रविष्टि_सूची[नाम]["files"].items():
        if सञ्चालनप्रणाली.path_kind(मार्ग) != 1 or 지문(सञ्चालनप्रणाली.read(मार्ग)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + मार्ग)
    for मार्ग in प्रविष्टि_सूची[नाम]["files"]:
        सञ्चालनप्रणाली.remove(मार्ग)
    del प्रविष्टि_सूची[नाम]
    लेख्नुहोस्_लग(सूची_बाटो, json.dumps(प्रविष्टि_सूची).encode())
    print("हटाउनुहोस्_प्रविष्टि 완료:", नाम)


def चलाउनुहोस्(तर्क):
    접속번호 = 8027
    if len(तर्क) >= 2 and तर्क[-2] == "--port":
        접속번호 = int(तर्क[-1])
        तर्क = तर्क[:-2]
    if तर्क == ["list"]:
        for नाम, प्रणाली_जानकारी in 목록읽기().items():
            print(नाम, प्रणाली_जानकारी["version"])
    elif len(तर्क) == 2 and तर्क[0] == "install":
        स्थापना_गर्नुहोस्_मान(तर्क[1], 접속번호)
    elif len(तर्क) == 2 and तर्क[0] == "uninstall":
        हटाउनुहोस्_प्रविष्टि(तर्क[1])
    elif not तर्क or तर्क in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython स्रोत_वृक्ष 설치기 (PyPA pip 전체가 아님)")
        print("pip install नाम[==버전] [--port 8027] | pip list | pip uninstall नाम")
        print("होस्ट: उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        चलाउनुहोस्(sys.argv[1:])
    except Exception as त्रुटि:
        print("पोको त्रुटि:", त्रुटि)
        sys.exit(1)
