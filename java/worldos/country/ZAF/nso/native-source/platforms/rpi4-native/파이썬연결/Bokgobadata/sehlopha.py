"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 go_nea_ditirelo 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as tshepedišotirišo

Lenaneo_tsela = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % boleng for boleng in hashlib.sha256(data).digest())


def 목록읽기():
    if tshepedišotirišo.path_kind(Lenaneo_tsela) == 0:
        return {}
    return json.loads(tshepedišotirišo.read(Lenaneo_tsela).decode("utf-8"))


def ngwala_pego(Tsejana, data):
    if tshepedišotirišo.write(Tsejana, data) != len(data):
        raise OSError(28)


def lekola_tsela(Tsejana):
    if not isinstance(Tsejana, str) or not Tsejana.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Tsejana.split("/")):
        raise ValueError("허용하지 않는 sehlopha Tsejana")
    if "\\" in Tsejana or any(ord(tlhaka_boleng) < 32 or ord(tlhaka_boleng) == 127 for tlhaka_boleng in Tsejana):
        raise ValueError("잘못된 Tsejana 문자")
    결과 = "/lib/" + Tsejana
    if len(결과.encode("utf-8")) > 63 or Tsejana in ("한국어.py", "sehlopha.py"):
        raise ValueError("sehlopha 경로가 너무 길거나 setsenywa_sa_tirelwa 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Diriša = tshepedišotirišo.ticks_ms()

    def 정확히읽기(자신, botelele_boleng):
        data = bytearray()
        while len(data) < botelele_boleng:
            if tshepedišotirišo.ticks_ms() - 자신.Diriša > 90000:
                raise ValueError("sehlopha 중계 fetola 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = tshepedišotirišo.tcp_read(자신.종단, 512)
                except OSError as Phošo:
                    if Phošo.args[0] != 11:
                        raise
                    tshepedišotirišo.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("sehlopha 전송이 중간에 끝났습니다.")
            개수 = min(botelele_boleng - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            tshepedišotirišo.sleep_ms(0)
        return bytes(data)


def tanelouto(요청, 접속번호):
    if len(요청) > 96 or any(tlhaka_boleng not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for tlhaka_boleng in 요청):
        raise ValueError("사용법: pip install Leina 또는 Leina==버전")
    종단 = tshepedišotirišo.tcp_open()
    try:
        Diriša = tshepedišotirišo.ticks_ms()
        while True:
            try:
                tshepedišotirišo.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Phošo:
                if Phošo.args[0] not in (11, 115) or tshepedišotirišo.ticks_ms() - Diriša > 5000:
                    raise ValueError("sehlopha 중계 Ikgokaganye go_palelwa_boleng: 호스트에서 --network --pip로 실행하십시오.")
                tshepedišotirišo.sleep_ms(10)
        data = (요청 + "\n").encode()
        while data:
            try:
                개수 = tshepedišotirišo.tcp_write(종단, data)
                if not 개수:
                    raise ValueError("sehlopha 요청 fetišetša_boleng go_palelwa_boleng")
                data = data[개수:]
            except OSError as Phošo:
                if Phošo.args[0] != 11:
                    raise
                tshepedišotirišo.sleep_ms(10)
                if tshepedišotirišo.ticks_ms() - Diriša > 10000:
                    raise ValueError("sehlopha 요청 fetišetša_boleng 시간 초과")
        Stream_boleng = 수신흐름(종단)
        머리 = Stream_boleng.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("sehlopha fetišetša_boleng taba_boleng 불일치")
        botelele_boleng = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if botelele_boleng > 8192:
            raise ValueError("sehlopha 명세가 너무 큽니다.")
        명세 = json.loads(Stream_boleng.정확히읽기(botelele_boleng).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 mohlodi_mohlare 파일은 1~16개여야 합니다.")
        if sum(go_tsenya_tshedimošo_boleng["size"] for go_tsenya_tshedimošo_boleng in 명세["files"]) > 65536:
            raise ValueError("sehlopha mohlodi_mohlare 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for go_tsenya_tshedimošo_boleng in 명세["files"]:
            Tsejana = lekola_tsela(go_tsenya_tshedimošo_boleng["path"])
            if Tsejana in 파일들 or not 0 <= go_tsenya_tshedimošo_boleng["size"] <= 16384:
                raise ValueError("중복 Tsejana 또는 Faele Bogolo 초과")
            data = Stream_boleng.정확히읽기(go_tsenya_tshedimošo_boleng["size"])
            if 지문(data) != go_tsenya_tshedimošo_boleng["sha256"]:
                raise ValueError("sehlopha Faele SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), Tsejana, "exec")
            파일들[Tsejana] = data
            gc.collect()
        return 명세, 파일들
    finally:
        tshepedišotirišo.udp_close(종단)


def hloma_boleng(요청, 접속번호):
    print("sehlopha tanelouto:", 요청)
    명세, 파일들 = tanelouto(요청, 접속번호)
    go_tsenya_tshedimošo_Lenaneo = 목록읽기()
    Leina = 명세["name"]
    if Leina in go_tsenya_tshedimošo_Lenaneo:
        if go_tsenya_tshedimošo_Lenaneo[Leina]["version"] == 명세["version"]:
            for Tsejana, 지문값 in go_tsenya_tshedimošo_Lenaneo[Leina]["files"].items():
                if tshepedišotirišo.path_kind(Tsejana) != 1 or 지문(tshepedišotirišo.read(Tsejana)) != 지문값:
                    raise ValueError("설치된 sehlopha 파일이 달라졌습니다: " + Tsejana)
            print("이미 설치됨:", Leina, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Morago_boleng 설치하십시오.")
    for Tsejana in 파일들:
        if tshepedišotirišo.path_kind(Tsejana):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Tsejana)
    go_tsenya_tshedimošo_Lenaneo[Leina] = {"version": 명세["version"], "files": {Tsejana: 지문(data) for Tsejana, data in 파일들.items()}}
    새목록 = json.dumps(go_tsenya_tshedimošo_Lenaneo).encode()
    if len(새목록) > 16384:
        raise ValueError("sehlopha go_tsenya_tshedimošo_Lenaneo Bogolo 초과")
    이전목록 = tshepedišotirišo.read(Lenaneo_tsela) if tshepedišotirišo.path_kind(Lenaneo_tsela) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Tsejana, data in 파일들.items():
            부분들 = Tsejana.split("/")
            for 수 in range(2, len(부분들)):
                lelokelelo_boleng = "/".join(부분들[:수])
                종류 = tshepedišotirišo.path_kind(lelokelelo_boleng)
                if 종류 == 0:
                    tshepedišotirišo.mkdir(lelokelelo_boleng)
                    만든폴더.append(lelokelelo_boleng)
                elif 종류 != 2:
                    raise ValueError("lelokelelo_boleng 경로에 파일이 있습니다: " + lelokelelo_boleng)
            만든파일.append(Tsejana)
            ngwala_pego(Tsejana, data)
        ngwala_pego(Lenaneo_tsela, 새목록)
    except Exception:
        for Tsejana in 만든파일:
            if tshepedišotirišo.path_kind(Tsejana):
                tshepedišotirišo.remove(Tsejana)
        for lelokelelo_boleng in reversed(만든폴더):
            tshepedišotirišo.rmdir(lelokelelo_boleng)
        if 이전목록 is not None:
            ngwala_pego(Lenaneo_tsela, 이전목록)
        elif tshepedišotirišo.path_kind(Lenaneo_tsela):
            tshepedišotirišo.remove(Lenaneo_tsela)
        raise
    print("hloma_boleng 완료:", Leina, 명세["version"], "→ /lib (RAM)")


def tloša_go_tsenya_tshedimošo(Leina):
    go_tsenya_tshedimošo_Lenaneo = 목록읽기()
    if Leina not in go_tsenya_tshedimošo_Lenaneo:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Leina)
    for Tsejana, 지문값 in go_tsenya_tshedimošo_Lenaneo[Leina]["files"].items():
        if tshepedišotirišo.path_kind(Tsejana) != 1 or 지문(tshepedišotirišo.read(Tsejana)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Tsejana)
    for Tsejana in go_tsenya_tshedimošo_Lenaneo[Leina]["files"]:
        tshepedišotirišo.remove(Tsejana)
    del go_tsenya_tshedimošo_Lenaneo[Leina]
    ngwala_pego(Lenaneo_tsela, json.dumps(go_tsenya_tshedimošo_Lenaneo).encode())
    print("tloša_go_tsenya_tshedimošo 완료:", Leina)


def Diriša(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Leina, msinfo32_exe in 목록읽기().items():
            print(Leina, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        hloma_boleng(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        tloša_go_tsenya_tshedimošo(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython mohlodi_mohlare 설치기 (PyPA pip 전체가 아님)")
        print("pip install Leina[==버전] [--port 8027] | pip list | pip uninstall Leina")
        print("go_nea_ditirelo: Ditholosi/phethagatša_taelo.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Diriša(sys.argv[1:])
    except Exception as Phošo:
        print("sehlopha Phošo:", Phošo)
        sys.exit(1)
