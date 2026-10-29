"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 umsingathi 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as Indlela_yokusebenza

uludwe_indlela = "/lib/.pip.json"


def 지문(iingcombolo):
    return "".join("%02x" % ixabiso for ixabiso in hashlib.sha256(iingcombolo).digest())


def 목록읽기():
    if Indlela_yokusebenza.path_kind(uludwe_indlela) == 0:
        return {}
    return json.loads(Indlela_yokusebenza.read(uludwe_indlela).decode("utf-8"))


def bhala_ilog(INDLELA, iingcombolo):
    if Indlela_yokusebenza.write(INDLELA, iingcombolo) != len(iingcombolo):
        raise OSError(28)


def jonga_indlela(INDLELA):
    if not isinstance(INDLELA, str) or not INDLELA.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in INDLELA.split("/")):
        raise ValueError("허용하지 않는 umqulu INDLELA")
    if "\\" in INDLELA or any(ord(ikharakhtha_ixabiso) < 32 or ord(ikharakhtha_ixabiso) == 127 for ikharakhtha_ixabiso in INDLELA):
        raise ValueError("잘못된 INDLELA 문자")
    결과 = "/lib/" + INDLELA
    if len(결과.encode("utf-8")) > 63 or INDLELA in ("isiXhosa.py", "umqulu.py"):
        raise ValueError("umqulu 경로가 너무 길거나 ixabiso_elisisiseko 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Phumeza = Indlela_yokusebenza.ticks_ms()

    def 정확히읽기(자신, ubude_ixabiso):
        iingcombolo = bytearray()
        while len(iingcombolo) < ubude_ixabiso:
            if Indlela_yokusebenza.ticks_ms() - 자신.Phumeza > 90000:
                raise ValueError("umqulu 중계 phendula 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = Indlela_yokusebenza.tcp_read(자신.종단, 512)
                except OSError as Impazamo:
                    if Impazamo.args[0] != 11:
                        raise
                    Indlela_yokusebenza.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("umqulu 전송이 중간에 끝났습니다.")
            개수 = min(ubude_ixabiso - len(iingcombolo), len(자신.남은자료))
            iingcombolo.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            Indlela_yokusebenza.sleep_ms(0)
        return bytes(iingcombolo)


def khuphela(요청, 접속번호):
    if len(요청) > 96 or any(ikharakhtha_ixabiso not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for ikharakhtha_ixabiso in 요청):
        raise ValueError("사용법: pip install Igama 또는 Igama==버전")
    종단 = Indlela_yokusebenza.tcp_open()
    try:
        Phumeza = Indlela_yokusebenza.ticks_ms()
        while True:
            try:
                Indlela_yokusebenza.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Impazamo:
                if Impazamo.args[0] not in (11, 115) or Indlela_yokusebenza.ticks_ms() - Phumeza > 5000:
                    raise ValueError("umqulu 중계 Nxulumanisa ukungaphumeleli_ixabiso: 호스트에서 --network --pip로 실행하십시오.")
                Indlela_yokusebenza.sleep_ms(10)
        iingcombolo = (요청 + "\n").encode()
        while iingcombolo:
            try:
                개수 = Indlela_yokusebenza.tcp_write(종단, iingcombolo)
                if not 개수:
                    raise ValueError("umqulu 요청 gqithisela_ixabiso ukungaphumeleli_ixabiso")
                iingcombolo = iingcombolo[개수:]
            except OSError as Impazamo:
                if Impazamo.args[0] != 11:
                    raise
                Indlela_yokusebenza.sleep_ms(10)
                if Indlela_yokusebenza.ticks_ms() - Phumeza > 10000:
                    raise ValueError("umqulu 요청 gqithisela_ixabiso 시간 초과")
        Stream_ixabiso = 수신흐름(종단)
        머리 = Stream_ixabiso.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("umqulu gqithisela_ixabiso isiganeko_ixabiso 불일치")
        ubude_ixabiso = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ubude_ixabiso > 8192:
            raise ValueError("umqulu 명세가 너무 큽니다.")
        명세 = json.loads(Stream_ixabiso.정확히읽기(ubude_ixabiso).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 umthombo_umthi 파일은 1~16개여야 합니다.")
        if sum(ufako_nkcukacha_ixabiso["size"] for ufako_nkcukacha_ixabiso in 명세["files"]) > 65536:
            raise ValueError("umqulu umthombo_umthi 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ufako_nkcukacha_ixabiso in 명세["files"]:
            INDLELA = jonga_indlela(ufako_nkcukacha_ixabiso["path"])
            if INDLELA in 파일들 or not 0 <= ufako_nkcukacha_ixabiso["size"] <= 16384:
                raise ValueError("중복 INDLELA 또는 iFayili Ubukhulu 초과")
            iingcombolo = Stream_ixabiso.정확히읽기(ufako_nkcukacha_ixabiso["size"])
            if 지문(iingcombolo) != ufako_nkcukacha_ixabiso["sha256"]:
                raise ValueError("umqulu iFayili SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(iingcombolo.decode("utf-8"), INDLELA, "exec")
            파일들[INDLELA] = iingcombolo
            gc.collect()
        return 명세, 파일들
    finally:
        Indlela_yokusebenza.udp_close(종단)


def fakela_ixabiso(요청, 접속번호):
    print("umqulu khuphela:", 요청)
    명세, 파일들 = khuphela(요청, 접속번호)
    ufako_nkcukacha_uludwe = 목록읽기()
    Igama = 명세["name"]
    if Igama in ufako_nkcukacha_uludwe:
        if ufako_nkcukacha_uludwe[Igama]["version"] == 명세["version"]:
            for INDLELA, 지문값 in ufako_nkcukacha_uludwe[Igama]["files"].items():
                if Indlela_yokusebenza.path_kind(INDLELA) != 1 or 지문(Indlela_yokusebenza.read(INDLELA)) != 지문값:
                    raise ValueError("설치된 umqulu 파일이 달라졌습니다: " + INDLELA)
            print("이미 설치됨:", Igama, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Emva_ixabiso 설치하십시오.")
    for INDLELA in 파일들:
        if Indlela_yokusebenza.path_kind(INDLELA):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + INDLELA)
    ufako_nkcukacha_uludwe[Igama] = {"version": 명세["version"], "files": {INDLELA: 지문(iingcombolo) for INDLELA, iingcombolo in 파일들.items()}}
    새목록 = json.dumps(ufako_nkcukacha_uludwe).encode()
    if len(새목록) > 16384:
        raise ValueError("umqulu ufako_nkcukacha_uludwe Ubukhulu 초과")
    이전목록 = Indlela_yokusebenza.read(uludwe_indlela) if Indlela_yokusebenza.path_kind(uludwe_indlela) else None
    만든파일 = []
    만든폴더 = []
    try:
        for INDLELA, iingcombolo in 파일들.items():
            부분들 = INDLELA.split("/")
            for 수 in range(2, len(부분들)):
                isalathisi_ixabiso_e5561a2b = "/".join(부분들[:수])
                종류 = Indlela_yokusebenza.path_kind(isalathisi_ixabiso_e5561a2b)
                if 종류 == 0:
                    Indlela_yokusebenza.mkdir(isalathisi_ixabiso_e5561a2b)
                    만든폴더.append(isalathisi_ixabiso_e5561a2b)
                elif 종류 != 2:
                    raise ValueError("isalathisi_ixabiso_e5561a2b 경로에 파일이 있습니다: " + isalathisi_ixabiso_e5561a2b)
            만든파일.append(INDLELA)
            bhala_ilog(INDLELA, iingcombolo)
        bhala_ilog(uludwe_indlela, 새목록)
    except Exception:
        for INDLELA in 만든파일:
            if Indlela_yokusebenza.path_kind(INDLELA):
                Indlela_yokusebenza.remove(INDLELA)
        for isalathisi_ixabiso_e5561a2b in reversed(만든폴더):
            Indlela_yokusebenza.rmdir(isalathisi_ixabiso_e5561a2b)
        if 이전목록 is not None:
            bhala_ilog(uludwe_indlela, 이전목록)
        elif Indlela_yokusebenza.path_kind(uludwe_indlela):
            Indlela_yokusebenza.remove(uludwe_indlela)
        raise
    print("fakela_ixabiso 완료:", Igama, 명세["version"], "→ /lib (RAM)")


def shenxisa_ufako_nkcukacha(Igama):
    ufako_nkcukacha_uludwe = 목록읽기()
    if Igama not in ufako_nkcukacha_uludwe:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Igama)
    for INDLELA, 지문값 in ufako_nkcukacha_uludwe[Igama]["files"].items():
        if Indlela_yokusebenza.path_kind(INDLELA) != 1 or 지문(Indlela_yokusebenza.read(INDLELA)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + INDLELA)
    for INDLELA in ufako_nkcukacha_uludwe[Igama]["files"]:
        Indlela_yokusebenza.remove(INDLELA)
    del ufako_nkcukacha_uludwe[Igama]
    bhala_ilog(uludwe_indlela, json.dumps(ufako_nkcukacha_uludwe).encode())
    print("shenxisa_ufako_nkcukacha 완료:", Igama)


def Phumeza(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Igama, i_msinfo32_exe in 목록읽기().items():
            print(Igama, i_msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        fakela_ixabiso(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        shenxisa_ufako_nkcukacha(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython umthombo_umthi 설치기 (PyPA pip 전체가 아님)")
        print("pip install Igama[==버전] [--port 8027] | pip list | pip uninstall Igama")
        print("umsingathi: Izixhobo/ukwenza_umyalelo.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Phumeza(sys.argv[1:])
    except Exception as Impazamo:
        print("umqulu Impazamo:", Impazamo)
        sys.exit(1)
