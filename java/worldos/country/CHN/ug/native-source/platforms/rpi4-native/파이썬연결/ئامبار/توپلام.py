"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 باقار 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as مەشغۇلات_سىستېمىسى

تىزىم_يول = "/lib/.pip.json"


def 지문(مەلۇمات):
    return "".join("%02x" % قىممىتى for قىممىتى in hashlib.sha256(مەلۇمات).digest())


def 목록읽기():
    if مەشغۇلات_سىستېمىسى.path_kind(تىزىم_يول) == 0:
        return {}
    return json.loads(مەشغۇلات_سىستېمىسى.read(تىزىم_يول).decode("utf-8"))


def يازماق_خاتىرە(يول, مەلۇمات):
    if مەشغۇلات_سىستېمىسى.write(يول, مەلۇمات) != len(مەلۇمات):
        raise OSError(28)


def تەكشۈرۈش_يول(يول):
    if not isinstance(يول, str) or not يول.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in يول.split("/")):
        raise ValueError("허용하지 않는 توپلام يول")
    if "\\" in يول or any(ord(ھەرپ_بەلگە_قىممىتى) < 32 or ord(ھەرپ_بەلگە_قىممىتى) == 127 for ھەرپ_بەلگە_قىممىتى in يول):
        raise ValueError("잘못된 يول 문자")
    ئۆلچەم = "/lib/" + يول
    if len(ئۆلچەم.encode("utf-8")) > 63 or يول in ("한국어.py", "توپلام.py"):
        raise ValueError("توپلام 경로가 너무 길거나 سۈكۈتتىكى_قىممەت 라이브러리와 겹칩니다.")
    return ئۆلچەم


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ئىجرا_قىل_2 = مەشغۇلات_سىستېمىسى.ticks_ms()

    def 정확히읽기(자신, ئۇزۇنلۇق_قىممىتى):
        مەلۇمات = bytearray()
        while len(مەلۇمات) < ئۇزۇنلۇق_قىممىتى:
            if مەشغۇلات_سىستېمىسى.ticks_ms() - 자신.ئىجرا_قىل_2 > 90000:
                raise ValueError("توپلام 중계 جاۋابلاش 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = مەشغۇلات_سىستېمىسى.tcp_read(자신.종단, 512)
                except OSError as خاتالىق:
                    if خاتالىق.args[0] != 11:
                        raise
                    مەشغۇلات_سىستېمىسى.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("توپلام 전송이 중간에 끝났습니다.")
            개수 = min(ئۇزۇنلۇق_قىممىتى - len(مەلۇمات), len(자신.남은자료))
            مەلۇمات.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            مەشغۇلات_سىستېمىسى.sleep_ms(0)
        return bytes(مەلۇمات)


def چۈشۈرۈش(요청, 접속번호):
    if len(요청) > 96 or any(ھەرپ_بەلگە_قىممىتى not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ھەرپ_بەلگە_قىممىتى in 요청):
        raise ValueError("사용법: pip install ئاتى 또는 ئاتى==버전")
    종단 = مەشغۇلات_سىستېمىسى.tcp_open()
    try:
        ئىجرا_قىل_2 = مەشغۇلات_سىستېمىسى.ticks_ms()
        while True:
            try:
                مەشغۇلات_سىستېمىسى.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as خاتالىق:
                if خاتالىق.args[0] not in (11, 115) or مەشغۇلات_سىستېمىسى.ticks_ms() - ئىجرا_قىل_2 > 5000:
                    raise ValueError("توپلام 중계 ئۇلا مەغلۇپ_بولۇش_قىممىتى: 호스트에서 --network --pip로 실행하십시오.")
                مەشغۇلات_سىستېمىسى.sleep_ms(10)
        مەلۇمات = (요청 + "\n").encode()
        while مەلۇمات:
            try:
                개수 = مەشغۇلات_سىستېمىسى.tcp_write(종단, مەلۇمات)
                if not 개수:
                    raise ValueError("توپلام 요청 يوللاش_قىممىتى_630ba093 مەغلۇپ_بولۇش_قىممىتى")
                مەلۇمات = مەلۇمات[개수:]
            except OSError as خاتالىق:
                if خاتالىق.args[0] != 11:
                    raise
                مەشغۇلات_سىستېمىسى.sleep_ms(10)
                if مەشغۇلات_سىستېمىسى.ticks_ms() - ئىجرا_قىل_2 > 10000:
                    raise ValueError("توپلام 요청 يوللاش_قىممىتى_630ba093 시간 초과")
        ئېقىم_قىممىتى = 수신흐름(종단)
        머리 = ئېقىم_قىممىتى.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("توپلام يوللاش_قىممىتى_630ba093 خىزمەت_قىممىتى 불일치")
        ئۇزۇنلۇق_قىممىتى = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ئۇزۇنلۇق_قىممىتى > 8192:
            raise ValueError("توپلام 명세가 너무 큽니다.")
        명세 = json.loads(ئېقىم_قىممىتى.정확히읽기(ئۇزۇنلۇق_قىممىتى).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 مەنبە_دەرەخ 파일은 1~16개여야 합니다.")
        if sum(كىرگۈزۈش_قىممىتى["size"] for كىرگۈزۈش_قىممىتى in 명세["files"]) > 65536:
            raise ValueError("توپلام مەنبە_دەرەخ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for كىرگۈزۈش_قىممىتى in 명세["files"]:
            يول = تەكشۈرۈش_يول(كىرگۈزۈش_قىممىتى["path"])
            if يول in 파일들 or not 0 <= كىرگۈزۈش_قىممىتى["size"] <= 16384:
                raise ValueError("중복 يول 또는 ھۆججەت چوڭلۇقى 초과")
            مەلۇمات = ئېقىم_قىممىتى.정확히읽기(كىرگۈزۈش_قىممىتى["size"])
            if 지문(مەلۇمات) != كىرگۈزۈش_قىممىتى["sha256"]:
                raise ValueError("توپلام ھۆججەت SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(مەلۇمات.decode("utf-8"), يول, "exec")
            파일들[يول] = مەلۇمات
            gc.collect()
        return 명세, 파일들
    finally:
        مەشغۇلات_سىستېمىسى.udp_close(종단)


def قاچىلاش_قىممىتى(요청, 접속번호):
    print("توپلام چۈشۈرۈش:", 요청)
    명세, 파일들 = چۈشۈرۈش(요청, 접속번호)
    كىرگۈزۈش_تىزىم = 목록읽기()
    ئاتى = 명세["name"]
    if ئاتى in كىرگۈزۈش_تىزىم:
        if كىرگۈزۈش_تىزىم[ئاتى]["version"] == 명세["version"]:
            for يول, 지문값 in كىرگۈزۈش_تىزىم[ئاتى]["files"].items():
                if مەشغۇلات_سىستېمىسى.path_kind(يول) != 1 or 지문(مەشغۇلات_سىستېمىسى.read(يول)) != 지문값:
                    raise ValueError("설치된 توپلام 파일이 달라졌습니다: " + يول)
            print("이미 설치됨:", ئاتى, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ئارقىغا_قىممىتى 설치하십시오.")
    for يول in 파일들:
        if مەشغۇلات_سىستېمىسى.path_kind(يول):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + يول)
    كىرگۈزۈش_تىزىم[ئاتى] = {"version": 명세["version"], "files": {يول: 지문(مەلۇمات) for يول, مەلۇمات in 파일들.items()}}
    새목록 = json.dumps(كىرگۈزۈش_تىزىم).encode()
    if len(새목록) > 16384:
        raise ValueError("توپلام كىرگۈزۈش_تىزىم چوڭلۇقى 초과")
    이전목록 = مەشغۇلات_سىستېمىسى.read(تىزىم_يول) if مەشغۇلات_سىستېمىسى.path_kind(تىزىم_يول) else None
    만든파일 = []
    만든폴더 = []
    try:
        for يول, مەلۇمات in 파일들.items():
            부분들 = يول.split("/")
            for 수 in range(2, len(부분들)):
                مۇندەرىجە_قىممىتى = "/".join(부분들[:수])
                종류 = مەشغۇلات_سىستېمىسى.path_kind(مۇندەرىجە_قىممىتى)
                if 종류 == 0:
                    مەشغۇلات_سىستېمىسى.mkdir(مۇندەرىجە_قىممىتى)
                    만든폴더.append(مۇندەرىجە_قىممىتى)
                elif 종류 != 2:
                    raise ValueError("مۇندەرىجە_قىممىتى 경로에 파일이 있습니다: " + مۇندەرىجە_قىممىتى)
            만든파일.append(يول)
            يازماق_خاتىرە(يول, مەلۇمات)
        يازماق_خاتىرە(تىزىم_يول, 새목록)
    except Exception:
        for يول in 만든파일:
            if مەشغۇلات_سىستېمىسى.path_kind(يول):
                مەشغۇلات_سىستېمىسى.remove(يول)
        for مۇندەرىجە_قىممىتى in reversed(만든폴더):
            مەشغۇلات_سىستېمىسى.rmdir(مۇندەرىجە_قىممىتى)
        if 이전목록 is not None:
            يازماق_خاتىرە(تىزىم_يول, 이전목록)
        elif مەشغۇلات_سىستېمىسى.path_kind(تىزىم_يول):
            مەشغۇلات_سىستېمىسى.remove(تىزىم_يول)
        raise
    print("قاچىلاش_قىممىتى 완료:", ئاتى, 명세["version"], "→ /lib (RAM)")


def چىقىرىۋەتمەك_كىرگۈزۈش(ئاتى):
    كىرگۈزۈش_تىزىم = 목록읽기()
    if ئاتى not in كىرگۈزۈش_تىزىم:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ئاتى)
    for يول, 지문값 in كىرگۈزۈش_تىزىم[ئاتى]["files"].items():
        if مەشغۇلات_سىستېمىسى.path_kind(يول) != 1 or 지문(مەشغۇلات_سىستېمىسى.read(يول)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + يول)
    for يول in كىرگۈزۈش_تىزىم[ئاتى]["files"]:
        مەشغۇلات_سىستېمىسى.remove(يول)
    del كىرگۈزۈش_تىزىم[ئاتى]
    يازماق_خاتىرە(تىزىم_يول, json.dumps(كىرگۈزۈش_تىزىم).encode())
    print("چىقىرىۋەتمەك_كىرگۈزۈش 완료:", ئاتى)


def ئىجرا_قىل_2(ئۆزگەرگۈچىلەر):
    접속번호 = 8027
    if len(ئۆزگەرگۈچىلەر) >= 2 and ئۆزگەرگۈچىلەر[-2] == "--port":
        접속번호 = int(ئۆزگەرگۈچىلەر[-1])
        ئۆزگەرگۈچىلەر = ئۆزگەرگۈچىلەر[:-2]
    if ئۆزگەرگۈچىلەر == ["list"]:
        for ئاتى, سىستېما_ئۇچۇرى in 목록읽기().items():
            print(ئاتى, سىستېما_ئۇچۇرى["version"])
    elif len(ئۆزگەرگۈچىلەر) == 2 and ئۆزگەرگۈچىلەر[0] == "install":
        قاچىلاش_قىممىتى(ئۆزگەرگۈچىلەر[1], 접속번호)
    elif len(ئۆزگەرگۈچىلەر) == 2 and ئۆزگەرگۈچىلەر[0] == "uninstall":
        چىقىرىۋەتمەك_كىرگۈزۈش(ئۆزگەرگۈچىلەر[1])
    elif not ئۆزگەرگۈچىلەر or ئۆزگەرگۈچىلەر in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython مەنبە_دەرەخ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ئاتى[==버전] [--port 8027] | pip list | pip uninstall ئاتى")
        print("باقار: قوراللار/ئىجرا_قىلىش_بۇيرۇق.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ئىجرا_قىل_2(sys.argv[1:])
    except Exception as خاتالىق:
        print("توپلام خاتالىق:", خاتالىق)
        sys.exit(1)
