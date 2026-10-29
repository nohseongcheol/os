"""nativo 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistema_operativo

elenco_percorso = "/lib/.pip.json"


def impronta_digitale_VALORE(dati):
    return "".join("%02x" % VALORE for VALORE in hashlib.sha256(dati).digest())


def 목록읽기():
    if sistema_operativo.path_kind(elenco_percorso) == 0:
        return {}
    return json.loads(sistema_operativo.read(elenco_percorso).decode("utf-8"))


def scrivere_LOG(percorso, dati):
    if sistema_operativo.write(percorso, dati) != len(dati):
        raise OSError(28)


def assegno_percorso(percorso):
    if not isinstance(percorso, str) or not percorso.endswith(".py"):
        raise ValueError("Python 소스만 설치할 numero 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in percorso.split("/")):
        raise ValueError("허용하지 않는 aggregare percorso")
    if "\\" in percorso or any(ord(carattere_VALORE) < 32 or ord(carattere_VALORE) == 127 for carattere_VALORE in percorso):
        raise ValueError("잘못된 percorso 문자")
    risultato = "/lib/" + percorso
    if len(risultato.encode("utf-8")) > 63 or percorso in ("Italiano.py", "aggregare.py"):
        raise ValueError("aggregare 경로가 너무 길거나 valore_predefinito 라이브러리와 겹칩니다.")
    return risultato


class ricevere_Stream:
    def __init__(자신, endpoint):
        자신.endpoint = endpoint
        자신.남은자료 = b""
        자신.avvia = sistema_operativo.ticks_ms()

    def 정확히읽기(자신, durata_VALORE):
        dati = bytearray()
        while len(dati) < durata_VALORE:
            if sistema_operativo.ticks_ms() - 자신.avvia > 90000:
                raise ValueError("aggregare Inoltro_VALORE replica valore 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistema_operativo.tcp_read(자신.endpoint, 512)
                except OSError as errore:
                    if errore.args[0] != 11:
                        raise
                    sistema_operativo.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("aggregare 전송이 중간에 끝났습니다.")
            articolo_CONTA_NUMERI = min(durata_VALORE - len(dati), len(자신.남은자료))
            dati.extend(자신.남은자료[:articolo_CONTA_NUMERI])
            자신.남은자료 = 자신.남은자료[articolo_CONTA_NUMERI:]
            sistema_operativo.sleep_ms(0)
        return bytes(dati)


def download(richiesta, numero_di_porta):
    if len(richiesta) > 96 or any(carattere_VALORE not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for carattere_VALORE in richiesta):
        raise ValueError("사용법: pip install Nome 또는 Nome==버전")
    endpoint = sistema_operativo.tcp_open()
    try:
        avvia = sistema_operativo.ticks_ms()
        while True:
            try:
                sistema_operativo.tcp_connect(endpoint, "10.0.2.2", numero_di_porta)
                break
            except OSError as errore:
                if errore.args[0] not in (11, 115) or sistema_operativo.ticks_ms() - avvia > 5000:
                    raise ValueError("aggregare Inoltro_VALORE Connetti errore_VALORE: 호스트에서 --network --pip로 실행하십시오.")
                sistema_operativo.sleep_ms(10)
        dati = (richiesta + "\n").encode()
        while dati:
            try:
                articolo_CONTA_NUMERI = sistema_operativo.tcp_write(endpoint, dati)
                if not articolo_CONTA_NUMERI:
                    raise ValueError("aggregare richiesta trasferire_VALORE errore_VALORE")
                dati = dati[articolo_CONTA_NUMERI:]
            except OSError as errore:
                if errore.args[0] != 11:
                    raise
                sistema_operativo.sleep_ms(10)
                if sistema_operativo.ticks_ms() - avvia > 10000:
                    raise ValueError("aggregare richiesta trasferire_VALORE valore 초과")
        Stream_VALORE = ricevere_Stream(endpoint)
        intestazione_VALORE = Stream_VALORE.정확히읽기(8)
        if intestazione_VALORE[:4] != b"JKP1":
            raise ValueError("aggregare trasferire_VALORE valore_di_contratto 불일치")
        durata_VALORE = (intestazione_VALORE[4] << 24) | (intestazione_VALORE[5] << 16) | (intestazione_VALORE[6] << 8) | intestazione_VALORE[7]
        if durata_VALORE > 8192:
            raise ValueError("aggregare 명세가 너무 큽니다.")
        specifica = json.loads(Stream_VALORE.정확히읽기(durata_VALORE).decode())
        if "error" in specifica:
            raise ValueError(specifica["error"])
        if not 1 <= len(specifica["files"]) <= 16:
            raise ValueError("꾸러미당 fonte_albero 파일은 1~16개여야 합니다.")
        if sum(voce_VALORE["size"] for voce_VALORE in specifica["files"]) > 65536:
            raise ValueError("aggregare fonte_albero 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for voce_VALORE in specifica["files"]:
            percorso = assegno_percorso(voce_VALORE["path"])
            if percorso in 파일들 or not 0 <= voce_VALORE["size"] <= 16384:
                raise ValueError("중복 percorso 또는 file Dimensione 초과")
            dati = Stream_VALORE.정확히읽기(voce_VALORE["size"])
            if impronta_digitale_VALORE(dati) != voce_VALORE["sha256"]:
                raise ValueError("aggregare file SHA-256 불일치")
            # 실행하지 않고 Regolari_articolo MicroPython의 문법으로 먼저 검사한다.
            compile(dati.decode("utf-8"), percorso, "exec")
            파일들[percorso] = dati
            gc.collect()
        return specifica, 파일들
    finally:
        sistema_operativo.udp_close(endpoint)


def installare_VALORE(richiesta, numero_di_porta):
    print("aggregare download:", richiesta)
    specifica, 파일들 = download(richiesta, numero_di_porta)
    voce_elenco = 목록읽기()
    Nome = specifica["name"]
    if Nome in voce_elenco:
        if voce_elenco[Nome]["version"] == specifica["version"]:
            for percorso, impronta_digitale_dati in voce_elenco[Nome]["files"].items():
                if sistema_operativo.path_kind(percorso) != 1 or impronta_digitale_VALORE(sistema_operativo.read(percorso)) != impronta_digitale_dati:
                    raise ValueError("설치된 aggregare 파일이 달라졌습니다: " + percorso)
            print("이미 설치됨:", Nome, specifica["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 BACK_VALORE 설치하십시오.")
    for percorso in 파일들:
        if sistema_operativo.path_kind(percorso):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + percorso)
    voce_elenco[Nome] = {"version": specifica["version"], "files": {percorso: impronta_digitale_VALORE(dati) for percorso, dati in 파일들.items()}}
    새목록 = json.dumps(voce_elenco).encode()
    if len(새목록) > 16384:
        raise ValueError("aggregare voce_elenco Dimensione 초과")
    Indietro_elenco = sistema_operativo.read(elenco_percorso) if sistema_operativo.path_kind(elenco_percorso) else None
    만든파일 = []
    만든폴더 = []
    try:
        for percorso, dati in 파일들.items():
            부분들 = percorso.split("/")
            for numero in range(2, len(부분들)):
                elenco_VALORE = "/".join(부분들[:numero])
                Kind_VALORE = sistema_operativo.path_kind(elenco_VALORE)
                if Kind_VALORE == 0:
                    sistema_operativo.mkdir(elenco_VALORE)
                    만든폴더.append(elenco_VALORE)
                elif Kind_VALORE != 2:
                    raise ValueError("elenco_VALORE 경로에 파일이 있습니다: " + elenco_VALORE)
            만든파일.append(percorso)
            scrivere_LOG(percorso, dati)
        scrivere_LOG(elenco_percorso, 새목록)
    except Exception:
        for percorso in 만든파일:
            if sistema_operativo.path_kind(percorso):
                sistema_operativo.remove(percorso)
        for elenco_VALORE in reversed(만든폴더):
            sistema_operativo.rmdir(elenco_VALORE)
        if Indietro_elenco is not None:
            scrivere_LOG(elenco_percorso, Indietro_elenco)
        elif sistema_operativo.path_kind(elenco_percorso):
            sistema_operativo.remove(elenco_percorso)
        raise
    print("installare_VALORE 완료:", Nome, specifica["version"], "→ /lib (RAM)")


def rimuovere_voce(Nome):
    voce_elenco = 목록읽기()
    if Nome not in voce_elenco:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nome)
    for percorso, impronta_digitale_dati in voce_elenco[Nome]["files"].items():
        if sistema_operativo.path_kind(percorso) != 1 or impronta_digitale_VALORE(sistema_operativo.read(percorso)) != impronta_digitale_dati:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + percorso)
    for percorso in voce_elenco[Nome]["files"]:
        sistema_operativo.remove(percorso)
    del voce_elenco[Nome]
    scrivere_LOG(elenco_percorso, json.dumps(voce_elenco).encode())
    print("rimuovere_voce 완료:", Nome)


def avvia(argomenti):
    numero_di_porta = 8027
    if len(argomenti) >= 2 and argomenti[-2] == "--port":
        numero_di_porta = int(argomenti[-1])
        argomenti = argomenti[:-2]
    if argomenti == ["list"]:
        for Nome, msinfo32_exe in 목록읽기().items():
            print(Nome, msinfo32_exe["version"])
    elif len(argomenti) == 2 and argomenti[0] == "install":
        installare_VALORE(argomenti[1], numero_di_porta)
    elif len(argomenti) == 2 and argomenti[0] == "uninstall":
        rimuovere_voce(argomenti[1])
    elif not argomenti or argomenti in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython fonte_albero 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nome[==버전] [--port 8027] | pip list | pip uninstall Nome")
        print("host: strumenti/Esegui_comando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        avvia(sys.argv[1:])
    except Exception as errore:
        print("aggregare errore:", errore)
        sys.exit(1)
