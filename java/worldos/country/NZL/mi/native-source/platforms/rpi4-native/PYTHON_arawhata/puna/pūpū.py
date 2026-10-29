"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 taurima 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as pūnaha_mahi

Rārangi_ara = "/lib/.pip.json"


def 지문(raraunga):
    return "".join("%02x" % uara for uara in hashlib.sha256(raraunga).digest())


def 목록읽기():
    if pūnaha_mahi.path_kind(Rārangi_ara) == 0:
        return {}
    return json.loads(pūnaha_mahi.read(Rārangi_ara).decode("utf-8"))


def tuhi_LOG(ara, raraunga):
    if pūnaha_mahi.write(ara, raraunga) != len(raraunga):
        raise OSError(28)


def taki_ara(ara):
    if not isinstance(ara, str) or not ara.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in ara.split("/")):
        raise ValueError("허용하지 않는 pūpū ara")
    if "\\" in ara or any(ord(pūāhua_uara) < 32 or ord(pūāhua_uara) == 127 for pūāhua_uara in ara):
        raise ValueError("잘못된 ara 문자")
    mēhua = "/lib/" + ara
    if len(mēhua.encode("utf-8")) > 63 or ara in ("Reo_Māori.py", "pūpū.py"):
        raise ValueError("pūpū 경로가 너무 길거나 uara_taunoa 라이브러리와 겹칩니다.")
    return mēhua


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.whakahaere = pūnaha_mahi.ticks_ms()

    def 정확히읽기(자신, roa_uara):
        raraunga = bytearray()
        while len(raraunga) < roa_uara:
            if pūnaha_mahi.ticks_ms() - 자신.whakahaere > 90000:
                raise ValueError("pūpū 중계 whakautu TIME_uara 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = pūnaha_mahi.tcp_read(자신.종단, 512)
                except OSError as Pōhēhē:
                    if Pōhēhē.args[0] != 11:
                        raise
                    pūnaha_mahi.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("pūpū 전송이 중간에 끝났습니다.")
            tuemi_COUNT = min(roa_uara - len(raraunga), len(자신.남은자료))
            raraunga.extend(자신.남은자료[:tuemi_COUNT])
            자신.남은자료 = 자신.남은자료[tuemi_COUNT:]
            pūnaha_mahi.sleep_ms(0)
        return bytes(raraunga)


def tikiake(요청, 접속번호):
    if len(요청) > 96 or any(pūāhua_uara not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for pūāhua_uara in 요청):
        raise ValueError("사용법: pip install Ingoa 또는 Ingoa==버전")
    종단 = pūnaha_mahi.tcp_open()
    try:
        whakahaere = pūnaha_mahi.ticks_ms()
        while True:
            try:
                pūnaha_mahi.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Pōhēhē:
                if Pōhēhē.args[0] not in (11, 115) or pūnaha_mahi.ticks_ms() - whakahaere > 5000:
                    raise ValueError("pūpū 중계 TŪHONO rahunga_uara: 호스트에서 --network --pip로 실행하십시오.")
                pūnaha_mahi.sleep_ms(10)
        raraunga = (요청 + "\n").encode()
        while raraunga:
            try:
                tuemi_COUNT = pūnaha_mahi.tcp_write(종단, raraunga)
                if not tuemi_COUNT:
                    raise ValueError("pūpū 요청 whakawhiti_uara_630ba093 rahunga_uara")
                raraunga = raraunga[tuemi_COUNT:]
            except OSError as Pōhēhē:
                if Pōhēhē.args[0] != 11:
                    raise
                pūnaha_mahi.sleep_ms(10)
                if pūnaha_mahi.ticks_ms() - whakahaere > 10000:
                    raise ValueError("pūpū 요청 whakawhiti_uara_630ba093 TIME_uara 초과")
        roma_uara = 수신흐름(종단)
        머리 = roma_uara.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("pūpū whakawhiti_uara_630ba093 kēhi_uara 불일치")
        roa_uara = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if roa_uara > 8192:
            raise ValueError("pūpū 명세가 너무 큽니다.")
        명세 = json.loads(roma_uara.정확히읽기(roa_uara).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 pūtake_rākau 파일은 1~16개여야 합니다.")
        if sum(tāurunga_uara["size"] for tāurunga_uara in 명세["files"]) > 65536:
            raise ValueError("pūpū pūtake_rākau 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for tāurunga_uara in 명세["files"]:
            ara = taki_ara(tāurunga_uara["path"])
            if ara in 파일들 or not 0 <= tāurunga_uara["size"] <= 16384:
                raise ValueError("중복 ara 또는 Kōnae rahi 초과")
            raraunga = roma_uara.정확히읽기(tāurunga_uara["size"])
            if 지문(raraunga) != tāurunga_uara["sha256"]:
                raise ValueError("pūpū Kōnae SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(raraunga.decode("utf-8"), ara, "exec")
            파일들[ara] = raraunga
            gc.collect()
        return 명세, 파일들
    finally:
        pūnaha_mahi.udp_close(종단)


def tāuta_uara(요청, 접속번호):
    print("pūpū tikiake:", 요청)
    명세, 파일들 = tikiake(요청, 접속번호)
    tāurunga_Rārangi = 목록읽기()
    Ingoa = 명세["name"]
    if Ingoa in tāurunga_Rārangi:
        if tāurunga_Rārangi[Ingoa]["version"] == 명세["version"]:
            for ara, 지문값 in tāurunga_Rārangi[Ingoa]["files"].items():
                if pūnaha_mahi.path_kind(ara) != 1 or 지문(pūnaha_mahi.read(ara)) != 지문값:
                    raise ValueError("설치된 pūpū 파일이 달라졌습니다: " + ara)
            print("이미 설치됨:", Ingoa, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Hoki_uara 설치하십시오.")
    for ara in 파일들:
        if pūnaha_mahi.path_kind(ara):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + ara)
    tāurunga_Rārangi[Ingoa] = {"version": 명세["version"], "files": {ara: 지문(raraunga) for ara, raraunga in 파일들.items()}}
    새목록 = json.dumps(tāurunga_Rārangi).encode()
    if len(새목록) > 16384:
        raise ValueError("pūpū tāurunga_Rārangi rahi 초과")
    이전목록 = pūnaha_mahi.read(Rārangi_ara) if pūnaha_mahi.path_kind(Rārangi_ara) else None
    만든파일 = []
    만든폴더 = []
    try:
        for ara, raraunga in 파일들.items():
            부분들 = ara.split("/")
            for 수 in range(2, len(부분들)):
                whaiaronga_uara = "/".join(부분들[:수])
                종류 = pūnaha_mahi.path_kind(whaiaronga_uara)
                if 종류 == 0:
                    pūnaha_mahi.mkdir(whaiaronga_uara)
                    만든폴더.append(whaiaronga_uara)
                elif 종류 != 2:
                    raise ValueError("whaiaronga_uara 경로에 파일이 있습니다: " + whaiaronga_uara)
            만든파일.append(ara)
            tuhi_LOG(ara, raraunga)
        tuhi_LOG(Rārangi_ara, 새목록)
    except Exception:
        for ara in 만든파일:
            if pūnaha_mahi.path_kind(ara):
                pūnaha_mahi.remove(ara)
        for whaiaronga_uara in reversed(만든폴더):
            pūnaha_mahi.rmdir(whaiaronga_uara)
        if 이전목록 is not None:
            tuhi_LOG(Rārangi_ara, 이전목록)
        elif pūnaha_mahi.path_kind(Rārangi_ara):
            pūnaha_mahi.remove(Rārangi_ara)
        raise
    print("tāuta_uara 완료:", Ingoa, 명세["version"], "→ /lib (RAM)")


def tango_tāurunga(Ingoa):
    tāurunga_Rārangi = 목록읽기()
    if Ingoa not in tāurunga_Rārangi:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Ingoa)
    for ara, 지문값 in tāurunga_Rārangi[Ingoa]["files"].items():
        if pūnaha_mahi.path_kind(ara) != 1 or 지문(pūnaha_mahi.read(ara)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + ara)
    for ara in tāurunga_Rārangi[Ingoa]["files"]:
        pūnaha_mahi.remove(ara)
    del tāurunga_Rārangi[Ingoa]
    tuhi_LOG(Rārangi_ara, json.dumps(tāurunga_Rārangi).encode())
    print("tango_tāurunga 완료:", Ingoa)


def whakahaere(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Ingoa, msinfo32_exe in 목록읽기().items():
            print(Ingoa, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        tāuta_uara(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        tango_tāurunga(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython pūtake_rākau 설치기 (PyPA pip 전체가 아님)")
        print("pip install Ingoa[==버전] [--port 8027] | pip list | pip uninstall Ingoa")
        print("taurima: Ngā_Utauta/kawe_tono.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        whakahaere(sys.argv[1:])
    except Exception as Pōhēhē:
        print("pūpū Pōhēhē:", Pōhēhē)
        sys.exit(1)
