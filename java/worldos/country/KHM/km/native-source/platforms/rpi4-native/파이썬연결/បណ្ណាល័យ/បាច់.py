"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ហូស 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ប្រព័ន្ធប្រតិបត្តិការណ៏

បញ្ជី_ផ្លូវ = "/lib/.pip.json"


def 지문(ទិន្នន័យ):
    return "".join("%02x" % តំលៃ for តំលៃ in hashlib.sha256(ទិន្នន័យ).digest())


def 목록읽기():
    if ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(បញ្ជី_ផ្លូវ) == 0:
        return {}
    return json.loads(ប្រព័ន្ធប្រតិបត្តិការណ៏.read(បញ្ជី_ផ្លូវ).decode("utf-8"))


def សរសេរ_កំណត់_ហេតុ(ផ្លូវ, ទិន្នន័យ):
    if ប្រព័ន្ធប្រតិបត្តិការណ៏.write(ផ្លូវ, ទិន្នន័យ) != len(ទិន្នន័យ):
        raise OSError(28)


def ត្រួតពិនិត្យ_ផ្លូវ(ផ្លូវ):
    if not isinstance(ផ្លូវ, str) or not ផ្លូវ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ផ្លូវ.split("/")):
        raise ValueError("허용하지 않는 បាច់ ផ្លូវ")
    if "\\" in ផ្លូវ or any(ord(តួអក្សរ_តំលៃ) < 32 or ord(តួអក្សរ_តំលៃ) == 127 for តួអក្សរ_តំលៃ in ផ្លូវ):
        raise ValueError("잘못된 ផ្លូវ 문자")
    ការវាស់វែង = "/lib/" + ផ្លូវ
    if len(ការវាស់វែង.encode("utf-8")) > 63 or ផ្លូវ in ("한국어.py", "បាច់.py"):
        raise ValueError("បាច់ 경로가 너무 길거나 តំលៃស្វ័យប្រវត្តិ 라이브러리와 겹칩니다.")
    return ការវាស់វែង


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.រត់ = ប្រព័ន្ធប្រតិបត្តិការណ៏.ticks_ms()

    def 정확히읽기(자신, ប្រវែង_តំលៃ):
        ទិន្នន័យ = bytearray()
        while len(ទិន្នន័យ) < ប្រវែង_តំលៃ:
            if ប្រព័ន្ធប្រតិបត្តិការណ៏.ticks_ms() - 자신.រត់ > 90000:
                raise ValueError("បាច់ 중계 ឆ្លើយតប ពេល_វេលា_តំលៃ 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ប្រព័ន្ធប្រតិបត្តិការណ៏.tcp_read(자신.종단, 512)
                except OSError as កំហុស:
                    if កំហុស.args[0] != 11:
                        raise
                    ប្រព័ន្ធប្រតិបត្តិការណ៏.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("បាច់ 전송이 중간에 끝났습니다.")
            개수 = min(ប្រវែង_តំលៃ - len(ទិន្នន័យ), len(자신.남은자료))
            ទិន្នន័យ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ប្រព័ន្ធប្រតិបត្តិការណ៏.sleep_ms(0)
        return bytes(ទិន្នន័យ)


def ទាញយក(요청, លេខរន្ធ):
    if len(요청) > 96 or any(តួអក្សរ_តំលៃ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for តួអក្សរ_តំលៃ in 요청):
        raise ValueError("사용법: pip install ឈ្មោះ 또는 ឈ្មោះ==버전")
    종단 = ប្រព័ន្ធប្រតិបត្តិការណ៏.tcp_open()
    try:
        រត់ = ប្រព័ន្ធប្រតិបត្តិការណ៏.ticks_ms()
        while True:
            try:
                ប្រព័ន្ធប្រតិបត្តិការណ៏.tcp_connect(종단, "10.0.2.2", លេខរន្ធ)
                break
            except OSError as កំហុស:
                if កំហុស.args[0] not in (11, 115) or ប្រព័ន្ធប្រតិបត្តិការណ៏.ticks_ms() - រត់ > 5000:
                    raise ValueError("បាច់ 중계 ភ្ជាប់ បរាជ័យ_តំលៃ: 호스트에서 --network --pip로 실행하십시오.")
                ប្រព័ន្ធប្រតិបត្តិការណ៏.sleep_ms(10)
        ទិន្នន័យ = (요청 + "\n").encode()
        while ទិន្នន័យ:
            try:
                개수 = ប្រព័ន្ធប្រតិបត្តិការណ៏.tcp_write(종단, ទិន្នន័យ)
                if not 개수:
                    raise ValueError("បាច់ 요청 ផ្ទេរ_តំលៃ បរាជ័យ_តំលៃ")
                ទិន្នន័យ = ទិន្នន័យ[개수:]
            except OSError as កំហុស:
                if កំហុស.args[0] != 11:
                    raise
                ប្រព័ន្ធប្រតិបត្តិការណ៏.sleep_ms(10)
                if ប្រព័ន្ធប្រតិបត្តិការណ៏.ticks_ms() - រត់ > 10000:
                    raise ValueError("បាច់ 요청 ផ្ទេរ_តំលៃ ពេល_វេលា_តំលៃ 초과")
        ស្ទ្រីម_តំលៃ = 수신흐름(종단)
        머리 = ស្ទ្រីម_តំលៃ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("បាច់ ផ្ទេរ_តំលៃ ករណី_តំលៃ 불일치")
        ប្រវែង_តំលៃ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ប្រវែង_តំលៃ > 8192:
            raise ValueError("បាច់ 명세가 너무 큽니다.")
        명세 = json.loads(ស្ទ្រីម_តំលៃ.정확히읽기(ប្រវែង_តំលៃ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ប្រភព_មែកធាង 파일은 1~16개여야 합니다.")
        if sum(ការបញ្ចូល_តំលៃ["size"] for ការបញ្ចូល_តំលៃ in 명세["files"]) > 65536:
            raise ValueError("បាច់ ប្រភព_មែកធាង 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ការបញ្ចូល_តំលៃ in 명세["files"]:
            ផ្លូវ = ត្រួតពិនិត្យ_ផ្លូវ(ការបញ្ចូល_តំលៃ["path"])
            if ផ្លូវ in 파일들 or not 0 <= ការបញ្ចូល_តំលៃ["size"] <= 16384:
                raise ValueError("중복 ផ្លូវ 또는 ឯកសារ ដាក់ទំហំ 초과")
            ទិន្នន័យ = ស្ទ្រីម_តំលៃ.정확히읽기(ការបញ្ចូល_តំលៃ["size"])
            if 지문(ទិន្នន័យ) != ការបញ្ចូល_តំលៃ["sha256"]:
                raise ValueError("បាច់ ឯកសារ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ទិន្នន័យ.decode("utf-8"), ផ្លូវ, "exec")
            파일들[ផ្លូវ] = ទិន្នន័យ
            gc.collect()
        return 명세, 파일들
    finally:
        ប្រព័ន្ធប្រតិបត្តិការណ៏.udp_close(종단)


def ដំឡើង_តំលៃ(요청, លេខរន្ធ):
    print("បាច់ ទាញយក:", 요청)
    명세, 파일들 = ទាញយក(요청, លេខរន្ធ)
    ការបញ្ចូល_បញ្ជី = 목록읽기()
    ឈ្មោះ = 명세["name"]
    if ឈ្មោះ in ការបញ្ចូល_បញ្ជី:
        if ការបញ្ចូល_បញ្ជី[ឈ្មោះ]["version"] == 명세["version"]:
            for ផ្លូវ, 지문값 in ការបញ្ចូល_បញ្ជី[ឈ្មោះ]["files"].items():
                if ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(ផ្លូវ) != 1 or 지문(ប្រព័ន្ធប្រតិបត្តិការណ៏.read(ផ្លូវ)) != 지문값:
                    raise ValueError("설치된 បាច់ 파일이 달라졌습니다: " + ផ្លូវ)
            print("이미 설치됨:", ឈ្មោះ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ការថយ_តំលៃ 설치하십시오.")
    for ផ្លូវ in 파일들:
        if ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(ផ្លូវ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ផ្លូវ)
    ការបញ្ចូល_បញ្ជី[ឈ្មោះ] = {"version": 명세["version"], "files": {ផ្លូវ: 지문(ទិន្នន័យ) for ផ្លូវ, ទិន្នន័យ in 파일들.items()}}
    새목록 = json.dumps(ការបញ្ចូល_បញ្ជី).encode()
    if len(새목록) > 16384:
        raise ValueError("បាច់ ការបញ្ចូល_បញ្ជី ដាក់ទំហំ 초과")
    이전목록 = ប្រព័ន្ធប្រតិបត្តិការណ៏.read(បញ្ជី_ផ្លូវ) if ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(បញ្ជី_ផ្លូវ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ផ្លូវ, ទិន្នន័យ in 파일들.items():
            부분들 = ផ្លូវ.split("/")
            for 수 in range(2, len(부분들)):
                បញ្ជី_តំលៃ = "/".join(부분들[:수])
                종류 = ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(បញ្ជី_តំលៃ)
                if 종류 == 0:
                    ប្រព័ន្ធប្រតិបត្តិការណ៏.mkdir(បញ្ជី_តំលៃ)
                    만든폴더.append(បញ្ជី_តំលៃ)
                elif 종류 != 2:
                    raise ValueError("បញ្ជី_តំលៃ 경로에 파일이 있습니다: " + បញ្ជី_តំលៃ)
            만든파일.append(ផ្លូវ)
            សរសេរ_កំណត់_ហេតុ(ផ្លូវ, ទិន្នន័យ)
        សរសេរ_កំណត់_ហេតុ(បញ្ជី_ផ្លូវ, 새목록)
    except Exception:
        for ផ្លូវ in 만든파일:
            if ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(ផ្លូវ):
                ប្រព័ន្ធប្រតិបត្តិការណ៏.remove(ផ្លូវ)
        for បញ្ជី_តំលៃ in reversed(만든폴더):
            ប្រព័ន្ធប្រតិបត្តិការណ៏.rmdir(បញ្ជី_តំលៃ)
        if 이전목록 is not None:
            សរសេរ_កំណត់_ហេតុ(បញ្ជី_ផ្លូវ, 이전목록)
        elif ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(បញ្ជី_ផ្លូវ):
            ប្រព័ន្ធប្រតិបត្តិការណ៏.remove(បញ្ជី_ផ្លូវ)
        raise
    print("ដំឡើង_តំលៃ 완료:", ឈ្មោះ, 명세["version"], "→ /lib (RAM)")


def យកចេញ_ការបញ្ចូល(ឈ្មោះ):
    ការបញ្ចូល_បញ្ជី = 목록읽기()
    if ឈ្មោះ not in ការបញ្ចូល_បញ្ជី:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ឈ្មោះ)
    for ផ្លូវ, 지문값 in ការបញ្ចូល_បញ្ជី[ឈ្មោះ]["files"].items():
        if ប្រព័ន្ធប្រតិបត្តិការណ៏.path_kind(ផ្លូវ) != 1 or 지문(ប្រព័ន្ធប្រតិបត្តិការណ៏.read(ផ្លូវ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ផ្លូវ)
    for ផ្លូវ in ការបញ្ចូល_បញ្ជី[ឈ្មោះ]["files"]:
        ប្រព័ន្ធប្រតិបត្តិការណ៏.remove(ផ្លូវ)
    del ការបញ្ចូល_បញ្ជី[ឈ្មោះ]
    សរសេរ_កំណត់_ហេតុ(បញ្ជី_ផ្លូវ, json.dumps(ការបញ្ចូល_បញ្ជី).encode())
    print("យកចេញ_ការបញ្ចូល 완료:", ឈ្មោះ)


def រត់(អាគុយម៉ង់):
    លេខរន្ធ = 8027
    if len(អាគុយម៉ង់) >= 2 and អាគុយម៉ង់[-2] == "--port":
        លេខរន្ធ = int(អាគុយម៉ង់[-1])
        អាគុយម៉ង់ = អាគុយម៉ង់[:-2]
    if អាគុយម៉ង់ == ["list"]:
        for ឈ្មោះ, ប្រព័ន្ធព័ត៌មាន in 목록읽기().items():
            print(ឈ្មោះ, ប្រព័ន្ធព័ត៌មាន["version"])
    elif len(អាគុយម៉ង់) == 2 and អាគុយម៉ង់[0] == "install":
        ដំឡើង_តំលៃ(អាគុយម៉ង់[1], លេខរន្ធ)
    elif len(អាគុយម៉ង់) == 2 and អាគុយម៉ង់[0] == "uninstall":
        យកចេញ_ការបញ្ចូល(អាគុយម៉ង់[1])
    elif not អាគុយម៉ង់ or អាគុយម៉ង់ in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ប្រភព_មែកធាង 설치기 (PyPA pip 전체가 아님)")
        print("pip install ឈ្មោះ[==버전] [--port 8027] | pip list | pip uninstall ឈ្មោះ")
        print("ហូស: ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        រត់(sys.argv[1:])
    except Exception as កំហុស:
        print("បាច់ កំហុស:", កំហុស)
        sys.exit(1)
