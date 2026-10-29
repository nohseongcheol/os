"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 pinagare 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as Tsamaisotiriso

lenaane_tsela = "/lib/.pip.json"


def 지문(tshedimosetso):
    return "".join("%02x" % Boleng for Boleng in hashlib.sha256(tshedimosetso).digest())


def 목록읽기():
    if Tsamaisotiriso.path_kind(lenaane_tsela) == 0:
        return {}
    return json.loads(Tsamaisotiriso.read(lenaane_tsela).decode("utf-8"))


def kwala_rekota(tsela, tshedimosetso):
    if Tsamaisotiriso.write(tsela, tshedimosetso) != len(tshedimosetso):
        raise OSError(28)


def tlhola_tsela(tsela):
    if not isinstance(tsela, str) or not tsela.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in tsela.split("/")):
        raise ValueError("허용하지 않는 ngatanngwe tsela")
    if "\\" in tsela or any(ord(Letshwao_Boleng) < 32 or ord(Letshwao_Boleng) == 127 for Letshwao_Boleng in tsela):
        raise ValueError("잘못된 tsela 문자")
    결과 = "/lib/" + tsela
    if len(결과.encode("utf-8")) > 63 or tsela in ("한국어.py", "ngatanngwe.py"):
        raise ValueError("ngatanngwe 경로가 너무 길거나 boleng_jo_bo_rulaganyeditsweng_ruri 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.dirisa = Tsamaisotiriso.ticks_ms()

    def 정확히읽기(자신, boleele_Boleng):
        tshedimosetso = bytearray()
        while len(tshedimosetso) < boleele_Boleng:
            if Tsamaisotiriso.ticks_ms() - 자신.dirisa > 90000:
                raise ValueError("ngatanngwe 중계 araba 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = Tsamaisotiriso.tcp_read(자신.종단, 512)
                except OSError as phoso:
                    if phoso.args[0] != 11:
                        raise
                    Tsamaisotiriso.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ngatanngwe 전송이 중간에 끝났습니다.")
            개수 = min(boleele_Boleng - len(tshedimosetso), len(자신.남은자료))
            tshedimosetso.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            Tsamaisotiriso.sleep_ms(0)
        return bytes(tshedimosetso)


def laisolola(요청, 접속번호):
    if len(요청) > 96 or any(Letshwao_Boleng not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for Letshwao_Boleng in 요청):
        raise ValueError("사용법: pip install leina 또는 leina==버전")
    종단 = Tsamaisotiriso.tcp_open()
    try:
        dirisa = Tsamaisotiriso.ticks_ms()
        while True:
            try:
                Tsamaisotiriso.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as phoso:
                if phoso.args[0] not in (11, 115) or Tsamaisotiriso.ticks_ms() - dirisa > 5000:
                    raise ValueError("ngatanngwe 중계 Golaganya palelo_Boleng: 호스트에서 --network --pip로 실행하십시오.")
                Tsamaisotiriso.sleep_ms(10)
        tshedimosetso = (요청 + "\n").encode()
        while tshedimosetso:
            try:
                개수 = Tsamaisotiriso.tcp_write(종단, tshedimosetso)
                if not 개수:
                    raise ValueError("ngatanngwe 요청 fudusa_Boleng palelo_Boleng")
                tshedimosetso = tshedimosetso[개수:]
            except OSError as phoso:
                if phoso.args[0] != 11:
                    raise
                Tsamaisotiriso.sleep_ms(10)
                if Tsamaisotiriso.ticks_ms() - dirisa > 10000:
                    raise ValueError("ngatanngwe 요청 fudusa_Boleng 시간 초과")
        moela_Boleng = 수신흐름(종단)
        머리 = moela_Boleng.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ngatanngwe fudusa_Boleng konteraka_Boleng 불일치")
        boleele_Boleng = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if boleele_Boleng > 8192:
            raise ValueError("ngatanngwe 명세가 너무 큽니다.")
        명세 = json.loads(moela_Boleng.정확히읽기(boleele_Boleng).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 Motswedi_sebopego_sa_tshedimosetso 파일은 1~16개여야 합니다.")
        if sum(tsenyo_Boleng["size"] for tsenyo_Boleng in 명세["files"]) > 65536:
            raise ValueError("ngatanngwe Motswedi_sebopego_sa_tshedimosetso 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for tsenyo_Boleng in 명세["files"]:
            tsela = tlhola_tsela(tsenyo_Boleng["path"])
            if tsela in 파일들 or not 0 <= tsenyo_Boleng["size"] <= 16384:
                raise ValueError("중복 tsela 또는 faele lekanya 초과")
            tshedimosetso = moela_Boleng.정확히읽기(tsenyo_Boleng["size"])
            if 지문(tshedimosetso) != tsenyo_Boleng["sha256"]:
                raise ValueError("ngatanngwe faele SHA-256 불일치")
            # 실행하지 않고 ga_jaana_selwana MicroPython의 문법으로 먼저 검사한다.
            compile(tshedimosetso.decode("utf-8"), tsela, "exec")
            파일들[tsela] = tshedimosetso
            gc.collect()
        return 명세, 파일들
    finally:
        Tsamaisotiriso.udp_close(종단)


def tsenya_Boleng(요청, 접속번호):
    print("ngatanngwe laisolola:", 요청)
    명세, 파일들 = laisolola(요청, 접속번호)
    tsenyo_lenaane = 목록읽기()
    leina = 명세["name"]
    if leina in tsenyo_lenaane:
        if tsenyo_lenaane[leina]["version"] == 명세["version"]:
            for tsela, 지문값 in tsenyo_lenaane[leina]["files"].items():
                if Tsamaisotiriso.path_kind(tsela) != 1 or 지문(Tsamaisotiriso.read(tsela)) != 지문값:
                    raise ValueError("설치된 ngatanngwe 파일이 달라졌습니다: " + tsela)
            print("이미 설치됨:", leina, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Morago_Boleng 설치하십시오.")
    for tsela in 파일들:
        if Tsamaisotiriso.path_kind(tsela):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + tsela)
    tsenyo_lenaane[leina] = {"version": 명세["version"], "files": {tsela: 지문(tshedimosetso) for tsela, tshedimosetso in 파일들.items()}}
    새목록 = json.dumps(tsenyo_lenaane).encode()
    if len(새목록) > 16384:
        raise ValueError("ngatanngwe tsenyo_lenaane lekanya 초과")
    이전목록 = Tsamaisotiriso.read(lenaane_tsela) if Tsamaisotiriso.path_kind(lenaane_tsela) else None
    만든파일 = []
    만든폴더 = []
    try:
        for tsela, tshedimosetso in 파일들.items():
            부분들 = tsela.split("/")
            for 수 in range(2, len(부분들)):
                Lenaneofaele_Boleng = "/".join(부분들[:수])
                종류 = Tsamaisotiriso.path_kind(Lenaneofaele_Boleng)
                if 종류 == 0:
                    Tsamaisotiriso.mkdir(Lenaneofaele_Boleng)
                    만든폴더.append(Lenaneofaele_Boleng)
                elif 종류 != 2:
                    raise ValueError("Lenaneofaele_Boleng 경로에 파일이 있습니다: " + Lenaneofaele_Boleng)
            만든파일.append(tsela)
            kwala_rekota(tsela, tshedimosetso)
        kwala_rekota(lenaane_tsela, 새목록)
    except Exception:
        for tsela in 만든파일:
            if Tsamaisotiriso.path_kind(tsela):
                Tsamaisotiriso.remove(tsela)
        for Lenaneofaele_Boleng in reversed(만든폴더):
            Tsamaisotiriso.rmdir(Lenaneofaele_Boleng)
        if 이전목록 is not None:
            kwala_rekota(lenaane_tsela, 이전목록)
        elif Tsamaisotiriso.path_kind(lenaane_tsela):
            Tsamaisotiriso.remove(lenaane_tsela)
        raise
    print("tsenya_Boleng 완료:", leina, 명세["version"], "→ /lib (RAM)")


def tlosa_tsenyo(leina):
    tsenyo_lenaane = 목록읽기()
    if leina not in tsenyo_lenaane:
        raise ValueError("설치되지 않은 꾸러미입니다: " + leina)
    for tsela, 지문값 in tsenyo_lenaane[leina]["files"].items():
        if Tsamaisotiriso.path_kind(tsela) != 1 or 지문(Tsamaisotiriso.read(tsela)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + tsela)
    for tsela in tsenyo_lenaane[leina]["files"]:
        Tsamaisotiriso.remove(tsela)
    del tsenyo_lenaane[leina]
    kwala_rekota(lenaane_tsela, json.dumps(tsenyo_lenaane).encode())
    print("tlosa_tsenyo 완료:", leina)


def dirisa(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for leina, msinfo32_exe in 목록읽기().items():
            print(leina, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        tsenya_Boleng(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        tlosa_tsenyo(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython Motswedi_sebopego_sa_tshedimosetso 설치기 (PyPA pip 전체가 아님)")
        print("pip install leina[==버전] [--port 8027] | pip list | pip uninstall leina")
        print("pinagare: Thuluse/diragatsa_Taelo.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        dirisa(sys.argv[1:])
    except Exception as phoso:
        print("ngatanngwe phoso:", phoso)
        sys.exit(1)
