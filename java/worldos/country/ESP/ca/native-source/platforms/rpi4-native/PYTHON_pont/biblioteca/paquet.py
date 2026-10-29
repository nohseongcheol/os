"""propi 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 allotjar 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistema_operatiu

Llista_camí = "/lib/.pip.json"


def 지문(dades):
    return "".join("%02x" % VALOR for VALOR in hashlib.sha256(dades).digest())


def tancar_Llista():
    if sistema_operatiu.path_kind(Llista_camí) == 0:
        return {}
    return json.loads(sistema_operatiu.read(Llista_camí).decode("utf-8"))


def escriure_LOG(Camí, dades):
    if sistema_operatiu.write(Camí, dades) != len(dades):
        raise OSError(28)


def xec_camí(Camí):
    if not isinstance(Camí, str) or not Camí.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in Camí.split("/")):
        raise ValueError("허용하지 않는 paquet Camí")
    if "\\" in Camí or any(ord(caràcter_VALOR) < 32 or ord(caràcter_VALOR) == 127 for caràcter_VALOR in Camí):
        raise ValueError("잘못된 Camí 문자")
    RESULTAT = "/lib/" + Camí
    if len(RESULTAT.encode("utf-8")) > 63 or Camí in ("Català.py", "paquet.py"):
        raise ValueError("paquet 경로가 너무 길거나 valor_per_defecte 라이브러리와 겹칩니다.")
    return RESULTAT


class rebre_flux:
    def __init__(자신, extrem):
        자신.extrem = extrem
        자신.남은자료 = b""
        자신.Executa_2 = sistema_operatiu.ticks_ms()

    def 정확히읽기(자신, durada_VALOR):
        dades = bytearray()
        while len(dades) < durada_VALOR:
            if sistema_operatiu.ticks_ms() - 자신.Executa_2 > 90000:
                raise ValueError("paquet 중계 resposta Hora_VALOR 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistema_operatiu.tcp_read(자신.extrem, 512)
                except OSError as s_ha_produït_un_error:
                    if s_ha_produït_un_error.args[0] != 11:
                        raise
                    sistema_operatiu.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paquet 전송이 중간에 끝났습니다.")
            element_COMPT = min(durada_VALOR - len(dades), len(자신.남은자료))
            dades.extend(자신.남은자료[:element_COMPT])
            자신.남은자료 = 자신.남은자료[element_COMPT:]
            sistema_operatiu.sleep_ms(0)
        return bytes(dades)


def baixar(sol_licitud, número_de_port):
    if len(sol_licitud) > 96 or any(caràcter_VALOR not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for caràcter_VALOR in sol_licitud):
        raise ValueError("사용법: pip install Nom 또는 Nom==버전")
    extrem = sistema_operatiu.tcp_open()
    try:
        Executa_2 = sistema_operatiu.ticks_ms()
        while True:
            try:
                sistema_operatiu.tcp_connect(extrem, "10.0.2.2", número_de_port)
                break
            except OSError as s_ha_produït_un_error:
                if s_ha_produït_un_error.args[0] not in (11, 115) or sistema_operatiu.ticks_ms() - Executa_2 > 5000:
                    raise ValueError("paquet 중계 Connecta error_VALOR: 호스트에서 --network --pip로 실행하십시오.")
                sistema_operatiu.sleep_ms(10)
        dades = (sol_licitud + "\n").encode()
        while dades:
            try:
                element_COMPT = sistema_operatiu.tcp_write(extrem, dades)
                if not element_COMPT:
                    raise ValueError("paquet sol_licitud transferir_VALOR error_VALOR")
                dades = dades[element_COMPT:]
            except OSError as s_ha_produït_un_error:
                if s_ha_produït_un_error.args[0] != 11:
                    raise
                sistema_operatiu.sleep_ms(10)
                if sistema_operatiu.ticks_ms() - Executa_2 > 10000:
                    raise ValueError("paquet sol_licitud transferir_VALOR Hora_VALOR 초과")
        flux_VALOR = rebre_flux(extrem)
        머리 = flux_VALOR.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("paquet transferir_VALOR cas_VALOR 불일치")
        durada_VALOR = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if durada_VALOR > 8192:
            raise ValueError("paquet 명세가 너무 큽니다.")
        명세 = json.loads(flux_VALOR.정확히읽기(durada_VALOR).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 font_arbre 파일은 1~16개여야 합니다.")
        if sum(introducció_VALOR["size"] for introducció_VALOR in 명세["files"]) > 65536:
            raise ValueError("paquet font_arbre 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for introducció_VALOR in 명세["files"]:
            Camí = xec_camí(introducció_VALOR["path"])
            if Camí in 파일들 or not 0 <= introducció_VALOR["size"] <= 16384:
                raise ValueError("중복 Camí 또는 Fitxer Mida 초과")
            dades = flux_VALOR.정확히읽기(introducció_VALOR["size"])
            if 지문(dades) != introducció_VALOR["sha256"]:
                raise ValueError("paquet Fitxer SHA-256 불일치")
            # 실행하지 않고 현재 MicroPython의 문법으로 먼저 검사한다.
            compile(dades.decode("utf-8"), Camí, "exec")
            파일들[Camí] = dades
            gc.collect()
        return 명세, 파일들
    finally:
        sistema_operatiu.udp_close(extrem)


def instal_lar_VALOR(sol_licitud, número_de_port):
    print("paquet baixar:", sol_licitud)
    명세, 파일들 = baixar(sol_licitud, número_de_port)
    introducció_Llista = tancar_Llista()
    Nom = 명세["name"]
    if Nom in introducció_Llista:
        if introducció_Llista[Nom]["version"] == 명세["version"]:
            for Camí, 지문값 in introducció_Llista[Nom]["files"].items():
                if sistema_operatiu.path_kind(Camí) != 1 or 지문(sistema_operatiu.read(Camí)) != 지문값:
                    raise ValueError("설치된 paquet 파일이 달라졌습니다: " + Camí)
            print("이미 설치됨:", Nom, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ENRERE_VALOR 설치하십시오.")
    for Camí in 파일들:
        if sistema_operatiu.path_kind(Camí):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + Camí)
    introducció_Llista[Nom] = {"version": 명세["version"], "files": {Camí: 지문(dades) for Camí, dades in 파일들.items()}}
    새목록 = json.dumps(introducció_Llista).encode()
    if len(새목록) > 16384:
        raise ValueError("paquet introducció_Llista Mida 초과")
    이전목록 = sistema_operatiu.read(Llista_camí) if sistema_operatiu.path_kind(Llista_camí) else None
    만든파일 = []
    만든폴더 = []
    try:
        for Camí, dades in 파일들.items():
            부분들 = Camí.split("/")
            for 수 in range(2, len(부분들)):
                directori_VALOR = "/".join(부분들[:수])
                종류 = sistema_operatiu.path_kind(directori_VALOR)
                if 종류 == 0:
                    sistema_operatiu.mkdir(directori_VALOR)
                    만든폴더.append(directori_VALOR)
                elif 종류 != 2:
                    raise ValueError("directori_VALOR 경로에 파일이 있습니다: " + directori_VALOR)
            만든파일.append(Camí)
            escriure_LOG(Camí, dades)
        escriure_LOG(Llista_camí, 새목록)
    except Exception:
        for Camí in 만든파일:
            if sistema_operatiu.path_kind(Camí):
                sistema_operatiu.remove(Camí)
        for directori_VALOR in reversed(만든폴더):
            sistema_operatiu.rmdir(directori_VALOR)
        if 이전목록 is not None:
            escriure_LOG(Llista_camí, 이전목록)
        elif sistema_operatiu.path_kind(Llista_camí):
            sistema_operatiu.remove(Llista_camí)
        raise
    print("instal_lar_VALOR 완료:", Nom, 명세["version"], "→ /lib (RAM)")


def suprimir_introducció(Nom):
    introducció_Llista = tancar_Llista()
    if Nom not in introducció_Llista:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nom)
    for Camí, 지문값 in introducció_Llista[Nom]["files"].items():
        if sistema_operatiu.path_kind(Camí) != 1 or 지문(sistema_operatiu.read(Camí)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + Camí)
    for Camí in introducció_Llista[Nom]["files"]:
        sistema_operatiu.remove(Camí)
    del introducció_Llista[Nom]
    escriure_LOG(Llista_camí, json.dumps(introducció_Llista).encode())
    print("suprimir_introducció 완료:", Nom)


def Executa_2(인수):
    número_de_port = 8027
    if len(인수) >= 2 and 인수[-2] == "--port":
        número_de_port = int(인수[-1])
        인수 = 인수[:-2]
    if 인수 == ["list"]:
        for Nom, msinfo32_exe in tancar_Llista().items():
            print(Nom, msinfo32_exe["version"])
    elif len(인수) == 2 and 인수[0] == "install":
        instal_lar_VALOR(인수[1], número_de_port)
    elif len(인수) == 2 and 인수[0] == "uninstall":
        suprimir_introducció(인수[1])
    elif not 인수 or 인수 in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython font_arbre 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nom[==버전] [--port 8027] | pip list | pip uninstall Nom")
        print("allotjar: Eines/Executa_ordre.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Executa_2(sys.argv[1:])
    except Exception as s_ha_produït_un_error:
        print("paquet s_ha_produït_un_error:", s_ha_produït_un_error)
        sys.exit(1)
