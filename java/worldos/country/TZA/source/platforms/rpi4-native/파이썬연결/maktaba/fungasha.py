"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 mwenyeji 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as mfumo_endeshi

Orodha_njia = "/lib/.pip.json"


def 지문(data):
    return "".join("%02x" % thamani for thamani in hashlib.sha256(data).digest())


def 목록읽기():
    if mfumo_endeshi.path_kind(Orodha_njia) == 0:
        return {}
    return json.loads(mfumo_endeshi.read(Orodha_njia).decode("utf-8"))


def andika_batli(njia, data):
    if mfumo_endeshi.write(njia, data) != len(data):
        raise OSError(28)


def hundi_njia(njia):
    if not isinstance(njia, str) or not njia.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in njia.split("/")):
        raise ValueError("허용하지 않는 fungasha njia")
    if "\\" in njia or any(ord(kibambo_thamani) < 32 or ord(kibambo_thamani) == 127 for kibambo_thamani in njia):
        raise ValueError("잘못된 njia 문자")
    결과 = "/lib/" + njia
    if len(결과.encode("utf-8")) > 63 or njia in ("한국어.py", "fungasha.py"):
        raise ValueError("fungasha 경로가 너무 길거나 hali_ya_chaguo_msingi 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.endesha = mfumo_endeshi.ticks_ms()

    def 정확히읽기(자신, urefu_thamani):
        data = bytearray()
        while len(data) < urefu_thamani:
            if mfumo_endeshi.ticks_ms() - 자신.endesha > 90000:
                raise ValueError("fungasha 중계 jibu saa_thamani_4692cef5 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = mfumo_endeshi.tcp_read(자신.종단, 512)
                except OSError as kosa:
                    if kosa.args[0] != 11:
                        raise
                    mfumo_endeshi.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("fungasha 전송이 중간에 끝났습니다.")
            개수 = min(urefu_thamani - len(data), len(자신.남은자료))
            data.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            mfumo_endeshi.sleep_ms(0)
        return bytes(data)


def pakua(요청, namba_ya_kituo):
    if len(요청) > 96 or any(kibambo_thamani not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for kibambo_thamani in 요청):
        raise ValueError("사용법: pip install Jina 또는 Jina==버전")
    종단 = mfumo_endeshi.tcp_open()
    try:
        endesha = mfumo_endeshi.ticks_ms()
        while True:
            try:
                mfumo_endeshi.tcp_connect(종단, "10.0.2.2", namba_ya_kituo)
                break
            except OSError as kosa:
                if kosa.args[0] not in (11, 115) or mfumo_endeshi.ticks_ms() - endesha > 5000:
                    raise ValueError("fungasha 중계 UNGANISHA kushindwa_thamani: 호스트에서 --network --pip로 실행하십시오.")
                mfumo_endeshi.sleep_ms(10)
        data = (요청 + "\n").encode()
        while data:
            try:
                개수 = mfumo_endeshi.tcp_write(종단, data)
                if not 개수:
                    raise ValueError("fungasha 요청 hamisha_thamani_630ba093 kushindwa_thamani")
                data = data[개수:]
            except OSError as kosa:
                if kosa.args[0] != 11:
                    raise
                mfumo_endeshi.sleep_ms(10)
                if mfumo_endeshi.ticks_ms() - endesha > 10000:
                    raise ValueError("fungasha 요청 hamisha_thamani_630ba093 saa_thamani_4692cef5 초과")
        Stream_thamani = 수신흐름(종단)
        머리 = Stream_thamani.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("fungasha hamisha_thamani_630ba093 Kazi_thamani 불일치")
        urefu_thamani = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if urefu_thamani > 8192:
            raise ValueError("fungasha 명세가 너무 큽니다.")
        명세 = json.loads(Stream_thamani.정확히읽기(urefu_thamani).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 chanzo_mti 파일은 1~16개여야 합니다.")
        if sum(ingizo_thamani["size"] for ingizo_thamani in 명세["files"]) > 65536:
            raise ValueError("fungasha chanzo_mti 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for ingizo_thamani in 명세["files"]:
            njia = hundi_njia(ingizo_thamani["path"])
            if njia in 파일들 or not 0 <= ingizo_thamani["size"] <= 16384:
                raise ValueError("중복 njia 또는 faili panga_ukubwa 초과")
            data = Stream_thamani.정확히읽기(ingizo_thamani["size"])
            if 지문(data) != ingizo_thamani["sha256"]:
                raise ValueError("fungasha faili SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), njia, "exec")
            파일들[njia] = data
            gc.collect()
        return 명세, 파일들
    finally:
        mfumo_endeshi.udp_close(종단)


def sakinisha_thamani(요청, namba_ya_kituo):
    print("fungasha pakua:", 요청)
    명세, 파일들 = pakua(요청, namba_ya_kituo)
    ingizo_Orodha = 목록읽기()
    Jina = 명세["name"]
    if Jina in ingizo_Orodha:
        if ingizo_Orodha[Jina]["version"] == 명세["version"]:
            for njia, 지문값 in ingizo_Orodha[Jina]["files"].items():
                if mfumo_endeshi.path_kind(njia) != 1 or 지문(mfumo_endeshi.read(njia)) != 지문값:
                    raise ValueError("설치된 fungasha 파일이 달라졌습니다: " + njia)
            print("이미 설치됨:", Jina, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Nyuma_thamani 설치하십시오.")
    for njia in 파일들:
        if mfumo_endeshi.path_kind(njia):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + njia)
    ingizo_Orodha[Jina] = {"version": 명세["version"], "files": {njia: 지문(data) for njia, data in 파일들.items()}}
    새목록 = json.dumps(ingizo_Orodha).encode()
    if len(새목록) > 16384:
        raise ValueError("fungasha ingizo_Orodha panga_ukubwa 초과")
    이전목록 = mfumo_endeshi.read(Orodha_njia) if mfumo_endeshi.path_kind(Orodha_njia) else None
    만든파일 = []
    만든폴더 = []
    try:
        for njia, data in 파일들.items():
            부분들 = njia.split("/")
            for 수 in range(2, len(부분들)):
                Saraka_thamani = "/".join(부분들[:수])
                종류 = mfumo_endeshi.path_kind(Saraka_thamani)
                if 종류 == 0:
                    mfumo_endeshi.mkdir(Saraka_thamani)
                    만든폴더.append(Saraka_thamani)
                elif 종류 != 2:
                    raise ValueError("Saraka_thamani 경로에 파일이 있습니다: " + Saraka_thamani)
            만든파일.append(njia)
            andika_batli(njia, data)
        andika_batli(Orodha_njia, 새목록)
    except Exception:
        for njia in 만든파일:
            if mfumo_endeshi.path_kind(njia):
                mfumo_endeshi.remove(njia)
        for Saraka_thamani in reversed(만든폴더):
            mfumo_endeshi.rmdir(Saraka_thamani)
        if 이전목록 is not None:
            andika_batli(Orodha_njia, 이전목록)
        elif mfumo_endeshi.path_kind(Orodha_njia):
            mfumo_endeshi.remove(Orodha_njia)
        raise
    print("sakinisha_thamani 완료:", Jina, 명세["version"], "→ /lib (RAM)")


def ondoa_ingizo(Jina):
    ingizo_Orodha = 목록읽기()
    if Jina not in ingizo_Orodha:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Jina)
    for njia, 지문값 in ingizo_Orodha[Jina]["files"].items():
        if mfumo_endeshi.path_kind(njia) != 1 or 지문(mfumo_endeshi.read(njia)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + njia)
    for njia in ingizo_Orodha[Jina]["files"]:
        mfumo_endeshi.remove(njia)
    del ingizo_Orodha[Jina]
    andika_batli(Orodha_njia, json.dumps(ingizo_Orodha).encode())
    print("ondoa_ingizo 완료:", Jina)


def endesha(인수):
    namba_ya_kituo = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        namba_ya_kituo = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Jina, msinfo32_exe in 목록읽기().items():
            print(Jina, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        sakinisha_thamani(인수[1], namba_ya_kituo)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        ondoa_ingizo(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython chanzo_mti 설치기 (PyPA pip 전체가 아님)")
        print("pip install Jina[==버전] [--port 8027] | pip list | pip uninstall Jina")
        print("mwenyeji: Zana/tekeleza_amri.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        endesha(sys.argv[1:])
    except Exception as kosa:
        print("fungasha kosa:", kosa)
        sys.exit(1)
