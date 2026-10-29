"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 হ_ষ্ট 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as অপাৰেটিং_ছিষ্টেম

সূচী_পথ = "/lib/.pip.json"


def 지문(ডাটা):
    return "".join("%02x" % মান for মান in hashlib.sha256(ডাটা).digest())


def 목록읽기():
    if অপাৰেটিং_ছিষ্টেম.path_kind(সূচী_পথ) == 0:
        return {}
    return json.loads(অপাৰেটিং_ছিষ্টেম.read(সূচী_পথ).decode("utf-8"))


def লিখক_লগ(পথ, ডাটা):
    if অপাৰেটিং_ছিষ্টেম.write(পথ, ডাটা) != len(ডাটা):
        raise OSError(28)


def পৰীক্ষণ_পথ(পথ):
    if not isinstance(পথ, str) or not পথ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in পথ.split("/")):
        raise ValueError("허용하지 않는 বাণ্ডল পথ")
    if "\\" in পথ or any(ord(বৰ্ণ_মান) < 32 or ord(বৰ্ণ_মান) == 127 for বৰ্ণ_মান in পথ):
        raise ValueError("잘못된 পথ 문자")
    পৰিমাপ = "/lib/" + পথ
    if len(পৰিমাপ.encode("utf-8")) > 63 or পথ in ("한국어.py", "বাণ্ডল.py"):
        raise ValueError("বাণ্ডল 경로가 너무 길거나 ডিফ_ল্ট_মান 라이브러리와 겹칩니다.")
    return পৰিমাপ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.সঞ্চালন = অপাৰেটিং_ছিষ্টেম.ticks_ms()

    def 정확히읽기(자신, দৈর্ঘ্য_মান):
        ডাটা = bytearray()
        while len(ডাটা) < দৈর্ঘ্য_মান:
            if অপাৰেটিং_ছিষ্টেম.ticks_ms() - 자신.সঞ্চালন > 90000:
                raise ValueError("বাণ্ডল 중계 প্ৰত্যুত্তৰ_দিয়ক 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = অপাৰেটিং_ছিষ্টেম.tcp_read(자신.종단, 512)
                except OSError as ত্ৰুটি:
                    if ত্ৰুটি.args[0] != 11:
                        raise
                    অপাৰেটিং_ছিষ্টেম.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("বাণ্ডল 전송이 중간에 끝났습니다.")
            개수 = min(দৈর্ঘ্য_মান - len(ডাটা), len(자신.남은자료))
            ডাটা.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            অপাৰেটিং_ছিষ্টেম.sleep_ms(0)
        return bytes(ডাটা)


def ডাউনলোড(요청, 접속번호):
    if len(요청) > 96 or any(বৰ্ণ_মান not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for বৰ্ণ_মান in 요청):
        raise ValueError("사용법: pip install নাম 또는 নাম==버전")
    종단 = অপাৰেটিং_ছিষ্টেম.tcp_open()
    try:
        সঞ্চালন = অপাৰেটিং_ছিষ্টেম.ticks_ms()
        while True:
            try:
                অপাৰেটিং_ছিষ্টেম.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as ত্ৰুটি:
                if ত্ৰুটি.args[0] not in (11, 115) or অপাৰেটিং_ছিষ্টেম.ticks_ms() - সঞ্চালন > 5000:
                    raise ValueError("বাণ্ডল 중계 সংযোগ_স্থাপনা বিফলতা_মান: 호스트에서 --network --pip로 실행하십시오.")
                অপাৰেটিং_ছিষ্টেম.sleep_ms(10)
        ডাটা = (요청 + "\n").encode()
        while ডাটা:
            try:
                개수 = অপাৰেটিং_ছিষ্টেম.tcp_write(종단, ডাটা)
                if not 개수:
                    raise ValueError("বাণ্ডল 요청 স্থানান্তৰণ_মান বিফলতা_মান")
                ডাটা = ডাটা[개수:]
            except OSError as ত্ৰুটি:
                if ত্ৰুটি.args[0] != 11:
                    raise
                অপাৰেটিং_ছিষ্টেম.sleep_ms(10)
                if অপাৰেটিং_ছিষ্টেম.ticks_ms() - সঞ্চালন > 10000:
                    raise ValueError("বাণ্ডল 요청 স্থানান্তৰণ_মান 시간 초과")
        ষ্ট্ৰিম_মান = 수신흐름(종단)
        머리 = ষ্ট্ৰিম_মান.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("বাণ্ডল স্থানান্তৰণ_মান কেছ_মান 불일치")
        দৈর্ঘ্য_মান = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if দৈর্ঘ্য_মান > 8192:
            raise ValueError("বাণ্ডল 명세가 너무 큽니다.")
        명세 = json.loads(ষ্ট্ৰিম_মান.정확히읽기(দৈর্ঘ্য_মান).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 উৎস_ট্ৰি 파일은 1~16개여야 합니다.")
        if sum(প্রবিষ্ট_মান["size"] for প্রবিষ্ট_মান in 명세["files"]) > 65536:
            raise ValueError("বাণ্ডল উৎস_ট্ৰি 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for প্রবিষ্ট_মান in 명세["files"]:
            পথ = পৰীক্ষণ_পথ(প্রবিষ্ট_মান["path"])
            if পথ in 파일들 or not 0 <= প্রবিষ্ট_মান["size"] <= 16384:
                raise ValueError("중복 পথ 또는 নথিপত্ৰ মাপ 초과")
            ডাটা = ষ্ট্ৰিম_মান.정확히읽기(প্রবিষ্ট_মান["size"])
            if 지문(ডাটা) != প্রবিষ্ট_মান["sha256"]:
                raise ValueError("বাণ্ডল নথিপত্ৰ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ডাটা.decode("utf-8"), পথ, "exec")
            파일들[পথ] = ডাটা
            gc.collect()
        return 명세, 파일들
    finally:
        অপাৰেটিং_ছিষ্টেম.udp_close(종단)


def ইনষ্টল_কৰক_মান(요청, 접속번호):
    print("বাণ্ডল ডাউনলোড:", 요청)
    명세, 파일들 = ডাউনলোড(요청, 접속번호)
    প্রবিষ্ট_সূচী = 목록읽기()
    নাম = 명세["name"]
    if নাম in প্রবিষ্ট_সূচী:
        if প্রবিষ্ট_সূচী[নাম]["version"] == 명세["version"]:
            for পথ, 지문값 in প্রবিষ্ট_সূচী[নাম]["files"].items():
                if অপাৰেটিং_ছিষ্টেম.path_kind(পথ) != 1 or 지문(অপাৰেটিং_ছিষ্টেম.read(পথ)) != 지문값:
                    raise ValueError("설치된 বাণ্ডল 파일이 달라졌습니다: " + পথ)
            print("이미 설치됨:", নাম, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 পাছলৈ_মান 설치하십시오.")
    for পথ in 파일들:
        if অপাৰেটিং_ছিষ্টেম.path_kind(পথ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + পথ)
    প্রবিষ্ট_সূচী[নাম] = {"version": 명세["version"], "files": {পথ: 지문(ডাটা) for পথ, ডাটা in 파일들.items()}}
    새목록 = json.dumps(প্রবিষ্ট_সূচী).encode()
    if len(새목록) > 16384:
        raise ValueError("বাণ্ডল প্রবিষ্ট_সূচী মাপ 초과")
    이전목록 = অপাৰেটিং_ছিষ্টেম.read(সূচী_পথ) if অপাৰেটিং_ছিষ্টেম.path_kind(সূচী_পথ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for পথ, ডাটা in 파일들.items():
            부분들 = পথ.split("/")
            for 수 in range(2, len(부분들)):
                ডাইৰেক্টৰী_মান = "/".join(부분들[:수])
                종류 = অপাৰেটিং_ছিষ্টেম.path_kind(ডাইৰেক্টৰী_মান)
                if 종류 == 0:
                    অপাৰেটিং_ছিষ্টেম.mkdir(ডাইৰেক্টৰী_মান)
                    만든폴더.append(ডাইৰেক্টৰী_মান)
                elif 종류 != 2:
                    raise ValueError("ডাইৰেক্টৰী_মান 경로에 파일이 있습니다: " + ডাইৰেক্টৰী_মান)
            만든파일.append(পথ)
            লিখক_লগ(পথ, ডাটা)
        লিখক_লগ(সূচী_পথ, 새목록)
    except Exception:
        for পথ in 만든파일:
            if অপাৰেটিং_ছিষ্টেম.path_kind(পথ):
                অপাৰেটিং_ছিষ্টেম.remove(পথ)
        for ডাইৰেক্টৰী_মান in reversed(만든폴더):
            অপাৰেটিং_ছিষ্টেম.rmdir(ডাইৰেক্টৰী_মান)
        if 이전목록 is not None:
            লিখক_লগ(সূচী_পথ, 이전목록)
        elif অপাৰেটিং_ছিষ্টেম.path_kind(সূচী_পথ):
            অপাৰেটিং_ছিষ্টেম.remove(সূচী_পথ)
        raise
    print("ইনষ্টল_কৰক_মান 완료:", নাম, 명세["version"], "→ /lib (RAM)")


def আঁতৰাওক_প্রবিষ্ট(নাম):
    প্রবিষ্ট_সূচী = 목록읽기()
    if নাম not in প্রবিষ্ট_সূচী:
        raise ValueError("설치되지 않은 꾸러미입니다: " + নাম)
    for পথ, 지문값 in প্রবিষ্ট_সূচী[নাম]["files"].items():
        if অপাৰেটিং_ছিষ্টেম.path_kind(পথ) != 1 or 지문(অপাৰেটিং_ছিষ্টেম.read(পথ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + পথ)
    for পথ in প্রবিষ্ট_সূচী[নাম]["files"]:
        অপাৰেটিং_ছিষ্টেম.remove(পথ)
    del প্রবিষ্ট_সূচী[নাম]
    লিখক_লগ(সূচী_পথ, json.dumps(প্রবিষ্ট_সূচী).encode())
    print("আঁতৰাওক_প্রবিষ্ট 완료:", নাম)


def সঞ্চালন(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for নাম, ছিষ্টেম_তথ্য in 목록읽기().items():
            print(নাম, ছিষ্টেম_তথ্য["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ইনষ্টল_কৰক_মান(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        আঁতৰাওক_প্রবিষ্ট(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython উৎস_ট্ৰি 설치기 (PyPA pip 전체가 아님)")
        print("pip install নাম[==버전] [--port 8027] | pip list | pip uninstall নাম")
        print("হ_ষ্ট: সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        সঞ্চালন(sys.argv[1:])
    except Exception as ত্ৰুটি:
        print("বাণ্ডল ত্ৰুটি:", ত্ৰুটি)
        sys.exit(1)
