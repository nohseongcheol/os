"""Asli 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 hos 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistem_pengendalian

Senarai_laluan = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if sistem_pengendalian.path_kind(Senarai_laluan) == 0:
        return {}
    return json.loads(sistem_pengendalian.read(Senarai_laluan).decode("utf-8"))


def tulis_LOG(LALUAN, data):
    if sistem_pengendalian.write(LALUAN, data) != len(data):
        raise OSError(28)


def cek_laluan(LALUAN):
    if not isinstance(LALUAN, str) or not LALUAN.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in LALUAN.split("/")):
        raise ValueError("허용하지 않는 pakej LALUAN")
    if "\\" in LALUAN or any(ord(aksara_VALUE) < 32 or ord(aksara_VALUE) == 127 for aksara_VALUE in LALUAN):
        raise ValueError("잘못된 LALUAN 문자")
    ukuran = "/lib/" + LALUAN
    if len(ukuran.encode("utf-8")) > 63 or LALUAN in ("Melayu.py", "pakej.py"):
        raise ValueError("pakej 경로가 너무 길거나 nilai_lalai 라이브러리와 겹칩니다.")
    return ukuran


class 수신흐름:
    def __init__(자신, peserta):
        자신.peserta = peserta
        자신.남은자료 = b""
        자신.Jalan = sistem_pengendalian.ticks_ms()

    def 정확히읽기(자신, kepanjangan_VALUE):
        data = bytearray()
        while len(data) < kepanjangan_VALUE:
            if sistem_pengendalian.ticks_ms() - 자신.Jalan > 90000:
                raise ValueError("pakej 중계 balas nilai_masa 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistem_pengendalian.tcp_read(자신.peserta, 512)
                except OSError as RALAT:
                    if RALAT.args[0] != 11:
                        raise
                    sistem_pengendalian.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("pakej 전송이 중간에 끝났습니다.")
            item_COUNT = min(kepanjangan_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:item_COUNT])
            자신.남은자료 = 자신.남은자료[item_COUNT:]
            sistem_pengendalian.sleep_ms(0)
        return bytes(data)


def muat_turun(permintaan, nombor_port):
    if len(permintaan) > 96 or any(aksara_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for aksara_VALUE in permintaan):
        raise ValueError("사용법: pip install Nama 또는 Nama==버전")
    peserta = sistem_pengendalian.tcp_open()
    try:
        Jalan = sistem_pengendalian.ticks_ms()
        while True:
            try:
                sistem_pengendalian.tcp_connect(peserta, "10.0.2.2", nombor_port)
                break
            except OSError as RALAT:
                if RALAT.args[0] not in (11, 115) or sistem_pengendalian.ticks_ms() - Jalan > 5000:
                    raise ValueError("pakej 중계 Sambung kegagalan_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                sistem_pengendalian.sleep_ms(10)
        data = (permintaan + "\n").encode()
        while data:
            try:
                item_COUNT = sistem_pengendalian.tcp_write(peserta, data)
                if not item_COUNT:
                    raise ValueError("pakej permintaan pindah_VALUE kegagalan_VALUE")
                data = data[item_COUNT:]
            except OSError as RALAT:
                if RALAT.args[0] != 11:
                    raise
                sistem_pengendalian.sleep_ms(10)
                if sistem_pengendalian.ticks_ms() - Jalan > 10000:
                    raise ValueError("pakej permintaan pindah_VALUE nilai_masa 초과")
        strim_VALUE = 수신흐름(peserta)
        머리 = strim_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("pakej pindah_VALUE kes_VALUE 불일치")
        kepanjangan_VALUE = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if kepanjangan_VALUE > 8192:
            raise ValueError("pakej 명세가 너무 큽니다.")
        명세 = json.loads(strim_VALUE.정확히읽기(kepanjangan_VALUE).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 sumber_pepohon 파일은 1~16개여야 합니다.")
        if sum(pemasukan_VALUE["size"] for pemasukan_VALUE in 명세["files"]) > 65536:
            raise ValueError("pakej sumber_pepohon 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for pemasukan_VALUE in 명세["files"]:
            LALUAN = cek_laluan(pemasukan_VALUE["path"])
            if LALUAN in 파일들 or not 0 <= pemasukan_VALUE["size"] <= 16384:
                raise ValueError("중복 LALUAN 또는 Fail Saiz 초과")
            data = strim_VALUE.정확히읽기(pemasukan_VALUE["size"])
            if 지문(data) != pemasukan_VALUE["sha256"]:
                raise ValueError("pakej Fail SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), LALUAN, "exec")
            파일들[LALUAN] = data
            gc.collect()
        return 명세, 파일들
    finally:
        sistem_pengendalian.udp_close(peserta)


def pasang_VALUE(permintaan, nombor_port):
    print("pakej muat_turun:", permintaan)
    명세, 파일들 = muat_turun(permintaan, nombor_port)
    pemasukan_Senarai = 목록읽기()
    Nama = 명세["name"]
    if Nama in pemasukan_Senarai:
        if pemasukan_Senarai[Nama]["version"] == 명세["version"]:
            for LALUAN, 지문값 in pemasukan_Senarai[Nama]["files"].items():
                if sistem_pengendalian.path_kind(LALUAN) != 1 or 지문(sistem_pengendalian.read(LALUAN)) != 지문값:
                    raise ValueError("설치된 pakej 파일이 달라졌습니다: " + LALUAN)
            print("이미 설치됨:", Nama, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VALUE 설치하십시오.")
    for LALUAN in 파일들:
        if sistem_pengendalian.path_kind(LALUAN):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + LALUAN)
    pemasukan_Senarai[Nama] = {"version": 명세["version"], "files": {LALUAN: 지문(data) for LALUAN, data in 파일들.items()}}
    새목록 = json.dumps(pemasukan_Senarai).encode()
    if len(새목록) > 16384:
        raise ValueError("pakej pemasukan_Senarai Saiz 초과")
    이전목록 = sistem_pengendalian.read(Senarai_laluan) if sistem_pengendalian.path_kind(Senarai_laluan) else None
    만든파일 = []
    만든폴더 = []
    try:
        for LALUAN, data in 파일들.items():
            부분들 = LALUAN.split("/")
            for 수 in range(2, len(부분들)):
                direktori_VALUE = "/".join(부분들[:수])
                종류 = sistem_pengendalian.path_kind(direktori_VALUE)
                if 종류 == 0:
                    sistem_pengendalian.mkdir(direktori_VALUE)
                    만든폴더.append(direktori_VALUE)
                elif 종류 != 2:
                    raise ValueError("direktori_VALUE 경로에 파일이 있습니다: " + direktori_VALUE)
            만든파일.append(LALUAN)
            tulis_LOG(LALUAN, data)
        tulis_LOG(Senarai_laluan, 새목록)
    except Exception:
        for LALUAN in 만든파일:
            if sistem_pengendalian.path_kind(LALUAN):
                sistem_pengendalian.remove(LALUAN)
        for direktori_VALUE in reversed(만든폴더):
            sistem_pengendalian.rmdir(direktori_VALUE)
        if 이전목록 is not None:
            tulis_LOG(Senarai_laluan, 이전목록)
        elif sistem_pengendalian.path_kind(Senarai_laluan):
            sistem_pengendalian.remove(Senarai_laluan)
        raise
    print("pasang_VALUE 완료:", Nama, 명세["version"], "→ /lib (RAM)")


def alih_keluar_pemasukan(Nama):
    pemasukan_Senarai = 목록읽기()
    if Nama not in pemasukan_Senarai:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nama)
    for LALUAN, 지문값 in pemasukan_Senarai[Nama]["files"].items():
        if sistem_pengendalian.path_kind(LALUAN) != 1 or 지문(sistem_pengendalian.read(LALUAN)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + LALUAN)
    for LALUAN in pemasukan_Senarai[Nama]["files"]:
        sistem_pengendalian.remove(LALUAN)
    del pemasukan_Senarai[Nama]
    tulis_LOG(Senarai_laluan, json.dumps(pemasukan_Senarai).encode())
    print("alih_keluar_pemasukan 완료:", Nama)


def Jalan(인수):
    nombor_port = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        nombor_port = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Nama, msinfo32_exe in 목록읽기().items():
            print(Nama, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        pasang_VALUE(인수[1], nombor_port)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        alih_keluar_pemasukan(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython sumber_pepohon 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nama[==버전] [--port 8027] | pip list | pip uninstall Nama")
        print("hos: alat/laksanakan_perintah.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Jalan(sys.argv[1:])
    except Exception as RALAT:
        print("pakej RALAT:", RALAT)
        sys.exit(1)
