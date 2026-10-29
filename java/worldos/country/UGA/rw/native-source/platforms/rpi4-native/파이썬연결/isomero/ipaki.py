"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 gucumbikira 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sisitemu_ngengamikorere

Urutonde_inzira = "/lib/.pip.json"


def 지문(amakurushingiro):
    return "".join("%02x" % agaciro for agaciro in hashlib.sha256(amakurushingiro).digest())


def 목록읽기():
    if sisitemu_ngengamikorere.path_kind(Urutonde_inzira) == 0:
        return {}
    return json.loads(sisitemu_ngengamikorere.read(Urutonde_inzira).decode("utf-8"))


def kwandika_kubika(Inzira, amakurushingiro):
    if sisitemu_ngengamikorere.write(Inzira, amakurushingiro) != len(amakurushingiro):
        raise OSError(28)


def sheki_inzira(Inzira):
    if not isinstance(Inzira, str) or not Inzira.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Inzira.split("/")):
        raise ValueError("허용하지 않는 ipaki Inzira")
    if "\\" in Inzira or any(ord(inyuguti_agaciro) < 32 or ord(inyuguti_agaciro) == 127 for inyuguti_agaciro in Inzira):
        raise ValueError("잘못된 Inzira 문자")
    결과 = "/lib/" + Inzira
    if len(결과.encode("utf-8")) > 63 or Inzira in ("Ikinyarwanda.py", "ipaki.py"):
        raise ValueError("ipaki 경로가 너무 길거나 agaciro_gasanzweho 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.ihuriro = sisitemu_ngengamikorere.ticks_ms()

    def 정확히읽기(자신, uburebure_agaciro):
        amakurushingiro = bytearray()
        while len(amakurushingiro) < uburebure_agaciro:
            if sisitemu_ngengamikorere.ticks_ms() - 자신.ihuriro > 90000:
                raise ValueError("ipaki 중계 gusubiza 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sisitemu_ngengamikorere.tcp_read(자신.종단, 512)
                except OSError as IKOSA:
                    if IKOSA.args[0] != 11:
                        raise
                    sisitemu_ngengamikorere.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("ipaki 전송이 중간에 끝났습니다.")
            개수 = min(uburebure_agaciro - len(amakurushingiro), len(자신.남은자료))
            amakurushingiro.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            sisitemu_ngengamikorere.sleep_ms(0)
        return bytes(amakurushingiro)


def gukurura(요청, 접속번호):
    if len(요청) > 96 or any(inyuguti_agaciro not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for inyuguti_agaciro in 요청):
        raise ValueError("사용법: pip install Izina 또는 Izina==버전")
    종단 = sisitemu_ngengamikorere.tcp_open()
    try:
        ihuriro = sisitemu_ngengamikorere.ticks_ms()
        while True:
            try:
                sisitemu_ngengamikorere.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as IKOSA:
                if IKOSA.args[0] not in (11, 115) or sisitemu_ngengamikorere.ticks_ms() - ihuriro > 5000:
                    raise ValueError("ipaki 중계 Guhuza kudakora_agaciro: 호스트에서 --network --pip로 실행하십시오.")
                sisitemu_ngengamikorere.sleep_ms(10)
        amakurushingiro = (요청 + "\n").encode()
        while amakurushingiro:
            try:
                개수 = sisitemu_ngengamikorere.tcp_write(종단, amakurushingiro)
                if not 개수:
                    raise ValueError("ipaki 요청 iyimura_agaciro kudakora_agaciro")
                amakurushingiro = amakurushingiro[개수:]
            except OSError as IKOSA:
                if IKOSA.args[0] != 11:
                    raise
                sisitemu_ngengamikorere.sleep_ms(10)
                if sisitemu_ngengamikorere.ticks_ms() - ihuriro > 10000:
                    raise ValueError("ipaki 요청 iyimura_agaciro 시간 초과")
        Stream_agaciro = 수신흐름(종단)
        머리 = Stream_agaciro.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("ipaki iyimura_agaciro ikibazo_agaciro 불일치")
        uburebure_agaciro = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if uburebure_agaciro > 8192:
            raise ValueError("ipaki 명세가 너무 큽니다.")
        명세 = json.loads(Stream_agaciro.정확히읽기(uburebure_agaciro).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 inkomoko_igiti 파일은 1~16개여야 합니다.")
        if sum(icyinjizwa_agaciro["size"] for icyinjizwa_agaciro in 명세["files"]) > 65536:
            raise ValueError("ipaki inkomoko_igiti 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for icyinjizwa_agaciro in 명세["files"]:
            Inzira = sheki_inzira(icyinjizwa_agaciro["path"])
            if Inzira in 파일들 or not 0 <= icyinjizwa_agaciro["size"] <= 16384:
                raise ValueError("중복 Inzira 또는 Idosiye Ingano 초과")
            amakurushingiro = Stream_agaciro.정확히읽기(icyinjizwa_agaciro["size"])
            if 지문(amakurushingiro) != icyinjizwa_agaciro["sha256"]:
                raise ValueError("ipaki Idosiye SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(amakurushingiro.decode("utf-8"), Inzira, "exec")
            파일들[Inzira] = amakurushingiro
            gc.collect()
        return 명세, 파일들
    finally:
        sisitemu_ngengamikorere.udp_close(종단)


def kwinjiza_agaciro(요청, 접속번호):
    print("ipaki gukurura:", 요청)
    명세, 파일들 = gukurura(요청, 접속번호)
    icyinjizwa_Urutonde = 목록읽기()
    Izina = 명세["name"]
    if Izina in icyinjizwa_Urutonde:
        if icyinjizwa_Urutonde[Izina]["version"] == 명세["version"]:
            for Inzira, 지문값 in icyinjizwa_Urutonde[Izina]["files"].items():
                if sisitemu_ngengamikorere.path_kind(Inzira) != 1 or 지문(sisitemu_ngengamikorere.read(Inzira)) != 지문값:
                    raise ValueError("설치된 ipaki 파일이 달라졌습니다: " + Inzira)
            print("이미 설치됨:", Izina, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Ikibanza_agaciro 설치하십시오.")
    for Inzira in 파일들:
        if sisitemu_ngengamikorere.path_kind(Inzira):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Inzira)
    icyinjizwa_Urutonde[Izina] = {"version": 명세["version"], "files": {Inzira: 지문(amakurushingiro) for Inzira, amakurushingiro in 파일들.items()}}
    새목록 = json.dumps(icyinjizwa_Urutonde).encode()
    if len(새목록) > 16384:
        raise ValueError("ipaki icyinjizwa_Urutonde Ingano 초과")
    이전목록 = sisitemu_ngengamikorere.read(Urutonde_inzira) if sisitemu_ngengamikorere.path_kind(Urutonde_inzira) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Inzira, amakurushingiro in 파일들.items():
            부분들 = Inzira.split("/")
            for 수 in range(2, len(부분들)):
                ububiko_agaciro_e5561a2b = "/".join(부분들[:수])
                종류 = sisitemu_ngengamikorere.path_kind(ububiko_agaciro_e5561a2b)
                if 종류 == 0:
                    sisitemu_ngengamikorere.mkdir(ububiko_agaciro_e5561a2b)
                    만든폴더.append(ububiko_agaciro_e5561a2b)
                elif 종류 != 2:
                    raise ValueError("ububiko_agaciro_e5561a2b 경로에 파일이 있습니다: " + ububiko_agaciro_e5561a2b)
            만든파일.append(Inzira)
            kwandika_kubika(Inzira, amakurushingiro)
        kwandika_kubika(Urutonde_inzira, 새목록)
    except Exception:
        for Inzira in 만든파일:
            if sisitemu_ngengamikorere.path_kind(Inzira):
                sisitemu_ngengamikorere.remove(Inzira)
        for ububiko_agaciro_e5561a2b in reversed(만든폴더):
            sisitemu_ngengamikorere.rmdir(ububiko_agaciro_e5561a2b)
        if 이전목록 is not None:
            kwandika_kubika(Urutonde_inzira, 이전목록)
        elif sisitemu_ngengamikorere.path_kind(Urutonde_inzira):
            sisitemu_ngengamikorere.remove(Urutonde_inzira)
        raise
    print("kwinjiza_agaciro 완료:", Izina, 명세["version"], "→ /lib (RAM)")


def gukuramo_icyinjizwa(Izina):
    icyinjizwa_Urutonde = 목록읽기()
    if Izina not in icyinjizwa_Urutonde:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Izina)
    for Inzira, 지문값 in icyinjizwa_Urutonde[Izina]["files"].items():
        if sisitemu_ngengamikorere.path_kind(Inzira) != 1 or 지문(sisitemu_ngengamikorere.read(Inzira)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Inzira)
    for Inzira in icyinjizwa_Urutonde[Izina]["files"]:
        sisitemu_ngengamikorere.remove(Inzira)
    del icyinjizwa_Urutonde[Izina]
    kwandika_kubika(Urutonde_inzira, json.dumps(icyinjizwa_Urutonde).encode())
    print("gukuramo_icyinjizwa 완료:", Izina)


def ihuriro(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Izina, msinfo32_exe in 목록읽기().items():
            print(Izina, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        kwinjiza_agaciro(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        gukuramo_icyinjizwa(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython inkomoko_igiti 설치기 (PyPA pip 전체가 아님)")
        print("pip install Izina[==버전] [--port 8027] | pip list | pip uninstall Izina")
        print("gucumbikira: Ibikoresho/gukora_ibwiriza.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        ihuriro(sys.argv[1:])
    except Exception as IKOSA:
        print("ipaki IKOSA:", IKOSA)
        sys.exit(1)
