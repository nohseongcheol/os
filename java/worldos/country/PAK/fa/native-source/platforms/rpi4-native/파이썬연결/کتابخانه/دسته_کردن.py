"""بومی 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 میزبان 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as سیستم_عامل

لیست_مسیر = "/lib/.pip.json"


def 지문(داده_ها):
    return "".join("%02x" % مقدار for مقدار in hashlib.sha256(داده_ها).digest())


def 목록읽기():
    if سیستم_عامل.path_kind(لیست_مسیر) == 0:
        return {}
    return json.loads(سیستم_عامل.read(لیست_مسیر).decode("utf-8"))


def نوشتن_واقعه_نگار(مسیر, داده_ها):
    if سیستم_عامل.write(مسیر, داده_ها) != len(داده_ها):
        raise OSError(28)


def بررسی_مسیر(مسیر):
    if not isinstance(مسیر, str) or not مسیر.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in مسیر.split("/")):
        raise ValueError("허용하지 않는 دسته_کردن مسیر")
    if "\\" in مسیر or any(ord(نویسه_مقدار) < 32 or ord(نویسه_مقدار) == 127 for نویسه_مقدار in مسیر):
        raise ValueError("잘못된 مسیر 문자")
    سنجش = "/lib/" + مسیر
    if len(سنجش.encode("utf-8")) > 63 or مسیر in ("فارسی.py", "دسته_کردن.py"):
        raise ValueError("دسته_کردن 경로가 너무 길거나 مقدار_پیش_فرض 라이브러리와 겹칩니다.")
    return سنجش


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.اجرا_2 = سیستم_عامل.ticks_ms()

    def 정확히읽기(자신, طول_مقدار):
        داده_ها = bytearray()
        while len(داده_ها) < طول_مقدار:
            if سیستم_عامل.ticks_ms() - 자신.اجرا_2 > 90000:
                raise ValueError("دسته_کردن 중계 پاسخ_دادن زمان_مقدار 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = سیستم_عامل.tcp_read(자신.종단, 512)
                except OSError as خطا:
                    if خطا.args[0] != 11:
                        raise
                    سیستم_عامل.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("دسته_کردن 전송이 중간에 끝났습니다.")
            개수 = min(طول_مقدار - len(داده_ها), len(자신.남은자료))
            داده_ها.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            سیستم_عامل.sleep_ms(0)
        return bytes(داده_ها)


def دانلود(요청, شماره_درگاه):
    if len(요청) > 96 or any(نویسه_مقدار not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for نویسه_مقدار in 요청):
        raise ValueError("사용법: pip install نام 또는 نام==버전")
    종단 = سیستم_عامل.tcp_open()
    try:
        اجرا_2 = سیستم_عامل.ticks_ms()
        while True:
            try:
                سیستم_عامل.tcp_connect(종단, "10.0.2.2", شماره_درگاه)
                break
            except OSError as خطا:
                if خطا.args[0] not in (11, 115) or سیستم_عامل.ticks_ms() - اجرا_2 > 5000:
                    raise ValueError("دسته_کردن 중계 اتصال عدم_موفقیت_مقدار: 호스트에서 --network --pip로 실행하십시오.")
                سیستم_عامل.sleep_ms(10)
        داده_ها = (요청 + "\n").encode()
        while داده_ها:
            try:
                개수 = سیستم_عامل.tcp_write(종단, داده_ها)
                if not 개수:
                    raise ValueError("دسته_کردن 요청 انتقال_مقدار_630ba093 عدم_موفقیت_مقدار")
                داده_ها = داده_ها[개수:]
            except OSError as خطا:
                if خطا.args[0] != 11:
                    raise
                سیستم_عامل.sleep_ms(10)
                if سیستم_عامل.ticks_ms() - اجرا_2 > 10000:
                    raise ValueError("دسته_کردن 요청 انتقال_مقدار_630ba093 زمان_مقدار 초과")
        جریان_مقدار = 수신흐름(종단)
        머리 = جریان_مقدار.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("دسته_کردن انتقال_مقدار_630ba093 شغل_مقدار 불일치")
        طول_مقدار = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if طول_مقدار > 8192:
            raise ValueError("دسته_کردن 명세가 너무 큽니다.")
        명세 = json.loads(جریان_مقدار.정확히읽기(طول_مقدار).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 منبع_درخت 파일은 1~16개여야 합니다.")
        if sum(ورودی_مقدار["size"] for ورودی_مقدار in 명세["files"]) > 65536:
            raise ValueError("دسته_کردن منبع_درخت 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ورودی_مقدار in 명세["files"]:
            مسیر = بررسی_مسیر(ورودی_مقدار["path"])
            if مسیر in 파일들 or not 0 <= ورودی_مقدار["size"] <= 16384:
                raise ValueError("중복 مسیر 또는 پرونده اندازه 초과")
            داده_ها = جریان_مقدار.정확히읽기(ورودی_مقدار["size"])
            if 지문(داده_ها) != ورودی_مقدار["sha256"]:
                raise ValueError("دسته_کردن پرونده SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(داده_ها.decode("utf-8"), مسیر, "exec")
            파일들[مسیر] = داده_ها
            gc.collect()
        return 명세, 파일들
    finally:
        سیستم_عامل.udp_close(종단)


def نصب_مقدار(요청, شماره_درگاه):
    print("دسته_کردن دانلود:", 요청)
    명세, 파일들 = دانلود(요청, شماره_درگاه)
    ورودی_لیست = 목록읽기()
    نام = 명세["name"]
    if نام in ورودی_لیست:
        if ورودی_لیست[نام]["version"] == 명세["version"]:
            for مسیر, 지문값 in ورودی_لیست[نام]["files"].items():
                if سیستم_عامل.path_kind(مسیر) != 1 or 지문(سیستم_عامل.read(مسیر)) != 지문값:
                    raise ValueError("설치된 دسته_کردن 파일이 달라졌습니다: " + مسیر)
            print("이미 설치됨:", نام, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 برگشت_مقدار 설치하십시오.")
    for مسیر in 파일들:
        if سیستم_عامل.path_kind(مسیر):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + مسیر)
    ورودی_لیست[نام] = {"version": 명세["version"], "files": {مسیر: 지문(داده_ها) for مسیر, داده_ها in 파일들.items()}}
    새목록 = json.dumps(ورودی_لیست).encode()
    if len(새목록) > 16384:
        raise ValueError("دسته_کردن ورودی_لیست اندازه 초과")
    이전목록 = سیستم_عامل.read(لیست_مسیر) if سیستم_عامل.path_kind(لیست_مسیر) else None
    만든파일 = []
    만든폴더 = []
    try:
        for مسیر, داده_ها in 파일들.items():
            부분들 = مسیر.split("/")
            for 수 in range(2, len(부분들)):
                فهرست_مقدار_e5561a2b = "/".join(부분들[:수])
                종류 = سیستم_عامل.path_kind(فهرست_مقدار_e5561a2b)
                if 종류 == 0:
                    سیستم_عامل.mkdir(فهرست_مقدار_e5561a2b)
                    만든폴더.append(فهرست_مقدار_e5561a2b)
                elif 종류 != 2:
                    raise ValueError("فهرست_مقدار_e5561a2b 경로에 파일이 있습니다: " + فهرست_مقدار_e5561a2b)
            만든파일.append(مسیر)
            نوشتن_واقعه_نگار(مسیر, داده_ها)
        نوشتن_واقعه_نگار(لیست_مسیر, 새목록)
    except Exception:
        for مسیر in 만든파일:
            if سیستم_عامل.path_kind(مسیر):
                سیستم_عامل.remove(مسیر)
        for فهرست_مقدار_e5561a2b in reversed(만든폴더):
            سیستم_عامل.rmdir(فهرست_مقدار_e5561a2b)
        if 이전목록 is not None:
            نوشتن_واقعه_نگار(لیست_مسیر, 이전목록)
        elif سیستم_عامل.path_kind(لیست_مسیر):
            سیستم_عامل.remove(لیست_مسیر)
        raise
    print("نصب_مقدار 완료:", نام, 명세["version"], "→ /lib (RAM)")


def حذف_ورودی(نام):
    ورودی_لیست = 목록읽기()
    if نام not in ورودی_لیست:
        raise ValueError("설치되지 않은 꾸러미입니다: " + نام)
    for مسیر, 지문값 in ورودی_لیست[نام]["files"].items():
        if سیستم_عامل.path_kind(مسیر) != 1 or 지문(سیستم_عامل.read(مسیر)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + مسیر)
    for مسیر in ورودی_لیست[نام]["files"]:
        سیستم_عامل.remove(مسیر)
    del ورودی_لیست[نام]
    نوشتن_واقعه_نگار(لیست_مسیر, json.dumps(ورودی_لیست).encode())
    print("حذف_ورودی 완료:", نام)


def اجرا_2(نشانوندها):
    شماره_درگاه = 8027
    if len(نشانوندها) >= 2 and نشانوندها[-2] == "--port":
        شماره_درگاه = int(نشانوندها[-1])
        نشانوندها = نشانوندها[:-2]
    if نشانوندها == ["list"]:
        for نام, اطلاعات_سیستم in 목록읽기().items():
            print(نام, اطلاعات_سیستم["version"])
    elif len(نشانوندها) == 2 and نشانوندها[0] == "install":
        نصب_مقدار(نشانوندها[1], شماره_درگاه)
    elif len(نشانوندها) == 2 and نشانوندها[0] == "uninstall":
        حذف_ورودی(نشانوندها[1])
    elif not نشانوندها or نشانوندها in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython منبع_درخت 설치기 (PyPA pip 전체가 아님)")
        print("pip install نام[==버전] [--port 8027] | pip list | pip uninstall نام")
        print("میزبان: ابزارها/اجرا_فرمان.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        اجرا_2(sys.argv[1:])
    except Exception as خطا:
        print("دسته_کردن خطا:", خطا)
        sys.exit(1)
