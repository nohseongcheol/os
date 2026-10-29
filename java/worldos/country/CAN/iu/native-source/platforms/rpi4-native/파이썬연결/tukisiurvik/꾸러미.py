"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 tuttarvik 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as qarasaujakkut_aulattijjut

Titiqpalliagaq_aqqut = "/lib/.pip.json"


def 지문(titiqqat):
    return "".join("%02x" % atuutilik for atuutilik in hashlib.sha256(titiqqat).digest())


def 목록읽기():
    if qarasaujakkut_aulattijjut.path_kind(Titiqpalliagaq_aqqut) == 0:
        return {}
    return json.loads(qarasaujakkut_aulattijjut.read(Titiqpalliagaq_aqqut).decode("utf-8"))


def titiraq_papattivik(aqqut, titiqqat):
    if qarasaujakkut_aulattijjut.write(aqqut, titiqqat) != len(titiqqat):
        raise OSError(28)


def qaujigiarli_aqqut(aqqut):
    if not isinstance(aqqut, str) or not aqqut.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in aqqut.split("/")):
        raise ValueError("허용하지 않는 꾸러미 aqqut")
    if "\\" in aqqut or any(ord(immikkuuqtuq_atuutilik) < 32 or ord(immikkuuqtuq_atuutilik) == 127 for immikkuuqtuq_atuutilik in aqqut):
        raise ValueError("잘못된 aqqut 문자")
    결과 = "/lib/" + aqqut
    if len(결과.encode("utf-8")) > 63 or aqqut in ("한국어.py", "꾸러미.py"):
        raise ValueError("꾸러미 경로가 너무 길거나 Aturniliuvagiiqtut 라이브러리와 겹칩니다.")
    return 결과


class 수신흐름:
    def __init__(자신, 종단):
        자신.종단 = 종단
        자신.남은자료 = b""
        자신.시작 = qarasaujakkut_aulattijjut.ticks_ms()

    def 정확히읽기(자신, takininga_atuutilik):
        titiqqat = bytearray()
        while len(titiqqat) < takininga_atuutilik:
            if qarasaujakkut_aulattijjut.ticks_ms() - 자신.시작 > 90000:
                raise ValueError("꾸러미 중계 응답 시간 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = qarasaujakkut_aulattijjut.tcp_read(자신.종단, 512)
                except OSError as tammarniq:
                    if tammarniq.args[0] != 11:
                        raise
                    qarasaujakkut_aulattijjut.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("꾸러미 전송이 중간에 끝났습니다.")
            개수 = min(takininga_atuutilik - len(titiqqat), len(자신.남은자료))
            titiqqat.extend(자신.남은자료[:개수])
            자신.남은자료 = 자신.남은자료[개수:]
            qarasaujakkut_aulattijjut.sleep_ms(0)
        return bytes(titiqqat)


def minaq(요청, 접속번호):
    if len(요청) > 96 or any(immikkuuqtuq_atuutilik not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for immikkuuqtuq_atuutilik in 요청):
        raise ValueError("사용법: pip install atiq 또는 atiq==버전")
    종단 = qarasaujakkut_aulattijjut.tcp_open()
    try:
        시작 = qarasaujakkut_aulattijjut.ticks_ms()
        while True:
            try:
                qarasaujakkut_aulattijjut.tcp_connect(종단, "10.0.2.2", 접속번호)
                break
            except OSError as tammarniq:
                if tammarniq.args[0] not in (11, 115) or qarasaujakkut_aulattijjut.ticks_ms() - 시작 > 5000:
                    raise ValueError("꾸러미 중계 kasurli itigaqtuq_atuutilik: 호스트에서 --network --pip로 실행하십시오.")
                qarasaujakkut_aulattijjut.sleep_ms(10)
        titiqqat = (요청 + "\n").encode()
        while titiqqat:
            try:
                개수 = qarasaujakkut_aulattijjut.tcp_write(종단, titiqqat)
                if not 개수:
                    raise ValueError("꾸러미 요청 aullaaqtilli_atuutilik itigaqtuq_atuutilik")
                titiqqat = titiqqat[개수:]
            except OSError as tammarniq:
                if tammarniq.args[0] != 11:
                    raise
                qarasaujakkut_aulattijjut.sleep_ms(10)
                if qarasaujakkut_aulattijjut.ticks_ms() - 시작 > 10000:
                    raise ValueError("꾸러미 요청 aullaaqtilli_atuutilik 시간 초과")
        ingirrania_aulataup_atuutilik = 수신흐름(종단)
        머리 = ingirrania_aulataup_atuutilik.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("꾸러미 aullaaqtilli_atuutilik pijatsaq_atuutilik 불일치")
        takininga_atuutilik = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if takininga_atuutilik > 8192:
            raise ValueError("꾸러미 명세가 너무 큽니다.")
        명세 = json.loads(ingirrania_aulataup_atuutilik.정확히읽기(takininga_atuutilik).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 pivviujuq_attavigiit 파일은 1~16개여야 합니다.")
        if sum(Iliniku_atuutilik["size"] for Iliniku_atuutilik in 명세["files"]) > 65536:
            raise ValueError("꾸러미 pivviujuq_attavigiit 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for Iliniku_atuutilik in 명세["files"]:
            aqqut = qaujigiarli_aqqut(Iliniku_atuutilik["path"])
            if aqqut in 파일들 or not 0 <= Iliniku_atuutilik["size"] <= 16384:
                raise ValueError("중복 aqqut 또는 ini anininga 초과")
            titiqqat = ingirrania_aulataup_atuutilik.정확히읽기(Iliniku_atuutilik["size"])
            if 지문(titiqqat) != Iliniku_atuutilik["sha256"]:
                raise ValueError("꾸러미 ini SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(titiqqat.decode("utf-8"), aqqut, "exec")
            파일들[aqqut] = titiqqat
            gc.collect()
        return 명세, 파일들
    finally:
        qarasaujakkut_aulattijjut.udp_close(종단)


def ilili_atuutilik(요청, 접속번호):
    print("꾸러미 minaq:", 요청)
    명세, 파일들 = minaq(요청, 접속번호)
    Iliniku_Titiqpalliagaq = 목록읽기()
    atiq = 명세["name"]
    if atiq in Iliniku_Titiqpalliagaq:
        if Iliniku_Titiqpalliagaq[atiq]["version"] == 명세["version"]:
            for aqqut, 지문값 in Iliniku_Titiqpalliagaq[atiq]["files"].items():
                if qarasaujakkut_aulattijjut.path_kind(aqqut) != 1 or 지문(qarasaujakkut_aulattijjut.read(aqqut)) != 지문값:
                    raise ValueError("설치된 꾸러미 파일이 달라졌습니다: " + aqqut)
            print("이미 설치됨:", atiq, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 Utimut_atuutilik 설치하십시오.")
    for aqqut in 파일들:
        if qarasaujakkut_aulattijjut.path_kind(aqqut):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + aqqut)
    Iliniku_Titiqpalliagaq[atiq] = {"version": 명세["version"], "files": {aqqut: 지문(titiqqat) for aqqut, titiqqat in 파일들.items()}}
    새목록 = json.dumps(Iliniku_Titiqpalliagaq).encode()
    if len(새목록) > 16384:
        raise ValueError("꾸러미 Iliniku_Titiqpalliagaq anininga 초과")
    이전목록 = qarasaujakkut_aulattijjut.read(Titiqpalliagaq_aqqut) if qarasaujakkut_aulattijjut.path_kind(Titiqpalliagaq_aqqut) else None
    만든파일 = []
    만든폴더 = []
    try:
        for aqqut, titiqqat in 파일들.items():
            부분들 = aqqut.split("/")
            for 수 in range(2, len(부분들)):
                tukimuagutiit_atuutilik = "/".join(부분들[:수])
                종류 = qarasaujakkut_aulattijjut.path_kind(tukimuagutiit_atuutilik)
                if 종류 == 0:
                    qarasaujakkut_aulattijjut.mkdir(tukimuagutiit_atuutilik)
                    만든폴더.append(tukimuagutiit_atuutilik)
                elif 종류 != 2:
                    raise ValueError("tukimuagutiit_atuutilik 경로에 파일이 있습니다: " + tukimuagutiit_atuutilik)
            만든파일.append(aqqut)
            titiraq_papattivik(aqqut, titiqqat)
        titiraq_papattivik(Titiqpalliagaq_aqqut, 새목록)
    except Exception:
        for aqqut in 만든파일:
            if qarasaujakkut_aulattijjut.path_kind(aqqut):
                qarasaujakkut_aulattijjut.remove(aqqut)
        for tukimuagutiit_atuutilik in reversed(만든폴더):
            qarasaujakkut_aulattijjut.rmdir(tukimuagutiit_atuutilik)
        if 이전목록 is not None:
            titiraq_papattivik(Titiqpalliagaq_aqqut, 이전목록)
        elif qarasaujakkut_aulattijjut.path_kind(Titiqpalliagaq_aqqut):
            qarasaujakkut_aulattijjut.remove(Titiqpalliagaq_aqqut)
        raise
    print("ilili_atuutilik 완료:", atiq, 명세["version"], "→ /lib (RAM)")


def sanirvalli_Iliniku(atiq):
    Iliniku_Titiqpalliagaq = 목록읽기()
    if atiq not in Iliniku_Titiqpalliagaq:
        raise ValueError("설치되지 않은 꾸러미입니다: " + atiq)
    for aqqut, 지문값 in Iliniku_Titiqpalliagaq[atiq]["files"].items():
        if qarasaujakkut_aulattijjut.path_kind(aqqut) != 1 or 지문(qarasaujakkut_aulattijjut.read(aqqut)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + aqqut)
    for aqqut in Iliniku_Titiqpalliagaq[atiq]["files"]:
        qarasaujakkut_aulattijjut.remove(aqqut)
    del Iliniku_Titiqpalliagaq[atiq]
    titiraq_papattivik(Titiqpalliagaq_aqqut, json.dumps(Iliniku_Titiqpalliagaq).encode())
    print("sanirvalli_Iliniku 완료:", atiq)


def 시작(인수):
    접속번호 = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        접속번호 = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for atiq, msinfo32_exe in 목록읽기().items():
            print(atiq, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        ilili_atuutilik(인수[1], 접속번호)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        sanirvalli_Iliniku(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython pivviujuq_attavigiit 설치기 (PyPA pip 전체가 아님)")
        print("pip install atiq[==버전] [--port 8027] | pip list | pip uninstall atiq")
        print("tuttarvik: 도구/실행.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        시작(sys.argv[1:])
    except Exception as tammarniq:
        print("꾸러미 tammarniq:", tammarniq)
        sys.exit(1)
