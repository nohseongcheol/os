"""Öz 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 konak 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as işletim_sistemi

Liste_yol = "/lib/.pip.json"


def parmak_izi_değer(veri):
    return "".join("%02x" % değer for değer in hashlib.sha256(veri).digest())


def 목록읽기():
    if işletim_sistemi.path_kind(Liste_yol) == 0:
        return {}
    return json.loads(işletim_sistemi.read(Liste_yol).decode("utf-8"))


def yazma_LOG(yol, veri):
    if işletim_sistemi.write(yol, veri) != len(veri):
        raise OSError(28)


def çek_yol(yol):
    if not isinstance(yol, str) or not yol.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in yol.split("/")):
        raise ValueError("허용하지 않는 paket_iş yol")
    if "\\" in yol or any(ord(karakter_değer) < 32 or ord(karakter_değer) == 127 for karakter_değer in yol):
        raise ValueError("잘못된 yol 문자")
    sonuç = "/lib/" + yol
    if len(sonuç.encode("utf-8")) > 63 or yol in ("Türkçe.py", "paket_iş.py"):
        raise ValueError("paket_iş 경로가 너무 길거나 varsayılan_değer 라이브러리와 겹칩니다.")
    return sonuç


class almak_akış:
    def __init__(자신, uç_nokta):
        자신.uç_nokta = uç_nokta
        자신.남은자료 = b""
        자신.çalıştır = işletim_sistemi.ticks_ms()

    def 정확히읽기(자신, süre_değer):
        veri = bytearray()
        while len(veri) < süre_değer:
            if işletim_sistemi.ticks_ms() - 자신.çalıştır > 90000:
                raise ValueError("paket_iş Geçiş_değer yanıt zaman_değeri 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = işletim_sistemi.tcp_read(자신.uç_nokta, 512)
                except OSError as hata:
                    if hata.args[0] != 11:
                        raise
                    işletim_sistemi.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paket_iş 전송이 중간에 끝났습니다.")
            öğe_BAĞ_DEĞ_SAY = min(süre_değer - len(veri), len(자신.남은자료))
            veri.extend(자신.남은자료[:öğe_BAĞ_DEĞ_SAY])
            자신.남은자료 = 자신.남은자료[öğe_BAĞ_DEĞ_SAY:]
            işletim_sistemi.sleep_ms(0)
        return bytes(veri)


def indir(istek, bağlantı_noktası_numarası):
    if len(istek) > 96 or any(karakter_değer not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for karakter_değer in istek):
        raise ValueError("사용법: pip install İsim 또는 İsim==버전")
    uç_nokta = işletim_sistemi.tcp_open()
    try:
        çalıştır = işletim_sistemi.ticks_ms()
        while True:
            try:
                işletim_sistemi.tcp_connect(uç_nokta, "10.0.2.2", bağlantı_noktası_numarası)
                break
            except OSError as hata:
                if hata.args[0] not in (11, 115) or işletim_sistemi.ticks_ms() - çalıştır > 5000:
                    raise ValueError("paket_iş Geçiş_değer Bağlan hata_değer: 호스트에서 --network --pip로 실행하십시오.")
                işletim_sistemi.sleep_ms(10)
        veri = (istek + "\n").encode()
        while veri:
            try:
                öğe_BAĞ_DEĞ_SAY = işletim_sistemi.tcp_write(uç_nokta, veri)
                if not öğe_BAĞ_DEĞ_SAY:
                    raise ValueError("paket_iş istek devir_değer hata_değer")
                veri = veri[öğe_BAĞ_DEĞ_SAY:]
            except OSError as hata:
                if hata.args[0] != 11:
                    raise
                işletim_sistemi.sleep_ms(10)
                if işletim_sistemi.ticks_ms() - çalıştır > 10000:
                    raise ValueError("paket_iş istek devir_değer zaman_değeri 초과")
        akış_değer = almak_akış(uç_nokta)
        머리 = akış_değer.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("paket_iş devir_değer sözleşme_değeri 불일치")
        süre_değer = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if süre_değer > 8192:
            raise ValueError("paket_iş 명세가 너무 큽니다.")
        명세 = json.loads(akış_değer.정확히읽기(süre_değer).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 kaynak_ağaç 파일은 1~16개여야 합니다.")
        if sum(girdi_değer["size"] for girdi_değer in 명세["files"]) > 65536:
            raise ValueError("paket_iş kaynak_ağaç 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for girdi_değer in 명세["files"]:
            yol = çek_yol(girdi_değer["path"])
            if yol in 파일들 or not 0 <= girdi_değer["size"] <= 16384:
                raise ValueError("중복 yol 또는 dosya Boyut 초과")
            veri = akış_değer.정확히읽기(girdi_değer["size"])
            if parmak_izi_değer(veri) != girdi_değer["sha256"]:
                raise ValueError("paket_iş dosya SHA-256 불일치")
            # 실행하지 않고 geçerli_öğe MicroPython의 문법으로 먼저 검사한다.
            compile(veri.decode("utf-8"), yol, "exec")
            파일들[yol] = veri
            gc.collect()
        return 명세, 파일들
    finally:
        işletim_sistemi.udp_close(uç_nokta)


def yükle_değer(istek, bağlantı_noktası_numarası):
    print("paket_iş indir:", istek)
    명세, 파일들 = indir(istek, bağlantı_noktası_numarası)
    girdi_Liste = 목록읽기()
    İsim = 명세["name"]
    if İsim in girdi_Liste:
        if girdi_Liste[İsim]["version"] == 명세["version"]:
            for yol, parmak_izi_veri in girdi_Liste[İsim]["files"].items():
                if işletim_sistemi.path_kind(yol) != 1 or parmak_izi_değer(işletim_sistemi.read(yol)) != parmak_izi_veri:
                    raise ValueError("설치된 paket_iş 파일이 달라졌습니다: " + yol)
            print("이미 설치됨:", İsim, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_değer 설치하십시오.")
    for yol in 파일들:
        if işletim_sistemi.path_kind(yol):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + yol)
    girdi_Liste[İsim] = {"version": 명세["version"], "files": {yol: parmak_izi_değer(veri) for yol, veri in 파일들.items()}}
    새목록 = json.dumps(girdi_Liste).encode()
    if len(새목록) > 16384:
        raise ValueError("paket_iş girdi_Liste Boyut 초과")
    Önceki_Liste = işletim_sistemi.read(Liste_yol) if işletim_sistemi.path_kind(Liste_yol) else None
    만든파일 = []
    만든폴더 = []
    try:
        for yol, veri in 파일들.items():
            부분들 = yol.split("/")
            for 수 in range(2, len(부분들)):
                dizin_değer = "/".join(부분들[:수])
                Tip_değer = işletim_sistemi.path_kind(dizin_değer)
                if Tip_değer == 0:
                    işletim_sistemi.mkdir(dizin_değer)
                    만든폴더.append(dizin_değer)
                elif Tip_değer != 2:
                    raise ValueError("dizin_değer 경로에 파일이 있습니다: " + dizin_değer)
            만든파일.append(yol)
            yazma_LOG(yol, veri)
        yazma_LOG(Liste_yol, 새목록)
    except Exception:
        for yol in 만든파일:
            if işletim_sistemi.path_kind(yol):
                işletim_sistemi.remove(yol)
        for dizin_değer in reversed(만든폴더):
            işletim_sistemi.rmdir(dizin_değer)
        if Önceki_Liste is not None:
            yazma_LOG(Liste_yol, Önceki_Liste)
        elif işletim_sistemi.path_kind(Liste_yol):
            işletim_sistemi.remove(Liste_yol)
        raise
    print("yükle_değer 완료:", İsim, 명세["version"], "→ /lib (RAM)")


def kaldırmak_girdi(İsim):
    girdi_Liste = 목록읽기()
    if İsim not in girdi_Liste:
        raise ValueError("설치되지 않은 꾸러미입니다: " + İsim)
    for yol, parmak_izi_veri in girdi_Liste[İsim]["files"].items():
        if işletim_sistemi.path_kind(yol) != 1 or parmak_izi_değer(işletim_sistemi.read(yol)) != parmak_izi_veri:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + yol)
    for yol in girdi_Liste[İsim]["files"]:
        işletim_sistemi.remove(yol)
    del girdi_Liste[İsim]
    yazma_LOG(Liste_yol, json.dumps(girdi_Liste).encode())
    print("kaldırmak_girdi 완료:", İsim)


def çalıştır(bağımsız_değişkenler):
    bağlantı_noktası_numarası = 8027
    if len(bağımsız_değişkenler) >= 2 and bağımsız_değişkenler[-2] == "--port":
        bağlantı_noktası_numarası = int(bağımsız_değişkenler[-1])
        bağımsız_değişkenler = bağımsız_değişkenler[:-2]
    if bağımsız_değişkenler == ["list"]:
        for İsim, msinfo32_exe in 목록읽기().items():
            print(İsim, msinfo32_exe["version"])
    elif len(bağımsız_değişkenler) == 2 and bağımsız_değişkenler[0] == "install":
        yükle_değer(bağımsız_değişkenler[1], bağlantı_noktası_numarası)
    elif len(bağımsız_değişkenler) == 2 and bağımsız_değişkenler[0] == "uninstall":
        kaldırmak_girdi(bağımsız_değişkenler[1])
    elif not bağımsız_değişkenler or bağımsız_değişkenler in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython kaynak_ağaç 설치기 (PyPA pip 전체가 아님)")
        print("pip install İsim[==버전] [--port 8027] | pip list | pip uninstall İsim")
        print("konak: araçlar/yürütmek_komut.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        çalıştır(sys.argv[1:])
    except Exception as hata:
        print("paket_iş hata:", hata)
        sys.exit(1)
