"""เอง 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 โฮสต์ 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as ระบบปฏิบัติการ

รายการ_พาธ = "/lib/.pip.json"


def 지문(ข้อมูล):
    return "".join("%02x" % ค่า for ค่า in hashlib.sha256(ข้อมูล).digest())


def 목록읽기():
    if ระบบปฏิบัติการ.path_kind(รายการ_พาธ) == 0:
        return {}
    return json.loads(ระบบปฏิบัติการ.read(รายการ_พาธ).decode("utf-8"))


def 기록쓰기(เส้นทาง, ข้อมูล):
    if ระบบปฏิบัติการ.write(เส้นทาง, ข้อมูล) != len(ข้อมูล):
        raise OSError(28)


def เช็ค_พาธ(เส้นทาง):
    if not isinstance(เส้นทาง, str) or not เส้นทาง.endswith(".py"):
        raise ValueError("Python 소스만 설치할 หมายเลข 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in เส้นทาง.split("/")):
        raise ValueError("허용하지 않는 รวม เส้นทาง")
    if "\\" in เส้นทาง or any(ord(อักขระ_ค่า) < 32 or ord(อักขระ_ค่า) == 127 for อักขระ_ค่า in เส้นทาง):
        raise ValueError("잘못된 เส้นทาง 문자")
    ผลลัพธ์ = "/lib/" + เส้นทาง
    if len(ผลลัพธ์.encode("utf-8")) > 63 or เส้นทาง in ("ไทย.py", "รวม.py"):
        raise ValueError("รวม 경로가 너무 길거나 ค่าเริ่มต้น 라이브러리와 겹칩니다.")
    return ผลลัพธ์


class รับ_สตรีม:
    def __init__(자신, ปลายทาง):
        자신.ปลายทาง = ปลายทาง
        자신.남은자료 = b""
        자신.เรียกใช้งาน = ระบบปฏิบัติการ.ticks_ms()

    def 정확히읽기(자신, 길이):
        ข้อมูล = bytearray()
        while len(ข้อมูล) < 길이:
            if ระบบปฏิบัติการ.ticks_ms() - 자신.เรียกใช้งาน > 90000:
                raise ValueError("รวม 중계 ตอบกลับ ค่าเวลา 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = ระบบปฏิบัติการ.tcp_read(자신.ปลายทาง, 512)
                except OSError as ข้อผิดพลาด:
                    if ข้อผิดพลาด.args[0] != 11:
                        raise
                    ระบบปฏิบัติการ.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("รวม 전송이 중간에 끝났습니다.")
            개수 = min(길이 - len(ข้อมูล), len(자신.남은자료))
            ข้อมูล.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            ระบบปฏิบัติการ.sleep_ms(0)
        return bytes(ข้อมูล)


def ดาวน์โหลด(คําขอ, หมายเลขพอร์ต):
    if len(คําขอ) > 96 or any(อักขระ_ค่า not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for อักขระ_ค่า in คําขอ):
        raise ValueError("사용법: pip install ชื่อ 또는 ชื่อ==버전")
    ปลายทาง = ระบบปฏิบัติการ.tcp_open()
    try:
        เรียกใช้งาน = ระบบปฏิบัติการ.ticks_ms()
        while True:
            try:
                ระบบปฏิบัติการ.tcp_connect(ปลายทาง, "10.0.2.2", หมายเลขพอร์ต)
                break
            except OSError as ข้อผิดพลาด:
                if ข้อผิดพลาด.args[0] not in (11, 115) or ระบบปฏิบัติการ.ticks_ms() - เรียกใช้งาน > 5000:
                    raise ValueError("รวม 중계 เชื่อมต่อ ความล้มเหลว_ค่า: 호스트에서 --network --pip로 실행하십시오.")
                ระบบปฏิบัติการ.sleep_ms(10)
        ข้อมูล = (คําขอ + "\n").encode()
        while ข้อมูล:
            try:
                개수 = ระบบปฏิบัติการ.tcp_write(ปลายทาง, ข้อมูล)
                if not 개수:
                    raise ValueError("รวม คําขอ โอน_ค่า ความล้มเหลว_ค่า")
                ข้อมูล = ข้อมูล[개수:]
            except OSError as ข้อผิดพลาด:
                if ข้อผิดพลาด.args[0] != 11:
                    raise
                ระบบปฏิบัติการ.sleep_ms(10)
                if ระบบปฏิบัติการ.ticks_ms() - เรียกใช้งาน > 10000:
                    raise ValueError("รวม คําขอ โอน_ค่า ค่าเวลา 초과")
        สตรีม_ค่า = รับ_สตรีม(ปลายทาง)
        머리 = สตรีม_ค่า.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("รวม โอน_ค่า มูลค่าตามสัญญา 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("รวม 명세가 너무 큽니다.")
        명세 = json.loads(สตรีม_ค่า.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 แหล่ง_ทรี 파일은 1~16개여야 합니다.")
        if sum(รายการ_ค่า["size"] for รายการ_ค่า in 명세["files"]) > 65536:
            raise ValueError("รวม แหล่ง_ทรี 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for รายการ_ค่า in 명세["files"]:
            เส้นทาง = เช็ค_พาธ(รายการ_ค่า["path"])
            if เส้นทาง in 파일들 or not 0 <= รายการ_ค่า["size"] <= 16384:
                raise ValueError("중복 เส้นทาง 또는 แฟ้ม ขนาด 초과")
            ข้อมูล = สตรีม_ค่า.정확히읽기(รายการ_ค่า["size"])
            if 지문(ข้อมูล) != รายการ_ค่า["sha256"]:
                raise ValueError("รวม แฟ้ม SHA-256 불일치")
            # 실행하지 않고 ปัจจุบัน_รายการ MicroPython의 문법으로 먼저 검사한다.
            compile(ข้อมูล.decode("utf-8"), เส้นทาง, "exec")
            파일들[เส้นทาง] = ข้อมูล
            gc.collect()
        return 명세, 파일들
    finally:
        ระบบปฏิบัติการ.udp_close(ปลายทาง)


def ติดตั้ง_ค่า(คําขอ, หมายเลขพอร์ต):
    print("รวม ดาวน์โหลด:", คําขอ)
    명세, 파일들 = ดาวน์โหลด(คําขอ, หมายเลขพอร์ต)
    รายการ_รายการ = 목록읽기()
    ชื่อ = 명세["name"]
    if ชื่อ in รายการ_รายการ:
        if รายการ_รายการ[ชื่อ]["version"] == 명세["version"]:
            for เส้นทาง, 지문값 in รายการ_รายการ[ชื่อ]["files"].items():
                if ระบบปฏิบัติการ.path_kind(เส้นทาง) != 1 or 지문(ระบบปฏิบัติการ.read(เส้นทาง)) != 지문값:
                    raise ValueError("설치된 รวม 파일이 달라졌습니다: " + เส้นทาง)
            print("이미 설치됨:", ชื่อ, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ย้อนกลับ_ค่า 설치하십시오.")
    for เส้นทาง in 파일들:
        if ระบบปฏิบัติการ.path_kind(เส้นทาง):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + เส้นทาง)
    รายการ_รายการ[ชื่อ] = {"version": 명세["version"], "files": {เส้นทาง: 지문(ข้อมูล) for เส้นทาง, ข้อมูล in 파일들.items()}}
    새목록 = json.dumps(รายการ_รายการ).encode()
    if len(새목록) > 16384:
        raise ValueError("รวม รายการ_รายการ ขนาด 초과")
    이전목록 = ระบบปฏิบัติการ.read(รายการ_พาธ) if ระบบปฏิบัติการ.path_kind(รายการ_พาธ) else None
    만든파일 = []
    만든폴더 = []
    try:
        for เส้นทาง, ข้อมูล in 파일들.items():
            부분들 = เส้นทาง.split("/")
            for หมายเลข in range(2, len(부분들)):
                ไดเรกทอรี_ค่า = "/".join(부분들[:หมายเลข])
                종류 = ระบบปฏิบัติการ.path_kind(ไดเรกทอรี_ค่า)
                if 종류 == 0:
                    ระบบปฏิบัติการ.mkdir(ไดเรกทอรี_ค่า)
                    만든폴더.append(ไดเรกทอรี_ค่า)
                elif 종류 != 2:
                    raise ValueError("ไดเรกทอรี_ค่า 경로에 파일이 있습니다: " + ไดเรกทอรี_ค่า)
            만든파일.append(เส้นทาง)
            기록쓰기(เส้นทาง, ข้อมูล)
        기록쓰기(รายการ_พาธ, 새목록)
    except Exception:
        for เส้นทาง in 만든파일:
            if ระบบปฏิบัติการ.path_kind(เส้นทาง):
                ระบบปฏิบัติการ.remove(เส้นทาง)
        for ไดเรกทอรี_ค่า in reversed(만든폴더):
            ระบบปฏิบัติการ.rmdir(ไดเรกทอรี_ค่า)
        if 이전목록 is not None:
            기록쓰기(รายการ_พาธ, 이전목록)
        elif ระบบปฏิบัติการ.path_kind(รายการ_พาธ):
            ระบบปฏิบัติการ.remove(รายการ_พาธ)
        raise
    print("ติดตั้ง_ค่า 완료:", ชื่อ, 명세["version"], "→ /lib (RAM)")


def นําออก_รายการ(ชื่อ):
    รายการ_รายการ = 목록읽기()
    if ชื่อ not in รายการ_รายการ:
        raise ValueError("설치되지 않은 꾸러미입니다: " + ชื่อ)
    for เส้นทาง, 지문값 in รายการ_รายการ[ชื่อ]["files"].items():
        if ระบบปฏิบัติการ.path_kind(เส้นทาง) != 1 or 지문(ระบบปฏิบัติการ.read(เส้นทาง)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + เส้นทาง)
    for เส้นทาง in รายการ_รายการ[ชื่อ]["files"]:
        ระบบปฏิบัติการ.remove(เส้นทาง)
    del รายการ_รายการ[ชื่อ]
    기록쓰기(รายการ_พาธ, json.dumps(รายการ_รายการ).encode())
    print("นําออก_รายการ 완료:", ชื่อ)


def เรียกใช้งาน(อาร์กิวเมนต์):
    หมายเลขพอร์ต = 8027
    if len(อาร์กิวเมนต์) >= 2 and อาร์กิวเมนต์[-2] == "--port":
        หมายเลขพอร์ต = int(อาร์กิวเมนต์[-1])
        อาร์กิวเมนต์ = อาร์กิวเมนต์[:-2]
    if อาร์กิวเมนต์ == ["list"]:
        for ชื่อ, ข้อมูลระบบ in 목록읽기().items():
            print(ชื่อ, ข้อมูลระบบ["version"])
    elif len(อาร์กิวเมนต์) == 2 and อาร์กิวเมนต์[0] == "install":
        ติดตั้ง_ค่า(อาร์กิวเมนต์[1], หมายเลขพอร์ต)
    elif len(อาร์กิวเมนต์) == 2 and อาร์กิวเมนต์[0] == "uninstall":
        นําออก_รายการ(อาร์กิวเมนต์[1])
    elif not อาร์กิวเมนต์ or อาร์กิวเมนต์ in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython แหล่ง_ทรี 설치기 (PyPA pip 전체가 아님)")
        print("pip install ชื่อ[==버전] [--port 8027] | pip list | pip uninstall ชื่อ")
        print("โฮสต์: เครื่องมือ/ดําเนินการ_คําสั่ง.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        เรียกใช้งาน(sys.argv[1:])
    except Exception as ข้อผิดพลาด:
        print("รวม ข้อผิดพลาด:", ข้อผิดพลาด)
        sys.exit(1)
