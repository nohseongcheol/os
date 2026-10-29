"""עצמי 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ארח 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as מערכת_הפעלה

רשימה_נתיב = "/lib/.pip.json"


def 지문(נתונים):
    return "".join("%02x" % ערך for ערך in hashlib.sha256(נתונים).digest())


def 목록읽기():
    if מערכת_הפעלה.path_kind(רשימה_נתיב) == 0:
        return {}
    return json.loads(מערכת_הפעלה.read(רשימה_נתיב).decode("utf-8"))


def כתיבה_לרשום(נתיב, נתונים):
    if מערכת_הפעלה.write(נתיב, נתונים) != len(נתונים):
        raise OSError(28)


def שיק_נתיב(נתיב):
    if not isinstance(נתיב, str) or not נתיב.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in נתיב.split("/")):
        raise ValueError("허용하지 않는 חבילה נתיב")
    if "\\" in נתיב or any(ord(תו_ערך) < 32 or ord(תו_ערך) == 127 for תו_ערך in נתיב):
        raise ValueError("잘못된 נתיב 문자")
    תוצאה = "/lib/" + נתיב
    if len(תוצאה.encode("utf-8")) > 63 or נתיב in ("עברית.py", "חבילה.py"):
        raise ValueError("חבילה 경로가 너무 길거나 ערך_ברירת_מחדל 라이브러리와 겹칩니다.")
    return תוצאה


class לקבל_זרם:
    def __init__(자신, משתתף):
        자신.משתתף = משתתף
        자신.남은자료 = b""
        자신.הפעלה = מערכת_הפעלה.ticks_ms()

    def 정확히읽기(자신, 길이):
        נתונים = bytearray()
        while len(נתונים) < 길이:
            if מערכת_הפעלה.ticks_ms() - 자신.הפעלה > 90000:
                raise ValueError("חבילה 중계 מענה ערך_זמן 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = מערכת_הפעלה.tcp_read(자신.משתתף, 512)
                except OSError as שגיאה:
                    if שגיאה.args[0] != 11:
                        raise
                    מערכת_הפעלה.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("חבילה 전송이 중간에 끝났습니다.")
            개수 = min(길이 - len(נתונים), len(자신.남은자료))
            נתונים.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            מערכת_הפעלה.sleep_ms(0)
        return bytes(נתונים)


def הורד(בקשה, מספר_יציאה):
    if len(בקשה) > 96 or any(תו_ערך not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for תו_ערך in בקשה):
        raise ValueError("사용법: pip install שם 또는 שם==버전")
    משתתף = מערכת_הפעלה.tcp_open()
    try:
        הפעלה = מערכת_הפעלה.ticks_ms()
        while True:
            try:
                מערכת_הפעלה.tcp_connect(משתתף, "10.0.2.2", מספר_יציאה)
                break
            except OSError as שגיאה:
                if שגיאה.args[0] not in (11, 115) or מערכת_הפעלה.ticks_ms() - הפעלה > 5000:
                    raise ValueError("חבילה 중계 חיבור כשל_ערך: 호스트에서 --network --pip로 실행하십시오.")
                מערכת_הפעלה.sleep_ms(10)
        נתונים = (בקשה + "\n").encode()
        while נתונים:
            try:
                개수 = מערכת_הפעלה.tcp_write(משתתף, נתונים)
                if not 개수:
                    raise ValueError("חבילה בקשה העבר_ערך כשל_ערך")
                נתונים = נתונים[개수:]
            except OSError as שגיאה:
                if שגיאה.args[0] != 11:
                    raise
                מערכת_הפעלה.sleep_ms(10)
                if מערכת_הפעלה.ticks_ms() - הפעלה > 10000:
                    raise ValueError("חבילה בקשה העבר_ערך ערך_זמן 초과")
        זרם_ערך = לקבל_זרם(משתתף)
        ראש_ערך = זרם_ערך.정확히읽기(8)
        if ראש_ערך[:4] != b"JKP1":
            raise ValueError("חבילה העבר_ערך ערך_חוזה 불일치")
        길이 = (ראש_ערך[4] << 24) | (ראש_ערך[5] << 16) | (ראש_ערך[6] << 8) | ראש_ערך[7]
        if 길이 > 8192:
            raise ValueError("חבילה 명세가 너무 큽니다.")
        מפרט = json.loads(זרם_ערך.정확히읽기(길이).decode())
        if "error" in מפרט:
            raise ValueError(מפרט["error"])
        if not 1 <= len(מפרט["files"]) <= 16:
            raise ValueError("꾸러미당 מקור_עץ 파일은 1~16개여야 합니다.")
        if sum(ערך_ערך["size"] for ערך_ערך in מפרט["files"]) > 65536:
            raise ValueError("חבילה מקור_עץ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ערך_ערך in מפרט["files"]:
            נתיב = שיק_נתיב(ערך_ערך["path"])
            if נתיב in 파일들 or not 0 <= ערך_ערך["size"] <= 16384:
                raise ValueError("중복 נתיב 또는 קובץ גודל 초과")
            נתונים = זרם_ערך.정확히읽기(ערך_ערך["size"])
            if 지문(נתונים) != ערך_ערך["sha256"]:
                raise ValueError("חבילה קובץ SHA-256 불일치")
            # 실행하지 않고 נוכחי_פריט MicroPython의 문법으로 먼저 검사한다.
            compile(נתונים.decode("utf-8"), נתיב, "exec")
            파일들[נתיב] = נתונים
            gc.collect()
        return מפרט, 파일들
    finally:
        מערכת_הפעלה.udp_close(משתתף)


def התקן_ערך(בקשה, מספר_יציאה):
    print("חבילה הורד:", בקשה)
    מפרט, 파일들 = הורד(בקשה, מספר_יציאה)
    ערך_רשימה = 목록읽기()
    שם = מפרט["name"]
    if שם in ערך_רשימה:
        if ערך_רשימה[שם]["version"] == מפרט["version"]:
            for נתיב, 지문값 in ערך_רשימה[שם]["files"].items():
                if מערכת_הפעלה.path_kind(נתיב) != 1 or 지문(מערכת_הפעלה.read(נתיב)) != 지문값:
                    raise ValueError("설치된 חבילה 파일이 달라졌습니다: " + נתיב)
            print("이미 설치됨:", שם, מפרט["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 הקודם_ערך 설치하십시오.")
    for נתיב in 파일들:
        if מערכת_הפעלה.path_kind(נתיב):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + נתיב)
    ערך_רשימה[שם] = {"version": מפרט["version"], "files": {נתיב: 지문(נתונים) for נתיב, נתונים in 파일들.items()}}
    새목록 = json.dumps(ערך_רשימה).encode()
    if len(새목록) > 16384:
        raise ValueError("חבילה ערך_רשימה גודל 초과")
    이전목록 = מערכת_הפעלה.read(רשימה_נתיב) if מערכת_הפעלה.path_kind(רשימה_נתיב) else None
    만든파일 = []
    만든폴더 = []
    try:
        for נתיב, נתונים in 파일들.items():
            부분들 = נתיב.split("/")
            for 수 in range(2, len(부분들)):
                מדריך_ערך = "/".join(부분들[:수])
                종류 = מערכת_הפעלה.path_kind(מדריך_ערך)
                if 종류 == 0:
                    מערכת_הפעלה.mkdir(מדריך_ערך)
                    만든폴더.append(מדריך_ערך)
                elif 종류 != 2:
                    raise ValueError("מדריך_ערך 경로에 파일이 있습니다: " + מדריך_ערך)
            만든파일.append(נתיב)
            כתיבה_לרשום(נתיב, נתונים)
        כתיבה_לרשום(רשימה_נתיב, 새목록)
    except Exception:
        for נתיב in 만든파일:
            if מערכת_הפעלה.path_kind(נתיב):
                מערכת_הפעלה.remove(נתיב)
        for מדריך_ערך in reversed(만든폴더):
            מערכת_הפעלה.rmdir(מדריך_ערך)
        if 이전목록 is not None:
            כתיבה_לרשום(רשימה_נתיב, 이전목록)
        elif מערכת_הפעלה.path_kind(רשימה_נתיב):
            מערכת_הפעלה.remove(רשימה_נתיב)
        raise
    print("התקן_ערך 완료:", שם, מפרט["version"], "→ /lib (RAM)")


def הסר_ערך(שם):
    ערך_רשימה = 목록읽기()
    if שם not in ערך_רשימה:
        raise ValueError("설치되지 않은 꾸러미입니다: " + שם)
    for נתיב, 지문값 in ערך_רשימה[שם]["files"].items():
        if מערכת_הפעלה.path_kind(נתיב) != 1 or 지문(מערכת_הפעלה.read(נתיב)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + נתיב)
    for נתיב in ערך_רשימה[שם]["files"]:
        מערכת_הפעלה.remove(נתיב)
    del ערך_רשימה[שם]
    כתיבה_לרשום(רשימה_נתיב, json.dumps(ערך_רשימה).encode())
    print("הסר_ערך 완료:", שם)


def הפעלה(ארגומנטים):
    מספר_יציאה = 8027
    if len(ארגומנטים) >= 2 and ארגומנטים[-2] == "--port":
        מספר_יציאה = int(ארגומנטים[-1])
        ארגומנטים = ארגומנטים[:-2]
    if ארגומנטים == ["list"]:
        for שם, מידע_מערכת in 목록읽기().items():
            print(שם, מידע_מערכת["version"])
    elif len(ארגומנטים) == 2 and ארגומנטים[0] == "install":
        התקן_ערך(ארגומנטים[1], מספר_יציאה)
    elif len(ארגומנטים) == 2 and ארגומנטים[0] == "uninstall":
        הסר_ערך(ארגומנטים[1])
    elif not ארגומנטים or ארגומנטים in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython מקור_עץ 설치기 (PyPA pip 전체가 아님)")
        print("pip install שם[==버전] [--port 8027] | pip list | pip uninstall שם")
        print("ארח: כלים/לבצע_פקודה.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        הפעלה(sys.argv[1:])
    except Exception as שגיאה:
        print("חבילה שגיאה:", שגיאה)
        sys.exit(1)
