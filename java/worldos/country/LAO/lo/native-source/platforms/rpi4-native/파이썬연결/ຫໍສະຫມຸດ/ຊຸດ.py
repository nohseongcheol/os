"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 ໂຮສ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ລະບົບປະຕິບັດການ

ລາຍຊື່_ທາງໂຄຈອນ = "/lib/.pip.json"


def 지문(ຂໍ້ມູນ):
    return "".join("%02x" % ຄ່າ for ຄ່າ in hashlib.sha256(ຂໍ້ມູນ).digest())


def 목록읽기():
    if ລະບົບປະຕິບັດການ.path_kind(ລາຍຊື່_ທາງໂຄຈອນ) == 0:
        return {}
    return json.loads(ລະບົບປະຕິບັດການ.read(ລາຍຊື່_ທາງໂຄຈອນ).decode("utf-8"))


def ຂຽນ_ບັນທຶກ(ທາງໂຄຈອນ, ຂໍ້ມູນ):
    if ລະບົບປະຕິບັດການ.write(ທາງໂຄຈອນ, ຂໍ້ມູນ) != len(ຂໍ້ມູນ):
        raise OSError(28)


def ເຊັກເງິນ_ທາງໂຄຈອນ(ທາງໂຄຈອນ):
    if not isinstance(ທາງໂຄຈອນ, str) or not ທາງໂຄຈອນ.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ທາງໂຄຈອນ.split("/")):
        raise ValueError("허용하지 않는 ຊຸດ ທາງໂຄຈອນ")
    if "\\" in ທາງໂຄຈອນ or any(ord(ຕົວອັກສອນ_ຄ່າ) < 32 or ord(ຕົວອັກສອນ_ຄ່າ) == 127 for ຕົວອັກສອນ_ຄ່າ in ທາງໂຄຈອນ):
        raise ValueError("잘못된 ທາງໂຄຈອນ 문자")
    ມາດຕະການ = "/lib/" + ທາງໂຄຈອນ
    if len(ມາດຕະການ.encode("utf-8")) > 63 or ທາງໂຄຈອນ in ("한국어.py", "ຊຸດ.py"):
        raise ValueError("ຊຸດ 경로가 너무 길거나 ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ 라이브러리와 겹칩니다.")
    return ມາດຕະການ


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ແລ່ນ = ລະບົບປະຕິບັດການ.ticks_ms()

    def 정확히읽기(자신, ຄວາມຍາວ_ຄ່າ):
        ຂໍ້ມູນ = bytearray()
        while len(ຂໍ້ມູນ) < ຄວາມຍາວ_ຄ່າ:
            if ລະບົບປະຕິບັດການ.ticks_ms() - 자신.ແລ່ນ > 90000:
                raise ValueError("ຊຸດ 중계 ຕອບກັບ ເວລາ_ຄ່າ 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ລະບົບປະຕິບັດການ.tcp_read(자신.종단, 512)
                except OSError as ຂໍ້ຜິດພາດ:
                    if ຂໍ້ຜິດພາດ.args[0] != 11:
                        raise
                    ລະບົບປະຕິບັດການ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ຊຸດ 전송이 중간에 끝났습니다.")
            개수 = min(ຄວາມຍາວ_ຄ່າ - len(ຂໍ້ມູນ), len(자신.남은자료))
            ຂໍ້ມູນ.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ລະບົບປະຕິບັດການ.sleep_ms(0)
        return bytes(ຂໍ້ມູນ)


def ດາວໂຫຼດ(요청, ຫມາຍເລກພອດ):
    if len(요청) > 96 or any(ຕົວອັກສອນ_ຄ່າ not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ຕົວອັກສອນ_ຄ່າ in 요청):
        raise ValueError("사용법: pip install ຊື່ 또는 ຊື່==버전")
    종단 = ລະບົບປະຕິບັດການ.tcp_open()
    try:
        ແລ່ນ = ລະບົບປະຕິບັດການ.ticks_ms()
        while True:
            try:
                ລະບົບປະຕິບັດການ.tcp_connect(종단, "10.0.2.2", ຫມາຍເລກພອດ)
                break
            except OSError as ຂໍ້ຜິດພາດ:
                if ຂໍ້ຜິດພາດ.args[0] not in (11, 115) or ລະບົບປະຕິບັດການ.ticks_ms() - ແລ່ນ > 5000:
                    raise ValueError("ຊຸດ 중계 ເຊື່ອມຕໍ່ ຫຼົ້ມເຫຼວ_ຄ່າ: 호스트에서 --network --pip로 실행하십시오.")
                ລະບົບປະຕິບັດການ.sleep_ms(10)
        ຂໍ້ມູນ = (요청 + "\n").encode()
        while ຂໍ້ມູນ:
            try:
                개수 = ລະບົບປະຕິບັດການ.tcp_write(종단, ຂໍ້ມູນ)
                if not 개수:
                    raise ValueError("ຊຸດ 요청 ໂອນ_ຄ່າ ຫຼົ້ມເຫຼວ_ຄ່າ")
                ຂໍ້ມູນ = ຂໍ້ມູນ[개수:]
            except OSError as ຂໍ້ຜິດພາດ:
                if ຂໍ້ຜິດພາດ.args[0] != 11:
                    raise
                ລະບົບປະຕິບັດການ.sleep_ms(10)
                if ລະບົບປະຕິບັດການ.ticks_ms() - ແລ່ນ > 10000:
                    raise ValueError("ຊຸດ 요청 ໂອນ_ຄ່າ ເວລາ_ຄ່າ 초과")
        ສະຕຣີມ_ຄ່າ = 수신흐름(종단)
        머리 = ສະຕຣີມ_ຄ່າ.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ຊຸດ ໂອນ_ຄ່າ ສັນຍາ_ຄ່າ 불일치")
        ຄວາມຍາວ_ຄ່າ = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ຄວາມຍາວ_ຄ່າ > 8192:
            raise ValueError("ຊຸດ 명세가 너무 큽니다.")
        명세 = json.loads(ສະຕຣີມ_ຄ່າ.정확히읽기(ຄວາມຍາວ_ຄ່າ).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 파일은 1~16개여야 합니다.")
        if sum(ເຂົ້າໃນ_ຄ່າ["size"] for ເຂົ້າໃນ_ຄ່າ in 명세["files"]) > 65536:
            raise ValueError("ຊຸດ ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ເຂົ້າໃນ_ຄ່າ in 명세["files"]:
            ທາງໂຄຈອນ = ເຊັກເງິນ_ທາງໂຄຈອນ(ເຂົ້າໃນ_ຄ່າ["path"])
            if ທາງໂຄຈອນ in 파일들 or not 0 <= ເຂົ້າໃນ_ຄ່າ["size"] <= 16384:
                raise ValueError("중복 ທາງໂຄຈອນ 또는 ຟາຍ ຂະ_ຫນາດ 초과")
            ຂໍ້ມູນ = ສະຕຣີມ_ຄ່າ.정확히읽기(ເຂົ້າໃນ_ຄ່າ["size"])
            if 지문(ຂໍ້ມູນ) != ເຂົ້າໃນ_ຄ່າ["sha256"]:
                raise ValueError("ຊຸດ ຟາຍ SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(ຂໍ້ມູນ.decode("utf-8"), ທາງໂຄຈອນ, "exec")
            파일들[ທາງໂຄຈອນ] = ຂໍ້ມູນ
            gc.collect()
        return 명세, 파일들
    finally:
        ລະບົບປະຕິບັດການ.udp_close(종단)


def ຕິດຕັ້ງ_ຄ່າ(요청, ຫມາຍເລກພອດ):
    print("ຊຸດ ດາວໂຫຼດ:", 요청)
    명세, 파일들 = ດາວໂຫຼດ(요청, ຫມາຍເລກພອດ)
    ເຂົ້າໃນ_ລາຍຊື່ = 목록읽기()
    ຊື່ = 명세["name"]
    if ຊື່ in ເຂົ້າໃນ_ລາຍຊື່:
        if ເຂົ້າໃນ_ລາຍຊື່[ຊື່]["version"] == 명세["version"]:
            for ທາງໂຄຈອນ, 지문값 in ເຂົ້າໃນ_ລາຍຊື່[ຊື່]["files"].items():
                if ລະບົບປະຕິບັດການ.path_kind(ທາງໂຄຈອນ) != 1 or 지문(ລະບົບປະຕິບັດການ.read(ທາງໂຄຈອນ)) != 지문값:
                    raise ValueError("설치된 ຊຸດ 파일이 달라졌습니다: " + ທາງໂຄຈອນ)
            print("이미 설치됨:", ຊື່, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ກັບ_ຄືນ_ຄ່າ 설치하십시오.")
    for ທາງໂຄຈອນ in 파일들:
        if ລະບົບປະຕິບັດການ.path_kind(ທາງໂຄຈອນ):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ທາງໂຄຈອນ)
    ເຂົ້າໃນ_ລາຍຊື່[ຊື່] = {"version": 명세["version"], "files": {ທາງໂຄຈອນ: 지문(ຂໍ້ມູນ) for ທາງໂຄຈອນ, ຂໍ້ມູນ in 파일들.items()}}
    새목록 = json.dumps(ເຂົ້າໃນ_ລາຍຊື່).encode()
    if len(새목록) > 16384:
        raise ValueError("ຊຸດ ເຂົ້າໃນ_ລາຍຊື່ ຂະ_ຫນາດ 초과")
    이전목록 = ລະບົບປະຕິບັດການ.read(ລາຍຊື່_ທາງໂຄຈອນ) if ລະບົບປະຕິບັດການ.path_kind(ລາຍຊື່_ທາງໂຄຈອນ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ທາງໂຄຈອນ, ຂໍ້ມູນ in 파일들.items():
            부분들 = ທາງໂຄຈອນ.split("/")
            for 수 in range(2, len(부분들)):
                ກຸ່ມຂໍ້ມູນ_ຄ່າ = "/".join(부분들[:수])
                종류 = ລະບົບປະຕິບັດການ.path_kind(ກຸ່ມຂໍ້ມູນ_ຄ່າ)
                if 종류 == 0:
                    ລະບົບປະຕິບັດການ.mkdir(ກຸ່ມຂໍ້ມູນ_ຄ່າ)
                    만든폴더.append(ກຸ່ມຂໍ້ມູນ_ຄ່າ)
                elif 종류 != 2:
                    raise ValueError("ກຸ່ມຂໍ້ມູນ_ຄ່າ 경로에 파일이 있습니다: " + ກຸ່ມຂໍ້ມູນ_ຄ່າ)
            만든파일.append(ທາງໂຄຈອນ)
            ຂຽນ_ບັນທຶກ(ທາງໂຄຈອນ, ຂໍ້ມູນ)
        ຂຽນ_ບັນທຶກ(ລາຍຊື່_ທາງໂຄຈອນ, 새목록)
    except Exception:
        for ທາງໂຄຈອນ in 만든파일:
            if ລະບົບປະຕິບັດການ.path_kind(ທາງໂຄຈອນ):
                ລະບົບປະຕິບັດການ.remove(ທາງໂຄຈອນ)
        for ກຸ່ມຂໍ້ມູນ_ຄ່າ in reversed(만든폴더):
            ລະບົບປະຕິບັດການ.rmdir(ກຸ່ມຂໍ້ມູນ_ຄ່າ)
        if 이전목록 is not None:
            ຂຽນ_ບັນທຶກ(ລາຍຊື່_ທາງໂຄຈອນ, 이전목록)
        elif ລະບົບປະຕິບັດການ.path_kind(ລາຍຊື່_ທາງໂຄຈອນ):
            ລະບົບປະຕິບັດການ.remove(ລາຍຊື່_ທາງໂຄຈອນ)
        raise
    print("ຕິດຕັ້ງ_ຄ່າ 완료:", ຊື່, 명세["version"], "→ /lib (RAM)")


def 제거(ຊື່):
    ເຂົ້າໃນ_ລາຍຊື່ = 목록읽기()
    if ຊື່ not in ເຂົ້າໃນ_ລາຍຊື່:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ຊື່)
    for ທາງໂຄຈອນ, 지문값 in ເຂົ້າໃນ_ລາຍຊື່[ຊື່]["files"].items():
        if ລະບົບປະຕິບັດການ.path_kind(ທາງໂຄຈອນ) != 1 or 지문(ລະບົບປະຕິບັດການ.read(ທາງໂຄຈອນ)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ທາງໂຄຈອນ)
    for ທາງໂຄຈອນ in ເຂົ້າໃນ_ລາຍຊື່[ຊື່]["files"]:
        ລະບົບປະຕິບັດການ.remove(ທາງໂຄຈອນ)
    del ເຂົ້າໃນ_ລາຍຊື່[ຊື່]
    ຂຽນ_ບັນທຶກ(ລາຍຊື່_ທາງໂຄຈອນ, json.dumps(ເຂົ້າໃນ_ລາຍຊື່).encode())
    print("제거 완료:", ຊື່)


def ແລ່ນ(인수):
    ຫມາຍເລກພອດ = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        ຫມາຍເລກພອດ = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for ຊື່, ລະບົບ_ຂໍ້_ມູນ in 목록읽기().items():
            print(ຊື່, ລະບົບ_ຂໍ້_ມູນ["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ຕິດຕັ້ງ_ຄ່າ(인수[1], ຫມາຍເລກພອດ)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        제거(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 설치기 (PyPA pip 전체가 아님)")
        print("pip install ຊື່[==버전] [--port 8027] | pip list | pip uninstall ຊື່")
        print("ໂຮສ: ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ແລ່ນ(sys.argv[1:])
    except Exception as ຂໍ້ຜິດພາດ:
        print("ຊຸດ ຂໍ້ຜິດພາດ:", ຂໍ້ຜິດພາດ)
        sys.exit(1)
