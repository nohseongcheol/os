"""اپنا 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 میزبان 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as آپریٹنگ_سسٹم

فہرست_راہ = "/lib/.pip.json"


def 지문(کوائف):
    return "".join("%02x" % قدر for قدر in hashlib.sha256(کوائف).digest())


def 목록읽기():
    if آپریٹنگ_سسٹم.path_kind(فہرست_راہ) == 0:
        return {}
    return json.loads(آپریٹنگ_سسٹم.read(فہرست_راہ).decode("utf-8"))


def لکھیں_لاگ(راستہ_2, کوائف):
    if آپریٹنگ_سسٹم.write(راستہ_2, کوائف) != len(کوائف):
        raise OSError(28)


def پڑتال_کریں_راہ(راستہ_2):
    if not isinstance(راستہ_2, str) or not راستہ_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in راستہ_2.split("/")):
        raise ValueError("허용하지 않는 بنڈل راستہ_2")
    if "\\" in راستہ_2 or any(ord(کریکٹر_قدر) < 32 or ord(کریکٹر_قدر) == 127 for کریکٹر_قدر in راستہ_2):
        raise ValueError("잘못된 راستہ_2 문자")
    پیمائش = "/lib/" + راستہ_2
    if len(پیمائش.encode("utf-8")) > 63 or راستہ_2 in ("اردو.py", "بنڈل.py"):
        raise ValueError("بنڈل 경로가 너무 길거나 طے_شدہ_قدر 라이브러리와 겹칩니다.")
    return پیمائش


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.چلائیں = آپریٹنگ_سسٹم.ticks_ms()

    def 정확히읽기(자신, لمبا_ئی_قدر):
        کوائف = bytearray()
        while len(کوائف) < لمبا_ئی_قدر:
            if آپریٹنگ_سسٹم.ticks_ms() - 자신.چلائیں > 90000:
                raise ValueError("بنڈل 중계 جواب_دیں وقت_قدر 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = آپریٹنگ_سسٹم.tcp_read(자신.종단, 512)
                except OSError as غلطی:
                    if غلطی.args[0] != 11:
                        raise
                    آپریٹنگ_سسٹم.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("بنڈل 전송이 중간에 끝났습니다.")
            개수 = min(لمبا_ئی_قدر - len(کوائف), len(자신.남은자료))
            کوائف.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            آپریٹنگ_سسٹم.sleep_ms(0)
        return bytes(کوائف)


def ڈاؤن_لوڈ(요청, دہانہ_نمبر):
    if len(요청) > 96 or any(کریکٹر_قدر not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for کریکٹر_قدر in 요청):
        raise ValueError("사용법: pip install نام 또는 نام==버전")
    종단 = آپریٹنگ_سسٹم.tcp_open()
    try:
        چلائیں = آپریٹنگ_سسٹم.ticks_ms()
        while True:
            try:
                آپریٹنگ_سسٹم.tcp_connect(종단, "10.0.2.2", دہانہ_نمبر)
                break
            except OSError as غلطی:
                if غلطی.args[0] not in (11, 115) or آپریٹنگ_سسٹم.ticks_ms() - چلائیں > 5000:
                    raise ValueError("بنڈل 중계 متصل_ہوں ناکامی_قدر: 호스트에서 --network --pip로 실행하십시오.")
                آپریٹنگ_سسٹم.sleep_ms(10)
        کوائف = (요청 + "\n").encode()
        while کوائف:
            try:
                개수 = آپریٹنگ_سسٹم.tcp_write(종단, کوائف)
                if not 개수:
                    raise ValueError("بنڈل 요청 منتقلی_قدر ناکامی_قدر")
                کوائف = کوائف[개수:]
            except OSError as غلطی:
                if غلطی.args[0] != 11:
                    raise
                آپریٹنگ_سسٹم.sleep_ms(10)
                if آپریٹنگ_سسٹم.ticks_ms() - چلائیں > 10000:
                    raise ValueError("بنڈل 요청 منتقلی_قدر وقت_قدر 초과")
        بہاؤ_قدر = 수신흐름(종단)
        머리 = بہاؤ_قدر.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("بنڈل منتقلی_قدر جاب_قدر 불일치")
        لمبا_ئی_قدر = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if لمبا_ئی_قدر > 8192:
            raise ValueError("بنڈل 명세가 너무 큽니다.")
        명세 = json.loads(بہاؤ_قدر.정확히읽기(لمبا_ئی_قدر).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ماخذ_شجر 파일은 1~16개여야 합니다.")
        if sum(اندراج_قدر["size"] for اندراج_قدر in 명세["files"]) > 65536:
            raise ValueError("بنڈل ماخذ_شجر 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for اندراج_قدر in 명세["files"]:
            راستہ_2 = پڑتال_کریں_راہ(اندراج_قدر["path"])
            if راستہ_2 in 파일들 or not 0 <= اندراج_قدر["size"] <= 16384:
                raise ValueError("중복 راستہ_2 또는 فائل_کا_نام حجم 초과")
            کوائف = بہاؤ_قدر.정확히읽기(اندراج_قدر["size"])
            if 지문(کوائف) != اندراج_قدر["sha256"]:
                raise ValueError("بنڈل فائل_کا_نام SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(کوائف.decode("utf-8"), راستہ_2, "exec")
            파일들[راستہ_2] = کوائف
            gc.collect()
        return 명세, 파일들
    finally:
        آپریٹنگ_سسٹم.udp_close(종단)


def نصب_کریں_قدر(요청, دہانہ_نمبر):
    print("بنڈل ڈاؤن_لوڈ:", 요청)
    명세, 파일들 = ڈاؤن_لوڈ(요청, دہانہ_نمبر)
    اندراج_فہرست = 목록읽기()
    نام = 명세["name"]
    if نام in اندراج_فہرست:
        if اندراج_فہرست[نام]["version"] == 명세["version"]:
            for راستہ_2, 지문값 in اندراج_فہرست[نام]["files"].items():
                if آپریٹنگ_سسٹم.path_kind(راستہ_2) != 1 or 지문(آپریٹنگ_سسٹم.read(راستہ_2)) != 지문값:
                    raise ValueError("설치된 بنڈل 파일이 달라졌습니다: " + راستہ_2)
            print("이미 설치됨:", نام, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 واپس_قدر 설치하십시오.")
    for راستہ_2 in 파일들:
        if آپریٹنگ_سسٹم.path_kind(راستہ_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + راستہ_2)
    اندراج_فہرست[نام] = {"version": 명세["version"], "files": {راستہ_2: 지문(کوائف) for راستہ_2, کوائف in 파일들.items()}}
    새목록 = json.dumps(اندراج_فہرست).encode()
    if len(새목록) > 16384:
        raise ValueError("بنڈل اندراج_فہرست حجم 초과")
    이전목록 = آپریٹنگ_سسٹم.read(فہرست_راہ) if آپریٹنگ_سسٹم.path_kind(فہرست_راہ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for راستہ_2, کوائف in 파일들.items():
            부분들 = راستہ_2.split("/")
            for 수 in range(2, len(부분들)):
                ڈائریکٹری_قدر = "/".join(부분들[:수])
                종류 = آپریٹنگ_سسٹم.path_kind(ڈائریکٹری_قدر)
                if 종류 == 0:
                    آپریٹنگ_سسٹم.mkdir(ڈائریکٹری_قدر)
                    만든폴더.append(ڈائریکٹری_قدر)
                elif 종류 != 2:
                    raise ValueError("ڈائریکٹری_قدر 경로에 파일이 있습니다: " + ڈائریکٹری_قدر)
            만든파일.append(راستہ_2)
            لکھیں_لاگ(راستہ_2, کوائف)
        لکھیں_لاگ(فہرست_راہ, 새목록)
    except Exception:
        for راستہ_2 in 만든파일:
            if آپریٹنگ_سسٹم.path_kind(راستہ_2):
                آپریٹنگ_سسٹم.remove(راستہ_2)
        for ڈائریکٹری_قدر in reversed(만든폴더):
            آپریٹنگ_سسٹم.rmdir(ڈائریکٹری_قدر)
        if 이전목록 is not None:
            لکھیں_لاگ(فہرست_راہ, 이전목록)
        elif آپریٹنگ_سسٹم.path_kind(فہرست_راہ):
            آپریٹنگ_سسٹم.remove(فہرست_راہ)
        raise
    print("نصب_کریں_قدر 완료:", نام, 명세["version"], "→ /lib (RAM)")


def ہٹائیں_اندراج(نام):
    اندراج_فہرست = 목록읽기()
    if نام not in اندراج_فہرست:
        raise ValueError("설치되지 않은 꾸러미입니다: " + نام)
    for راستہ_2, 지문값 in اندراج_فہرست[نام]["files"].items():
        if آپریٹنگ_سسٹم.path_kind(راستہ_2) != 1 or 지문(آپریٹنگ_سسٹم.read(راستہ_2)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + راستہ_2)
    for راستہ_2 in اندراج_فہرست[نام]["files"]:
        آپریٹنگ_سسٹم.remove(راستہ_2)
    del اندراج_فہرست[نام]
    لکھیں_لاگ(فہرست_راہ, json.dumps(اندراج_فہرست).encode())
    print("ہٹائیں_اندراج 완료:", نام)


def چلائیں(دلائل):
    دہانہ_نمبر = 8027
    if len(دلائل) >= 2 and دلائل[-2] == "--port":
        دہانہ_نمبر = int(دلائل[-1])
        دلائل = دلائل[:-2]
    if دلائل == ["list"]:
        for نام, نظام_کی_معلومات in 목록읽기().items():
            print(نام, نظام_کی_معلومات["version"])
    elif len(دلائل) == 2 and دلائل[0] == "install":
        نصب_کریں_قدر(دلائل[1], دہانہ_نمبر)
    elif len(دلائل) == 2 and دلائل[0] == "uninstall":
        ہٹائیں_اندراج(دلائل[1])
    elif not دلائل or دلائل in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ماخذ_شجر 설치기 (PyPA pip 전체가 아님)")
        print("pip install نام[==버전] [--port 8027] | pip list | pip uninstall نام")
        print("میزبان: ٹولز/نفاذ_کریں_حکم.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        چلائیں(sys.argv[1:])
    except Exception as غلطی:
        print("بنڈل غلطی:", غلطی)
        sys.exit(1)
