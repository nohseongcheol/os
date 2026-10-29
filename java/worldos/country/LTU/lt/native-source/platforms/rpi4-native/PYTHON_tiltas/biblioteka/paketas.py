"""savas 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 organizuoti 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as operacinė_sistema

Sąrašas_kelias = "/lib/.pip.json"


def 지문(duomenys):
    return "".join("%02x" % VALUE for VALUE in hashlib.sha256(duomenys).digest())


def 목록읽기():
    if operacinė_sistema.path_kind(Sąrašas_kelias) == 0:
        return {}
    return json.loads(operacinė_sistema.read(Sąrašas_kelias).decode("utf-8"))


def rašymas_LOG(KELIAS, duomenys):
    if operacinė_sistema.write(KELIAS, duomenys) != len(duomenys):
        raise OSError(28)


def čekis_kelias(KELIAS):
    if not isinstance(KELIAS, str) or not KELIAS.endswith(".py"):
        raise ValueError("Python 소스만 설치할 numeris 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in KELIAS.split("/")):
        raise ValueError("허용하지 않는 paketas KELIAS")
    if "\\" in KELIAS or any(ord(simbolis_VALUE_068c2631) < 32 or ord(simbolis_VALUE_068c2631) == 127 for simbolis_VALUE_068c2631 in KELIAS):
        raise ValueError("잘못된 KELIAS 문자")
    REZULTATAS = "/lib/" + KELIAS
    if len(REZULTATAS.encode("utf-8")) > 63 or KELIAS in ("Lietuvių.py", "paketas.py"):
        raise ValueError("paketas 경로가 너무 길거나 numatytoji_reikšmė 라이브러리와 겹칩니다.")
    return REZULTATAS


class gauti_Stream:
    def __init__(자신, dalyvis):
        자신.dalyvis = dalyvis
        자신.남은자료 = b""
        자신.Paleisti = operacinė_sistema.ticks_ms()

    def 정확히읽기(자신, 길이):
        duomenys = bytearray()
        while len(duomenys) < 길이:
            if operacinė_sistema.ticks_ms() - 자신.Paleisti > 90000:
                raise ValueError("paketas 중계 atsakyti TIME_VALUE 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = operacinė_sistema.tcp_read(자신.dalyvis, 512)
                except OSError as KLAIDA:
                    if KLAIDA.args[0] != 11:
                        raise
                    operacinė_sistema.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paketas 전송이 중간에 끝났습니다.")
            prekė_COUNT = min(길이 - len(duomenys), len(자신.남은자료))
            duomenys.extend(자신.남은자료[:prekė_COUNT])
            자신.남은자료 = 자신.남은자료[prekė_COUNT:]
            operacinė_sistema.sleep_ms(0)
        return bytes(duomenys)


def atsisiųsti(užklausa, prievado_numeris):
    if len(užklausa) > 96 or any(simbolis_VALUE_068c2631 not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for simbolis_VALUE_068c2631 in užklausa):
        raise ValueError("사용법: pip install Pavadinimas_2 또는 Pavadinimas_2==버전")
    dalyvis = operacinė_sistema.tcp_open()
    try:
        Paleisti = operacinė_sistema.ticks_ms()
        while True:
            try:
                operacinė_sistema.tcp_connect(dalyvis, "10.0.2.2", prievado_numeris)
                break
            except OSError as KLAIDA:
                if KLAIDA.args[0] not in (11, 115) or operacinė_sistema.ticks_ms() - Paleisti > 5000:
                    raise ValueError("paketas 중계 Prisijungti triktis_VALUE: 호스트에서 --network --pip로 실행하십시오.")
                operacinė_sistema.sleep_ms(10)
        duomenys = (užklausa + "\n").encode()
        while duomenys:
            try:
                prekė_COUNT = operacinė_sistema.tcp_write(dalyvis, duomenys)
                if not prekė_COUNT:
                    raise ValueError("paketas užklausa perduoti_VALUE_630ba093 triktis_VALUE")
                duomenys = duomenys[prekė_COUNT:]
            except OSError as KLAIDA:
                if KLAIDA.args[0] != 11:
                    raise
                operacinė_sistema.sleep_ms(10)
                if operacinė_sistema.ticks_ms() - Paleisti > 10000:
                    raise ValueError("paketas užklausa perduoti_VALUE_630ba093 TIME_VALUE 초과")
        Stream_VALUE = gauti_Stream(dalyvis)
        머리 = Stream_VALUE.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("paketas perduoti_VALUE_630ba093 sutarties_vertė 불일치")
        길이 = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if 길이 > 8192:
            raise ValueError("paketas 명세가 너무 큽니다.")
        명세 = json.loads(Stream_VALUE.정확히읽기(길이).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 šaltinis_medis 파일은 1~16개여야 합니다.")
        if sum(įrašas_VALUE["size"] for įrašas_VALUE in 명세["files"]) > 65536:
            raise ValueError("paketas šaltinis_medis 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for įrašas_VALUE in 명세["files"]:
            KELIAS = čekis_kelias(įrašas_VALUE["path"])
            if KELIAS in 파일들 or not 0 <= įrašas_VALUE["size"] <= 16384:
                raise ValueError("중복 KELIAS 또는 Failas Dydis 초과")
            duomenys = Stream_VALUE.정확히읽기(įrašas_VALUE["size"])
            if 지문(duomenys) != įrašas_VALUE["sha256"]:
                raise ValueError("paketas Failas SHA-256 불일치")
            # 실행하지 않고 dabartinis_prekė MicroPython의 문법으로 먼저 검사한다.
            compile(duomenys.decode("utf-8"), KELIAS, "exec")
            파일들[KELIAS] = duomenys
            gc.collect()
        return 명세, 파일들
    finally:
        operacinė_sistema.udp_close(dalyvis)


def diegti_VALUE(užklausa, prievado_numeris):
    print("paketas atsisiųsti:", užklausa)
    명세, 파일들 = atsisiųsti(užklausa, prievado_numeris)
    įrašas_Sąrašas = 목록읽기()
    Pavadinimas_2 = 명세["name"]
    if Pavadinimas_2 in įrašas_Sąrašas:
        if įrašas_Sąrašas[Pavadinimas_2]["version"] == 명세["version"]:
            for KELIAS, 지문값 in įrašas_Sąrašas[Pavadinimas_2]["files"].items():
                if operacinė_sistema.path_kind(KELIAS) != 1 or 지문(operacinė_sistema.read(KELIAS)) != 지문값:
                    raise ValueError("설치된 paketas 파일이 달라졌습니다: " + KELIAS)
            print("이미 설치됨:", Pavadinimas_2, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ATGAL_VALUE 설치하십시오.")
    for KELIAS in 파일들:
        if operacinė_sistema.path_kind(KELIAS):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + KELIAS)
    įrašas_Sąrašas[Pavadinimas_2] = {"version": 명세["version"], "files": {KELIAS: 지문(duomenys) for KELIAS, duomenys in 파일들.items()}}
    새목록 = json.dumps(įrašas_Sąrašas).encode()
    if len(새목록) > 16384:
        raise ValueError("paketas įrašas_Sąrašas Dydis 초과")
    이전목록 = operacinė_sistema.read(Sąrašas_kelias) if operacinė_sistema.path_kind(Sąrašas_kelias) else None
    만든파일 = []
    만든폴더 = []
    try:
        for KELIAS, duomenys in 파일들.items():
            부분들 = KELIAS.split("/")
            for numeris in range(2, len(부분들)):
                Katalogas_VALUE = "/".join(부분들[:numeris])
                종류 = operacinė_sistema.path_kind(Katalogas_VALUE)
                if 종류 == 0:
                    operacinė_sistema.mkdir(Katalogas_VALUE)
                    만든폴더.append(Katalogas_VALUE)
                elif 종류 != 2:
                    raise ValueError("Katalogas_VALUE 경로에 파일이 있습니다: " + Katalogas_VALUE)
            만든파일.append(KELIAS)
            rašymas_LOG(KELIAS, duomenys)
        rašymas_LOG(Sąrašas_kelias, 새목록)
    except Exception:
        for KELIAS in 만든파일:
            if operacinė_sistema.path_kind(KELIAS):
                operacinė_sistema.remove(KELIAS)
        for Katalogas_VALUE in reversed(만든폴더):
            operacinė_sistema.rmdir(Katalogas_VALUE)
        if 이전목록 is not None:
            rašymas_LOG(Sąrašas_kelias, 이전목록)
        elif operacinė_sistema.path_kind(Sąrašas_kelias):
            operacinė_sistema.remove(Sąrašas_kelias)
        raise
    print("diegti_VALUE 완료:", Pavadinimas_2, 명세["version"], "→ /lib (RAM)")


def pašalinti_įrašas(Pavadinimas_2):
    įrašas_Sąrašas = 목록읽기()
    if Pavadinimas_2 not in įrašas_Sąrašas:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Pavadinimas_2)
    for KELIAS, 지문값 in įrašas_Sąrašas[Pavadinimas_2]["files"].items():
        if operacinė_sistema.path_kind(KELIAS) != 1 or 지문(operacinė_sistema.read(KELIAS)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + KELIAS)
    for KELIAS in įrašas_Sąrašas[Pavadinimas_2]["files"]:
        operacinė_sistema.remove(KELIAS)
    del įrašas_Sąrašas[Pavadinimas_2]
    rašymas_LOG(Sąrašas_kelias, json.dumps(įrašas_Sąrašas).encode())
    print("pašalinti_įrašas 완료:", Pavadinimas_2)


def Paleisti(Argumentai):
    prievado_numeris = 8027
    if len(Argumentai) >= 2 and Argumentai[-2] == "--port":
        prievado_numeris = int(Argumentai[-1])
        Argumentai = Argumentai[:-2]
    if Argumentai == ["list"]:
        for Pavadinimas_2, msinfo32_exe in 목록읽기().items():
            print(Pavadinimas_2, msinfo32_exe["version"])
    elif len(Argumentai) == 2 and Argumentai[0] == "install":
        diegti_VALUE(Argumentai[1], prievado_numeris)
    elif len(Argumentai) == 2 and Argumentai[0] == "uninstall":
        pašalinti_įrašas(Argumentai[1])
    elif not Argumentai or Argumentai in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython šaltinis_medis 설치기 (PyPA pip 전체가 아님)")
        print("pip install Pavadinimas_2[==버전] [--port 8027] | pip list | pip uninstall Pavadinimas_2")
        print("organizuoti: Įrankiai/Vykdyti_komanda.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Paleisti(sys.argv[1:])
    except Exception as KLAIDA:
        print("paketas KLAIDA:", KLAIDA)
        sys.exit(1)
