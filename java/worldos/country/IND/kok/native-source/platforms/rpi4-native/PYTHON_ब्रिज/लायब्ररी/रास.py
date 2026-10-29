"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 येजमान 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ऑपरेटिंग_प्रणाली

सुची_पाथ = "/lib/.pip.json"


def 지문(डेटा):
    return "".join("%02x" % मोल for मोल in hashlib.sha256(डेटा).digest())


def 목록읽기():
    if ऑपरेटिंग_प्रणाली.path_kind(सुची_पाथ) == 0:
        return {}
    return json.loads(ऑपरेटिंग_प्रणाली.read(सुची_पाथ).decode("utf-8"))


def बरोवचें_LOG(पाथ, डेटा):
    if ऑपरेटिंग_प्रणाली.write(पाथ, डेटा) != len(डेटा):
        raise OSError(28)


def तपासचें_पाथ(पाथ):
    if not isinstance(पाथ, str) or not पाथ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in पाथ.split("/")):
        raise ValueError("허용하지 않는 रास पाथ")
    if "\\" in पाथ or any(ord(वर्ण_मोल) < 32 or ord(वर्ण_मोल) == 127 for वर्ण_मोल in पाथ):
        raise ValueError("잘못된 पाथ 문자")
    मेजप = "/lib/" + पाथ
    if len(मेजप.encode("utf-8")) > 63 or पाथ in ("한국어.py", "रास.py"):
        raise ValueError("रास 경로가 너무 길거나 डिफॉल्ट_मोल 라이브러리와 겹칩니다.")
    return मेजप


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.चलोवप = ऑपरेटिंग_प्रणाली.ticks_ms()

    def 정확히읽기(자신, लांबाय_मोल):
        डेटा = bytearray()
        while len(डेटा) < लांबाय_मोल:
            if ऑपरेटिंग_प्रणाली.ticks_ms() - 자신.चलोवप > 90000:
                raise ValueError("रास 중계 जाप_दिवप TIME_मोल 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ऑपरेटिंग_प्रणाली.tcp_read(자신.종단, 512)
                except OSError as चूक:
                    if चूक.args[0] != 11:
                        raise
                    ऑपरेटिंग_प्रणाली.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("रास 전송이 중간에 끝났습니다.")
            आयटम_COUNT = min(लांबाय_मोल - len(डेटा), len(자신.남은자료))
            डेटा.extend(자신.남은자료[:आयटम_COUNT])
            자신.남은자료 = 자신.남은자료[आयटम_COUNT:]
            ऑपरेटिंग_प्रणाली.sleep_ms(0)
        return bytes(डेटा)


def डावनलोड(요청, 접속번호):
    if len(요청) > 96 or any(वर्ण_मोल not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for वर्ण_मोल in 요청):
        raise ValueError("사용법: pip install नांव 또는 नांव==버전")
    종단 = ऑपरेटिंग_प्रणाली.tcp_open()
    try:
        चलोवप = ऑपरेटिंग_प्रणाली.ticks_ms()
        while True:
            try:
                ऑपरेटिंग_प्रणाली.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as चूक:
                if चूक.args[0] not in (11, 115) or ऑपरेटिंग_प्रणाली.ticks_ms() - चलोवप > 5000:
                    raise ValueError("रास 중계 कनॅक्ट अपेस_मोल: 호스트에서 --network --pip로 실행하십시오.")
                ऑपरेटिंग_प्रणाली.sleep_ms(10)
        डेटा = (요청 + "\n").encode()
        while डेटा:
            try:
                आयटम_COUNT = ऑपरेटिंग_प्रणाली.tcp_write(종단, डेटा)
                if not आयटम_COUNT:
                    raise ValueError("रास 요청 ट्रान्सफर_मोल अपेस_मोल")
                डेटा = डेटा[आयटम_COUNT:]
            except OSError as चूक:
                if चूक.args[0] != 11:
                    raise
                ऑपरेटिंग_प्रणाली.sleep_ms(10)
                if ऑपरेटिंग_प्रणाली.ticks_ms() - चलोवप > 10000:
                    raise ValueError("रास 요청 ट्रान्सफर_मोल TIME_मोल 초과")
        Stream_मोल = 수신흐름(종단)
        머리 = Stream_मोल.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("रास ट्रान्सफर_मोल काम_मोल 불일치")
        लांबाय_मोल = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if लांबाय_मोल > 8192:
            raise ValueError("रास 명세가 너무 큽니다.")
        명세 = json.loads(Stream_मोल.정확히읽기(लांबाय_मोल).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 स्त्रोत_ट्री 파일은 1~16개여야 합니다.")
        if sum(प्रवेश_मोल["size"] for प्रवेश_मोल in 명세["files"]) > 65536:
            raise ValueError("रास स्त्रोत_ट्री 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for प्रवेश_मोल in 명세["files"]:
            पाथ = तपासचें_पाथ(प्रवेश_मोल["path"])
            if पाथ in 파일들 or not 0 <= प्रवेश_मोल["size"] <= 16384:
                raise ValueError("중복 पाथ 또는 फायल आवाठ 초과")
            डेटा = Stream_मोल.정확히읽기(प्रवेश_मोल["size"])
            if 지문(डेटा) != प्रवेश_मोल["sha256"]:
                raise ValueError("रास फायल SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(डेटा.decode("utf-8"), पाथ, "exec")
            파일들[पाथ] = डेटा
            gc.collect()
        return 명세, 파일들
    finally:
        ऑपरेटिंग_प्रणाली.udp_close(종단)


def स्थापणूक_मोल(요청, 접속번호):
    print("रास डावनलोड:", 요청)
    명세, 파일들 = डावनलोड(요청, 접속번호)
    प्रवेश_सुची = 목록읽기()
    नांव = 명세["name"]
    if नांव in प्रवेश_सुची:
        if प्रवेश_सुची[नांव]["version"] == 명세["version"]:
            for पाथ, 지문값 in प्रवेश_सुची[नांव]["files"].items():
                if ऑपरेटिंग_प्रणाली.path_kind(पाथ) != 1 or 지문(ऑपरेटिंग_प्रणाली.read(पाथ)) != 지문값:
                    raise ValueError("설치된 रास 파일이 달라졌습니다: " + पाथ)
            print("이미 설치됨:", नांव, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 फाटीं_मोल 설치하십시오.")
    for पाथ in 파일들:
        if ऑपरेटिंग_प्रणाली.path_kind(पाथ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + पाथ)
    प्रवेश_सुची[नांव] = {"version": 명세["version"], "files": {पाथ: 지문(डेटा) for पाथ, डेटा in 파일들.items()}}
    새목록 = json.dumps(प्रवेश_सुची).encode()
    if len(새목록) > 16384:
        raise ValueError("रास प्रवेश_सुची आवाठ 초과")
    이전목록 = ऑपरेटिंग_प्रणाली.read(सुची_पाथ) if ऑपरेटिंग_प्रणाली.path_kind(सुची_पाथ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for पाथ, डेटा in 파일들.items():
            부분들 = पाथ.split("/")
            for 수 in range(2, len(부분들)):
                नामावळ_मोल = "/".join(부분들[:수])
                종류 = ऑपरेटिंग_प्रणाली.path_kind(नामावळ_मोल)
                if 종류 == 0:
                    ऑपरेटिंग_प्रणाली.mkdir(नामावळ_मोल)
                    만든폴더.append(नामावळ_मोल)
                elif 종류 != 2:
                    raise ValueError("नामावळ_मोल 경로에 파일이 있습니다: " + नामावळ_मोल)
            만든파일.append(पाथ)
            बरोवचें_LOG(पाथ, डेटा)
        बरोवचें_LOG(सुची_पाथ, 새목록)
    except Exception:
        for पाथ in 만든파일:
            if ऑपरेटिंग_प्रणाली.path_kind(पाथ):
                ऑपरेटिंग_प्रणाली.remove(पाथ)
        for नामावळ_मोल in reversed(만든폴더):
            ऑपरेटिंग_प्रणाली.rmdir(नामावळ_मोल)
        if 이전목록 is not None:
            बरोवचें_LOG(सुची_पाथ, 이전목록)
        elif ऑपरेटिंग_प्रणाली.path_kind(सुची_पाथ):
            ऑपरेटिंग_प्रणाली.remove(सुची_पाथ)
        raise
    print("स्थापणूक_मोल 완료:", नांव, 명세["version"], "→ /lib (RAM)")


def काडचें_प्रवेश(नांव):
    प्रवेश_सुची = 목록읽기()
    if नांव not in प्रवेश_सुची:
        raise ValueError("설치되지 않은 꾸러미입니다: " + नांव)
    for पाथ, 지문값 in प्रवेश_सुची[नांव]["files"].items():
        if ऑपरेटिंग_प्रणाली.path_kind(पाथ) != 1 or 지문(ऑपरेटिंग_प्रणाली.read(पाथ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + पाथ)
    for पाथ in प्रवेश_सुची[नांव]["files"]:
        ऑपरेटिंग_प्रणाली.remove(पाथ)
    del प्रवेश_सुची[नांव]
    बरोवचें_LOG(सुची_पाथ, json.dumps(प्रवेश_सुची).encode())
    print("काडचें_प्रवेश 완료:", नांव)


def चलोवप(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for नांव, msinfo32_exe in 목록읽기().items():
            print(नांव, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        स्थापणूक_मोल(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        काडचें_प्रवेश(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython स्त्रोत_ट्री 설치기 (PyPA pip 전체가 아님)")
        print("pip install नांव[==버전] [--port 8027] | pip list | pip uninstall नांव")
        print("येजमान: साधनां/पाळो_दिवचो_आदेश.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        चलोवप(sys.argv[1:])
    except Exception as चूक:
        print("रास चूक:", चूक)
        sys.exit(1)
