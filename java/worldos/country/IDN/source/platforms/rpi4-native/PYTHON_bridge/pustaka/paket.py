"""Asli 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistem_operasi

Daftar_jalur = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(data).digest())


def 목록읽기():
    if sistem_operasi.path_kind(Daftar_jalur) == 0:
        return {}
    return json.loads(sistem_operasi.read(Daftar_jalur).decode("utf-8"))


def tulis_LOG(jalur, data):
    if sistem_operasi.write(jalur, data) != len(data):
        raise OSError(28)


def cek_jalur(jalur):
    if not isinstance(jalur, str) or not jalur.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in jalur.split("/")):
        raise ValueError("허용하지 않는 paket jalur")
    if "\\" in jalur or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in jalur):
        raise ValueError("잘못된 jalur 문자")
    hasil = "/lib/" + jalur
    if len(hasil.encode("utf-8")) > 63 or jalur in ("Indonesia.py", "paket.py"):
        raise ValueError("paket 경로가 너무 길거나 nilai_default 라이브러리와 겹칩니다.")
    return hasil


class terima_Stream:
    def __init__(자신, peserta):
        자신.peserta = peserta
        자신.남은자료 = b""
        자신.jalankan = sistem_operasi.ticks_ms()

    def 정확히읽기(자신, panjang_VALUE):
        data = bytearray()
        while len(data) < panjang_VALUE:
            if sistem_operasi.ticks_ms() - 자신.jalankan > 90000:
                raise ValueError("paket 중계 balas TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistem_operasi.tcp_read(자신.peserta, 512)
                except OSError as galat:
                    if galat.args[0] != 11:
                        raise
                    sistem_operasi.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paket 전송이 중간에 끝났습니다.")
            item_COUNT = min(panjang_VALUE - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:item_COUNT])
            자신.남은자료 = 자신.남은자료[item_COUNT:]
            sistem_operasi.sleep_ms(0)
        return bytes(data)


def unduh(permintaan, nomor_port):
    if len(permintaan) > 96 or any(karakter_VALUE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karakter_VALUE in permintaan):
        raise ValueError("사용법: pip install Nama_2 또는 Nama_2==버전")
    peserta = sistem_operasi.tcp_open()
    try:
        jalankan = sistem_operasi.ticks_ms()
        while True:
            try:
                sistem_operasi.tcp_connect(peserta, "10.0.2.2", nomor_port)
                break
            except OSError as galat:
                if galat.args[0] not in (11, 115) or sistem_operasi.ticks_ms() - jalankan > 5000:
                    raise ValueError("paket 중계 Sambung kegagalan_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                sistem_operasi.sleep_ms(10)
        data = (permintaan + "\n").encode()
        while data:
            try:
                item_COUNT = sistem_operasi.tcp_write(peserta, data)
                if not item_COUNT:
                    raise ValueError("paket permintaan Transfer_VALUE kegagalan_VALUE")
                data = data[item_COUNT:]
            except OSError as galat:
                if galat.args[0] != 11:
                    raise
                sistem_operasi.sleep_ms(10)
                if sistem_operasi.ticks_ms() - jalankan > 10000:
                    raise ValueError("paket permintaan Transfer_VALUE TIME_VALUE 초과")
        Stream_VALUE = terima_Stream(peserta)
        kepala_VALUE = Stream_VALUE.정확히읽기(8)
        if kepala_VALUE[:4] != b"JKP1":
            raise ValueError("paket Transfer_VALUE kasus_VALUE 불일치")
        panjang_VALUE = (kepala_VALUE[4] << 24) | (kepala_VALUE[5] << 16) | (kepala_VALUE[6] << 8) | kepala_VALUE[7]
        if panjang_VALUE > 8192:
            raise ValueError("paket 명세가 너무 큽니다.")
        spes = json.loads(Stream_VALUE.정확히읽기(panjang_VALUE).decode())
        if "error" in spes:
            raise ValueError(spes["error"])
        if not 1 <= len(spes["files"]) <= 16:
            raise ValueError("꾸러미당 sumber_pohon 파일은 1~16개여야 합니다.")
        if sum(entri_VALUE["size"] for entri_VALUE in spes["files"]) > 65536:
            raise ValueError("paket sumber_pohon 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for entri_VALUE in spes["files"]:
            jalur = cek_jalur(entri_VALUE["path"])
            if jalur in 파일들 or not 0 <= entri_VALUE["size"] <= 16384:
                raise ValueError("중복 jalur 또는 berkas Ukuran 초과")
            data = Stream_VALUE.정확히읽기(entri_VALUE["size"])
            if 지문(data) != entri_VALUE["sha256"]:
                raise ValueError("paket berkas SHA-256 불일치")
            # 실행하지 않고 saat_ini_item MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), jalur, "exec")
            파일들[jalur] = data
            gc.collect()
        return spes, 파일들
    finally:
        sistem_operasi.udp_close(peserta)


def instal_VALUE(permintaan, nomor_port):
    print("paket unduh:", permintaan)
    spes, 파일들 = unduh(permintaan, nomor_port)
    entri_Daftar = 목록읽기()
    Nama_2 = spes["name"]
    if Nama_2 in entri_Daftar:
        if entri_Daftar[Nama_2]["version"] == spes["version"]:
            for jalur, 지문값 in entri_Daftar[Nama_2]["files"].items():
                if sistem_operasi.path_kind(jalur) != 1 or 지문(sistem_operasi.read(jalur)) != 지문값:
                    raise ValueError("설치된 paket 파일이 달라졌습니다: " + jalur)
            print("이미 설치됨:", Nama_2, spes["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VALUE 설치하십시오.")
    for jalur in 파일들:
        if sistem_operasi.path_kind(jalur):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + jalur)
    entri_Daftar[Nama_2] = {"version": spes["version"], "files": {jalur: 지문(data) for jalur, data in 파일들.items()}}
    새목록 = json.dumps(entri_Daftar).encode()
    if len(새목록) > 16384:
        raise ValueError("paket entri_Daftar Ukuran 초과")
    이전목록 = sistem_operasi.read(Daftar_jalur) if sistem_operasi.path_kind(Daftar_jalur) else None
    만든파일 = []
    만든폴더 = []
    try:
        for jalur, data in 파일들.items():
            부분들 = jalur.split("/")
            for 수 in range(2, len(부분들)):
                Direktori_VALUE = "/".join(부분들[:수])
                종류 = sistem_operasi.path_kind(Direktori_VALUE)
                if 종류 == 0:
                    sistem_operasi.mkdir(Direktori_VALUE)
                    만든폴더.append(Direktori_VALUE)
                elif 종류 != 2:
                    raise ValueError("Direktori_VALUE 경로에 파일이 있습니다: " + Direktori_VALUE)
            만든파일.append(jalur)
            tulis_LOG(jalur, data)
        tulis_LOG(Daftar_jalur, 새목록)
    except Exception:
        for jalur in 만든파일:
            if sistem_operasi.path_kind(jalur):
                sistem_operasi.remove(jalur)
        for Direktori_VALUE in reversed(만든폴더):
            sistem_operasi.rmdir(Direktori_VALUE)
        if 이전목록 is not None:
            tulis_LOG(Daftar_jalur, 이전목록)
        elif sistem_operasi.path_kind(Daftar_jalur):
            sistem_operasi.remove(Daftar_jalur)
        raise
    print("instal_VALUE 완료:", Nama_2, spes["version"], "→ /lib (RAM)")


def hapus_entri(Nama_2):
    entri_Daftar = 목록읽기()
    if Nama_2 not in entri_Daftar:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nama_2)
    for jalur, 지문값 in entri_Daftar[Nama_2]["files"].items():
        if sistem_operasi.path_kind(jalur) != 1 or 지문(sistem_operasi.read(jalur)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + jalur)
    for jalur in entri_Daftar[Nama_2]["files"]:
        sistem_operasi.remove(jalur)
    del entri_Daftar[Nama_2]
    tulis_LOG(Daftar_jalur, json.dumps(entri_Daftar).encode())
    print("hapus_entri 완료:", Nama_2)


def jalankan(argumen):
    nomor_port = 8027
    if len(argumen) >= 2 and argumen[-2] == "--port":
        nomor_port = int(argumen[-1])
        argumen = argumen[:-2]
    if argumen == ["list"]:
        for Nama_2, msinfo32_exe in 목록읽기().items():
            print(Nama_2, msinfo32_exe["version"])
    elif len(argumen) == 2 and argumen[0] == "install":
        instal_VALUE(argumen[1], nomor_port)
    elif len(argumen) == 2 and argumen[0] == "uninstall":
        hapus_entri(argumen[1])
    elif not argumen or argumen in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython sumber_pohon 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nama_2[==버전] [--port 8027] | pip list | pip uninstall Nama_2")
        print("host: alat/Jalankan_perintah.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        jalankan(sys.argv[1:])
    except Exception as galat:
        print("paket galat:", galat)
        sys.exit(1)
