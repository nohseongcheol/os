"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 مهمان 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as آپريٽنگ_سسٽم

فهرست_راههه = "/lib/.pip.json"


def 지문(ڪوائف):
    return "".join("%02x" % قدر for قدر in hashlib.sha256(ڪوائف).digest())


def 목록읽기():
    if آپريٽنگ_سسٽم.path_kind(فهرست_راههه) == 0:
        return {}
    return json.loads(آپريٽنگ_سسٽم.read(فهرست_راههه).decode("utf-8"))


def لکو_لاگ(راههه, ڪوائف):
    if آپريٽنگ_سسٽم.write(راههه, ڪوائف) != len(ڪوائف):
        raise OSError(28)


def پڙتال_ڪريو_راههه(راههه):
    if not isinstance(راههه, str) or not راههه.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in راههه.split("/")):
        raise ValueError("허용하지 않는 بنڊل راههه")
    if "\\" in راههه or any(ord(ڪريڪٽر_قدر) < 32 or ord(ڪريڪٽر_قدر) == 127 for ڪريڪٽر_قدر in راههه):
        raise ValueError("잘못된 راههه 문자")
    결과 = "/lib/" + راههه
    if len(결과.encode("utf-8")) > 63 or راههه in ("한국어.py", "بنڊل.py"):
        raise ValueError("بنڊل 경로가 너무 길거나 طئي_ٿيل_ملهه 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.هلائڻ = آپريٽنگ_سسٽم.ticks_ms()

    def 정확히읽기(자신, لمبائي_قدر):
        ڪوائف = bytearray()
        while len(ڪوائف) < لمبائي_قدر:
            if آپريٽنگ_سسٽم.ticks_ms() - 자신.هلائڻ > 90000:
                raise ValueError("بنڊل 중계 جواب_ڏيو 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = آپريٽنگ_سسٽم.tcp_read(자신.종단, 512)
                except OSError as نقص:
                    if نقص.args[0] != 11:
                        raise
                    آپريٽنگ_سسٽم.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("بنڊل 전송이 중간에 끝났습니다.")
            개수 = min(لمبائي_قدر - len(ڪوائف), len(자신.남은자료))
            ڪوائف.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            آپريٽنگ_سسٽم.sleep_ms(0)
        return bytes(ڪوائف)


def ڊائونلوڊ(요청, 접속번호):
    if len(요청) > 96 or any(ڪريڪٽر_قدر not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ڪريڪٽر_قدر in 요청):
        raise ValueError("사용법: pip install نالو 또는 نالو==버전")
    종단 = آپريٽنگ_سسٽم.tcp_open()
    try:
        هلائڻ = آپريٽنگ_سسٽم.ticks_ms()
        while True:
            try:
                آپريٽنگ_سسٽم.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as نقص:
                if نقص.args[0] not in (11, 115) or آپريٽنگ_سسٽم.ticks_ms() - هلائڻ > 5000:
                    raise ValueError("بنڊل 중계 ڪنيڪٽ ناڪامي_قدر: 호스트에서 --network --pip로 실행하십시오.")
                آپريٽنگ_سسٽم.sleep_ms(10)
        ڪوائف = (요청 + "\n").encode()
        while ڪوائف:
            try:
                개수 = آپريٽنگ_سسٽم.tcp_write(종단, ڪوائف)
                if not 개수:
                    raise ValueError("بنڊل 요청 منتقلي_قدر ناڪامي_قدر")
                ڪوائف = ڪوائف[개수:]
            except OSError as نقص:
                if نقص.args[0] != 11:
                    raise
                آپريٽنگ_سسٽم.sleep_ms(10)
                if آپريٽنگ_سسٽم.ticks_ms() - هلائڻ > 10000:
                    raise ValueError("بنڊل 요청 منتقلي_قدر 시간 초과")
        اسٽريم_قدر = 수신흐름(종단)
        머리 = اسٽريم_قدر.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("بنڊل منتقلي_قدر حالت_قدر_102996da 불일치")
        لمبائي_قدر = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if لمبائي_قدر > 8192:
            raise ValueError("بنڊل 명세가 너무 큽니다.")
        명세 = json.loads(اسٽريم_قدر.정확히읽기(لمبائي_قدر).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ماخذ_شجرو 파일은 1~16개여야 합니다.")
        if sum(داخلا_قدر["size"] for داخلا_قدر in 명세["files"]) > 65536:
            raise ValueError("بنڊل ماخذ_شجرو 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for داخلا_قدر in 명세["files"]:
            راههه = پڙتال_ڪريو_راههه(داخلا_قدر["path"])
            if راههه in 파일들 or not 0 <= داخلا_قدر["size"] <= 16384:
                raise ValueError("중복 راههه 또는 فائل سائيز 초과")
            ڪوائف = اسٽريم_قدر.정확히읽기(داخلا_قدر["size"])
            if 지문(ڪوائف) != داخلا_قدر["sha256"]:
                raise ValueError("بنڊل فائل SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ڪوائف.decode("utf-8"), راههه, "exec")
            파일들[راههه] = ڪوائف
            gc.collect()
        return 명세, 파일들
    finally:
        آپريٽنگ_سسٽم.udp_close(종단)


def نصب_ڪريو_قدر(요청, 접속번호):
    print("بنڊل ڊائونلوڊ:", 요청)
    명세, 파일들 = ڊائونلوڊ(요청, 접속번호)
    داخلا_فهرست = 목록읽기()
    نالو = 명세["name"]
    if نالو in داخلا_فهرست:
        if داخلا_فهرست[نالو]["version"] == 명세["version"]:
            for راههه, 지문값 in داخلا_فهرست[نالو]["files"].items():
                if آپريٽنگ_سسٽم.path_kind(راههه) != 1 or 지문(آپريٽنگ_سسٽم.read(راههه)) != 지문값:
                    raise ValueError("설치된 بنڊل 파일이 달라졌습니다: " + راههه)
            print("이미 설치됨:", نالو, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 واپس_قدر 설치하십시오.")
    for راههه in 파일들:
        if آپريٽنگ_سسٽم.path_kind(راههه):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + راههه)
    داخلا_فهرست[نالو] = {"version": 명세["version"], "files": {راههه: 지문(ڪوائف) for راههه, ڪوائف in 파일들.items()}}
    새목록 = json.dumps(داخلا_فهرست).encode()
    if len(새목록) > 16384:
        raise ValueError("بنڊل داخلا_فهرست سائيز 초과")
    이전목록 = آپريٽنگ_سسٽم.read(فهرست_راههه) if آپريٽنگ_سسٽم.path_kind(فهرست_راههه) else None
    만든파일 = []
    만든폴더 = []
    try:
        for راههه, ڪوائف in 파일들.items():
            부분들 = راههه.split("/")
            for 수 in range(2, len(부분들)):
                ڊائريڪٽري_قدر = "/".join(부분들[:수])
                종류 = آپريٽنگ_سسٽم.path_kind(ڊائريڪٽري_قدر)
                if 종류 == 0:
                    آپريٽنگ_سسٽم.mkdir(ڊائريڪٽري_قدر)
                    만든폴더.append(ڊائريڪٽري_قدر)
                elif 종류 != 2:
                    raise ValueError("ڊائريڪٽري_قدر 경로에 파일이 있습니다: " + ڊائريڪٽري_قدر)
            만든파일.append(راههه)
            لکو_لاگ(راههه, ڪوائف)
        لکو_لاگ(فهرست_راههه, 새목록)
    except Exception:
        for راههه in 만든파일:
            if آپريٽنگ_سسٽم.path_kind(راههه):
                آپريٽنگ_سسٽم.remove(راههه)
        for ڊائريڪٽري_قدر in reversed(만든폴더):
            آپريٽنگ_سسٽم.rmdir(ڊائريڪٽري_قدر)
        if 이전목록 is not None:
            لکو_لاگ(فهرست_راههه, 이전목록)
        elif آپريٽنگ_سسٽم.path_kind(فهرست_راههه):
            آپريٽنگ_سسٽم.remove(فهرست_راههه)
        raise
    print("نصب_ڪريو_قدر 완료:", نالو, 명세["version"], "→ /lib (RAM)")


def هٽايو_داخلا(نالو):
    داخلا_فهرست = 목록읽기()
    if نالو not in داخلا_فهرست:
        raise ValueError("설치되지 않은 꾸러미입니다: " + نالو)
    for راههه, 지문값 in داخلا_فهرست[نالو]["files"].items():
        if آپريٽنگ_سسٽم.path_kind(راههه) != 1 or 지문(آپريٽنگ_سسٽم.read(راههه)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + راههه)
    for راههه in داخلا_فهرست[نالو]["files"]:
        آپريٽنگ_سسٽم.remove(راههه)
    del داخلا_فهرست[نالو]
    لکو_لاگ(فهرست_راههه, json.dumps(داخلا_فهرست).encode())
    print("هٽايو_داخلا 완료:", نالو)


def هلائڻ(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for نالو, سسٽم_معلومات in 목록읽기().items():
            print(نالو, سسٽم_معلومات["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        نصب_ڪريو_قدر(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        هٽايو_داخلا(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ماخذ_شجرو 설치기 (PyPA pip 전체가 아님)")
        print("pip install نالو[==버전] [--port 8027] | pip list | pip uninstall نالو")
        print("مهمان: اوزار/تعميل_ڪرڻ_حڪم.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        هلائڻ(sys.argv[1:])
    except Exception as نقص:
        print("بنڊل نقص:", نقص)
        sys.exit(1)
