"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 singatha 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as isistimu_yokusebenza

Uhlu_umzila = "/lib/.pip.json"


def 지문(imininingwane):
    return "".join("%02x" % inani for inani in hashlib.sha256(imininingwane).digest())


def 목록읽기():
    if isistimu_yokusebenza.path_kind(Uhlu_umzila) == 0:
        return {}
    return json.loads(isistimu_yokusebenza.read(Uhlu_umzila).decode("utf-8"))


def bhala_loga(Indlela_2, imininingwane):
    if isistimu_yokusebenza.write(Indlela_2, imininingwane) != len(imininingwane):
        raise OSError(28)


def hlola_umzila(Indlela_2):
    if not isinstance(Indlela_2, str) or not Indlela_2.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Indlela_2.split("/")):
        raise ValueError("허용하지 않는 isigaxa Indlela_2")
    if "\\" in Indlela_2 or any(ord(uhlamvusimo_inani) < 32 or ord(uhlamvusimo_inani) == 127 for uhlamvusimo_inani in Indlela_2):
        raise ValueError("잘못된 Indlela_2 문자")
    결과 = "/lib/" + Indlela_2
    if len(결과.encode("utf-8")) > 63 or Indlela_2 in ("Isi_Zulu.py", "isigaxa.py"):
        raise ValueError("isigaxa 경로가 너무 길거나 inani_elimisiwe 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.Sebenzisa = isistimu_yokusebenza.ticks_ms()

    def 정확히읽기(자신, ubude_inani):
        imininingwane = bytearray()
        while len(imininingwane) < ubude_inani:
            if isistimu_yokusebenza.ticks_ms() - 자신.Sebenzisa > 90000:
                raise ValueError("isigaxa 중계 phendula 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = isistimu_yokusebenza.tcp_read(자신.종단, 512)
                except OSError as Iphutha:
                    if Iphutha.args[0] != 11:
                        raise
                    isistimu_yokusebenza.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("isigaxa 전송이 중간에 끝났습니다.")
            개수 = min(ubude_inani - len(imininingwane), len(자신.남은자료))
            imininingwane.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            isistimu_yokusebenza.sleep_ms(0)
        return bytes(imininingwane)


def ehlisa(요청, 접속번호):
    if len(요청) > 96 or any(uhlamvusimo_inani not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for uhlamvusimo_inani in 요청):
        raise ValueError("사용법: pip install Igama 또는 Igama==버전")
    종단 = isistimu_yokusebenza.tcp_open()
    try:
        Sebenzisa = isistimu_yokusebenza.ticks_ms()
        while True:
            try:
                isistimu_yokusebenza.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as Iphutha:
                if Iphutha.args[0] not in (11, 115) or isistimu_yokusebenza.ticks_ms() - Sebenzisa > 5000:
                    raise ValueError("isigaxa 중계 Xhumanisa ukwehluleka_inani: 호스트에서 --network --pip로 실행하십시오.")
                isistimu_yokusebenza.sleep_ms(10)
        imininingwane = (요청 + "\n").encode()
        while imininingwane:
            try:
                개수 = isistimu_yokusebenza.tcp_write(종단, imininingwane)
                if not 개수:
                    raise ValueError("isigaxa 요청 dlulisa_inani_630ba093 ukwehluleka_inani")
                imininingwane = imininingwane[개수:]
            except OSError as Iphutha:
                if Iphutha.args[0] != 11:
                    raise
                isistimu_yokusebenza.sleep_ms(10)
                if isistimu_yokusebenza.ticks_ms() - Sebenzisa > 10000:
                    raise ValueError("isigaxa 요청 dlulisa_inani_630ba093 시간 초과")
        Stream_inani = 수신흐름(종단)
        머리 = Stream_inani.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("isigaxa dlulisa_inani_630ba093 udaba_inani 불일치")
        ubude_inani = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if ubude_inani > 8192:
            raise ValueError("isigaxa 명세가 너무 큽니다.")
        명세 = json.loads(Stream_inani.정확히읽기(ubude_inani).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 umthombo_isihlahla 파일은 1~16개여야 합니다.")
        if sum(okufakwayo_inani["size"] for okufakwayo_inani in 명세["files"]) > 65536:
            raise ValueError("isigaxa umthombo_isihlahla 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for okufakwayo_inani in 명세["files"]:
            Indlela_2 = hlola_umzila(okufakwayo_inani["path"])
            if Indlela_2 in 파일들 or not 0 <= okufakwayo_inani["size"] <= 16384:
                raise ValueError("중복 Indlela_2 또는 Ihele Ubungako 초과")
            imininingwane = Stream_inani.정확히읽기(okufakwayo_inani["size"])
            if 지문(imininingwane) != okufakwayo_inani["sha256"]:
                raise ValueError("isigaxa Ihele SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(imininingwane.decode("utf-8"), Indlela_2, "exec")
            파일들[Indlela_2] = imininingwane
            gc.collect()
        return 명세, 파일들
    finally:
        isistimu_yokusebenza.udp_close(종단)


def faka_inani(요청, 접속번호):
    print("isigaxa ehlisa:", 요청)
    명세, 파일들 = ehlisa(요청, 접속번호)
    okufakwayo_Uhlu = 목록읽기()
    Igama = 명세["name"]
    if Igama in okufakwayo_Uhlu:
        if okufakwayo_Uhlu[Igama]["version"] == 명세["version"]:
            for Indlela_2, 지문값 in okufakwayo_Uhlu[Igama]["files"].items():
                if isistimu_yokusebenza.path_kind(Indlela_2) != 1 or 지문(isistimu_yokusebenza.read(Indlela_2)) != 지문값:
                    raise ValueError("설치된 isigaxa 파일이 달라졌습니다: " + Indlela_2)
            print("이미 설치됨:", Igama, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Impindamuva_inani 설치하십시오.")
    for Indlela_2 in 파일들:
        if isistimu_yokusebenza.path_kind(Indlela_2):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Indlela_2)
    okufakwayo_Uhlu[Igama] = {"version": 명세["version"], "files": {Indlela_2: 지문(imininingwane) for Indlela_2, imininingwane in 파일들.items()}}
    새목록 = json.dumps(okufakwayo_Uhlu).encode()
    if len(새목록) > 16384:
        raise ValueError("isigaxa okufakwayo_Uhlu Ubungako 초과")
    이전목록 = isistimu_yokusebenza.read(Uhlu_umzila) if isistimu_yokusebenza.path_kind(Uhlu_umzila) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Indlela_2, imininingwane in 파일들.items():
            부분들 = Indlela_2.split("/")
            for 수 in range(2, len(부분들)):
                umkhombandlela_inani = "/".join(부분들[:수])
                종류 = isistimu_yokusebenza.path_kind(umkhombandlela_inani)
                if 종류 == 0:
                    isistimu_yokusebenza.mkdir(umkhombandlela_inani)
                    만든폴더.append(umkhombandlela_inani)
                elif 종류 != 2:
                    raise ValueError("umkhombandlela_inani 경로에 파일이 있습니다: " + umkhombandlela_inani)
            만든파일.append(Indlela_2)
            bhala_loga(Indlela_2, imininingwane)
        bhala_loga(Uhlu_umzila, 새목록)
    except Exception:
        for Indlela_2 in 만든파일:
            if isistimu_yokusebenza.path_kind(Indlela_2):
                isistimu_yokusebenza.remove(Indlela_2)
        for umkhombandlela_inani in reversed(만든폴더):
            isistimu_yokusebenza.rmdir(umkhombandlela_inani)
        if 이전목록 is not None:
            bhala_loga(Uhlu_umzila, 이전목록)
        elif isistimu_yokusebenza.path_kind(Uhlu_umzila):
            isistimu_yokusebenza.remove(Uhlu_umzila)
        raise
    print("faka_inani 완료:", Igama, 명세["version"], "→ /lib (RAM)")


def khipha_okufakwayo(Igama):
    okufakwayo_Uhlu = 목록읽기()
    if Igama not in okufakwayo_Uhlu:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Igama)
    for Indlela_2, 지문값 in okufakwayo_Uhlu[Igama]["files"].items():
        if isistimu_yokusebenza.path_kind(Indlela_2) != 1 or 지문(isistimu_yokusebenza.read(Indlela_2)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Indlela_2)
    for Indlela_2 in okufakwayo_Uhlu[Igama]["files"]:
        isistimu_yokusebenza.remove(Indlela_2)
    del okufakwayo_Uhlu[Igama]
    bhala_loga(Uhlu_umzila, json.dumps(okufakwayo_Uhlu).encode())
    print("khipha_okufakwayo 완료:", Igama)


def Sebenzisa(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Igama, I_msinfo32_exe in 목록읽기().items():
            print(Igama, I_msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        faka_inani(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        khipha_okufakwayo(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython umthombo_isihlahla 설치기 (PyPA pip 전체가 아님)")
        print("pip install Igama[==버전] [--port 8027] | pip list | pip uninstall Igama")
        print("singatha: Amathuluzi/yenza_umyalo.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Sebenzisa(sys.argv[1:])
    except Exception as Iphutha:
        print("isigaxa Iphutha:", Iphutha)
        sys.exit(1)
