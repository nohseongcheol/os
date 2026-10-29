"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 sauka 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as OS

Jeri_Hanyar_shiga = "/lib/.pip.json"


def 지문(Tarin_bayani):
    return "".join("%02x" % Daraja for Daraja in hashlib.sha256(Tarin_bayani).digest())


def 목록읽기():
    if OS.path_kind(Jeri_Hanyar_shiga) == 0:
        return {}
    return json.loads(OS.read(Jeri_Hanyar_shiga).decode("utf-8"))


def Rubuta_logu(Hanyar_shiga, Tarin_bayani):
    if OS.write(Hanyar_shiga, Tarin_bayani) != len(Tarin_bayani):
        raise OSError(28)


def Bincika_Hanyar_shiga(Hanyar_shiga):
    if not isinstance(Hanyar_shiga, str) or not Hanyar_shiga.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Hanyar_shiga.split("/")):
        raise ValueError("허용하지 않는 dami Hanyar_shiga")
    if "\\" in Hanyar_shiga or any(ord(Harafi_Daraja) < 32 or ord(Harafi_Daraja) == 127 for Harafi_Daraja in Hanyar_shiga):
        raise ValueError("잘못된 Hanyar_shiga 문자")
    결과 = "/lib/" + Hanyar_shiga
    if len(결과.encode("utf-8")) > 63 or Hanyar_shiga in ("한국어.py", "dami.py"):
        raise ValueError("dami 경로가 너무 길거나 Tanadaddiyar_daraja 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Tafiyar_da = OS.ticks_ms()

    def 정확히읽기(자신, Tsawo_Daraja):
        Tarin_bayani = bytearray()
        while len(Tarin_bayani) < Tsawo_Daraja:
            if OS.ticks_ms() - 자신.Tafiyar_da > 90000:
                raise ValueError("dami 중계 mayar_da_martani lokaci_Daraja 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = OS.tcp_read(자신.종단, 512)
                except OSError as Kuskure:
                    if Kuskure.args[0] != 11:
                        raise
                    OS.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("dami 전송이 중간에 끝났습니다.")
            개수 = min(Tsawo_Daraja - len(Tarin_bayani), len(자신.남은자료))
            Tarin_bayani.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            OS.sleep_ms(0)
        return bytes(Tarin_bayani)


def zazzage(요청, lambar_kafa):
    if len(요청) > 96 or any(Harafi_Daraja not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for Harafi_Daraja in 요청):
        raise ValueError("사용법: pip install Suna 또는 Suna==버전")
    종단 = OS.tcp_open()
    try:
        Tafiyar_da = OS.ticks_ms()
        while True:
            try:
                OS.tcp_connect(종단, "10.0.2.2", lambar_kafa)
                break
            except OSError as Kuskure:
                if Kuskure.args[0] not in (11, 115) or OS.ticks_ms() - Tafiyar_da > 5000:
                    raise ValueError("dami 중계 Haɗi Kasa_aiki_Daraja: 호스트에서 --network --pip로 실행하십시오.")
                OS.sleep_ms(10)
        Tarin_bayani = (요청 + "\n").encode()
        while Tarin_bayani:
            try:
                개수 = OS.tcp_write(종단, Tarin_bayani)
                if not 개수:
                    raise ValueError("dami 요청 Gusar_da_Daraja Kasa_aiki_Daraja")
                Tarin_bayani = Tarin_bayani[개수:]
            except OSError as Kuskure:
                if Kuskure.args[0] != 11:
                    raise
                OS.sleep_ms(10)
                if OS.ticks_ms() - Tafiyar_da > 10000:
                    raise ValueError("dami 요청 Gusar_da_Daraja lokaci_Daraja 초과")
        watsuwa_Daraja = 수신흐름(종단)
        머리 = watsuwa_Daraja.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("dami Gusar_da_Daraja Kes_Daraja 불일치")
        Tsawo_Daraja = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if Tsawo_Daraja > 8192:
            raise ValueError("dami 명세가 너무 큽니다.")
        명세 = json.loads(watsuwa_Daraja.정확히읽기(Tsawo_Daraja).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 tushe_Li_irabin_tarin_bayanai 파일은 1~16개여야 합니다.")
        if sum(Mashigar_bayanai_Daraja["size"] for Mashigar_bayanai_Daraja in 명세["files"]) > 65536:
            raise ValueError("dami tushe_Li_irabin_tarin_bayanai 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for Mashigar_bayanai_Daraja in 명세["files"]:
            Hanyar_shiga = Bincika_Hanyar_shiga(Mashigar_bayanai_Daraja["path"])
            if Hanyar_shiga in 파일들 or not 0 <= Mashigar_bayanai_Daraja["size"] <= 16384:
                raise ValueError("중복 Hanyar_shiga 또는 Fayil Girma 초과")
            Tarin_bayani = watsuwa_Daraja.정확히읽기(Mashigar_bayanai_Daraja["size"])
            if 지문(Tarin_bayani) != Mashigar_bayanai_Daraja["sha256"]:
                raise ValueError("dami Fayil SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(Tarin_bayani.decode("utf-8"), Hanyar_shiga, "exec")
            파일들[Hanyar_shiga] = Tarin_bayani
            gc.collect()
        return 명세, 파일들
    finally:
        OS.udp_close(종단)


def Girka_Daraja(요청, lambar_kafa):
    print("dami zazzage:", 요청)
    명세, 파일들 = zazzage(요청, lambar_kafa)
    Mashigar_bayanai_Jeri = 목록읽기()
    Suna = 명세["name"]
    if Suna in Mashigar_bayanai_Jeri:
        if Mashigar_bayanai_Jeri[Suna]["version"] == 명세["version"]:
            for Hanyar_shiga, 지문값 in Mashigar_bayanai_Jeri[Suna]["files"].items():
                if OS.path_kind(Hanyar_shiga) != 1 or 지문(OS.read(Hanyar_shiga)) != 지문값:
                    raise ValueError("설치된 dami 파일이 달라졌습니다: " + Hanyar_shiga)
            print("이미 설치됨:", Suna, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Baya_Daraja 설치하십시오.")
    for Hanyar_shiga in 파일들:
        if OS.path_kind(Hanyar_shiga):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Hanyar_shiga)
    Mashigar_bayanai_Jeri[Suna] = {"version": 명세["version"], "files": {Hanyar_shiga: 지문(Tarin_bayani) for Hanyar_shiga, Tarin_bayani in 파일들.items()}}
    새목록 = json.dumps(Mashigar_bayanai_Jeri).encode()
    if len(새목록) > 16384:
        raise ValueError("dami Mashigar_bayanai_Jeri Girma 초과")
    이전목록 = OS.read(Jeri_Hanyar_shiga) if OS.path_kind(Jeri_Hanyar_shiga) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Hanyar_shiga, Tarin_bayani in 파일들.items():
            부분들 = Hanyar_shiga.split("/")
            for 수 in range(2, len(부분들)):
                ma_ajiya_Daraja = "/".join(부분들[:수])
                종류 = OS.path_kind(ma_ajiya_Daraja)
                if 종류 == 0:
                    OS.mkdir(ma_ajiya_Daraja)
                    만든폴더.append(ma_ajiya_Daraja)
                elif 종류 != 2:
                    raise ValueError("ma_ajiya_Daraja 경로에 파일이 있습니다: " + ma_ajiya_Daraja)
            만든파일.append(Hanyar_shiga)
            Rubuta_logu(Hanyar_shiga, Tarin_bayani)
        Rubuta_logu(Jeri_Hanyar_shiga, 새목록)
    except Exception:
        for Hanyar_shiga in 만든파일:
            if OS.path_kind(Hanyar_shiga):
                OS.remove(Hanyar_shiga)
        for ma_ajiya_Daraja in reversed(만든폴더):
            OS.rmdir(ma_ajiya_Daraja)
        if 이전목록 is not None:
            Rubuta_logu(Jeri_Hanyar_shiga, 이전목록)
        elif OS.path_kind(Jeri_Hanyar_shiga):
            OS.remove(Jeri_Hanyar_shiga)
        raise
    print("Girka_Daraja 완료:", Suna, 명세["version"], "→ /lib (RAM)")


def Cire_Mashigar_bayanai(Suna):
    Mashigar_bayanai_Jeri = 목록읽기()
    if Suna not in Mashigar_bayanai_Jeri:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Suna)
    for Hanyar_shiga, 지문값 in Mashigar_bayanai_Jeri[Suna]["files"].items():
        if OS.path_kind(Hanyar_shiga) != 1 or 지문(OS.read(Hanyar_shiga)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Hanyar_shiga)
    for Hanyar_shiga in Mashigar_bayanai_Jeri[Suna]["files"]:
        OS.remove(Hanyar_shiga)
    del Mashigar_bayanai_Jeri[Suna]
    Rubuta_logu(Jeri_Hanyar_shiga, json.dumps(Mashigar_bayanai_Jeri).encode())
    print("Cire_Mashigar_bayanai 완료:", Suna)


def Tafiyar_da(인수):
    lambar_kafa = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        lambar_kafa = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Suna, msinfo32_exe in 목록읽기().items():
            print(Suna, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        Girka_Daraja(인수[1], lambar_kafa)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        Cire_Mashigar_bayanai(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython tushe_Li_irabin_tarin_bayanai 설치기 (PyPA pip 전체가 아님)")
        print("pip install Suna[==버전] [--port 8027] | pip list | pip uninstall Suna")
        print("sauka: Kaya/gudanar_Umarni.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Tafiyar_da(sys.argv[1:])
    except Exception as Kuskure:
        print("dami Kuskure:", Kuskure)
        sys.exit(1)
