"""자체 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 hospedar 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as sistema_operativo

Lista_camiño = "/lib/.pip.json"


def 지문(datos):
    return "".join("%02x" % VALOR for VALOR in hashlib.sha256(datos).digest())


def 목록읽기():
    if sistema_operativo.path_kind(Lista_camiño) == 0:
        return {}
    return json.loads(sistema_operativo.read(Lista_camiño).decode("utf-8"))


def escribir_LOG(CAMIÑO, datos):
    if sistema_operativo.write(CAMIÑO, datos) != len(datos):
        raise OSError(28)


def cheque_camiño(CAMIÑO):
    if not isinstance(CAMIÑO, str) or not CAMIÑO.endswith(".py"):
        raise ValueError("Python 소스만 설치할 수 있습니다.")
    if any(부분 in ("", ".", "..") or 부분.startswith(".") for 부분 in CAMIÑO.split("/")):
        raise ValueError("허용하지 않는 paquete CAMIÑO")
    if "\\" in CAMIÑO or any(ord(carácter_VALOR) < 32 or ord(carácter_VALOR) == 127 for carácter_VALOR in CAMIÑO):
        raise ValueError("잘못된 CAMIÑO 문자")
    RESULTANTE = "/lib/" + CAMIÑO
    if len(RESULTANTE.encode("utf-8")) > 63 or CAMIÑO in ("Galego.py", "paquete.py"):
        raise ValueError("paquete 경로가 너무 길거나 valor_predefinido 라이브러리와 겹칩니다.")
    return RESULTANTE


class 수신흐름:
    def __init__(자신, extremo):
        자신.extremo = extremo
        자신.남은자료 = b""
        자신.Executar_2 = sistema_operativo.ticks_ms()

    def 정확히읽기(자신, duración_VALOR):
        datos = bytearray()
        while len(datos) < duración_VALOR:
            if sistema_operativo.ticks_ms() - 자신.Executar_2 > 90000:
                raise ValueError("paquete 중계 resposta hora_VALOR 초과")
            if not 자신.남은자료:
                try:
                    자신.남은자료 = sistema_operativo.tcp_read(자신.extremo, 512)
                except OSError as ERRO:
                    if ERRO.args[0] != 11:
                        raise
                    sistema_operativo.sleep_ms(10)
                    continue
                if not 자신.남은자료:
                    raise ValueError("paquete 전송이 중간에 끝났습니다.")
            elemento_CONTAR = min(duración_VALOR - len(datos), len(자신.남은자료))
            datos.extend(자신.남은자료[:elemento_CONTAR])
            자신.남은자료 = 자신.남은자료[elemento_CONTAR:]
            sistema_operativo.sleep_ms(0)
        return bytes(datos)


def descarga(solicitude, número_do_porto):
    if len(solicitude) > 96 or any(carácter_VALOR not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for carácter_VALOR in solicitude):
        raise ValueError("사용법: pip install Nome 또는 Nome==버전")
    extremo = sistema_operativo.tcp_open()
    try:
        Executar_2 = sistema_operativo.ticks_ms()
        while True:
            try:
                sistema_operativo.tcp_connect(extremo, "10.0.2.2", número_do_porto)
                break
            except OSError as ERRO:
                if ERRO.args[0] not in (11, 115) or sistema_operativo.ticks_ms() - Executar_2 > 5000:
                    raise ValueError("paquete 중계 Conectar erro_VALOR: 호스트에서 --network --pip로 실행하십시오.")
                sistema_operativo.sleep_ms(10)
        datos = (solicitude + "\n").encode()
        while datos:
            try:
                elemento_CONTAR = sistema_operativo.tcp_write(extremo, datos)
                if not elemento_CONTAR:
                    raise ValueError("paquete solicitude Transferir_VALOR erro_VALOR")
                datos = datos[elemento_CONTAR:]
            except OSError as ERRO:
                if ERRO.args[0] != 11:
                    raise
                sistema_operativo.sleep_ms(10)
                if sistema_operativo.ticks_ms() - Executar_2 > 10000:
                    raise ValueError("paquete solicitude Transferir_VALOR hora_VALOR 초과")
        fluxo_VALOR = 수신흐름(extremo)
        머리 = fluxo_VALOR.정확히읽기(8)
        if 머리[:4] != b"JKP1":
            raise ValueError("paquete Transferir_VALOR caso_VALOR 불일치")
        duración_VALOR = (머리[4] << 24) | (머리[5] << 16) | (머리[6] << 8) | 머리[7]
        if duración_VALOR > 8192:
            raise ValueError("paquete 명세가 너무 큽니다.")
        명세 = json.loads(fluxo_VALOR.정확히읽기(duración_VALOR).decode())
        if "error" in 명세:
            raise ValueError(명세["error"])
        if not 1 <= len(명세["files"]) <= 16:
            raise ValueError("꾸러미당 fonte_árbore 파일은 1~16개여야 합니다.")
        if sum(introdución_VALOR["size"] for introdución_VALOR in 명세["files"]) > 65536:
            raise ValueError("paquete fonte_árbore 합계는 64 KiB 이하여야 합니다.")
        파일들 = {}
        for introdución_VALOR in 명세["files"]:
            CAMIÑO = cheque_camiño(introdución_VALOR["path"])
            if CAMIÑO in 파일들 or not 0 <= introdución_VALOR["size"] <= 16384:
                raise ValueError("중복 CAMIÑO 또는 Ficheiro Tamaño 초과")
            datos = fluxo_VALOR.정확히읽기(introdución_VALOR["size"])
            if 지문(datos) != introdución_VALOR["sha256"]:
                raise ValueError("paquete Ficheiro SHA-256 불일치")
            # 실행하지 않고 ao_corrente_elemento MicroPython의 문법으로 먼저 검사한다.
            compile(datos.decode("utf-8"), CAMIÑO, "exec")
            파일들[CAMIÑO] = datos
            gc.collect()
        return 명세, 파일들
    finally:
        sistema_operativo.udp_close(extremo)


def instalar_VALOR(solicitude, número_do_porto):
    print("paquete descarga:", solicitude)
    명세, 파일들 = descarga(solicitude, número_do_porto)
    introdución_Lista = 목록읽기()
    Nome = 명세["name"]
    if Nome in introdución_Lista:
        if introdución_Lista[Nome]["version"] == 명세["version"]:
            for CAMIÑO, 지문값 in introdución_Lista[Nome]["files"].items():
                if sistema_operativo.path_kind(CAMIÑO) != 1 or 지문(sistema_operativo.read(CAMIÑO)) != 지문값:
                    raise ValueError("설치된 paquete 파일이 달라졌습니다: " + CAMIÑO)
            print("이미 설치됨:", Nome, 명세["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 ATRÁS_VALOR 설치하십시오.")
    for CAMIÑO in 파일들:
        if sistema_operativo.path_kind(CAMIÑO):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + CAMIÑO)
    introdución_Lista[Nome] = {"version": 명세["version"], "files": {CAMIÑO: 지문(datos) for CAMIÑO, datos in 파일들.items()}}
    새목록 = json.dumps(introdución_Lista).encode()
    if len(새목록) > 16384:
        raise ValueError("paquete introdución_Lista Tamaño 초과")
    이전목록 = sistema_operativo.read(Lista_camiño) if sistema_operativo.path_kind(Lista_camiño) else None
    만든파일 = []
    만든폴더 = []
    try:
        for CAMIÑO, datos in 파일들.items():
            부분들 = CAMIÑO.split("/")
            for 수 in range(2, len(부분들)):
                directorio_VALOR = "/".join(부분들[:수])
                종류 = sistema_operativo.path_kind(directorio_VALOR)
                if 종류 == 0:
                    sistema_operativo.mkdir(directorio_VALOR)
                    만든폴더.append(directorio_VALOR)
                elif 종류 != 2:
                    raise ValueError("directorio_VALOR 경로에 파일이 있습니다: " + directorio_VALOR)
            만든파일.append(CAMIÑO)
            escribir_LOG(CAMIÑO, datos)
        escribir_LOG(Lista_camiño, 새목록)
    except Exception:
        for CAMIÑO in 만든파일:
            if sistema_operativo.path_kind(CAMIÑO):
                sistema_operativo.remove(CAMIÑO)
        for directorio_VALOR in reversed(만든폴더):
            sistema_operativo.rmdir(directorio_VALOR)
        if 이전목록 is not None:
            escribir_LOG(Lista_camiño, 이전목록)
        elif sistema_operativo.path_kind(Lista_camiño):
            sistema_operativo.remove(Lista_camiño)
        raise
    print("instalar_VALOR 완료:", Nome, 명세["version"], "→ /lib (RAM)")


def eliminar_introdución(Nome):
    introdución_Lista = 목록읽기()
    if Nome not in introdución_Lista:
        raise ValueError("설치되지 않은 꾸러미입니다: " + Nome)
    for CAMIÑO, 지문값 in introdución_Lista[Nome]["files"].items():
        if sistema_operativo.path_kind(CAMIÑO) != 1 or 지문(sistema_operativo.read(CAMIÑO)) != 지문값:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + CAMIÑO)
    for CAMIÑO in introdución_Lista[Nome]["files"]:
        sistema_operativo.remove(CAMIÑO)
    del introdución_Lista[Nome]
    escribir_LOG(Lista_camiño, json.dumps(introdución_Lista).encode())
    print("eliminar_introdución 완료:", Nome)


def Executar_2(Argumentos):
    número_do_porto = 8027
    if len(Argumentos) >= 2 and Argumentos[-2] == "--port":
        número_do_porto = int(Argumentos[-1])
        Argumentos = Argumentos[:-2]
    if Argumentos == ["list"]:
        for Nome, msinfo32_exe in 목록읽기().items():
            print(Nome, msinfo32_exe["version"])
    elif len(Argumentos) == 2 and Argumentos[0] == "install":
        instalar_VALOR(Argumentos[1], número_do_porto)
    elif len(Argumentos) == 2 and Argumentos[0] == "uninstall":
        eliminar_introdución(Argumentos[1])
    elif not Argumentos or Argumentos in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython fonte_árbore 설치기 (PyPA pip 전체가 아님)")
        print("pip install Nome[==버전] [--port 8027] | pip list | pip uninstall Nome")
        print("hospedar: Ferramentas/executar_comando.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        Executar_2(sys.argv[1:])
    except Exception as ERRO:
        print("paquete ERRO:", ERRO)
        sys.exit(1)
