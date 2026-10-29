"""নিজ 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 হোস্ট 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as অপারেটিং_সিস্টেম

তালিকা_পথ = "/lib/.pip.json"


def 지문(ডাটা):
    return "".join("%02x" % মান for মান in hashlib.sha256(ডাটা).digest())


def 목록읽기():
    if অপারেটিং_সিস্টেম.path_kind(তালিকা_পথ) == 0:
        return {}
    return json.loads(অপারেটিং_সিস্টেম.read(তালিকা_পথ).decode("utf-8"))


def লেখা_লগ(পথ_2, ডাটা):
    if অপারেটিং_সিস্টেম.write(পথ_2, ডাটা) != len(ডাটা):
        raise OSError(28)


def চেক_পথ(পথ_2):
    if not isinstance(পথ_2, str) or not পথ_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in পথ_2.split("/")):
        raise ValueError("허용하지 않는 পাঁজা পথ_2")
    if "\\" in পথ_2 or any(ord(অক্ষর_মান) < 32 or ord(অক্ষর_মান) == 127 for অক্ষর_মান in পথ_2):
        raise ValueError("잘못된 পথ_2 문자")
    পরিমাপ = "/lib/" + পথ_2
    if len(পরিমাপ.encode("utf-8")) > 63 or পথ_2 in ("বাংলা.py", "পাঁজা.py"):
        raise ValueError("পাঁজা 경로가 너무 길거나 অমনোনীত_মান 라이브러리와 겹칩니다.")
    return পরিমাপ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.চালনা = অপারেটিং_সিস্টেম.ticks_ms()

    def 정확히읽기(자신, দৈর্ঘ্য_মান):
        ডাটা = bytearray()
        while len(ডাটা) < দৈর্ঘ্য_মান:
            if অপারেটিং_সিস্টেম.ticks_ms() - 자신.চালনা > 90000:
                raise ValueError("পাঁজা 중계 উত্তর_দিন সময়_মান 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = অপারেটিং_সিস্টেম.tcp_read(자신.종단, 512)
                except OSError as ত্রুটি:
                    if ত্রুটি.args[0] != 11:
                        raise
                    অপারেটিং_সিস্টেম.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("পাঁজা 전송이 중간에 끝났습니다.")
            개수 = min(দৈর্ঘ্য_মান - len(ডাটা), len(자신.남은자료))
            ডাটা.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            অপারেটিং_সিস্টেম.sleep_ms(0)
        return bytes(ডাটা)


def ডাউনলোড(요청, পোর্ট_নম্বর):
    if len(요청) > 96 or any(অক্ষর_মান not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for অক্ষর_মান in 요청):
        raise ValueError("사용법: pip install নাম 또는 নাম==버전")
    종단 = অপারেটিং_সিস্টেম.tcp_open()
    try:
        চালনা = অপারেটিং_সিস্টেম.ticks_ms()
        while True:
            try:
                অপারেটিং_সিস্টেম.tcp_connect(종단, "10.0.2.2", পোর্ট_নম্বর)
                break
            except OSError as ত্রুটি:
                if ত্রুটি.args[0] not in (11, 115) or অপারেটিং_সিস্টেম.ticks_ms() - চালনা > 5000:
                    raise ValueError("পাঁজা 중계 সংযোগ_স্থাপনা বিফলতা_মান: 호스트에서 --network --pip로 실행하십시오.")
                অপারেটিং_সিস্টেম.sleep_ms(10)
        ডাটা = (요청 + "\n").encode()
        while ডাটা:
            try:
                개수 = অপারেটিং_সিস্টেম.tcp_write(종단, ডাটা)
                if not 개수:
                    raise ValueError("পাঁজা 요청 স্থানান্তর_মান বিফলতা_মান")
                ডাটা = ডাটা[개수:]
            except OSError as ত্রুটি:
                if ত্রুটি.args[0] != 11:
                    raise
                অপারেটিং_সিস্টেম.sleep_ms(10)
                if অপারেটিং_সিস্টেম.ticks_ms() - চালনা > 10000:
                    raise ValueError("পাঁজা 요청 স্থানান্তর_মান সময়_মান 초과")
        প্রবাহ_মান = 수신흐름(종단)
        머리 = প্রবাহ_মান.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("পাঁজা স্থানান্তর_মান কাজ_মান 불일치")
        দৈর্ঘ্য_মান = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if দৈর্ঘ্য_মান > 8192:
            raise ValueError("পাঁজা 명세가 너무 큽니다.")
        명세 = json.loads(প্রবাহ_মান.정확히읽기(দৈর্ঘ্য_মান).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 উত্স_ট্রী 파일은 1~16개여야 합니다.")
        if sum(ভুক্তি_মান["size"] for ভুক্তি_মান in 명세["files"]) > 65536:
            raise ValueError("পাঁজা উত্স_ট্রী 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ভুক্তি_মান in 명세["files"]:
            পথ_2 = চেক_পথ(ভুক্তি_মান["path"])
            if পথ_2 in 파일들 or not 0 <= ভুক্তি_মান["size"] <= 16384:
                raise ValueError("중복 পথ_2 또는 নথির_নাম আকার 초과")
            ডাটা = প্রবাহ_মান.정확히읽기(ভুক্তি_মান["size"])
            if 지문(ডাটা) != ভুক্তি_মান["sha256"]:
                raise ValueError("পাঁজা নথির_নাম SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ডাটা.decode("utf-8"), পথ_2, "exec")
            파일들[পথ_2] = ডাটা
            gc.collect()
        return 명세, 파일들
    finally:
        অপারেটিং_সিস্টেম.udp_close(종단)


def ইনস্টল_করুন_মান(요청, পোর্ট_নম্বর):
    print("পাঁজা ডাউনলোড:", 요청)
    명세, 파일들 = ডাউনলোড(요청, পোর্ট_নম্বর)
    ভুক্তি_তালিকা = 목록읽기()
    নাম = 명세["name"]
    if নাম in ভুক্তি_তালিকা:
        if ভুক্তি_তালিকা[নাম]["version"] == 명세["version"]:
            for পথ_2, 지문값 in ভুক্তি_তালিকা[নাম]["files"].items():
                if অপারেটিং_সিস্টেম.path_kind(পথ_2) != 1 or 지문(অপারেটিং_সিস্টেম.read(পথ_2)) != 지문값:
                    raise ValueError("설치된 পাঁজা 파일이 달라졌습니다: " + পথ_2)
            print("이미 설치됨:", নাম, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ফিরে_যান_মান 설치하십시오.")
    for পথ_2 in 파일들:
        if অপারেটিং_সিস্টেম.path_kind(পথ_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + পথ_2)
    ভুক্তি_তালিকা[নাম] = {"version": 명세["version"], "files": {পথ_2: 지문(ডাটা) for পথ_2, ডাটা in 파일들.items()}}
    새목록 = json.dumps(ভুক্তি_তালিকা).encode()
    if len(새목록) > 16384:
        raise ValueError("পাঁজা ভুক্তি_তালিকা আকার 초과")
    이전목록 = অপারেটিং_সিস্টেম.read(তালিকা_পথ) if অপারেটিং_সিস্টেম.path_kind(তালিকা_পথ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for পথ_2, ডাটা in 파일들.items():
            부분들 = পথ_2.split("/")
            for 수 in range(2, len(부분들)):
                ডিরেক্টরি_মান = "/".join(부분들[:수])
                종류 = অপারেটিং_সিস্টেম.path_kind(ডিরেক্টরি_মান)
                if 종류 == 0:
                    অপারেটিং_সিস্টেম.mkdir(ডিরেক্টরি_মান)
                    만든폴더.append(ডিরেক্টরি_মান)
                elif 종류 != 2:
                    raise ValueError("ডিরেক্টরি_মান 경로에 파일이 있습니다: " + ডিরেক্টরি_মান)
            만든파일.append(পথ_2)
            লেখা_লগ(পথ_2, ডাটা)
        লেখা_লগ(তালিকা_পথ, 새목록)
    except Exception:
        for পথ_2 in 만든파일:
            if অপারেটিং_সিস্টেম.path_kind(পথ_2):
                অপারেটিং_সিস্টেম.remove(পথ_2)
        for ডিরেক্টরি_মান in reversed(만든폴더):
            অপারেটিং_সিস্টেম.rmdir(ডিরেক্টরি_মান)
        if 이전목록 is not None:
            লেখা_লগ(তালিকা_পথ, 이전목록)
        elif অপারেটিং_সিস্টেম.path_kind(তালিকা_পথ):
            অপারেটিং_সিস্টেম.remove(তালিকা_পথ)
        raise
    print("ইনস্টল_করুন_মান 완료:", নাম, 명세["version"], "→ /lib (RAM)")


def সরানো_ভুক্তি(নাম):
    ভুক্তি_তালিকা = 목록읽기()
    if নাম not in ভুক্তি_তালিকা:
        raise ValueError("설치되지 않은 꾸러미입니다: " + নাম)
    for পথ_2, 지문값 in ভুক্তি_তালিকা[নাম]["files"].items():
        if অপারেটিং_সিস্টেম.path_kind(পথ_2) != 1 or 지문(অপারেটিং_সিস্টেম.read(পথ_2)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + পথ_2)
    for পথ_2 in ভুক্তি_তালিকা[নাম]["files"]:
        অপারেটিং_সিস্টেম.remove(পথ_2)
    del ভুক্তি_তালিকা[নাম]
    লেখা_লগ(তালিকা_পথ, json.dumps(ভুক্তি_তালিকা).encode())
    print("সরানো_ভুক্তি 완료:", নাম)


def চালনা(আর্গুমেন্ট_তালিকা):
    পোর্ট_নম্বর = 8027
    if len(আর্গুমেন্ট_তালিকা) >= 2 and আর্গুমেন্ট_তালিকা[-2] == "--port":
        পোর্ট_নম্বর = int(আর্গুমেন্ট_তালিকা[-1])
        আর্গুমেন্ট_তালিকা = আর্গুমেন্ট_তালিকা[:-2]
    if আর্গুমেন্ট_তালিকা == ["list"]:
        for নাম, সিসটেম_তথ্য in 목록읽기().items():
            print(নাম, সিসটেম_তথ্য["version"])
    elif len(আর্গুমেন্ট_তালিকা) == 2 and আর্গুমেন্ট_তালিকা[0] == "install":
        ইনস্টল_করুন_মান(আর্গুমেন্ট_তালিকা[1], পোর্ট_নম্বর)
    elif len(আর্গুমেন্ট_তালিকা) == 2 and আর্গুমেন্ট_তালিকা[0] == "uninstall":
        সরানো_ভুক্তি(আর্গুমেন্ট_তালিকা[1])
    elif not আর্গুমেন্ট_তালিকা or আর্গুমেন্ট_তালিকা in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython উত্স_ট্রী 설치기 (PyPA pip 전체가 아님)")
        print("pip install নাম[==버전] [--port 8027] | pip list | pip uninstall নাম")
        print("হোস্ট: সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        চালনা(sys.argv[1:])
    except Exception as ত্রুটি:
        print("পাঁজা ত্রুটি:", ত্রুটি)
        sys.exit(1)
