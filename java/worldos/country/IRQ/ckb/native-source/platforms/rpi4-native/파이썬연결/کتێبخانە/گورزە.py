"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 جێدەر 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as سیستەمی_کارپێکردن

لیست_گوزەر = "/lib/.pip.json"


def 지문(دەیتا):
    return "".join("%02x" % نرخ for نرخ in hashlib.sha256(دەیتا).digest())


def 목록읽기():
    if سیستەمی_کارپێکردن.path_kind(لیست_گوزەر) == 0:
        return {}
    return json.loads(سیستەمی_کارپێکردن.read(لیست_گوزەر).decode("utf-8"))


def ڕایت_کردن_تۆمار(گوزەر, دەیتا):
    if سیستەمی_کارپێکردن.write(گوزەر, دەیتا) != len(دەیتا):
        raise OSError(28)


def پشکنین_گوزەر(گوزەر):
    if not isinstance(گوزەر, str) or not گوزەر.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in گوزەر.split("/")):
        raise ValueError("허용하지 않는 گورزە گوزەر")
    if "\\" in گوزەر or any(ord(نووسە_نرخ) < 32 or ord(نووسە_نرخ) == 127 for نووسە_نرخ in گوزەر):
        raise ValueError("잘못된 گوزەر 문자")
    결과 = "/lib/" + گوزەر
    if len(결과.encode("utf-8")) > 63 or گوزەر in ("한국어.py", "گورزە.py"):
        raise ValueError("گورزە 경로가 너무 길거나 بەهای_گریمانە 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ڕادان = سیستەمی_کارپێکردن.ticks_ms()

    def 정확히읽기(자신, درێژی_نرخ):
        دەیتا = bytearray()
        while len(دەیتا) < درێژی_نرخ:
            if سیستەمی_کارپێکردن.ticks_ms() - 자신.ڕادان > 90000:
                raise ValueError("گورزە 중계 وەڵامدانەوه کات_نرخ 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = سیستەمی_کارپێکردن.tcp_read(자신.종단, 512)
                except OSError as هەڵە:
                    if هەڵە.args[0] != 11:
                        raise
                    سیستەمی_کارپێکردن.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("گورزە 전송이 중간에 끝났습니다.")
            개수 = min(درێژی_نرخ - len(دەیتا), len(자신.남은자료))
            دەیتا.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            سیستەمی_کارپێکردن.sleep_ms(0)
        return bytes(دەیتا)


def داگرتن(요청, 접속번호):
    if len(요청) > 96 or any(نووسە_نرخ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for نووسە_نرخ in 요청):
        raise ValueError("사용법: pip install ناو 또는 ناو==버전")
    종단 = سیستەمی_کارپێکردن.tcp_open()
    try:
        ڕادان = سیستەمی_کارپێکردن.ticks_ms()
        while True:
            try:
                سیستەمی_کارپێکردن.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as هەڵە:
                if هەڵە.args[0] not in (11, 115) or سیستەمی_کارپێکردن.ticks_ms() - ڕادان > 5000:
                    raise ValueError("گورزە 중계 لكاندن شکستهێنان_نرخ: 호스트에서 --network --pip로 실행하십시오.")
                سیستەمی_کارپێکردن.sleep_ms(10)
        دەیتا = (요청 + "\n").encode()
        while دەیتا:
            try:
                개수 = سیستەمی_کارپێکردن.tcp_write(종단, دەیتا)
                if not 개수:
                    raise ValueError("گورزە 요청 گواستنەوە_نرخ_630ba093 شکستهێنان_نرخ")
                دەیتا = دەیتا[개수:]
            except OSError as هەڵە:
                if هەڵە.args[0] != 11:
                    raise
                سیستەمی_کارپێکردن.sleep_ms(10)
                if سیستەمی_کارپێکردن.ticks_ms() - ڕادان > 10000:
                    raise ValueError("گورزە 요청 گواستنەوە_نرخ_630ba093 کات_نرخ 초과")
        Stream_نرخ = 수신흐름(종단)
        머리 = Stream_نرخ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("گورزە گواستنەوە_نرخ_630ba093 ئەرک_نرخ 불일치")
        درێژی_نرخ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if درێژی_نرخ > 8192:
            raise ValueError("گورزە 명세가 너무 큽니다.")
        명세 = json.loads(Stream_نرخ.정확히읽기(درێژی_نرخ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ژێدەر_دار 파일은 1~16개여야 합니다.")
        if sum(تێنووسین_نرخ["size"] for تێنووسین_نرخ in 명세["files"]) > 65536:
            raise ValueError("گورزە ژێدەر_دار 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for تێنووسین_نرخ in 명세["files"]:
            گوزەر = پشکنین_گوزەر(تێنووسین_نرخ["path"])
            if گوزەر in 파일들 or not 0 <= تێنووسین_نرخ["size"] <= 16384:
                raise ValueError("중복 گوزەر 또는 فایل گۆڕینی_ئەندازە 초과")
            دەیتا = Stream_نرخ.정확히읽기(تێنووسین_نرخ["size"])
            if 지문(دەیتا) != تێنووسین_نرخ["sha256"]:
                raise ValueError("گورزە فایل SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(دەیتا.decode("utf-8"), گوزەر, "exec")
            파일들[گوزەر] = دەیتا
            gc.collect()
        return 명세, 파일들
    finally:
        سیستەمی_کارپێکردن.udp_close(종단)


def دامەزرێنە_نرخ(요청, 접속번호):
    print("گورزە داگرتن:", 요청)
    명세, 파일들 = داگرتن(요청, 접속번호)
    تێنووسین_لیست = 목록읽기()
    ناو = 명세["name"]
    if ناو in تێنووسین_لیست:
        if تێنووسین_لیست[ناو]["version"] == 명세["version"]:
            for گوزەر, 지문값 in تێنووسین_لیست[ناو]["files"].items():
                if سیستەمی_کارپێکردن.path_kind(گوزەر) != 1 or 지문(سیستەمی_کارپێکردن.read(گوزەر)) != 지문값:
                    raise ValueError("설치된 گورزە 파일이 달라졌습니다: " + گوزەر)
            print("이미 설치됨:", ناو, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 دواوە_نرخ 설치하십시오.")
    for گوزەر in 파일들:
        if سیستەمی_کارپێکردن.path_kind(گوزەر):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + گوزەر)
    تێنووسین_لیست[ناو] = {"version": 명세["version"], "files": {گوزەر: 지문(دەیتا) for گوزەر, دەیتا in 파일들.items()}}
    새목록 = json.dumps(تێنووسین_لیست).encode()
    if len(새목록) > 16384:
        raise ValueError("گورزە تێنووسین_لیست گۆڕینی_ئەندازە 초과")
    이전목록 = سیستەمی_کارپێکردن.read(لیست_گوزەر) if سیستەمی_کارپێکردن.path_kind(لیست_گوزەر) else None
    만든파일 = []
    만든폴더 = []
    try:
        for گوزەر, دەیتا in 파일들.items():
            부분들 = گوزەر.split("/")
            for 수 in range(2, len(부분들)):
                ڕێبەرنامە_نرخ = "/".join(부분들[:수])
                종류 = سیستەمی_کارپێکردن.path_kind(ڕێبەرنامە_نرخ)
                if 종류 == 0:
                    سیستەمی_کارپێکردن.mkdir(ڕێبەرنامە_نرخ)
                    만든폴더.append(ڕێبەرنامە_نرخ)
                elif 종류 != 2:
                    raise ValueError("ڕێبەرنامە_نرخ 경로에 파일이 있습니다: " + ڕێبەرنامە_نرخ)
            만든파일.append(گوزەر)
            ڕایت_کردن_تۆمار(گوزەر, دەیتا)
        ڕایت_کردن_تۆمار(لیست_گوزەر, 새목록)
    except Exception:
        for گوزەر in 만든파일:
            if سیستەمی_کارپێکردن.path_kind(گوزەر):
                سیستەمی_کارپێکردن.remove(گوزەر)
        for ڕێبەرنامە_نرخ in reversed(만든폴더):
            سیستەمی_کارپێکردن.rmdir(ڕێبەرنامە_نرخ)
        if 이전목록 is not None:
            ڕایت_کردن_تۆمار(لیست_گوزەر, 이전목록)
        elif سیستەمی_کارپێکردن.path_kind(لیست_گوزەر):
            سیستەمی_کارپێکردن.remove(لیست_گوزەر)
        raise
    print("دامەزرێنە_نرخ 완료:", ناو, 명세["version"], "→ /lib (RAM)")


def لابردن_تێنووسین(ناو):
    تێنووسین_لیست = 목록읽기()
    if ناو not in تێنووسین_لیست:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ناو)
    for گوزەر, 지문값 in تێنووسین_لیست[ناو]["files"].items():
        if سیستەمی_کارپێکردن.path_kind(گوزەر) != 1 or 지문(سیستەمی_کارپێکردن.read(گوزەر)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + گوزەر)
    for گوزەر in تێنووسین_لیست[ناو]["files"]:
        سیستەمی_کارپێکردن.remove(گوزەر)
    del تێنووسین_لیست[ناو]
    ڕایت_کردن_تۆمار(لیست_گوزەر, json.dumps(تێنووسین_لیست).encode())
    print("لابردن_تێنووسین 완료:", ناو)


def ڕادان(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ناو, msinfo32_exe in 목록읽기().items():
            print(ناو, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        دامەزرێنە_نرخ(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        لابردن_تێنووسین(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ژێدەر_دار 설치기 (PyPA pip 전체가 아님)")
        print("pip install ناو[==버전] [--port 8027] | pip list | pip uninstall ناو")
        print("جێدەر: ئامرازەکان/جێبەجێکردن_فەرمان.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ڕادان(sys.argv[1:])
    except Exception as هەڵە:
        print("گورزە هەڵە:", هەڵە)
        sys.exit(1)
