"""ذاتي 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 مضيف 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as نظام_تشغيل

قائمة_مسار = "/lib/.pip.json"


def 지문(بيانات):
    return "".join("%02x" % قيمة for قيمة in hashlib.sha256(بيانات).digest())


def يقرأ_قائمة():
    if نظام_تشغيل.path_kind(قائمة_مسار) == 0:
        return {}
    return json.loads(نظام_تشغيل.read(قائمة_مسار).decode("utf-8"))


def كتابة_سجل(مسار, بيانات):
    if نظام_تشغيل.write(مسار, بيانات) != len(بيانات):
        raise OSError(28)


def شيك_مسار(مسار):
    if not isinstance(مسار, str) or not مسار.endswith(".py"):
        raise ValueError("Python 소스만 설치할 رقم 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in مسار.split("/")):
        raise ValueError("허용하지 않는 يُجمع مسار")
    if "\\" in مسار or any(ord(حرف_قيمة) < 32 or ord(حرف_قيمة) == 127 for حرف_قيمة in مسار):
        raise ValueError("잘못된 مسار 문자")
    نتيجة = "/lib/" + مسار
    if len(نتيجة.encode("utf-8")) > 63 or مسار in ("العربية.py", "يُجمع.py"):
        raise ValueError("يُجمع 경로가 너무 길거나 قيمة_افتراضية 라이브러리와 겹칩니다.")
    return نتيجة


class يستلم_بث:
    def __init__(자신, المشارك):
        자신.المشارك = المشارك
        자신.남은자료 = b""
        자신.تشغيل = نظام_تشغيل.ticks_ms()

    def 정확히읽기(자신, 길이):
        بيانات = bytearray()
        while len(بيانات) < 길이:
            if نظام_تشغيل.ticks_ms() - 자신.تشغيل > 90000:
                raise ValueError("يُجمع 중계 رد قيمة_الوقت 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = نظام_تشغيل.tcp_read(자신.المشارك, 512)
                except OSError as خطأ:
                    if خطأ.args[0] != 11:
                        raise
                    نظام_تشغيل.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("يُجمع 전송이 중간에 끝났습니다.")
            개수 = min(길이 - len(بيانات), len(자신.남은자료))
            بيانات.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            نظام_تشغيل.sleep_ms(0)
        return bytes(بيانات)


def تنزيل(طلب, رقم_المنفذ):
    if len(طلب) > 96 or any(حرف_قيمة not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for حرف_قيمة in طلب):
        raise ValueError("사용법: pip install اسم 또는 اسم==버전")
    المشارك = نظام_تشغيل.tcp_open()
    try:
        تشغيل = نظام_تشغيل.ticks_ms()
        while True:
            try:
                نظام_تشغيل.tcp_connect(المشارك, "10.0.2.2", رقم_المنفذ)
                break
            except OSError as خطأ:
                if خطأ.args[0] not in (11, 115) or نظام_تشغيل.ticks_ms() - تشغيل > 5000:
                    raise ValueError("يُجمع 중계 اتصال فشل_قيمة: 호스트에서 --network --pip로 실행하십시오.")
                نظام_تشغيل.sleep_ms(10)
        بيانات = (طلب + "\n").encode()
        while بيانات:
            try:
                개수 = نظام_تشغيل.tcp_write(المشارك, بيانات)
                if not 개수:
                    raise ValueError("يُجمع طلب نقل_قيمة_630ba093 فشل_قيمة")
                بيانات = بيانات[개수:]
            except OSError as خطأ:
                if خطأ.args[0] != 11:
                    raise
                نظام_تشغيل.sleep_ms(10)
                if نظام_تشغيل.ticks_ms() - تشغيل > 10000:
                    raise ValueError("يُجمع طلب نقل_قيمة_630ba093 قيمة_الوقت 초과")
        بث_قيمة = يستلم_بث(المشارك)
        رأس_قيمة = بث_قيمة.정확히읽기(8)
        if رأس_قيمة[:4] != b"JKP1":
            raise ValueError("يُجمع نقل_قيمة_630ba093 قيمة_العقد 불일치")
        길이 = (رأس_قيمة[4] << 24) | (رأس_قيمة[5] << 16) | (رأس_قيمة[6] << 8) | رأس_قيمة[7]
        if 길이 > 8192:
            raise ValueError("يُجمع 명세가 너무 큽니다.")
        المواصفات = json.loads(بث_قيمة.정확히읽기(길이).decode())
        if "error" in المواصفات:
            raise ValueError(المواصفات["error"])
        if not 1 <= len(المواصفات["files"]) <= 16:
            raise ValueError("꾸러미당 مصدر_شجرة 파일은 1~16개여야 합니다.")
        if sum(إدخال_قيمة_962f286b["size"] for إدخال_قيمة_962f286b in المواصفات["files"]) > 65536:
            raise ValueError("يُجمع مصدر_شجرة 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for إدخال_قيمة_962f286b in المواصفات["files"]:
            مسار = شيك_مسار(إدخال_قيمة_962f286b["path"])
            if مسار in 파일들 or not 0 <= إدخال_قيمة_962f286b["size"] <= 16384:
                raise ValueError("중복 مسار 또는 ملف حجم 초과")
            بيانات = بث_قيمة.정확히읽기(إدخال_قيمة_962f286b["size"])
            if 지문(بيانات) != إدخال_قيمة_962f286b["sha256"]:
                raise ValueError("يُجمع ملف SHA-256 불일치")
            # 실행하지 않고 حديث_عنصر MicroPython의 문법으로 먼저 검사한다.
            compile(بيانات.decode("utf-8"), مسار, "exec")
            파일들[مسار] = بيانات
            gc.collect()
        return المواصفات, 파일들
    finally:
        نظام_تشغيل.udp_close(المشارك)


def تثبيت_قيمة(طلب, رقم_المنفذ):
    print("يُجمع تنزيل:", طلب)
    المواصفات, 파일들 = تنزيل(طلب, رقم_المنفذ)
    إدخال_قائمة_f07b3200 = يقرأ_قائمة()
    اسم = المواصفات["name"]
    if اسم in إدخال_قائمة_f07b3200:
        if إدخال_قائمة_f07b3200[اسم]["version"] == المواصفات["version"]:
            for مسار, 지문값 in إدخال_قائمة_f07b3200[اسم]["files"].items():
                if نظام_تشغيل.path_kind(مسار) != 1 or 지문(نظام_تشغيل.read(مسار)) != 지문값:
                    raise ValueError("설치된 يُجمع 파일이 달라졌습니다: " + مسار)
            print("이미 설치됨:", اسم, المواصفات["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 عودة_قيمة 설치하십시오.")
    for مسار in 파일들:
        if نظام_تشغيل.path_kind(مسار):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + مسار)
    إدخال_قائمة_f07b3200[اسم] = {"version": المواصفات["version"], "files": {مسار: 지문(بيانات) for مسار, بيانات in 파일들.items()}}
    새목록 = json.dumps(إدخال_قائمة_f07b3200).encode()
    if len(새목록) > 16384:
        raise ValueError("يُجمع إدخال_قائمة_f07b3200 حجم 초과")
    이전목록 = نظام_تشغيل.read(قائمة_مسار) if نظام_تشغيل.path_kind(قائمة_مسار) else None
    만든파일 = []
    만든폴더 = []
    try:
        for مسار, بيانات in 파일들.items():
            부분들 = مسار.split("/")
            for رقم in range(2, len(부분들)):
                دليل_قيمة = "/".join(부분들[:رقم])
                종류 = نظام_تشغيل.path_kind(دليل_قيمة)
                if 종류 == 0:
                    نظام_تشغيل.mkdir(دليل_قيمة)
                    만든폴더.append(دليل_قيمة)
                elif 종류 != 2:
                    raise ValueError("دليل_قيمة 경로에 파일이 있습니다: " + دليل_قيمة)
            만든파일.append(مسار)
            كتابة_سجل(مسار, بيانات)
        كتابة_سجل(قائمة_مسار, 새목록)
    except Exception:
        for مسار in 만든파일:
            if نظام_تشغيل.path_kind(مسار):
                نظام_تشغيل.remove(مسار)
        for دليل_قيمة in reversed(만든폴더):
            نظام_تشغيل.rmdir(دليل_قيمة)
        if 이전목록 is not None:
            كتابة_سجل(قائمة_مسار, 이전목록)
        elif نظام_تشغيل.path_kind(قائمة_مسار):
            نظام_تشغيل.remove(قائمة_مسار)
        raise
    print("تثبيت_قيمة 완료:", اسم, المواصفات["version"], "→ /lib (RAM)")


def يزيل_إدخال(اسم):
    إدخال_قائمة_f07b3200 = يقرأ_قائمة()
    if اسم not in إدخال_قائمة_f07b3200:
        raise ValueError("설치되지 않은 꾸러미입니다: " + اسم)
    for مسار, 지문값 in إدخال_قائمة_f07b3200[اسم]["files"].items():
        if نظام_تشغيل.path_kind(مسار) != 1 or 지문(نظام_تشغيل.read(مسار)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + مسار)
    for مسار in إدخال_قائمة_f07b3200[اسم]["files"]:
        نظام_تشغيل.remove(مسار)
    del إدخال_قائمة_f07b3200[اسم]
    كتابة_سجل(قائمة_مسار, json.dumps(إدخال_قائمة_f07b3200).encode())
    print("يزيل_إدخال 완료:", اسم)


def تشغيل(وسائط):
    رقم_المنفذ = 8027
    if len(وسائط) >= 2 and وسائط[-2] == "--port":
        رقم_المنفذ = int(وسائط[-1])
        وسائط = وسائط[:-2]
    if وسائط == ["list"]:
        for اسم, معلومات_النظام in يقرأ_قائمة().items():
            print(اسم, معلومات_النظام["version"])
    elif len(وسائط) == 2 and وسائط[0] == "install":
        تثبيت_قيمة(وسائط[1], رقم_المنفذ)
    elif len(وسائط) == 2 and وسائط[0] == "uninstall":
        يزيل_إدخال(وسائط[1])
    elif not وسائط or وسائط in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython مصدر_شجرة 설치기 (PyPA pip 전체가 아님)")
        print("pip install اسم[==버전] [--port 8027] | pip list | pip uninstall اسم")
        print("مضيف: أدوات/ينفذ_أمر.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        تشغيل(sys.argv[1:])
    except Exception as خطأ:
        print("يُجمع خطأ:", خطأ)
        sys.exit(1)
