"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 హోస్ట్ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as నిర్వహణా_వ్యవస్థ

జాబితా_పథం = "/lib/.pip.json"


def 지문(డేటా):
    return "".join("%02x" % మూల్యం for మూల్యం in hashlib.sha256(డేటా).digest())


def 목록읽기():
    if నిర్వహణా_వ్యవస్థ.path_kind(జాబితా_పథం) == 0:
        return {}
    return json.loads(నిర్వహణా_వ్యవస్థ.read(జాబితా_పథం).decode("utf-8"))


def వ్రాయి_లాగ్(పాత్, డేటా):
    if నిర్వహణా_వ్యవస్థ.write(పాత్, డేటా) != len(డేటా):
        raise OSError(28)


def తనిఖీ_పథం(పాత్):
    if not isinstance(పాత్, str) or not పాత్.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in పాత్.split("/")):
        raise ValueError("허용하지 않는 బండిల్ పాత్")
    if "\\" in పాత్ or any(ord(అక్షరం_మూల్యం) < 32 or ord(అక్షరం_మూల్యం) == 127 for అక్షరం_మూల్యం in పాత్):
        raise ValueError("잘못된 పాత్ 문자")
    ప్రమాణం = "/lib/" + పాత్
    if len(ప్రమాణం.encode("utf-8")) > 63 or పాత్ in ("한국어.py", "బండిల్.py"):
        raise ValueError("బండిల్ 경로가 너무 길거나 స్వయంసిద్ధ_విలువ 라이브러리와 겹칩니다.")
    return ప్రమాణం


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.నడుపుము = నిర్వహణా_వ్యవస్థ.ticks_ms()

    def 정확히읽기(자신, పొడవు_మూల్యం):
        డేటా = bytearray()
        while len(డేటా) < పొడవు_మూల్యం:
            if నిర్వహణా_వ్యవస్థ.ticks_ms() - 자신.నడుపుము > 90000:
                raise ValueError("బండిల్ 중계 ప్రత్యుత్తరం_ఇవ్వు సమయం_మూల్యం 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = నిర్వహణా_వ్యవస్థ.tcp_read(자신.종단, 512)
                except OSError as దోషం:
                    if దోషం.args[0] != 11:
                        raise
                    నిర్వహణా_వ్యవస్థ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("బండిల్ 전송이 중간에 끝났습니다.")
            개수 = min(పొడవు_మూల్యం - len(డేటా), len(자신.남은자료))
            డేటా.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            నిర్వహణా_వ్యవస్థ.sleep_ms(0)
        return bytes(డేటా)


def దిగుమతి(요청, పోర్ట్_సంఖ్య):
    if len(요청) > 96 or any(అక్షరం_మూల్యం not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for అక్షరం_మూల్యం in 요청):
        raise ValueError("사용법: pip install పేరు 또는 పేరు==버전")
    종단 = నిర్వహణా_వ్యవస్థ.tcp_open()
    try:
        నడుపుము = నిర్వహణా_వ్యవస్థ.ticks_ms()
        while True:
            try:
                నిర్వహణా_వ్యవస్థ.tcp_connect(종단, "10.0.2.2", పోర్ట్_సంఖ్య)
                break
            except OSError as దోషం:
                if దోషం.args[0] not in (11, 115) or నిర్వహణా_వ్యవస్థ.ticks_ms() - నడుపుము > 5000:
                    raise ValueError("బండిల్ 중계 కనెక్టుచేయి వైఫల్యం_మూల్యం: 호스트에서 --network --pip로 실행하십시오.")
                నిర్వహణా_వ్యవస్థ.sleep_ms(10)
        డేటా = (요청 + "\n").encode()
        while డేటా:
            try:
                개수 = నిర్వహణా_వ్యవస్థ.tcp_write(종단, డేటా)
                if not 개수:
                    raise ValueError("బండిల్ 요청 బదిలీ_మూల్యం వైఫల్యం_మూల్యం")
                డేటా = డేటా[개수:]
            except OSError as దోషం:
                if దోషం.args[0] != 11:
                    raise
                నిర్వహణా_వ్యవస్థ.sleep_ms(10)
                if నిర్వహణా_వ్యవస్థ.ticks_ms() - నడుపుము > 10000:
                    raise ValueError("బండిల్ 요청 బదిలీ_మూల్యం సమయం_మూల్యం 초과")
        ధార_మూల్యం = 수신흐름(종단)
        머리 = ధార_మూల్యం.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("బండిల్ బదిలీ_మూల్యం పని_మూల్యం_102996da 불일치")
        పొడవు_మూల్యం = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if పొడవు_మూల్యం > 8192:
            raise ValueError("బండిల్ 명세가 너무 큽니다.")
        명세 = json.loads(ధార_మూల్యం.정확히읽기(పొడవు_మూల్యం).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 మూలం_వృక్షాకృతి 파일은 1~16개여야 합니다.")
        if sum(ప్రవేశం_మూల్యం["size"] for ప్రవేశం_మూల్యం in 명세["files"]) > 65536:
            raise ValueError("బండిల్ మూలం_వృక్షాకృతి 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ప్రవేశం_మూల్యం in 명세["files"]:
            పాత్ = తనిఖీ_పథం(ప్రవేశం_మూల్యం["path"])
            if పాత్ in 파일들 or not 0 <= ప్రవేశం_మూల్యం["size"] <= 16384:
                raise ValueError("중복 పాత్ 또는 దస్త్రం పరిమాణం 초과")
            డేటా = ధార_మూల్యం.정확히읽기(ప్రవేశం_మూల్యం["size"])
            if 지문(డేటా) != ప్రవేశం_మూల్యం["sha256"]:
                raise ValueError("బండిల్ దస్త్రం SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(డేటా.decode("utf-8"), పాత్, "exec")
            파일들[పాత్] = డేటా
            gc.collect()
        return 명세, 파일들
    finally:
        నిర్వహణా_వ్యవస్థ.udp_close(종단)


def వ్యవస్థాపించు_మూల్యం(요청, పోర్ట్_సంఖ్య):
    print("బండిల్ దిగుమతి:", 요청)
    명세, 파일들 = దిగుమతి(요청, పోర్ట్_సంఖ్య)
    ప్రవేశం_జాబితా = 목록읽기()
    పేరు = 명세["name"]
    if పేరు in ప్రవేశం_జాబితా:
        if ప్రవేశం_జాబితా[పేరు]["version"] == 명세["version"]:
            for పాత్, 지문값 in ప్రవేశం_జాబితా[పేరు]["files"].items():
                if నిర్వహణా_వ్యవస్థ.path_kind(పాత్) != 1 or 지문(నిర్వహణా_వ్యవస్థ.read(పాత్)) != 지문값:
                    raise ValueError("설치된 బండిల్ 파일이 달라졌습니다: " + పాత్)
            print("이미 설치됨:", పేరు, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 వెనుకకు_మూల్యం 설치하십시오.")
    for పాత్ in 파일들:
        if నిర్వహణా_వ్యవస్థ.path_kind(పాత్):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + పాత్)
    ప్రవేశం_జాబితా[పేరు] = {"version": 명세["version"], "files": {పాత్: 지문(డేటా) for పాత్, డేటా in 파일들.items()}}
    새목록 = json.dumps(ప్రవేశం_జాబితా).encode()
    if len(새목록) > 16384:
        raise ValueError("బండిల్ ప్రవేశం_జాబితా పరిమాణం 초과")
    이전목록 = నిర్వహణా_వ్యవస్థ.read(జాబితా_పథం) if నిర్వహణా_వ్యవస్థ.path_kind(జాబితా_పథం) else None
    만든파일 = []
    만든폴더 = []
    try:
        for పాత్, డేటా in 파일들.items():
            부분들 = పాత్.split("/")
            for 수 in range(2, len(부분들)):
                సంచయని_మూల్యం = "/".join(부분들[:수])
                종류 = నిర్వహణా_వ్యవస్థ.path_kind(సంచయని_మూల్యం)
                if 종류 == 0:
                    నిర్వహణా_వ్యవస్థ.mkdir(సంచయని_మూల్యం)
                    만든폴더.append(సంచయని_మూల్యం)
                elif 종류 != 2:
                    raise ValueError("సంచయని_మూల్యం 경로에 파일이 있습니다: " + సంచయని_మూల్యం)
            만든파일.append(పాత్)
            వ్రాయి_లాగ్(పాత్, డేటా)
        వ్రాయి_లాగ్(జాబితా_పథం, 새목록)
    except Exception:
        for పాత్ in 만든파일:
            if నిర్వహణా_వ్యవస్థ.path_kind(పాత్):
                నిర్వహణా_వ్యవస్థ.remove(పాత్)
        for సంచయని_మూల్యం in reversed(만든폴더):
            నిర్వహణా_వ్యవస్థ.rmdir(సంచయని_మూల్యం)
        if 이전목록 is not None:
            వ్రాయి_లాగ్(జాబితా_పథం, 이전목록)
        elif నిర్వహణా_వ్యవస్థ.path_kind(జాబితా_పథం):
            నిర్వహణా_వ్యవస్థ.remove(జాబితా_పథం)
        raise
    print("వ్యవస్థాపించు_మూల్యం 완료:", పేరు, 명세["version"], "→ /lib (RAM)")


def తీసివెయ్యి_ప్రవేశం(పేరు):
    ప్రవేశం_జాబితా = 목록읽기()
    if పేరు not in ప్రవేశం_జాబితా:
        raise ValueError("설치되지 않은 꾸러미입니다: " + పేరు)
    for పాత్, 지문값 in ప్రవేశం_జాబితా[పేరు]["files"].items():
        if నిర్వహణా_వ్యవస్థ.path_kind(పాత్) != 1 or 지문(నిర్వహణా_వ్యవస్థ.read(పాత్)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + పాత్)
    for పాత్ in ప్రవేశం_జాబితా[పేరు]["files"]:
        నిర్వహణా_వ్యవస్థ.remove(పాత్)
    del ప్రవేశం_జాబితా[పేరు]
    వ్రాయి_లాగ్(జాబితా_పథం, json.dumps(ప్రవేశం_జాబితా).encode())
    print("తీసివెయ్యి_ప్రవేశం 완료:", పేరు)


def నడుపుము(인수):
    పోర్ట్_సంఖ్య = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        పోర్ట్_సంఖ్య = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for పేరు, సిస్టమ్_సమాచారం in 목록읽기().items():
            print(పేరు, సిస్టమ్_సమాచారం["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        వ్యవస్థాపించు_మూల్యం(인수[1], పోర్ట్_సంఖ్య)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        తీసివెయ్యి_ప్రవేశం(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython మూలం_వృక్షాకృతి 설치기 (PyPA pip 전체가 아님)")
        print("pip install పేరు[==버전] [--port 8027] | pip list | pip uninstall పేరు")
        print("హోస్ట్: ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        నడుపుము(sys.argv[1:])
    except Exception as దోషం:
        print("బండిల్ దోషం:", దోషం)
        sys.exit(1)
