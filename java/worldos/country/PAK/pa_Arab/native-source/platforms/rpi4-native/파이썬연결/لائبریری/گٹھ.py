"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 مہمان_b78e430d 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as آپریٹنگ_سسٹم

فرست_راہ = "/lib/.pip.json"


def 지문(کوائف):
    return "".join("%02x" % قدر for قدر in hashlib.sha256(کوائف).digest())


def 목록읽기():
    if آپریٹنگ_سسٹم.path_kind(فرست_راہ) == 0:
        return {}
    return json.loads(آپریٹنگ_سسٹم.read(فرست_راہ).decode("utf-8"))


def لکھو_لاگ(راہ, کوائف):
    if آپریٹنگ_سسٹم.write(راہ, کوائف) != len(کوائف):
        raise OSError(28)


def پڑتال_راہ(راہ):
    if not isinstance(راہ, str) or not راہ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in راہ.split("/")):
        raise ValueError("허용하지 않는 گٹھ راہ")
    if "\\" in راہ or any(ord(کریکٹر_قدر) < 32 or ord(کریکٹر_قدر) == 127 for کریکٹر_قدر in راہ):
        raise ValueError("잘못된 راہ 문자")
    결과 = "/lib/" + راہ
    if len(결과.encode("utf-8")) > 63 or راہ in ("한국어.py", "گٹھ.py"):
        raise ValueError("گٹھ 경로가 너무 길거나 طےشدہ_قدر 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.چلاؤ = آپریٹنگ_سسٹم.ticks_ms()

    def 정확히읽기(자신, لمبائی_قدر):
        کوائف = bytearray()
        while len(کوائف) < لمبائی_قدر:
            if آپریٹنگ_سسٹم.ticks_ms() - 자신.چلاؤ > 90000:
                raise ValueError("گٹھ 중계 جواب_دیوؤ 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = آپریٹنگ_سسٹم.tcp_read(자신.종단, 512)
                except OSError as نقص:
                    if نقص.args[0] != 11:
                        raise
                    آپریٹنگ_سسٹم.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("گٹھ 전송이 중간에 끝났습니다.")
            개수 = min(لمبائی_قدر - len(کوائف), len(자신.남은자료))
            کوائف.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            آپریٹنگ_سسٹم.sleep_ms(0)
        return bytes(کوائف)


def ڈاؤن_لوڈ(요청, 접속번호):
    if len(요청) > 96 or any(کریکٹر_قدر not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for کریکٹر_قدر in 요청):
        raise ValueError("사용법: pip install ناں 또는 ناں==버전")
    종단 = آپریٹنگ_سسٹم.tcp_open()
    try:
        چلاؤ = آپریٹنگ_سسٹم.ticks_ms()
        while True:
            try:
                آپریٹنگ_سسٹم.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as نقص:
                if نقص.args[0] not in (11, 115) or آپریٹنگ_سسٹم.ticks_ms() - چلاؤ > 5000:
                    raise ValueError("گٹھ 중계 جڑو ناکامی_قدر: 호스트에서 --network --pip로 실행하십시오.")
                آپریٹنگ_سسٹم.sleep_ms(10)
        کوائف = (요청 + "\n").encode()
        while کوائف:
            try:
                개수 = آپریٹنگ_سسٹم.tcp_write(종단, کوائف)
                if not 개수:
                    raise ValueError("گٹھ 요청 منتقلی_قدر ناکامی_قدر")
                کوائف = کوائف[개수:]
            except OSError as نقص:
                if نقص.args[0] != 11:
                    raise
                آپریٹنگ_سسٹم.sleep_ms(10)
                if آپریٹنگ_سسٹم.ticks_ms() - چلاؤ > 10000:
                    raise ValueError("گٹھ 요청 منتقلی_قدر 시간 초과")
        سٹریم_قدر = 수신흐름(종단)
        머리 = سٹریم_قدر.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("گٹھ منتقلی_قدر حالت_قدر_102996da 불일치")
        لمبائی_قدر = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if لمبائی_قدر > 8192:
            raise ValueError("گٹھ 명세가 너무 큽니다.")
        명세 = json.loads(سٹریم_قدر.정확히읽기(لمبائی_قدر).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ماخذ_شجرہ 파일은 1~16개여야 합니다.")
        if sum(داخلہ_قدر["size"] for داخلہ_قدر in 명세["files"]) > 65536:
            raise ValueError("گٹھ ماخذ_شجرہ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for داخلہ_قدر in 명세["files"]:
            راہ = پڑتال_راہ(داخلہ_قدر["path"])
            if راہ in 파일들 or not 0 <= داخلہ_قدر["size"] <= 16384:
                raise ValueError("중복 راہ 또는 فائل سائز 초과")
            کوائف = سٹریم_قدر.정확히읽기(داخلہ_قدر["size"])
            if 지문(کوائف) != داخلہ_قدر["sha256"]:
                raise ValueError("گٹھ فائل SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(کوائف.decode("utf-8"), راہ, "exec")
            파일들[راہ] = کوائف
            gc.collect()
        return 명세, 파일들
    finally:
        آپریٹنگ_سسٹم.udp_close(종단)


def تنصیب_کرو_قدر(요청, 접속번호):
    print("گٹھ ڈاؤن_لوڈ:", 요청)
    명세, 파일들 = ڈاؤن_لوڈ(요청, 접속번호)
    داخلہ_فرست = 목록읽기()
    ناں = 명세["name"]
    if ناں in داخلہ_فرست:
        if داخلہ_فرست[ناں]["version"] == 명세["version"]:
            for راہ, 지문값 in داخلہ_فرست[ناں]["files"].items():
                if آپریٹنگ_سسٹم.path_kind(راہ) != 1 or 지문(آپریٹنگ_سسٹم.read(راہ)) != 지문값:
                    raise ValueError("설치된 گٹھ 파일이 달라졌습니다: " + راہ)
            print("이미 설치됨:", ناں, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 پیچھے_قدر 설치하십시오.")
    for راہ in 파일들:
        if آپریٹنگ_سسٹم.path_kind(راہ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + راہ)
    داخلہ_فرست[ناں] = {"version": 명세["version"], "files": {راہ: 지문(کوائف) for راہ, کوائف in 파일들.items()}}
    새목록 = json.dumps(داخلہ_فرست).encode()
    if len(새목록) > 16384:
        raise ValueError("گٹھ داخلہ_فرست سائز 초과")
    이전목록 = آپریٹنگ_سسٹم.read(فرست_راہ) if آپریٹنگ_سسٹم.path_kind(فرست_راہ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for راہ, کوائف in 파일들.items():
            부분들 = راہ.split("/")
            for 수 in range(2, len(부분들)):
                ڈائریکٹری_قدر = "/".join(부분들[:수])
                종류 = آپریٹنگ_سسٹم.path_kind(ڈائریکٹری_قدر)
                if 종류 == 0:
                    آپریٹنگ_سسٹم.mkdir(ڈائریکٹری_قدر)
                    만든폴더.append(ڈائریکٹری_قدر)
                elif 종류 != 2:
                    raise ValueError("ڈائریکٹری_قدر 경로에 파일이 있습니다: " + ڈائریکٹری_قدر)
            만든파일.append(راہ)
            لکھو_لاگ(راہ, کوائف)
        لکھو_لاگ(فرست_راہ, 새목록)
    except Exception:
        for راہ in 만든파일:
            if آپریٹنگ_سسٹم.path_kind(راہ):
                آپریٹنگ_سسٹم.remove(راہ)
        for ڈائریکٹری_قدر in reversed(만든폴더):
            آپریٹنگ_سسٹم.rmdir(ڈائریکٹری_قدر)
        if 이전목록 is not None:
            لکھو_لاگ(فرست_راہ, 이전목록)
        elif آپریٹنگ_سسٹم.path_kind(فرست_راہ):
            آپریٹنگ_سسٹم.remove(فرست_راہ)
        raise
    print("تنصیب_کرو_قدر 완료:", ناں, 명세["version"], "→ /lib (RAM)")


def ہٹاؤ_داخلہ(ناں):
    داخلہ_فرست = 목록읽기()
    if ناں not in داخلہ_فرست:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ناں)
    for راہ, 지문값 in داخلہ_فرست[ناں]["files"].items():
        if آپریٹنگ_سسٹم.path_kind(راہ) != 1 or 지문(آپریٹنگ_سسٹم.read(راہ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + راہ)
    for راہ in داخلہ_فرست[ناں]["files"]:
        آپریٹنگ_سسٹم.remove(راہ)
    del داخلہ_فرست[ناں]
    لکھو_لاگ(فرست_راہ, json.dumps(داخلہ_فرست).encode())
    print("ہٹاؤ_داخلہ 완료:", ناں)


def چلاؤ(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ناں, سسٹم_دی_معلومات in 목록읽기().items():
            print(ناں, سسٹم_دی_معلومات["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        تنصیب_کرو_قدر(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ہٹاؤ_داخلہ(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ماخذ_شجرہ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ناں[==버전] [--port 8027] | pip list | pip uninstall ناں")
        print("مہمان_b78e430d: اوزار/نفاذ_کرو_حکم.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        چلاؤ(sys.argv[1:])
    except Exception as نقص:
        print("گٹھ نقص:", نقص)
        sys.exit(1)
